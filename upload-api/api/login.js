// POST /api/login {password} -> {token, exp}. Only the site's owner has an account.
import { json as reply, preflight } from "./_cors.js";
import { cleared, missed, newToken, passwordOk, tooMany } from "./_admin.js";

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

export const OPTIONS = preflight;

export async function POST(request) {
  const json = (body, status) => reply(request, body, status);
  const ip = (request.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "?";
  if (tooMany(ip)) return json({ error: "Too many wrong tries. Wait 15 minutes." }, 429);
  let body;
  try { body = await request.json(); } catch { return json({ error: "Bad request." }, 400); }
  if (!(await passwordOk(body.password || ""))) {
    missed(ip);
    await wait(1200);
    return json({ error: "Wrong password." }, 401);
  }
  cleared(ip);
  return json(newToken());
}
