/* Nguoi giu trang (service worker).
   Viec cua no: giu ban sao trang /links va /ig trong may khach, de:
     1. Lan thu hai tro di mo TUC THI, khong cho mang.
     2. Mat mang van xem duoc trang.
   Cach chay: tra ban luu ra truoc cho nhanh, dong thoi am tham tai ban moi
   ve de lan sau da moi (stale-while-revalidate). */
const KHO = "links-v1";
const GIU = ["/links/", "/ig/", "/avatar.jpg", "/favicon.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(KHO).then((c) => c.addAll(GIU)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((ten) => Promise.all(ten.filter((t) => t !== KHO).map((t) => caches.delete(t))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;           // khong dong vao Telegram, YouTube...
  if (!/^\/(links|ig)\/?$|\.(png|jpg|jpeg|webp|svg|css|js)$/.test(url.pathname)) return;

  e.respondWith(
    caches.open(KHO).then((kho) =>
      kho.match(req, { ignoreSearch: true }).then((daLuu) => {
        const mang = fetch(req)
          .then((res) => {
            if (res && res.status === 200) kho.put(req, res.clone());
            return res;
          })
          .catch(() => daLuu);
        return daLuu || mang;
      })
    )
  );
});
