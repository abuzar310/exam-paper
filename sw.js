// Exam Paper offline support.
// - The site itself (page, script, styles, font, list of papers) is kept so it opens without internet.
// - Every paper file you open (PDF, page image, photo) is saved the first time, and opens offline later.
//   Nothing is downloaded in advance (his choice, 24 Nov 2026).
// - Files have a ?v=<hash> in their links, so a changed paper is a new link and is fetched fresh;
//   the page sends the current list of links and old copies are deleted.
const SHELL = "shell-v1";
const FILES = "files-v1";
const SHELL_URLS = [
  "./",
  "index.html",
  "site/app.js",
  "site/style.css",
  "site/catalog.json",
  "site/manifest.webmanifest",
  "site/fonts/atkinson-next-latin.woff2",
  "site/icons/icon-192.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(SHELL).then((c) => c.addAll(SHELL_URLS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== SHELL && k !== FILES).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

const inScope = (url) => url.origin === self.location.origin && url.pathname.startsWith(new URL("./", self.location).pathname);
const isShell = (url) => /\/(index\.html|site\/app\.js|site\/style\.css|site\/catalog\.json|site\/solved-uploads\.json|site\/manifest\.webmanifest)$/.test(url.pathname)
  || url.pathname === new URL("./", self.location).pathname;

// Site files: try the internet first (so updates show), fall back to the saved copy.
// On a slow phone connection, give up waiting after 4 seconds if a saved copy exists.
async function networkFirst(req) {
  const cache = await caches.open(SHELL);
  const saved = (await cache.match(req, { ignoreSearch: true }))
    || (req.mode === "navigate" ? await cache.match("index.html") : undefined);
  const fromNet = fetch(req).then((res) => {
    if (res.ok) cache.put(req.url.split("?")[0], res.clone());
    return res;
  });
  if (!saved) return fromNet.catch(() => cache.match("index.html"));
  const timeout = new Promise((resolve) => setTimeout(() => resolve(saved), 4000));
  return Promise.race([fromNet.catch(() => saved), timeout]);
}

// Serve part of a saved file when the PDF viewer asks for a byte range.
async function partial(res, range) {
  const buf = await res.arrayBuffer();
  const m = /bytes=(\d*)-(\d*)/.exec(range || "");
  if (!m) return new Response(buf, { headers: res.headers });
  const start = m[1] === "" ? Math.max(0, buf.byteLength - Number(m[2])) : Number(m[1]);
  const end = m[1] !== "" && m[2] !== "" ? Math.min(Number(m[2]), buf.byteLength - 1) : buf.byteLength - 1;
  const headers = new Headers(res.headers);
  headers.set("Content-Range", `bytes ${start}-${end}/${buf.byteLength}`);
  headers.set("Content-Length", String(end - start + 1));
  return new Response(buf.slice(start, end + 1), { status: 206, statusText: "Partial Content", headers });
}

// Paper files: use the saved copy if there is one; otherwise download it, save it, and show it.
async function savedFirst(req) {
  const cache = await caches.open(FILES);
  const range = req.headers.get("range");
  const key = req.url;
  const saved = await caches.match(key); // either store: the font and icon are kept with the site
  if (saved) return range ? partial(saved, range) : saved;
  if (range) {
    // The viewer wants a piece: save the whole file in the background, pass this request through.
    fetch(key).then((res) => { if (res.ok && res.status === 200) cache.put(key, res); }).catch(() => {});
    return fetch(req);
  }
  const res = await fetch(req);
  if (res.ok && res.status === 200) cache.put(key, res.clone());
  return res;
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (!inScope(url)) return; // upload service and anything else: straight to the internet
  if (req.mode === "navigate") { e.respondWith(networkFirst(req)); return; }
  if (isShell(url)) { e.respondWith(networkFirst(req)); return; }
  e.respondWith(savedFirst(req).catch(() => new Response("", { status: 504, statusText: "Offline" })));
});

// The page sends the links in the current list; saved copies of older versions are removed.
self.addEventListener("message", (e) => {
  const d = e.data || {};
  if (d.type !== "keep" || !Array.isArray(d.urls)) return;
  const keep = new Set(d.urls.map((u) => new URL(u, self.location).href));
  e.waitUntil(caches.open(FILES).then(async (cache) => {
    for (const req of await cache.keys()) {
      const u = new URL(req.url);
      if (u.search.startsWith("?v=") && !keep.has(req.url)) await cache.delete(req);
    }
  }));
});
