importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");

// /web/service_worker.js
const CACHE_NAME = "mindful-cache-v5";
const CORE_ASSETS = ["/", "/index.html", "/manifest.json", "/assets/logo.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((c) => c.addAll(CORE_ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((k) => (k === CACHE_NAME ? null : caches.delete(k))))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  event.respondWith(
    fetch(req)
      .then((res) => {
        const clone = res.clone();
        caches.open(CACHE_NAME).then((c) => c.put(req, clone));
        return res;
      })
      .catch(() => caches.match(req).then((r) => r || caches.match("/index.html")))
  );
});
