// Service worker of the Middle-earth Explorer. It keeps a copy of the page so that the map opens without a connection.
// It asks the network first, so a new version shows at once when there is a connection. It never touches requests to other sites.
const CACHE = 'lotr-explorer-v1', PAGE = new URL('./', self.location).href;
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(CACHE).then(c => c.add(PAGE)).catch(() => {})); });
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET' || new URL(r.url).origin !== self.location.origin) return;
  const key = r.mode === 'navigate' ? PAGE : r;
  e.respondWith(fetch(r).then(res => {
    if (res.ok && res.type === 'basic') { const copy = res.clone(); e.waitUntil(caches.open(CACHE).then(c => c.put(key, copy))); return res; }
    return r.mode === 'navigate' ? caches.match(key).then(m => m || res) : res;
  }).catch(() => caches.match(key, { ignoreSearch: true }).then(m => m || Response.error())));
});
