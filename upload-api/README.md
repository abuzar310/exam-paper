# Upload service

Receives photos of question papers from the camera button on https://bcom3.vercel.app/ and
stores them in Vercel Blob (`inbox/<id>/`). Deployed separately, on the second Vercel account
(project `exam-paper-upload`), with `vercel deploy --prod` from this folder.

- `POST /api/upload?id=<id>&n=<page>` with the photo as the body; then
  `POST /api/upload?id=<id>&part=meta` with `{subject, pages, note}`.
- `GET /api/inbox`: uploaded papers not yet solved (ids not in the site's `site/solved-uploads.json`).

Alerts: when `DISCORD_WEBHOOK_URL` is set on the project, each finished upload posts to that
Discord channel (subject, pages, note, photo of page 1). The website also shows a banner, a count
in the tab title, and, after "Alert me", a browser notification when a new paper lands.

## Admin (the site's owner only)

The site has no sign-in button. The owner opens https://bcom3.vercel.app/#/admin and signs in;
the device stays signed in for 30 days (an "Admin" pill shows in the top bar).
Signed in, the owner can remove a "Just landed" paper (its photos are deleted) and hide or show
any solved paper or question paper. Hidden items are marker files `hidden/<key>` in Blob;
`/api/inbox` returns them as `hidden`, and the site leaves them out for everyone else.

- `POST /api/login {email, password}` -> `{token, exp}`; 5 wrong tries lock that address for 15 minutes.
- `POST /api/admin {action: check | remove-upload | hide | show}` with `Authorization: Bearer <token>`.

Secrets live only in the project's environment variables, never in this public repo:
`ADMIN_EMAIL`, `ADMIN_PASS_HASH` (`s1$<salt>$<scrypt hash>`, base64url; the password itself is
stored nowhere) and `ADMIN_SECRET` (signs the tokens; replace it to sign out every device).
To change the password, compute a new hash with Node's `crypto.scryptSync(pw, salt, 32, {N: 16384, r: 8, p: 1})`,
replace `ADMIN_PASS_HASH` and redeploy.

