(() => {
  'use strict';
  document.querySelectorAll('.site-nav a').forEach(a => {
    if (a.getAttribute('href') === location.pathname) a.setAttribute('aria-current', 'page');
  });
  const feed = document.querySelector('#journal .j-grid');
  if (feed) {
    const cards = [...feed.querySelectorAll('.jcard')];
    let shown = 6;
    const more = document.querySelector('[data-more]');
    const render = () => { cards.forEach((c, i) => c.hidden = i >= shown); more.hidden = shown >= cards.length; };
    more.addEventListener('click', () => { const next = cards[shown]; shown += 6; render(); next?.focus(); });
    render();
  }
  const library = document.querySelector('.journal-page .j-grid');
  if (library) {
    const search = document.getElementById('article-search'), topic = document.getElementById('article-topic');
    const cards = [...library.querySelectorAll('.jcard')];
    const category = card => {
      const title = card.querySelector('h3').textContent.toLowerCase();
      if (/emotion|revenge|patience|psychology|discipline|overtrading|consistent|marathon|mentor|profit too early/.test(title)) return 'psychology';
      if (/risk|margin|lot|capital|drawdown|loss|broker|scam|withdraw|slippage|swap|spread|commission|requote|account|sizing|balance/.test(title)) return 'risk';
      return 'markets';
    };
    const requested = new URLSearchParams(location.search).get('topic');
    if ([...topic.options].some(o => o.value === requested)) topic.value = requested;
    function filter() {
      let count = 0;
      const query = search.value.trim().toLowerCase();
      cards.forEach(card => {
        card.hidden = !(card.textContent.toLowerCase().includes(query) && (topic.value === 'all' || category(card) === topic.value));
        if (!card.hidden) count++;
      });
      document.getElementById('article-count').textContent = count ? `${count} of ${cards.length} articles` : 'No articles match. Try a different search or topic.';
    }
    search.addEventListener('input', filter); topic.addEventListener('change', filter); filter();
  }
  const form = document.getElementById('risk-form');
  if (form) {
    function calculate(e) {
      if(e) e.preventDefault();
      const values = Object.fromEntries(new FormData(form));
      const {balance,risk,entry,stop,target,contract,step} = Object.fromEntries(Object.entries(values).map(([k,v]) => [k, Number(v)]));
      const error = document.getElementById('calc-error'), results = document.getElementById('calc-results');
      error.textContent = ''; results.innerHTML = '';
      if (![balance,risk,entry,stop,target,contract,step].every(v => Number.isFinite(v) && v > 0) || risk > 100) { error.textContent = 'Enter positive values in every field, with risk at or below 100%.'; return; }
      if (entry === stop) { error.textContent = 'Entry and stop-loss must be different.'; return; }
      if ((target-entry)*(entry-stop) <= 0) { error.textContent = 'Place the target on the opposite side of entry from the stop-loss.'; return; }
      const distance = Math.abs(entry-stop), budget = balance*risk/100;
      const lots = Math.floor((budget/(distance*contract))/step + 1e-10)*step;
      const loss = lots*contract*distance, reward = Math.abs(target-entry)/distance;
      if (![lots,loss,reward,budget].every(Number.isFinite)) {error.textContent='These values are too large to calculate. Use smaller values.';return;}
      const usd = v => v.toLocaleString('en-US', {style:'currency',currency:'USD'});
      results.innerHTML = `<p class="result-number">${lots.toLocaleString('en-US',{maximumFractionDigits:8})} <span style="font-size:1rem">lots</span></p><p>${entry > stop ? 'Long' : 'Short'} position · rounded down</p><div class="result-row"><span>Risk budget</span><strong>${usd(budget)}</strong></div><div class="result-row"><span>Estimated stop loss</span><strong>${usd(loss)}</strong></div><div class="result-row"><span>Reward / risk</span><strong>${reward.toFixed(2)} : 1</strong></div><div class="result-row"><span>Estimated target profit</span><strong>${usd(loss*reward)}</strong></div>${lots === 0 ? '<p>Your risk budget is too small for this lot increment. Do not round the position up.</p>' : ''}`;
    }
    form.addEventListener('submit', calculate);
    form.addEventListener('input', () => {document.getElementById('calc-results').textContent='Inputs changed. Calculate again to update your plan.';document.getElementById('calc-error').textContent='';});
    calculate();
  }
})();
