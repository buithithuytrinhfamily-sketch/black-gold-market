/* Supabase enforces access. Client-side visibility never grants membership. */
(async()=>{
'use strict';
const $=id=>document.getElementById(id),status=$('member-status');
if(!status)return;
let db,user,order,expiryTimer;
const say=t=>status.textContent=t;
const show=(id,on)=>{if($(id))$(id).hidden=!on;};
const node=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n;};
const checked=r=>{if(r.error)throw r.error;return r.data;};
const run=fn=>async e=>{e.preventDefault();const buttons=[...e.currentTarget.querySelectorAll('button')];buttons.forEach(b=>b.disabled=true);try{await fn(e);}catch(err){say(err.message||'Unable to complete request. Please try again.');}finally{buttons.forEach(b=>b.disabled=false);}};
function link(text,url){const a=node('a',text);a.href=url;return a;}
function bind(id,fn){if($(id))$(id).addEventListener('submit',run(fn));}
try{
 const config=await fetch('/assets/member-config.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Configuration unavailable');return r.json();});
 if(!config.supabaseUrl||!config.publishableKey){say('Member enrollment is not open yet. No Analysis payment is being accepted. Please enjoy the free guides while we finish setup.');return;}
 if(!/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl))throw Error('Membership service configuration is invalid');
 db=window.supabase.createClient(config.supabaseUrl,config.publishableKey);
 async function loadOrder(id){
  order=checked(await db.from('bgm_orders').select('*').eq('id',id).single());
  show('payment-instructions',order.status==='awaiting_payment');
  if(order.status!=='awaiting_payment'){say('This order is '+order.status+'. Check My account for its status.');return;}
  $('order-details').textContent=`Order ${order.id} · ${order.plan} · ${order.amount} USDT`;
  $('payment-wallet').textContent=order.wallet;
 }
 async function refresh(){
  clearTimeout(expiryTimer);
  if($('premium-reader')){$('premium-reader').replaceChildren();show('premium-reader',false);}
  const session=checked(await db.auth.getSession());user=session.session?.user;
  show('auth-box',!user);show('session-box',!!user);
  ['account-box','checkout-box','admin-box'].forEach(id=>show(id,false));
  const settings=checked(await db.from('bgm_settings').select('enrollment_open').single());
  say(settings.enrollment_open?'Membership service is available.':'New enrollment is closed. Existing members can still sign in and read.');
  if(user){
   $('member-email').textContent=user.email;
   const memberships=checked(await db.from('bgm_memberships').select('expires_at').eq('user_id',user.id));
   const expiry=memberships[0]?.expires_at;const active=expiry&&Date.parse(expiry)>Date.now();
   if($('access-status'))$('access-status').textContent=active?'Active until '+new Date(expiry).toLocaleString():expiry?'Membership expired on '+new Date(expiry).toLocaleString():'No active membership. Submitted payments require manual verification.';
   if(active)expiryTimer=setTimeout(()=>{if($('premium-reader')){$('premium-reader').replaceChildren();show('premium-reader',false);}say('Please refresh to check your membership status.');},Math.min(Date.parse(expiry)-Date.now(),2147483647));
   show('account-box',true);show('checkout-box',true);
   if($('order-form'))$('order-form').hidden=!settings.enrollment_open;
   if($('order-list')){
    $('order-list').replaceChildren();const orders=checked(await db.from('bgm_orders').select('*').eq('user_id',user.id).order('created_at',{ascending:false}));
    if(!orders.length)$('order-list').textContent='No orders yet.';
    orders.forEach(o=>{const row=node('div',`${o.plan} · ${o.amount} USDT · ${o.status} · ${o.id}`);row.className='member-row';if(o.status==='awaiting_payment')row.append(link(' Continue payment request →','/membership/checkout/?order='+o.id));if(o.review_note)row.append(node('p',o.review_note));$('order-list').append(row);});
   }
   const admin=checked(await db.rpc('bgm_is_admin'));show('admin-link',admin);
   if($('admin-box')){if(admin){show('admin-box',true);await loadAdmin();}else say('Administrator access is required for this page.');}
   const oid=new URLSearchParams(location.search).get('order');if($('checkout-box')&&oid)await loadOrder(oid);
  }else{order=null;show('payment-instructions',false);}
  if($('premium-library'))await library();
 }
 async function library(){
  const articles=checked(await db.from('bgm_articles').select('id,slug,title,preview').eq('published',true).order('updated_at',{ascending:false}));
  const list=$('premium-library');list.replaceChildren();if(!articles.length)list.append(node('p','Premium articles will appear here when published.'));
  articles.forEach(a=>{const row=node('section','');row.className='member-row';row.append(node('h2',a.title),node('p',a.preview));const b=node('button','Read full article');b.className='button';b.onclick=async()=>{b.disabled=true;try{
   if(!user){say('Sign in to read with an active membership.');return;}
   const result=checked(await db.from('bgm_article_bodies').select('body').eq('article_id',a.id));
   if(!result.length){say('An active Analysis membership is required.');return;}
   const reader=$('premium-reader');reader.replaceChildren(node('h2',a.title));const body=node('div',result[0].body);body.className='member-body';reader.append(body);show('premium-reader',true);reader.scrollIntoView({behavior:'smooth'});
  }catch(e){say(e.message);}finally{b.disabled=false;}};row.append(b);list.append(row);});
 }
 async function loadAdmin(){
  const orders=checked(await db.from('bgm_orders').select('*').eq('status','pending').order('created_at'));
  const list=$('review-list');list.replaceChildren();if(!orders.length)list.textContent='No payments awaiting review.';
  orders.forEach(o=>{const row=node('form','');row.className='member-row';row.append(node('h3',o.plan+' · '+o.amount+' USDT'),node('p','Order: '+o.id),node('p','Member: '+o.user_id),node('p','Receiving wallet: '+o.wallet));const a=link('Inspect transaction on Tronscan','https://tronscan.org/#/transaction/'+o.txid);a.target='_blank';a.rel='noopener noreferrer';row.append(a);const label=node('label','Verification note (visible to member)');const note=node('textarea','');note.name='note';note.required=true;note.minLength=5;label.append(note);row.append(label);const check=node('label','');const box=document.createElement('input');box.type='checkbox';box.name='verified';check.append(box,document.createTextNode(' I verified successful USDT transfer, network, recipient, net amount and confirmations.'));row.append(check);for(const [value,text]of [['approve','Approve and activate'],['reject','Reject']]){const b=node('button',text);b.value=value;b.className='button secondary';row.append(b);}row.addEventListener('submit',run(async e=>{const approve=e.submitter.value==='approve';if(approve&&!box.checked)throw Error('Verify the on-chain transfer before approving.');checked(await db.rpc('bgm_review_order',{p_order:o.id,p_approve:approve,p_note:note.value}));say(approve?'Payment approved. Membership extended.':'Payment rejected.');await loadAdmin();}));list.append(row);});
  const articles=checked(await db.from('bgm_articles').select('*').order('updated_at',{ascending:false}));$('admin-articles').replaceChildren(node('h3','Existing articles'));
  articles.forEach(a=>{const b=node('button',a.title+(a.published?' · Published':' · Draft'));b.type='button';b.className='button secondary';b.onclick=async()=>{try{const rows=checked(await db.from('bgm_article_bodies').select('body').eq('article_id',a.id));const f=$('article-form');for(const key of ['slug','title','preview'])f.elements[key].value=a[key];f.elements.body.value=rows[0]?.body||'';f.elements.published.checked=a.published;}catch(e){say(e.message);}};$('admin-articles').append(b);});
 }
 bind('auth-form',async e=>{const f=e.currentTarget;const email=f.elements.email.value.trim(),password=f.elements.password.value,action=e.submitter.value;
  if(action==='reset'){if(!f.elements.email.checkValidity())throw Error('Enter a valid email address.');checked(await db.auth.resetPasswordForEmail(email,{redirectTo:location.origin+'/account/'}));say('If an account exists, check its email for a password-reset link.');return;}
  if(action==='signup'){checked(await db.auth.signUp({email,password,options:{emailRedirectTo:location.origin+'/account/'}}));say('Check your email to confirm your account, then sign in.');}else{checked(await db.auth.signInWithPassword({email,password}));await refresh();}f.elements.password.value='';
 });
 $('signout').onclick=async()=>{try{checked(await db.auth.signOut());await refresh();}catch(e){say(e.message);}};
 bind('password-form',async e=>{checked(await db.auth.updateUser({password:e.currentTarget.elements.password.value}));e.currentTarget.reset();say('Password updated.');});
 bind('order-form',async e=>{order=checked(await db.rpc('bgm_create_order',{p_plan:e.currentTarget.elements.plan.value}));history.replaceState(null,'','?order='+order.id);await loadOrder(order.id);say('Payment request created. Keep the order ID for your records.');});
 bind('tx-form',async e=>{if(!order)throw Error('Create a payment request first');checked(await db.rpc('bgm_submit_tx',{p_order:order.id,p_txid:e.currentTarget.elements.txid.value.trim()}));show('payment-instructions',false);say('Transaction submitted. The team must verify it before access is activated. View status in My account.');});
 if($('copy-wallet'))$('copy-wallet').onclick=async()=>{try{await navigator.clipboard.writeText(order.wallet);say('Wallet address copied.');}catch{say('Copy the displayed wallet address manually.');}};
 bind('article-form',async e=>{const f=e.currentTarget.elements;checked(await db.rpc('bgm_save_article',{p_slug:f.slug.value,p_title:f.title.value,p_preview:f.preview.value,p_body:f.body.value,p_published:f.published.checked}));say('Article saved.');await loadAdmin();});
 db.auth.onAuthStateChange(event=>{if(['SIGNED_OUT','PASSWORD_RECOVERY'].includes(event))setTimeout(()=>refresh().catch(e=>say(e.message)),0);});
 await refresh();
}catch(e){say('Membership service is unavailable. No payment should be sent. '+(e.message||''));}
})();
