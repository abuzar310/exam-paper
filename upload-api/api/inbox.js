// Lists question papers uploaded from the camera button that are not solved yet, plus
// the papers the admin hid from the site ({items, hidden}). A paper counts as solved once
// its id is in site/solved-uploads.json on the website (committed to the exam-paper repo).
import { list } from "@vercel/blob";
import { json as reply, preflight } from "./_cors.js";


export const OPTIONS = preflight;

export async function GET(request) {
  const json = (body, status) => reply(request, body, status);
  const solved = new Set(
    await fetch("https://bcom3.vercel.app/site/solved-uploads.json", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : []))
      .then((d) => (Array.isArray(d) ? d.map((x) => (typeof x === "string" ? x : x.id)) : []))
      .catch(() => []),
  );

  const groups = new Map();
  const hidden = [];
  let cursor;
  do {
    const page = await list({ limit: 1000, cursor }); // one call: inbox/ and hidden/
    for (const b of page.blobs) {
      const [dir, id, file] = b.pathname.split("/");
      if (dir === "hidden" && id) {
        const key = Buffer.from(id, "base64url").toString();
        if (/^[pq]:/.test(key)) hidden.push(key);
        continue;
      }
      if (dir !== "inbox") continue;
      if (!id || !file || solved.has(id)) continue;
      const g = groups.get(id) || { id, pages: [], metaUrl: null };
      if (file === "meta.json") g.metaUrl = b.url;
      else if (/^page-\d+\./.test(file)) g.pages.push({ n: Number(file.match(/\d+/)[0]), url: b.url, size: b.size });
      groups.set(id, g);
    }
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);

  const items = [];
  for (const g of groups.values()) {
    if (!g.metaUrl) continue; // still uploading, or abandoned half-way
    const meta = await fetch(g.metaUrl, { cache: "no-store" }).then((r) => r.json()).catch(() => null);
    if (!meta) continue;
    items.push({ ...meta, photos: g.pages.sort((a, b) => a.n - b.n).map((p) => p.url) });
  }
  items.sort((a, b) => b.uploaded.localeCompare(a.uploaded));
  return json({ items, hidden });
}
