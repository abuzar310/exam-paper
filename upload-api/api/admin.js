// POST /api/admin {action, ...} with "Authorization: Bearer <token>" from /api/login.
//   check                       is this token still signed in?
//   remove-upload {id}          delete a "Just landed" paper (its photos and details)
//   hide {key, title}           hide a solved paper or question paper from the site
//   show {key}                  put it back
// Hidden items are marker files hidden/<key in base64url>; /api/inbox lists them for the site.
import { del, list, put } from "@vercel/blob";
import { json as reply, preflight } from "./_cors.js";
import { isAdmin } from "./_admin.js";

export const OPTIONS = preflight;

const KEY = /^[pq]:[\w./-]{1,200}$/;
export const markerPath = (key) => `hidden/${Buffer.from(key).toString("base64url")}`;

export async function POST(request) {
  const json = (body, status) => reply(request, body, status);
  if (!isAdmin(request)) return json({ error: "Signed out. Sign in again." }, 401);
  let body;
  try { body = await request.json(); } catch { return json({ error: "Bad request." }, 400); }

  switch (body.action) {
    case "check":
      return json({ ok: true });

    case "remove-upload": {
      const id = String(body.id || "");
      if (!/^\d{8}-\d{6}-[a-z0-9]{4}$/.test(id)) return json({ error: "Bad upload id." }, 400);
      const { blobs } = await list({ prefix: `inbox/${id}/`, limit: 50 });
      if (!blobs.length) return json({ error: "That paper is already gone." }, 404);
      await del(blobs.map((b) => b.url));
      return json({ ok: true, removed: blobs.length });
    }

    case "hide": {
      const key = String(body.key || "");
      if (!KEY.test(key)) return json({ error: "Bad item." }, 400);
      const record = { key, title: String(body.title || "").slice(0, 200), hidden: new Date().toISOString() };
      await put(markerPath(key), JSON.stringify(record), {
        access: "public", contentType: "application/json", addRandomSuffix: false, allowOverwrite: true,
      });
      return json({ ok: true });
    }

    case "show": {
      const key = String(body.key || "");
      if (!KEY.test(key)) return json({ error: "Bad item." }, 400);
      const { blobs } = await list({ prefix: markerPath(key), limit: 20 });
      const mine = blobs.filter((b) => b.pathname === markerPath(key));
      if (mine.length) await del(mine.map((b) => b.url));
      return json({ ok: true });
    }

    default:
      return json({ error: "Unknown action." }, 400);
  }
}
