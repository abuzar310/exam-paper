// Admin sign-in for the site's owner. Nothing secret is in this repo (it is public):
// ADMIN_PASS_HASH ("s1$<salt>$<scrypt hash>", base64url) and ADMIN_SECRET
// (the key that signs sign-in tokens) are environment variables on the Vercel project.
// Changing ADMIN_SECRET signs out every device.
import { createHmac, scrypt, timingSafeEqual } from "node:crypto";

const DAY = 86_400_000;
export const SESSION_DAYS = 30;

const same = (a, b) => a.length === b.length && timingSafeEqual(a, b);
const hashOf = (password, salt) =>
  new Promise((ok, fail) => scrypt(password, salt, 32, { N: 16384, r: 8, p: 1 }, (e, k) => (e ? fail(e) : ok(k))));

// Password only (the owner's call, 2026-11-09): there is a single admin.
export async function passwordOk(password) {
  const [kind, salt, hash] = String(process.env.ADMIN_PASS_HASH || "").split("$");
  if (kind !== "s1" || !salt || !hash) return false;
  const got = await hashOf(String(password).slice(0, 200), Buffer.from(salt, "base64url"));
  return same(got, Buffer.from(hash, "base64url"));
}

const sign = (exp) => createHmac("sha256", process.env.ADMIN_SECRET || "").update(`admin.${exp}`).digest("base64url");

export function newToken() {
  if (!process.env.ADMIN_SECRET) throw new Error("ADMIN_SECRET is not set");
  const exp = Date.now() + SESSION_DAYS * DAY;
  return { token: `${exp}.${sign(exp)}`, exp };
}

export function isAdmin(request) {
  if (!process.env.ADMIN_SECRET) return false;
  const m = (request.headers.get("authorization") || "").match(/^Bearer (\d{13})\.([\w-]{43})$/);
  if (!m || Number(m[1]) < Date.now()) return false;
  return same(Buffer.from(m[2]), Buffer.from(sign(m[1])));
}

// Wrong guesses are slowed down per address, on top of the cost of scrypt.
const misses = new Map();
export function tooMany(ip) {
  const m = misses.get(ip);
  return Boolean(m && m.n >= 5 && Date.now() - m.at < 15 * 60_000);
}
export function missed(ip) {
  const m = misses.get(ip) || { n: 0, at: 0 };
  misses.set(ip, { n: Date.now() - m.at > 15 * 60_000 ? 1 : m.n + 1, at: Date.now() });
}
export const cleared = (ip) => misses.delete(ip);
