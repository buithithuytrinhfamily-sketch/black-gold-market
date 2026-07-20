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

  /* form đăng ký email (nếu nhúng trên trang quà) */
  document.addEventListener('submit', function () {
    send('lead_form_submit', { page: page });
  }, true);

  /* đọc hết bài: biết bài nào giữ chân được người đọc */
  var fired = false;
  window.addEventListener('scroll', function () {
    if (fired) return;
    var h = document.documentElement;
    var pct = (h.scrollTop + window.innerHeight) / h.scrollHeight;
    if (pct >= 0.9) { fired = true; send('article_read_90', { page: page }); }
  }, { passive: true });
})();
