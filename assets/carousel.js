(() => {
  'use strict';
  const root=document.querySelector('.hero-carousel');
  if(!root)return;
  const slides=[...root.querySelectorAll('.hero-slide')];
  const dots=[...root.querySelectorAll('[data-carousel-to]')];
  const pause=root.querySelector('[data-carousel-pause]');
  const status=root.querySelector('[data-carousel-status]');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let current=0,paused=reduced.matches,hovered=false,timer=null;
  const duration=6500;
  root.querySelector('.carousel-control-row').hidden=false;
  function schedule(){
    clearTimeout(timer);
    pause.textContent=paused?'Play':'Pause';
    pause.setAttribute('aria-label',paused?'Start automatic banners':'Pause automatic banners');
    if(!paused&&!hovered&&!document.hidden)timer=setTimeout(()=>show(current+1),duration);
  }
  function show(index,manual=false){
    current=(index+slides.length)%slides.length;
    slides.forEach((slide,i)=>slide.hidden=i!==current);
    dots.forEach((dot,i)=>{if(i===current)dot.setAttribute('aria-current','true');else dot.removeAttribute('aria-current');});
    if(manual)status.textContent=slides[current].getAttribute('aria-label');
    schedule();
  }
  pause.addEventListener('click',()=>{paused=!paused;schedule();});
  dots.forEach((dot,i)=>dot.addEventListener('click',()=>{paused=true;show(i,true);}));
  root.querySelector('[data-carousel-prev]').addEventListener('click',()=>{paused=true;show(current-1,true);});
  root.querySelector('[data-carousel-next]').addEventListener('click',()=>{paused=true;show(current+1,true);});
  root.addEventListener('pointerenter',e=>{if(e.pointerType==='mouse'){hovered=true;schedule();}});
  root.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse'){hovered=false;schedule();}});
  root.addEventListener('focusin',e=>{if(e.target!==pause){paused=true;schedule();}});
  document.addEventListener('visibilitychange',schedule);
  reduced.addEventListener('change',()=>{if(reduced.matches)paused=true;schedule();});
  let start=null,suppressClick=false;
  root.addEventListener('pointerdown',e=>{if(e.pointerType==='touch'&&e.isPrimary)start={x:e.clientX,y:e.clientY};});
  root.addEventListener('pointerup',e=>{if(!start)return;const x=e.clientX-start.x,y=e.clientY-start.y;start=null;if(Math.abs(x)>55&&Math.abs(x)>Math.abs(y)*1.5){paused=true;suppressClick=true;show(current+(x<0?1:-1),true);setTimeout(()=>suppressClick=false,400);}});
  root.addEventListener('pointercancel',()=>start=null);
  root.addEventListener('click',e=>{if(suppressClick){e.preventDefault();e.stopPropagation();} },true);
  schedule();
})();
