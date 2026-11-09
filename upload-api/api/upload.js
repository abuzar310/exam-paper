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

const NAMES = {
  hindi: "Hindi", "corporate-accounting": "Corporate Accounting", english: "English",
  "accounting-standards": "Accounting Standards", "business-statistics": "Business Statistics",
  hrd: "Human Resource Development", "personality-development": "Personality Development", other: "Other",
};

// Posts to the Discord channel whose webhook is in DISCORD_WEBHOOK_URL. Never blocks the upload.
async function tellDiscord(record, firstPhoto) {
  const hook = process.env.DISCORD_WEBHOOK_URL;
  if (!hook) return;
  const clean = (t) => t.replace(/[@*_`~|>#\[\]]/g, "").slice(0, 200);
  const body = {
    username: "Exam Paper",
    allowed_mentions: { parse: [] },
    embeds: [{
      title: `New question paper: ${NAMES[record.subject] || "Other"}`,
      url: "https://bcom3.vercel.app/",
      description: [
        `${record.pages} page${record.pages === 1 ? "" : "s"} uploaded from the site.`,
        record.note ? `Note: ${clean(record.note)}` : "",
        "Waiting under Just landed. Say \"solve the paper that just landed\".",
      ].filter(Boolean).join("\n"),
      color: 0x234fbf,
      image: firstPhoto ? { url: firstPhoto } : undefined,
      timestamp: record.uploaded,
    }],
  };
  try {
    await fetch(hook, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body), signal: AbortSignal.timeout(4000) });
  } catch { /* the upload already succeeded; a missed alert is not worth failing it */ }
}

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
    // The page sends the URL of page 1 (returned by its upload); only a photo of this upload is shown.
    const first = typeof meta.first === "string" && /^https:\/\/[a-z0-9]+\.public\.blob\.vercel-storage\.com\/inbox\//.test(meta.first)
      && meta.first.includes(`/inbox/${id}/`) ? meta.first : null;
    await tellDiscord(record, first);
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
