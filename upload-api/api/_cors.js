// The website lives on another domain, so the browser needs these CORS headers.
const ALLOWED = new Set([
  "https://bcom3.vercel.app",
  "https://exam-paper-bcom.vercel.app",
  "https://abuzar310.github.io",
  "http://localhost:8765",
]);

export function cors(request) {
  const origin = request.headers.get("origin") || "";
  return {
    "access-control-allow-origin": ALLOWED.has(origin) ? origin : "https://bcom3.vercel.app",
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type, authorization",
    "access-control-max-age": "86400",
    vary: "origin",
  };
}

export const json = (request, body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store", ...cors(request) },
  });

export const preflight = (request) => new Response(null, { status: 204, headers: cors(request) });
