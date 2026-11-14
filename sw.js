/* TrickySSC app service worker — TSSC-APP-V2 (2026-11-14)
   Deliberately small. It only touches page navigations:
     • /app.html opens instantly from cache and refreshes itself in the background
     • every other page loads from the network as before, with one line added: the
       /tssc-app.js script tag. That script does nothing in a normal browser; inside the
       app it swaps the website header for the app bar and bottom tabs. Adding it here
       means no page (and no page-build script) has to be edited.
     • if the phone is offline, the visitor sees /offline.html instead of the browser's
       error page
   Scripts, images, Firestore and payments are never intercepted or cached.
   Bump VERSION whenever app.html or offline.html must reach phones at once. */
const VERSION = 'tssc-app-v8';
const SHELL = ['/app.html', '/offline.html', '/app-icon-192.png'];
const APP_JS = '<script src="/tssc-app.js?v=6"></script>';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith('tssc-app-') && k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

/* network page + the app script tag; any problem → the page exactly as the server sent it */
async function page(req) {
  const res = await fetch(req);
  try {
    const type = res.headers.get('content-type') || '';
    if (!res.ok || res.status !== 200 || !type.includes('text/html')) return res;
    const html = await res.clone().text();
    const at = html.search(/<\/head>/i);
    if (at < 0 || html.includes('/tssc-app.js')) return res;
    const headers = new Headers(res.headers);
    headers.delete('content-length');
    headers.delete('content-encoding');
    return new Response(html.slice(0, at) + APP_JS + html.slice(at), { status: 200, statusText: res.statusText, headers });
  } catch (err) {
    return res;
  }
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || req.mode !== 'navigate') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (url.pathname === '/app.html') {
    e.respondWith(caches.open(VERSION).then(async cache => {
      const cached = await cache.match('/app.html');
      const fresh = fetch('/app.html', { cache: 'no-cache' })
        .then(r => { if (r.ok) cache.put('/app.html', r.clone()); return r; })
        .catch(() => null);
      return cached || (await fresh) || cache.match('/offline.html');
    }));
    return;
  }
  if (url.pathname === '/offline.html') return;
  e.respondWith(page(req).catch(() => caches.match('/offline.html')));
});
