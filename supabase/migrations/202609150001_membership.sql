-- Run once in the project's SQL Editor. No paid content or secrets belong in Git.
begin;
create schema if not exists bgm_private;
revoke all on schema bgm_private from public, anon, authenticated;
create table bgm_private.admins(user_id uuid primary key references auth.users(id));
alter table bgm_private.admins enable row level security;
create table public.bgm_settings(id boolean primary key default true check(id), enrollment_open boolean not null default false);
insert into public.bgm_settings values(true,false);
create table public.bgm_memberships(user_id uuid primary key references auth.users(id), expires_at timestamptz not null);
create table public.bgm_orders(
 id uuid primary key default gen_random_uuid(),user_id uuid not null references auth.users(id),
 plan text not null check(plan in ('monthly','annual')), amount integer not null check(amount in(29,204)),
 network text not null default 'TRC20' check(network='TRC20'),
 wallet text not null default 'TVF22a1qKYLHXWV6FUSgRAT1hKEGLfJm22',
 txid text check(txid ~ '^[0-9a-f]{64}$'),status text not null default 'awaiting_payment' check(status in('awaiting_payment','pending','approved','rejected')),
 created_at timestamptz not null default now(), reviewed_at timestamptz, reviewer uuid references auth.users(id), review_note text,
 check((plan='monthly' and amount=29) or (plan='annual' and amount=204))
);
create unique index bgm_unique_txid on public.bgm_orders(txid) where txid is not null and status <> 'rejected';
create table public.bgm_articles(id uuid primary key default gen_random_uuid(),slug text unique not null check(slug ~ '^[a-z0-9-]+$'),title text not null, preview text not null, published boolean not null default false,updated_at timestamptz not null default now());
create table public.bgm_article_bodies(article_id uuid primary key references public.bgm_articles(id) on delete cascade,body text not null);
create function public.bgm_is_admin() returns boolean language sql stable security definer set search_path='' as $$select exists(select 1 from bgm_private.admins where user_id=auth.uid())$$;
revoke all on function public.bgm_is_admin() from public; grant execute on function public.bgm_is_admin() to authenticated;
alter table public.bgm_settings enable row level security;
alter table public.bgm_memberships enable row level security;
alter table public.bgm_orders enable row level security;
alter table public.bgm_articles enable row level security;
alter table public.bgm_article_bodies enable row level security;
revoke all on public.bgm_settings,public.bgm_memberships,public.bgm_orders,public.bgm_articles,public.bgm_article_bodies from anon,authenticated;
grant select on public.bgm_settings,public.bgm_articles to anon,authenticated;
grant select on public.bgm_memberships,public.bgm_orders,public.bgm_article_bodies to authenticated;
create policy settings_read on public.bgm_settings for select to anon,authenticated using(true);
create policy article_public on public.bgm_articles for select to anon,authenticated using(published);
create policy article_admin on public.bgm_articles for select to authenticated using(public.bgm_is_admin());
create policy membership_read on public.bgm_memberships for select to authenticated using(user_id=auth.uid() or public.bgm_is_admin());
create policy order_read on public.bgm_orders for select to authenticated using(user_id=auth.uid() or public.bgm_is_admin());
create policy body_read on public.bgm_article_bodies for select to authenticated using(public.bgm_is_admin() or (exists(select 1 from public.bgm_articles a where a.id=article_id and a.published) and exists(select 1 from public.bgm_memberships m where m.user_id=auth.uid() and m.expires_at>now())));
create function public.bgm_create_order(p_plan text) returns public.bgm_orders language plpgsql security definer set search_path='' as $$
declare result public.bgm_orders;
begin
 if auth.uid() is null then raise exception 'Sign in first'; end if;
 if not exists(select 1 from public.bgm_settings where enrollment_open) then raise exception 'Enrollment is not open'; end if;
 if p_plan not in ('monthly','annual') or p_plan is null then raise exception 'Invalid plan'; end if;
 perform pg_advisory_xact_lock(hashtext(auth.uid()::text));
 select * into result from public.bgm_orders where user_id=auth.uid() and plan=p_plan and status='awaiting_payment' order by created_at desc limit 1;
 if found then return result; end if;
 if (select count(*) from public.bgm_orders where user_id=auth.uid() and status in ('awaiting_payment','pending'))>=5 then raise exception 'Contact support about your existing orders'; end if;
 insert into public.bgm_orders(user_id,plan,amount) values(auth.uid(),p_plan,case when p_plan='monthly' then 29 else 204 end) returning * into result;
 return result;
end $$;
create function public.bgm_submit_tx(p_order uuid,p_txid text) returns void language plpgsql security definer set search_path='' as $$
begin
 if auth.uid() is null then raise exception 'Sign in first'; end if;
 if lower(trim(p_txid)) !~ '^[0-9a-f]{64}$' or p_txid is null then raise exception 'Enter a valid 64-character Tron transaction ID'; end if;
 update public.bgm_orders set txid=lower(trim(p_txid)),status='pending' where id=p_order and user_id=auth.uid() and status='awaiting_payment';
 if not found then raise exception 'Order cannot be submitted'; end if;
end $$;
create function public.bgm_review_order(p_order uuid,p_approve boolean,p_note text) returns void language plpgsql security definer set search_path='' as $$
declare o public.bgm_orders;
begin
 if not public.bgm_is_admin() then raise exception 'Administrator access required'; end if;
 if p_approve is null or length(trim(coalesce(p_note,'')))<5 then raise exception 'A verification note is required'; end if;
 select * into o from public.bgm_orders where id=p_order for update;
 if not found or o.status<>'pending' then raise exception 'Order already reviewed or not pending'; end if;
 if p_approve then
  insert into public.bgm_memberships(user_id,expires_at) values(o.user_id,now()+case when o.plan='annual' then interval '1 year' else interval '1 month' end)
  on conflict(user_id) do update set expires_at=greatest(public.bgm_memberships.expires_at,now())+case when o.plan='annual' then interval '1 year' else interval '1 month' end;
 end if;
 update public.bgm_orders set status=case when p_approve then 'approved' else 'rejected' end,reviewed_at=now(),reviewer=auth.uid(),review_note=left(p_note,1000) where id=p_order;
end $$;
create function public.bgm_save_article(p_slug text,p_title text,p_preview text,p_body text,p_published boolean) returns uuid language plpgsql security definer set search_path='' as $$
declare aid uuid;
begin
 if not public.bgm_is_admin() then raise exception 'Administrator access required'; end if;
 if length(trim(p_title))<3 or length(trim(p_preview))<10 or length(trim(p_body))<50 or p_published is null then raise exception 'Title, preview and article body are required'; end if;
 insert into public.bgm_articles(slug,title,preview,published) values(p_slug,p_title,p_preview,p_published)
 on conflict(slug) do update set title=excluded.title,preview=excluded.preview,published=excluded.published,updated_at=now() returning id into aid;
 insert into public.bgm_article_bodies values(aid,p_body) on conflict(article_id) do update set body=excluded.body;
 return aid;
end $$;
revoke all on function public.bgm_create_order(text),public.bgm_submit_tx(uuid,text),public.bgm_review_order(uuid,boolean,text),public.bgm_save_article(text,text,text,text,boolean) from public;
grant execute on function public.bgm_create_order(text),public.bgm_submit_tx(uuid,text),public.bgm_review_order(uuid,boolean,text),public.bgm_save_article(text,text,text,text,boolean) to authenticated;
commit;
