// Exam Paper: renders site/catalog.json (made by site/build.py) into the shelf and subject pages.
(() => {
  const view = document.getElementById("view");
  const viewer = document.getElementById("viewer");
  const viewerImg = document.getElementById("viewer-img");
  const viewerCaption = document.getElementById("viewer-caption");
  const viewerOpen = document.getElementById("viewer-open");
  let data = null;
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
      <div class="find">
        <label for="q">Find a subject</label>
        ${icon.search}
        <input id="q" type="search" placeholder="Subject or paper code" autocomplete="off" enterkeyhint="search">
      </div>
      <ul class="shelf" id="shelf">${data.subjects.map(subjectTile).join("")}</ul>
      <p class="no-match" id="no-match" hidden>No subject matches that. Try a paper code like 54321.</p>
      ${data.earlier.length ? `<section class="earlier"><h2>Earlier semesters</h2><ul class="shelf">${data.earlier.map(subjectTile).join("")}</ul></section>` : ""}`;
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

  function thumbs(items, label) {
    if (!items.length) return "";
    const key = encodeURIComponent(JSON.stringify(items.map((x) => x.full)));
    return `<div class="pages" role="list">${items.map((x, i) => `
      <div class="pages__item" role="listitem">
        <button type="button" class="thumb" data-gallery="${key}" data-index="${i}" data-label="${esc(label)}" aria-label="${esc(label)}, page ${i + 1}: view image">
          <img src="${esc(x.thumb)}" alt="" loading="lazy" decoding="async" width="112" height="158">
        </button>
        <span class="pages__label">Page ${i + 1}</span>
      </div>`).join("")}</div>`;
  }

  function solvedCard(p, subject) {
    const label = `${subject.name}, ${p.title}`;
    const meta = [plural(p.pdf_pages, "page"), p.pdf_size, `Updated ${p.updated}`];
    return `<article class="paper">
      <div>
        <h3>${esc(p.title)}</h3>
        <p class="paper__meta">${meta.map((m) => `<span>${esc(m)}</span>`).join("")}</p>
      </div>
      ${p.answered ? `<p class="paper__note">${esc(p.answered)}</p>` : ""}
      <div class="actions">
        <a class="btn btn--primary" href="${esc(p.pdf)}" target="_blank" rel="noopener">${icon.open}Open PDF</a>
        <a class="btn" href="${esc(p.pdf)}" download="${esc(fileName(p.pdf))}">${icon.download}Download PDF</a>
        ${p.single ? `<a class="btn" href="${esc(p.single)}" target="_blank" rel="noopener">${icon.open}Reading copy</a>` : ""}
      </div>
      ${thumbs(p.images, label)}
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
