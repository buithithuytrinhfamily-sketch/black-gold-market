/* Pure calculation functions shared by the UI and numerical checks. */
(function(root){
 'use strict';
 const need=(condition,message)=>{if(!condition)throw Error(message);};
 const positive=(...v)=>v.every(n=>Number.isFinite(n)&&n>0);
 const series=s=>{const a=String(s).trim().split(/[\s,;]+/).map(Number);need(a.length>=4&&a.length<=10000&&positive(...a),'Enter 4–10,000 positive closing prices, separated by commas or whitespace.');return a;};
 const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
 const returns=a=>a.slice(1).map((v,i)=>v/a[i]-1);
 const methods={
 position(v){need(positive(v.balance,v.risk,v.stop,v.pipValue,v.step)&&v.risk<=100,'Use positive inputs and a risk percentage no greater than 100.');const budget=v.balance*v.risk/100;const lots=Math.floor(budget/(v.stop*v.pipValue*v.step)+1e-10)*v.step;return {'Lots (rounded down)':lots,'Risk budget':budget,'Planned loss before costs':lots*v.stop*v.pipValue};},
 pip(v){need(positive(v.units,v.pip,v.rate),'All inputs must be positive.');return {'Pip value (account currency)':v.units*v.pip*v.rate,'Pip value (quote currency)':v.units*v.pip};},
 gain(v){need(positive(v.start)&&Number.isFinite(v.end)&&v.end>=0,'Starting balance must be positive; ending balance cannot be negative.');return {'Balance change':v.end-v.start,'Change (%)':(v.end/v.start-1)*100,'Recovery needed (%)':v.end===0?'No finite recovery':v.end<v.start?(v.start/v.end-1)*100:0};},
 pivot(v){need(positive(v.high,v.low,v.close)&&v.high>=v.low&&v.close>=v.low&&v.close<=v.high,'High must be at least low, and close must lie between them.');const p=(v.high+v.low+v.close)/3,d=v.high-v.low;return {'Pivot':p,'R1':2*p-v.low,'S1':2*p-v.high,'R2':p+d,'S2':p-d,'R3':v.high+2*(p-v.low),'S3':v.low-2*(v.high-p)};},
 expectancy(v){need([v.winRate,v.win,v.cost].every(n=>Number.isFinite(n)&&n>=0)&&v.winRate<=100&&positive(v.loss),'Use non-negative values, a positive average loss and win rate at or below 100.');const p=v.winRate/100;return {'Expected net outcome per trade':p*v.win-(1-p)*v.loss-v.cost,'Break-even win rate (%)':(v.loss+v.cost)/(v.win+v.loss)*100};},
 reward(v){need(positive(v.entry,v.stop,v.target)&&v.entry!==v.stop,'Use positive prices with entry different from stop.');need((v.target-v.entry)*(v.entry-v.stop)>0,'Target must be on the opposite side of entry from stop.');const risk=Math.abs(v.entry-v.stop),reward=Math.abs(v.target-v.entry);return {'Direction':v.entry>v.stop?'Long':'Short','Reward / risk':reward/risk,'Risk distance':risk,'Reward distance':reward,'Break-even win rate before costs (%)':risk/(risk+reward)*100};},
 correlation(v){const a=series(v.a),b=series(v.b);need(a.length===b.length,'Both series must have the same number of aligned closing prices.');const x=returns(a),y=returns(b),mx=mean(x),my=mean(y);let xx=0,yy=0,xy=0;x.forEach((n,i)=>{xx+=(n-mx)**2;yy+=(y[i]-my)**2;xy+=(n-mx)*(y[i]-my);});need(xx>1e-24&&yy>1e-24,'Correlation is undefined when either return series is constant.');return {'Return correlation':Math.max(-1,Math.min(1,xy/Math.sqrt(xx*yy))),'Paired returns':x.length};},
 volatility(v){const a=series(v.prices);need(Number.isInteger(v.periods)&&v.periods>0&&v.periods<=100000,'Observations per year must be an integer from 1 to 100,000.');const r=a.slice(1).map((p,i)=>Math.log(p/a[i])),m=mean(r),sd=Math.sqrt(r.reduce((s,n)=>s+(n-m)**2,0)/(r.length-1));return {'Per-observation volatility (%)':sd*100,'Annualized volatility (%)':sd*Math.sqrt(v.periods)*100,'Return observations':r.length};},
 sentiment(v){need(Object.values(v).every(Number.isFinite),'Enter finite changes for all four observations.');const score=Math.sign(v.equity)+Math.sign(v.aud)-Math.sign(v.vix)-Math.sign(v.credit);return {'Checklist score (−4 to +4)':score,'Observed tilt':score>=2?'More risk-on observations':score<=-2?'More risk-off observations':'Mixed or unchanged observations'};}
 };
 root.BgmMath={methods};if(typeof module!=='undefined')module.exports=root.BgmMath;
})(typeof window!=='undefined'?window:globalThis);
