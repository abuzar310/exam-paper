// Exam Paper: renders site/catalog.json (made by site/build.py) into the shelf and subject pages.
(() => {
  const view = document.getElementById("view");
  const viewer = document.getElementById("viewer");
  const viewerImg = document.getElementById("viewer-img");
  const viewerCaption = document.getElementById("viewer-caption");
  const viewerOpen = document.getElementById("viewer-open");
  const viewerDl = document.getElementById("viewer-dl");
  const UPLOAD_API = (location.hostname === "localhost" && localStorage.getItem("api")) || "https://exam-paper-upload.vercel.app/api";
  let data = null;
  let landed = [];
  let gallery = { items: [], index: 0, label: "" };

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const plural = (n, one, many = one + "s") => `${n} ${n === 1 ? one : many}`;
  const fileName = (path) => path.split("/").pop();

  const icon = {
    arrow: '<svg class="arrow" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    back: '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    open: '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    download: '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    search: '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    trash: '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M5 7h14M10 7V4.5h4V7M7 7l1 13h8l1-13M10.5 11v5.5M13.5 11v5.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    eyeOff: '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M3 3l18 18M10.6 6.1A9.7 9.7 0 0 1 12 6c5 0 8.5 4.4 9.5 6-.4.7-1.3 1.9-2.5 3.1M6.6 7.6C4.6 8.9 3.2 10.8 2.5 12c1 1.6 4.5 6 9.5 6 1.6 0 3-.4 4.3-1.1M9.9 10a3 3 0 0 0 4.2 4.2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    eye: '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M2.5 12c1-1.6 4.5-6 9.5-6s8.5 4.4 9.5 6c-1 1.6-4.5 6-9.5 6s-8.5-4.4-9.5-6z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.9"/></svg>',
    print: '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M7 9V4h10v5M7 17H5a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-2M7 14h10v6H7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
  };

  const codesOf = (s) => {
    const codes = new Set();
    [...s.solved, ...s.questions].forEach((p) => (p.title.match(/Q\.P\. (\w+)/g) || []).forEach((c) => codes.add(c.replace("Q.P. ", ""))));
    return [...codes];
  };

  function subjectTile(s, i) {
    const codes = codesOf(s);
    const solved = s.solved.length, qs = s.questions.length;
    const counts = [
      solved ? `<span class="count count--solved">${solved} solved</span>` : "",
      qs ? `<span class="count">${plural(qs, "question paper")}</span>` : "",
      !solved && !qs ? '<span class="count count--none">Nothing here yet</span>' : "",
    ].join("");
    const sub = s.semester ? s.semester : codes.length ? `Q.P. ${codes.slice(0, 3).join(", ")}` : "No paper code yet";
    const search = [s.name, ...codes].join(" ").toLowerCase();
    return `<li style="--i:${i}"><a class="subject" href="#/${esc(s.id)}" data-search="${esc(search)}">
      <span class="subject__name">${esc(s.name)}</span>
      <span class="subject__codes">${esc(sub)}</span>
      <span class="subject__foot"><span class="counts">${counts}</span>${icon.arrow}</span>
    </a></li>`;
  }

  function renderHome() {
    document.title = "Exam Paper · III B.Com solved papers";
    const solved = data.subjects.reduce((n, s) => n + seen(s).solved.length, 0);
    view.innerHTML = `
      <section class="intro">
        <h1>Solved papers for every subject, ready to print.</h1>
        <p>The seven subjects of the third semester. Open a subject to view or download its solved papers (${solved} so far) and its question papers.</p>
        <p class="tip">${icon.print}<span>Printing nine pages to a sheet? Print the <strong>PDF</strong>, not the page images. The PDF stays sharp; the images go blurry when shrunk.</span></p>
      </section>
      <section class="landed" id="landed" aria-labelledby="h-landed" hidden></section>
      <div class="find">
        <label for="q">Find a subject</label>
        ${icon.search}
        <input id="q" type="search" placeholder="Subject or paper code" autocomplete="off" enterkeyhint="search">
      </div>
      <ul class="shelf" id="shelf">${data.subjects.map((s, i) => subjectTile(seen(s), i)).join("")}</ul>
      <p class="no-match" id="no-match" hidden>No subject matches that. Try a paper code like 54321.</p>
      ${data.earlier.length ? `<section class="earlier"><h2>Earlier semesters</h2><ul class="shelf">${data.earlier.map((s, i) => subjectTile(seen(s), i)).join("")}</ul></section>` : ""}`;
    renderLanded();
    loadLanded();
    const q = document.getElementById("q");
    q.addEventListener("input", () => {
      const term = q.value.trim().toLowerCase();
      let shown = 0;
      document.querySelectorAll("#shelf .subject").forEach((a) => {
        const hit = !term || a.dataset.search.includes(term);
        a.parentElement.hidden = !hit;
        shown += hit;
      });
      document.getElementById("no-match").hidden = shown > 0;
    });
  }

  function thumbs(items, label, download = false) {
    if (!items.length) return "";
    const key = encodeURIComponent(JSON.stringify(items.map((x) => x.full)));
    return `<div class="pages" role="list">${items.map((x, i) => `
      <div class="pages__item" role="listitem">
        <button type="button" class="thumb" data-gallery="${key}" data-index="${i}" data-label="${esc(label)}" aria-label="${esc(label)}, page ${i + 1}: view image">
          <img src="${esc(x.thumb)}" alt="" loading="lazy" decoding="async" width="112" height="158">
        </button>
        <span class="pages__label">Page ${i + 1}</span>
        ${download ? `<a class="pages__dl" href="${esc(x.full)}" download="${esc(fileName(x.full))}" aria-label="Download page ${i + 1} as PNG">${icon.download}PNG</a>` : ""}
      </div>`).join("")}</div>`;
  }

  function versionBlock(v, label) {
    const meta = [plural(v.pdf_pages, "page"), v.pdf_size, v.images.length ? plural(v.images.length, "PNG page") : ""].filter(Boolean);
    return `<section class="version">
      <div class="version__head">
        <h4>${esc(v.label)}</h4>
        <p class="paper__meta">${meta.map((m) => `<span>${esc(m)}</span>`).join("")}</p>
      </div>
      <div class="actions">
        <a class="btn btn--primary" href="${esc(v.pdf)}" target="_blank" rel="noopener">${icon.open}Open PDF</a>
        <a class="btn" href="${esc(v.pdf)}" download="${esc(fileName(v.pdf))}">${icon.download}Download PDF</a>
      </div>
      ${thumbs(v.images, `${label}, ${v.label.split(",")[0].toLowerCase()}`, true)}
    </section>`;
  }

  function solvedCard(p, subject) {
    const label = `${subject.name}, ${p.title}`;
    const key = paperKey(p);
    return `<article class="paper${hidden.has(key) ? " is-hidden" : ""}">
      <div>
        <h3>${esc(p.title)}</h3>
        <p class="paper__meta"><span>Updated ${esc(p.updated)}</span><span>${plural(p.versions.length, "version")}</span></p>
        ${adminBar(key, label)}
      </div>
      ${p.answered ? `<p class="paper__note">${esc(p.answered)}</p>` : ""}
      ${p.versions.map((v) => versionBlock(v, label)).join("")}
    </article>`;
  }

  function questionRow(q, subject) {
    const key = questionKey(q);
    const cls = `qrow${hidden.has(key) ? " is-hidden" : ""}`;
    const bar = adminBar(key, `${subject.name}, ${q.title}`);
    if (q.photos) {
      const items = q.photos.map((f) => ({ full: f, thumb: f }));
      return `<div class="${cls}"><div><h3>${esc(q.title)}</h3><p class="paper__meta"><span>${plural(q.photos.length, "photo")}</span></p>${bar}</div>${thumbs(items, `${subject.name}, ${q.title}`)}</div>`;
    }
    return `<div class="${cls}">
      <div><h3>${esc(q.title)}</h3><p class="paper__meta"><span>${plural(q.pdf_pages, "page")}</span><span>${esc(q.pdf_size)}</span></p>${bar}</div>
      <div class="actions">
        <a class="btn" href="${esc(q.pdf)}" target="_blank" rel="noopener">${icon.open}Open</a>
        <a class="btn" href="${esc(q.pdf)}" download="${esc(fileName(q.pdf))}" aria-label="Download ${esc(q.title)}">${icon.download}Download</a>
      </div>
    </div>`;
  }

  function renderSubject(s) {
    s = seen(s);
    document.title = `${s.name} · Exam Paper`;
    const counts = [plural(s.solved.length, "solved paper"), plural(s.questions.length, "question paper")].join(" · ");
    view.innerHTML = `
      <a class="crumb" href="#/">${icon.back}All subjects</a>
      <header class="page-head">
        <h1 tabindex="-1">${esc(s.name)}</h1>
        <p>${esc(s.semester ? `${s.semester} · ${counts}` : counts)}</p>
      </header>
      <section class="section" aria-labelledby="h-solved">
        <h2 id="h-solved">Solved papers</h2>
        ${s.solved.length ? s.solved.map((p) => solvedCard(p, s)).join("") : `<p class="empty">No solved papers for ${esc(s.name)} yet.</p>`}
      </section>
      <section class="section" aria-labelledby="h-questions">
        <h2 id="h-questions">Question papers</h2>
        ${s.questions.length ? `<div class="qlist">${s.questions.map((q) => questionRow(q, s)).join("")}</div>` : `<p class="empty">No question papers for ${esc(s.name)} yet.</p>`}
      </section>`;
    view.querySelector("h1").focus({ preventScroll: true });
  }

  function route() {
    if (!data) return;
    const id = decodeURIComponent(location.hash.replace(/^#\/?/, ""));
    const s = [...data.subjects, ...data.earlier].find((x) => x.id === id);
    const draw = () => {
      id === "admin" ? renderAdmin() : s ? renderSubject(s) : renderHome();
      view.classList.remove("view-enter");
      void view.offsetWidth;
      view.classList.add("view-enter");
    };
    draw();
    window.scrollTo(0, 0);
  }

  // Page viewer
  function showPage() {
    const src = gallery.items[gallery.index];
    viewerImg.src = src;
    viewerImg.alt = `${gallery.label}, page ${gallery.index + 1}`;
    viewerCaption.textContent = `${gallery.label} · page ${gallery.index + 1} of ${gallery.items.length}`;
    viewerOpen.href = src;
    viewerDl.href = src;
    viewerDl.download = fileName(src);
    viewer.querySelectorAll("[data-step]").forEach((b) => {
      const next = gallery.index + Number(b.dataset.step);
      b.disabled = next < 0 || next >= gallery.items.length;
      b.hidden = gallery.items.length < 2;
    });
  }
  function step(n) {
    const next = gallery.index + n;
    if (next >= 0 && next < gallery.items.length) { gallery.index = next; showPage(); }
  }
  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-gallery]");
    if (!t) return;
    gallery = { items: JSON.parse(decodeURIComponent(t.dataset.gallery)), index: Number(t.dataset.index), label: t.dataset.label };
    showPage();
    viewer.showModal();
  });
  viewer.addEventListener("click", (e) => {
    if (e.target === viewer || e.target.closest("[data-close]")) viewer.close();
    const b = e.target.closest("[data-step]");
    if (b) step(Number(b.dataset.step));
  });
  viewer.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") step(1);
    if (e.key === "ArrowLeft") step(-1);
  });
  viewer.addEventListener("close", () => { viewerImg.removeAttribute("src"); });

  // ---- Just landed: question papers uploaded from the camera button, not solved yet
  const subjectName = (id) => ([...(data?.subjects || []), ...(data?.earlier || [])].find((s) => s.id === id) || {}).name || "Other";
  const when = (iso) => new Date(iso).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit", timeZone: "Asia/Kolkata" });

  function renderLanded() {
    const box = document.getElementById("landed");
    if (!box) return;
    box.hidden = !landed.length;
    if (!landed.length) { box.innerHTML = ""; return; }
    box.innerHTML = `
      <div class="landed__head">
        <h2 id="h-landed">Just landed</h2>
        <p>${plural(landed.length, "question paper")} uploaded, waiting to be solved.</p>
      </div>
      <div class="qlist">${landed.map((u) => {
        const items = u.photos.map((f) => ({ full: f, thumb: f }));
        const meta = [subjectName(u.subject), when(u.uploaded), plural(u.photos.length, "photo")];
        return `<div class="qrow landed__item">
          <div><h3>${esc(u.note || `${subjectName(u.subject)} question paper`)}</h3>
          <p class="paper__meta">${meta.map((m) => `<span>${esc(m)}</span>`).join("")}</p>
          ${admin ? `<div class="admin-row"><button type="button" class="btn btn--small btn--danger" data-admin="remove-upload" data-id="${esc(u.id)}">${icon.trash}Remove</button></div>` : ""}</div>
          ${thumbs(items, `${subjectName(u.subject)}, uploaded ${when(u.uploaded)}`, true)}
        </div>`;
      }).join("")}</div>`;
  }

  // ---- Alerts: banner + tab count while the site is open, system notification if allowed
  const ownUploads = new Set();
  const store = {
    get: () => { try { return JSON.parse(localStorage.getItem("seen-landed") || "null"); } catch { return null; } },
    set: (ids) => { try { localStorage.setItem("seen-landed", JSON.stringify(ids)); } catch { /* private mode */ } },
  };
  const baseTitle = () => document.title.replace(/^\(\d+\) /, "");
  let unseen = 0;

  function toast(text, link = true) {
    const t = document.getElementById("toast");
    t.innerHTML = `<span>${esc(text)}</span>${link ? '<a href="#/">See it</a>' : ""}<button type="button" aria-label="Dismiss">✕</button>`;
    t.hidden = false;
    t.classList.remove("toast--in"); void t.offsetWidth; t.classList.add("toast--in");
    if (link) t.querySelector("a").onclick = () => { t.hidden = true; };
    t.querySelector("button").onclick = () => { t.hidden = true; };
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => { t.hidden = true; }, 12000);
  }

  function noticeNew(items) {
    const seen = store.get();
    const ids = items.map((u) => u.id);
    if (seen === null) { store.set(ids); return; } // first visit: nothing is "new" yet
    const fresh = items.filter((u) => !seen.includes(u.id) && !ownUploads.has(u.id));
    store.set([...new Set([...seen, ...ids])].slice(-200));
    if (!fresh.length) return;
    const u = fresh[0];
    const text = fresh.length === 1
      ? `New question paper just landed: ${subjectName(u.subject)}${u.note ? `, ${u.note}` : ""}.`
      : `${fresh.length} new question papers just landed.`;
    toast(text);
    if (document.hidden) {
      unseen += fresh.length;
      document.title = `(${unseen}) ${baseTitle()}`;
    }
    if ("Notification" in window && Notification.permission === "granted" && document.hidden) {
      try { new Notification("Exam Paper", { body: text, icon: u.photos[0], tag: u.id }); } catch { /* some phones allow only service-worker notifications */ }
    }
  }

  function loadLanded() {
    fetch(`${UPLOAD_API}/inbox`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : { items: [] }))
      .then((d) => { landed = d.items || []; renderLanded(); noticeNew(landed); takeHidden(d.hidden); })
      .catch(() => {});
  }

  setInterval(() => { if (!document.hidden) loadLanded(); }, 60000);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) return;
    unseen = 0;
    document.title = baseTitle();
    loadLanded();
  });

  const bell = document.getElementById("bell");
  function drawBell() {
    const on = Notification.permission === "granted";
    bell.setAttribute("aria-pressed", String(on));
    bell.classList.toggle("bell--on", on);
    document.getElementById("bell-label").textContent = on ? "Alerts on" : Notification.permission === "denied" ? "Alerts blocked" : "Alert me";
    bell.disabled = Notification.permission !== "default";
    bell.title = on ? "You will get a notification when a new paper lands while this site is open."
      : Notification.permission === "denied" ? "Notifications are blocked for this site in your browser settings." : "";
  }
  if ("Notification" in window) {
    bell.hidden = false;
    drawBell();
    bell.addEventListener("click", () => Notification.requestPermission().then(drawBell));
  }

  // ---- Admin: only the site's owner signs in, at #/admin (no button for classmates).
  // Signed in, they can remove "Just landed" papers and hide or show any paper.
  const tokenStore = {
    get() { try { const t = JSON.parse(localStorage.getItem("admin-token") || "null"); return t && t.exp > Date.now() ? t : null; } catch { return null; } },
    set(t) { try { t ? localStorage.setItem("admin-token", JSON.stringify(t)) : localStorage.removeItem("admin-token"); } catch { /* private mode */ } },
  };
  let admin = tokenStore.get();
  let hidden = new Set((() => { try { return JSON.parse(localStorage.getItem("hidden-items") || "[]"); } catch { return []; } })());

  const paperKey = (p) => `p:${(p.versions[0]?.pdf || "").split("/")[1] || ""}`;
  const questionKey = (q) => `q:${q.pdf || (q.photos || [])[0] || ""}`;
  // What a visitor sees of a subject: everything for the admin, hidden papers left out for everyone else.
  const seen = (s) => admin ? s : {
    ...s,
    solved: s.solved.filter((p) => !hidden.has(paperKey(p))),
    questions: s.questions.filter((q) => !hidden.has(questionKey(q))),
  };

  function adminBar(key, title) {
    if (!admin) return "";
    const off = hidden.has(key);
    return `<div class="admin-row">
      ${off ? '<span class="tag-hidden">Hidden from classmates</span>' : ""}
      <button type="button" class="btn btn--small" data-admin="${off ? "show" : "hide"}" data-key="${esc(key)}" data-title="${esc(title)}">
        ${off ? `${icon.eye}Show on the site` : `${icon.eyeOff}Hide from the site`}</button>
    </div>`;
  }

  function redraw() {
    const y = window.scrollY;
    route();
    window.scrollTo(0, y);
  }

  function takeHidden(keys) {
    if (!Array.isArray(keys)) return;
    const next = new Set(keys);
    if (next.size === hidden.size && [...next].every((k) => hidden.has(k))) return;
    hidden = next;
    try { localStorage.setItem("hidden-items", JSON.stringify([...hidden])); } catch { /* private mode */ }
    redraw();
  }

  function drawPill() { document.getElementById("admin-pill").hidden = !admin; }
  drawPill();

  function signOut() {
    admin = null;
    tokenStore.set(null);
    drawPill();
  }

  async function adminCall(body) {
    const r = await fetch(`${UPLOAD_API}/admin`, {
      method: "POST",
      headers: { "content-type": "application/json", authorization: `Bearer ${admin?.token || ""}` },
      body: JSON.stringify(body),
    });
    const d = await r.json().catch(() => ({}));
    if (r.status === 401) { signOut(); redraw(); }
    if (!r.ok) throw new Error(d.error || `That did not work (${r.status}).`);
    return d;
  }

  function hiddenList() {
    const all = [];
    for (const s of [...data.subjects, ...data.earlier]) {
      s.solved.forEach((p) => all.push({ key: paperKey(p), title: p.title, kind: "Solved paper", subject: s.name }));
      s.questions.forEach((q) => all.push({ key: questionKey(q), title: q.title, kind: "Question paper", subject: s.name }));
    }
    return all.filter((x) => hidden.has(x.key));
  }

  function renderAdmin() {
    document.title = "Admin · Exam Paper";
    if (!admin) {
      view.innerHTML = `
        <a class="crumb" href="#/">${icon.back}All subjects</a>
        <header class="page-head"><h1 tabindex="-1">Admin</h1><p>Only for the person who runs this site.</p></header>
        <form class="admin-form" id="admin-form" novalidate>
          <input class="sr-only" type="text" name="username" autocomplete="username" value="Exam Paper admin" tabindex="-1" aria-hidden="true" readonly>
          <div class="field"><label for="ad-pass">Password</label>
            <input id="ad-pass" type="password" autocomplete="current-password" required></div>
          <p class="sheet__status" id="ad-status" role="status"></p>
          <button type="submit" class="btn btn--primary btn--wide" id="ad-send">Sign in</button>
        </form>`;
      const f = document.getElementById("admin-form");
      const st = document.getElementById("ad-status");
      const send = document.getElementById("ad-send");
      f.addEventListener("submit", async (e) => {
        e.preventDefault();
        const password = document.getElementById("ad-pass").value;
        if (!password) { st.textContent = "Type the password."; return; }
        send.disabled = true;
        st.textContent = "Signing in…";
        try {
          const r = await fetch(`${UPLOAD_API}/login`, {
            method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ password }),
          });
          const d = await r.json().catch(() => ({}));
          if (!r.ok) throw new Error(d.error || `Sign-in failed (${r.status}).`);
          admin = { token: d.token, exp: d.exp };
          tokenStore.set(admin);
          drawPill();
          route();
          toast("Signed in. Remove and Hide buttons now show on the site.", false);
        } catch (err) {
          st.textContent = err.message;
          send.disabled = false;
          document.getElementById("ad-pass").select();
        }
      });
      document.getElementById("ad-pass").focus();
      return;
    }
    const until = new Date(admin.exp).toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
    const off = hiddenList();
    view.innerHTML = `
      <a class="crumb" href="#/">${icon.back}All subjects</a>
      <header class="page-head"><h1 tabindex="-1">Admin</h1><p>Signed in on this device until ${esc(until)}.</p></header>
      <section class="section" aria-labelledby="h-can">
        <h2 id="h-can">What you can do</h2>
        <ul class="admin-help">
          <li><strong>Just landed</strong> on the home page: each paper has a Remove button. Removing deletes its photos for good.</li>
          <li>Inside a subject, every solved paper and question paper has <strong>Hide from the site</strong>. Classmates stop seeing it; you still see it, marked as hidden.</li>
        </ul>
      </section>
      <section class="section" aria-labelledby="h-off">
        <h2 id="h-off">Hidden from the site</h2>
        ${off.length ? `<div class="qlist">${off.map((x) => `<div class="qrow">
            <div><h3>${esc(x.title)}</h3><p class="paper__meta"><span>${esc(x.subject)}</span><span>${esc(x.kind)}</span></p></div>
            <div class="actions"><button type="button" class="btn btn--small" data-admin="show" data-key="${esc(x.key)}">${icon.eye}Show on the site</button></div>
          </div>`).join("")}</div>` : '<p class="empty">Nothing is hidden. Every paper is visible to classmates.</p>'}
      </section>
      <button type="button" class="btn" id="ad-out">Sign out on this device</button>`;
    document.getElementById("ad-out").addEventListener("click", () => {
      signOut();
      route();
      toast("Signed out.", false);
    });
  }

  document.addEventListener("click", async (e) => {
    const b = e.target.closest("[data-admin]");
    if (!b || !admin || b.disabled) return;
    const act = b.dataset.admin;
    if (act === "remove-upload" && !window.confirm("Remove this paper from Just landed? Its photos are deleted for good.")) return;
    b.disabled = true;
    try {
      await adminCall({ action: act, id: b.dataset.id, key: b.dataset.key, title: b.dataset.title });
      if (act === "remove-upload") {
        landed = landed.filter((u) => u.id !== b.dataset.id);
        renderLanded();
        toast("Removed from Just landed.", false);
      } else {
        if (act === "hide") hidden.add(b.dataset.key); else hidden.delete(b.dataset.key);
        try { localStorage.setItem("hidden-items", JSON.stringify([...hidden])); } catch { /* private mode */ }
        redraw();
        toast(act === "hide" ? "Hidden. Classmates no longer see it." : "Back on the site for everyone.", false);
      }
    } catch (err) {
      b.disabled = false;
      toast(err.message, false);
    }
  });


  // ---- Upload sheet: camera / gallery -> shrink on the phone -> upload page by page
  const sheet = document.getElementById("upload");
  const form = document.getElementById("upload-form");
  const shotsBox = document.getElementById("shots");
  const status = document.getElementById("up-status");
  const send = document.getElementById("up-send");
  const subjectSel = document.getElementById("up-subject");
  const noteInput = document.getElementById("up-note");
  const MAX_PAGES = 8;
  let shots = []; // { blob, url }
  let busy = false;

  function drawShots() {
    shotsBox.innerHTML = shots.length
      ? shots.map((s, i) => `<figure class="shot">
          <img src="${s.url}" alt="Page ${i + 1}">
          <figcaption>Page ${i + 1}</figcaption>
          <button type="button" class="shot__remove" data-remove="${i}" aria-label="Remove page ${i + 1}">
            <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>
          </button></figure>`).join("")
      : '<p class="shots__empty">No pages yet. Take a photo of page 1.</p>';
    document.getElementById("take-label").textContent = shots.length ? `Take page ${shots.length + 1}` : "Take photo";
    send.disabled = busy || !shots.length || !subjectSel.value;
    send.textContent = shots.length ? `Upload ${plural(shots.length, "page")}` : "Upload";
    form.querySelectorAll('input[type="file"]').forEach((i) => { i.disabled = busy || shots.length >= MAX_PAGES; });
  }

  // Phone photos are 3-8 MB; a long side of 2400 px keeps printed text sharp at about 0.5-1.5 MB.
  async function shrink(file) {
    const bmp = await createImageBitmap(file, { imageOrientation: "from-image" });
    const k = Math.min(1, 2400 / Math.max(bmp.width, bmp.height));
    const c = document.createElement("canvas");
    c.width = Math.round(bmp.width * k);
    c.height = Math.round(bmp.height * k);
    c.getContext("2d").drawImage(bmp, 0, 0, c.width, c.height);
    if (bmp.close) bmp.close();
    for (const q of [0.86, 0.78, 0.68]) {
      const blob = await new Promise((res) => c.toBlob(res, "image/jpeg", q));
      if (blob && blob.size < 3_800_000) return blob;
    }
    throw new Error("too large");
  }

  async function addFiles(files) {
    status.textContent = "";
    for (const f of files) {
      if (shots.length >= MAX_PAGES) { status.textContent = `Up to ${MAX_PAGES} pages per paper.`; break; }
      if (!f.type.startsWith("image/")) continue;
      try {
        const blob = await shrink(f);
        shots.push({ blob, url: URL.createObjectURL(blob) });
      } catch { status.textContent = "That photo could not be read. Try taking it again."; }
    }
    drawShots();
  }

  form.querySelectorAll('input[type="file"]').forEach((input) => input.addEventListener("change", () => {
    addFiles([...input.files]);
    input.value = "";
  }));
  shotsBox.addEventListener("click", (e) => {
    const b = e.target.closest("[data-remove]");
    if (!b || busy) return;
    const [gone] = shots.splice(Number(b.dataset.remove), 1);
    URL.revokeObjectURL(gone.url);
    drawShots();
  });
  subjectSel.addEventListener("change", drawShots);

  const newId = () => {
    const ist = new Date(Date.now() + 5.5 * 3600e3).toISOString(); // India time
    const rand = Math.random().toString(36).slice(2, 6).padEnd(4, "0");
    return `${ist.slice(0, 10).replace(/-/g, "")}-${ist.slice(11, 19).replace(/:/g, "")}-${rand}`;
  };

  async function post(url, body, type) {
    const r = await fetch(url, { method: "POST", headers: { "content-type": type }, body });
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(d.error || `Upload failed (${r.status}).`);
    return d;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (busy || !shots.length || !subjectSel.value) return;
    busy = true;
    drawShots();
    const id = newId();
    try {
      let first = null;
      for (let i = 0; i < shots.length; i++) {
        status.textContent = `Uploading page ${i + 1} of ${shots.length}…`;
        const r = await post(`${UPLOAD_API}/upload?id=${id}&n=${i + 1}`, shots[i].blob, "image/jpeg");
        if (i === 0) first = r.url;
      }
      ownUploads.add(id);
      status.textContent = "Saving…";
      await post(`${UPLOAD_API}/upload?id=${id}&part=meta`,
        JSON.stringify({ subject: subjectSel.value, pages: shots.length, note: noteInput.value.trim(), first }),
        "application/json");
      shots.forEach((s) => URL.revokeObjectURL(s.url));
      shots = [];
      noteInput.value = "";
      status.textContent = "Uploaded. It is under “Just landed” on the home page.";
      loadLanded();
    } catch (err) {
      status.textContent = `${err.message} Your photos are still here: check the connection and tap Upload again.`;
    } finally {
      busy = false;
      drawShots();
    }
  });

  document.getElementById("fab").addEventListener("click", () => {
    const current = decodeURIComponent(location.hash.replace(/^#\/?/, ""));
    subjectSel.innerHTML = '<option value="">Choose a subject</option>' +
      (data?.subjects || []).map((s) => `<option value="${esc(s.id)}">${esc(s.name)}</option>`).join("") +
      '<option value="other">Other</option>';
    if ((data?.subjects || []).some((s) => s.id === current)) subjectSel.value = current;
    if (!shots.length) status.textContent = "";
    drawShots();
    sheet.showModal();
  });
  sheet.addEventListener("click", (e) => {
    if ((e.target === sheet || e.target.closest("[data-close-upload]")) && !busy) sheet.close();
  });
  sheet.addEventListener("cancel", (e) => { if (busy) e.preventDefault(); });

  window.addEventListener("hashchange", route);
  fetch("site/catalog.json", { cache: "no-cache" })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((d) => {
      data = d;
      document.getElementById("built").textContent = `Last updated ${d.built}`;
      route();
      if (location.hash.replace(/^#\/?/, "")) loadLanded();
      if (admin) adminCall({ action: "check" }).catch(() => {});
    })
    .catch(() => {
      view.innerHTML = '<p class="notice">The list of papers could not be loaded. Check your connection and refresh. The files are also on <a href="https://github.com/abuzar310/exam-paper/tree/main/papers">GitHub</a>.</p>';
    });
})();
