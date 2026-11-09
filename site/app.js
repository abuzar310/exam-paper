// Exam Paper: renders site/catalog.json (made by site/build.py) into the shelf and subject pages.
(() => {
  const view = document.getElementById("view");
  const viewer = document.getElementById("viewer");
  const viewerImg = document.getElementById("viewer-img");
  const viewerCaption = document.getElementById("viewer-caption");
  const viewerOpen = document.getElementById("viewer-open");
  const viewerDl = document.getElementById("viewer-dl");
  const UPLOAD_API = "https://exam-paper-upload.vercel.app/api";
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
    const solved = data.subjects.reduce((n, s) => n + s.solved.length, 0);
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
      <ul class="shelf" id="shelf">${data.subjects.map(subjectTile).join("")}</ul>
      <p class="no-match" id="no-match" hidden>No subject matches that. Try a paper code like 54321.</p>
      ${data.earlier.length ? `<section class="earlier"><h2>Earlier semesters</h2><ul class="shelf">${data.earlier.map(subjectTile).join("")}</ul></section>` : ""}`;
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
    return `<article class="paper">
      <div>
        <h3>${esc(p.title)}</h3>
        <p class="paper__meta"><span>Updated ${esc(p.updated)}</span><span>${plural(p.versions.length, "version")}</span></p>
      </div>
      ${p.answered ? `<p class="paper__note">${esc(p.answered)}</p>` : ""}
      ${p.versions.map((v) => versionBlock(v, label)).join("")}
    </article>`;
  }

  function questionRow(q, subject) {
    if (q.photos) {
      const items = q.photos.map((f) => ({ full: f, thumb: f }));
      return `<div class="qrow"><div><h3>${esc(q.title)}</h3><p class="paper__meta"><span>${plural(q.photos.length, "photo")}</span></p></div>${thumbs(items, `${subject.name}, ${q.title}`)}</div>`;
    }
    return `<div class="qrow">
      <div><h3>${esc(q.title)}</h3><p class="paper__meta"><span>${plural(q.pdf_pages, "page")}</span><span>${esc(q.pdf_size)}</span></p></div>
      <div class="actions">
        <a class="btn" href="${esc(q.pdf)}" target="_blank" rel="noopener">${icon.open}Open</a>
        <a class="btn" href="${esc(q.pdf)}" download="${esc(fileName(q.pdf))}" aria-label="Download ${esc(q.title)}">${icon.download}Download</a>
      </div>
    </div>`;
  }

  function renderSubject(s) {
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
      s ? renderSubject(s) : renderHome();
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
          <p class="paper__meta">${meta.map((m) => `<span>${esc(m)}</span>`).join("")}</p></div>
          ${thumbs(items, `${subjectName(u.subject)}, uploaded ${when(u.uploaded)}`, true)}
        </div>`;
      }).join("")}</div>`;
  }

  function loadLanded() {
    fetch(`${UPLOAD_API}/inbox`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : { items: [] }))
      .then((d) => { landed = d.items || []; renderLanded(); })
      .catch(() => {});
  }

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
      for (let i = 0; i < shots.length; i++) {
        status.textContent = `Uploading page ${i + 1} of ${shots.length}…`;
        await post(`${UPLOAD_API}/upload?id=${id}&n=${i + 1}`, shots[i].blob, "image/jpeg");
      }
      status.textContent = "Saving…";
      await post(`${UPLOAD_API}/upload?id=${id}&part=meta`,
        JSON.stringify({ subject: subjectSel.value, pages: shots.length, note: noteInput.value.trim() }),
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
    })
    .catch(() => {
      view.innerHTML = '<p class="notice">The list of papers could not be loaded. Check your connection and refresh. The files are also on <a href="https://github.com/abuzar310/exam-paper/tree/main/papers">GitHub</a>.</p>';
    });
})();
