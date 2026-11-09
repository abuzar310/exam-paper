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
