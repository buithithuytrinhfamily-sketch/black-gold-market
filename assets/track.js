/* Black Gold Market — GA4 event tracking (G-NL24SJYSZ8). Loaded on every page.
   Mục đích: đo được BÀI NÀO kéo khách bấm Telegram / tải quà.
   Dùng sự kiện GA4 thay cho UTM, vì UTM gắn vào link nội bộ sẽ cắt phiên và ghi sai nguồn. */
(function () {
  function send(name, params) {
    if (typeof gtag === 'function') gtag('event', name, params || {});
  }
  var page = location.pathname;

  document.addEventListener('click', function (e) {
    var t = e.target;
    var a = t.closest ? t.closest('a') : null;
    if (!a) return;

    var href = a.getAttribute('href') || '';
    var text = (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80);

    if (href.indexOf('t.me/') !== -1) {
      send('telegram_click', { link_url: href, link_text: text, page: page });
    } else if (href.indexOf('/blueprint') !== -1) {
      send('cta_gift_click', { gift: 'blueprint', link_text: text, page: page });
    } else if (href.indexOf('/vip') !== -1) {
      send('cta_vip_click', { link_text: text, page: page });
    } else if (href.indexOf('/book') !== -1) {
      send('cta_book_click', { link_text: text, page: page });
    } else if (/\.pdf($|\?)/i.test(href)) {
      send('gift_pdf_download', { file: href.split('/').pop(), page: page });
    }
  }, true);

  /* KHÔNG đo form ở đây nữa (17/08/2026).
     Máy này bắn 'lead_form_submit' ngay lúc khách BẤM NÚT, tức là trước khi biết
     email có được lưu hay không. Cửa Telegram lại đang gửi vào một form đã chết,
     nên bảng đo hiện ra hàng chục "lead" trong khi danh sách email không thêm ai.
     Giờ chỉ chính đoạn mã của form tự bắn, và chỉ bắn khi máy chủ trả về ok. */

  /* đọc hết bài: biết bài nào giữ chân được người đọc */
  var fired = false;
  window.addEventListener('scroll', function () {
    if (fired) return;
    var h = document.documentElement;
    var pct = (h.scrollTop + window.innerHeight) / h.scrollHeight;
    if (pct >= 0.9) { fired = true; send('article_read_90', { page: page }); }
  }, { passive: true });
})();

/* quote strip */
(function(){
  var Q=[["The two most powerful warriors are patience and time.", "Leo Tolstoy"], ["Adopt the pace of nature: her secret is patience.", "Ralph Waldo Emerson"], ["The creation of a thousand forests is in one acorn.", "Ralph Waldo Emerson"], ["Nature does not hurry, yet everything is accomplished.", "Lao Tzu"], ["A journey of a thousand miles begins with a single step.", "Lao Tzu"], ["To the mind that is still, the whole universe surrenders.", "Lao Tzu"], ["Mastering others is strength. Mastering yourself is true power.", "Lao Tzu"], ["Someone is sitting in the shade today because someone planted a tree a long time ago.", "Warren Buffett"], ["Time is the friend of the wonderful company, the enemy of the mediocre.", "Warren Buffett"], ["The best investment you can make is in yourself.", "Warren Buffett"], ["The big money is not in the buying and selling, but in the waiting.", "Charlie Munger"], ["It is remarkable how much long-term advantage we have gotten by trying to be consistently not stupid.", "Charlie Munger"], ["Slow and steady wins the race.", "Aesop"], ["Little strokes fell great oaks.", "Benjamin Franklin"], ["He that can have patience can have what he will.", "Benjamin Franklin"], ["An ounce of prevention is worth a pound of cure.", "Benjamin Franklin"], ["Well done is better than well said.", "Benjamin Franklin"], ["Constant dripping hollows out a stone.", "Lucretius"], ["Rivers know this: there is no hurry. We shall get there some day.", "A. A. Milne"], ["Patience is not passive; it is concentrated strength.", "Edward Bulwer-Lytton"], ["Trees that are slow to grow bear the best fruit.", "Moliere"], ["With time and patience the mulberry leaf becomes a silk gown.", "Chinese proverb"], ["Have patience. All things are difficult before they become easy.", "Saadi"], ["Perseverance is not a long race; it is many short races one after the other.", "Walter Elliot"], ["It is not that I am so smart, it is just that I stay with problems longer.", "Albert Einstein"], ["Continuous effort, not strength or intelligence, is the key to unlocking our potential.", "Winston Churchill"], ["Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"], ["We suffer more often in imagination than in reality.", "Seneca"], ["Time discovers truth.", "Seneca"], ["No man is free who is not master of himself.", "Epictetus"], ["First say to yourself what you would be; and then do what you have to do.", "Epictetus"], ["It is not what happens to you, but how you react to it that matters.", "Epictetus"], ["Wealth consists not in having great possessions, but in having few wants.", "Epictetus"], ["You have power over your mind, not outside events. Realize this, and you will find strength.", "Marcus Aurelius"], ["Confine yourself to the present.", "Marcus Aurelius"], ["Great things are not done by impulse, but by a series of small things brought together.", "Vincent van Gogh"], ["Little by little, one travels far.", "J. R. R. Tolkien"], ["It always seems impossible until it is done.", "Nelson Mandela"], ["Motivation gets you going, but discipline keeps you growing.", "John C. Maxwell"], ["Small disciplines repeated with consistency every day lead to great achievements.", "John C. Maxwell"], ["The secret of getting ahead is getting started.", "Mark Twain"], ["Keep away from people who try to belittle your ambitions.", "Mark Twain"], ["Time is the most valuable thing a man can spend.", "Theophrastus"], ["Do not watch the clock; do what it does. Keep going.", "Sam Levenson"], ["A year from now you may wish you had started today.", "Karen Lamb"], ["The expert in anything was once a beginner.", "Helen Hayes"], ["Genius is eternal patience.", "Michelangelo"], ["Drop by drop is the water pot filled.", "Buddha"], ["Better than a thousand hollow words is one word that brings peace.", "Buddha"], ["He who would learn to fly one day must first learn to stand and walk and run and climb and dance.", "Friedrich Nietzsche"]];
  var CSS='.bgm-quote{background:#18231c;padding:34px 0;border-bottom:1px solid rgba(255,255,255,.12)}'
   +'.bgm-quote .bgm-quote-in{width:min(1180px,100%);margin:0 auto;padding:0 26px;box-sizing:border-box}'
   +'.bgm-quote blockquote{margin:0;max-width:860px}'
   +'.bgm-quote .bq-text{margin:0 0 10px;font:italic 400 21px/1.55 Georgia,"Times New Roman",serif;color:#f1f5ef}'
   +'.bgm-quote .bq-by{display:block;font:700 12.5px/1.5 system-ui,-apple-system,Arial,sans-serif;letter-spacing:1.5px;text-transform:uppercase;color:#d0a74a;font-style:normal}'
   +'@media(max-width:760px){.bgm-quote{padding:26px 0}.bgm-quote .bq-text{font-size:18px}}';
  function pick(){return Q[Math.floor(Math.random()*Q.length)];}
  function run(){
    try{
      var q=pick();
      var existing=document.querySelector('.daily-quote blockquote p');
      if(existing){
        existing.textContent=q[0];
        var cap=document.querySelector('.daily-quote figcaption');
        if(cap){cap.textContent='\u2014 '+q[1];}
        return;
      }
      var f=document.querySelector('footer.site-footer')||document.querySelector('footer');
      if(!f||document.querySelector('.bgm-quote'))return;
      var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
      var wrap=document.createElement('div');wrap.className='bgm-quote';
      wrap.innerHTML='<div class="bgm-quote-in"><blockquote><p class="bq-text"></p><cite class="bq-by"></cite></blockquote></div>';
      f.insertBefore(wrap,f.firstChild);
      wrap.querySelector('.bq-text').textContent='\u201C'+q[0]+'\u201D';
      wrap.querySelector('.bq-by').textContent=q[1];
      var pt=getComputedStyle(f).paddingTop;
      if(pt&&parseInt(pt,10)>0){wrap.style.marginTop='-'+pt;wrap.style.marginBottom='34px';}
    }catch(e){}
  }
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',run);}else{run();}
})();
