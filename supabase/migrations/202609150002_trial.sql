begin;
alter table public.bgm_settings add column trials_open boolean not null default false;
alter table public.bgm_memberships add column trial_started_at timestamptz;
create function public.bgm_start_trial() returns public.bgm_memberships language plpgsql security definer set search_path='' as $$
declare m public.bgm_memberships;
begin
 if auth.uid() is null or not exists(select 1 from auth.users where id=auth.uid() and email_confirmed_at is not null) then raise exception 'Confirm your email before starting a trial'; end if;
 if not exists(select 1 from public.bgm_settings where trials_open) then raise exception 'Free trials are not open yet'; end if;
 insert into public.bgm_memberships(user_id,expires_at,trial_started_at) values(auth.uid(),now()+interval '7 days',now()) on conflict(user_id) do nothing;
 select * into m from public.bgm_memberships where user_id=auth.uid();
 return m;
end $$;
revoke all on function public.bgm_start_trial() from public;
grant execute on function public.bgm_start_trial() to authenticated;
commit;
