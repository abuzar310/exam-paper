// Receives photos of a question paper from the site's camera button and saves them in
// Vercel Blob under inbox/<id>/. One request per photo, then one for the details (meta).
import { put } from "@vercel/blob";
import { json as reply, preflight } from "./_cors.js";

const SUBJECTS = new Set([
  "hindi", "corporate-accounting", "english", "accounting-standards",
  "business-statistics", "hrd", "personality-development", "other",
]);
const TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
const MAX_PHOTO = 4_000_000; // bytes; the page shrinks photos well below this
const MAX_PAGES = 8;


const save = (path, body, contentType) =>
  put(path, body, { access: "public", contentType, addRandomSuffix: false, allowOverwrite: true });

export const OPTIONS = preflight;

export async function POST(request) {
  const json = (body, status) => reply(request, body, status);
  const url = new URL(request.url);
  const id = url.searchParams.get("id") || "";
  if (!/^\d{8}-\d{6}-[a-z0-9]{4}$/.test(id)) return json({ error: "Bad upload id." }, 400);

  if (url.searchParams.get("part") === "meta") {
    let meta;
    try { meta = await request.json(); } catch { return json({ error: "Bad details." }, 400); }
    const pages = Number(meta.pages);
    if (!SUBJECTS.has(meta.subject)) return json({ error: "Unknown subject." }, 400);
    if (!Number.isInteger(pages) || pages < 1 || pages > MAX_PAGES) return json({ error: "Bad page count." }, 400);
    const record = {
      id,
      subject: meta.subject,
      note: String(meta.note || "").slice(0, 200),
      pages,
      uploaded: new Date().toISOString(),
    };
    await save(`inbox/${id}/meta.json`, JSON.stringify(record), "application/json");
    return json({ ok: true, id });
  }

  const n = Number(url.searchParams.get("n"));
  if (!Number.isInteger(n) || n < 1 || n > MAX_PAGES) return json({ error: "Bad page number." }, 400);
  const type = (request.headers.get("content-type") || "").split(";")[0].trim();
  if (!TYPES.has(type)) return json({ error: "Only photos (JPEG, PNG, WebP) can be uploaded." }, 415);
  const body = await request.arrayBuffer();
  if (!body.byteLength) return json({ error: "Empty photo." }, 400);
  if (body.byteLength > MAX_PHOTO) return json({ error: "Photo too large." }, 413);
  const ext = type === "image/png" ? "png" : type === "image/webp" ? "webp" : "jpg";
  const blob = await save(`inbox/${id}/page-${n}.${ext}`, body, type);
  return json({ ok: true, url: blob.url });
}
