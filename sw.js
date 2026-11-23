// Service worker of the Middle-earth Explorer. It keeps a copy of the page so that the map opens without a connection.
// The page is fetched network first and the browser cache is asked to revalidate, so a new build shows at once when there is a connection
// (an unchanged 24 MB page costs one small request, not a new download). The saved copy is used only when the network fails.
// The shared files /shared-ui/tokens.css and /shared-ui/shell.js are saved at run time and served from the saved copy first,
// so the app starts offline after one online visit. Old caches are removed when a new worker starts.
// Change the version number below when the rules in this file change.
const VERSION = 'v2', CACHE = 'lotr-explorer-' + VERSION, PAGE = new URL('./', self.location).href;
const SHARED = ['/shared-ui/tokens.css', '/shared-ui/shell.js'].map(p => new URL(p, self.location.origin).href);
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => Promise.all([c.add(PAGE), ...SHARED.map(u => c.add(u))].map(p => p.catch(() => {})))));
});
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith('lotr-explorer-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())
));
self.addEventListener('fetch', e => {
  const r = e.request, url = new URL(r.url);
  if (r.method !== 'GET' || url.origin !== self.location.origin) return;
  if (SHARED.includes(url.href.split('?')[0])) {   // saved copy first, refreshed in the background
    e.respondWith(caches.open(CACHE).then(c => c.match(url.href.split('?')[0]).then(hit => {
      const net = fetch(r).then(res => { if (res.ok && res.type === 'basic') c.put(url.href.split('?')[0], res.clone()); return res; });
      if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
      return net;
    })).catch(() => Response.error()));
    return;
  }
  const key = r.mode === 'navigate' ? PAGE : r;
  const net = r.mode === 'navigate' ? fetch(new Request(r.url, { cache: 'no-cache', credentials: 'same-origin', redirect: 'manual' })) : fetch(r);
  e.respondWith(net.then(res => {
    if (res.type === 'opaqueredirect') return res;
    if (res.ok && res.type === 'basic') { const copy = res.clone(); e.waitUntil(caches.open(CACHE).then(c => c.put(key, copy))); return res; }
    return r.mode === 'navigate' ? caches.match(key).then(m => m || res) : res;
  }).catch(() => caches.match(key, { ignoreSearch: true }).then(m => m || Response.error())));
});
