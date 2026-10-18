/* Navin Jairam M — portfolio interactions. Vanilla JS, no dependencies. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var ROOT = doc.getAttribute("data-root") || "";
  var EMAIL = "navin.jairam@gmail.com";
  var LINKS = {
    github: "https://github.com/Lucifer-Newstar",
    linkedin: "https://www.linkedin.com/in/navin-jairam",
    resume: ROOT + "assets/Navin_Jairam_M_Resume.pdf"
  };
  /* Portfolio Platform repo: set PORTFOLIO_PLATFORM_REPO in build.py (empty = private, no link). */
  var PP_REPO = doc.getAttribute("data-pp-repo") ? LINKS.github + "/" + doc.getAttribute("data-pp-repo") : null;
  var PROJECTS = [
    { id: "aegisdeploy", name: "AegisDeploy", page: "projects/aegisdeploy.html", repo: "https://github.com/Lucifer-Newstar/AegisDeploy", blurb: "SRE platform, phase 2: demo shop + registry, deployments API, console; K8s, 6-job CI, observability" },
    { id: "portfolio", name: "Portfolio Platform", page: "projects/portfolio-platform.html", repo: PP_REPO, blurb: "Serverless AWS: S3, CloudFront, API Gateway, Lambda, DynamoDB, Cognito, SES" },
    { id: "digicrave", name: "DigiCrave OS", page: "projects/digicrave-os.html", repo: "https://github.com/Lucifer-Newstar/DigiCraveOS", live: "https://digi-crave-os.vercel.app", blurb: "MERN restaurant POS & operations system, live" },
    { id: "java", name: "Distributed Java Web App", page: "projects/distributed-java-webapp.html", repo: "https://github.com/Lucifer-Newstar/distributed-java-webapp", blurb: "Multi-VM Vagrant stack: Nginx, Tomcat, MySQL, Memcached, RabbitMQ" },
    { id: "kaizen", name: "Kaizen – Productivity OS", page: null, repo: "https://github.com/Lucifer-Newstar/Productivity-App", blurb: "Productivity OS with CI/CD releases and basic MLOps" }
  ];
  var PAGES = { home: "index.html", about: "about.html", experience: "about.html#experience", projects: "projects.html", skills: "skills.html", contact: "contact.html" };

  /* ---------- toast + clipboard ---------- */
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); toastEl.setAttribute("aria-live", "polite"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 1900);
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }
  function legacyCopy(text) {
    var ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select(); var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta); return ok;
  }
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      copyText(b.getAttribute("data-copy")).then(function (ok) {
        toast(ok ? "✓ copied " + b.getAttribute("data-copy") : "Couldn't copy, the email is " + EMAIL);
        var label = b.querySelector(".lbl"); if (label && ok) { var o = label.textContent; label.textContent = "Copied!"; setTimeout(function () { label.textContent = o; }, 1600); }
      });
    });
  });

  /* ---------- mobile nav ---------- */
  var menuBtn = document.querySelector(".menu-btn"), navList = document.getElementById("nav-links");
  if (menuBtn && navList) {
    menuBtn.addEventListener("click", function () {
      var open = menuBtn.getAttribute("aria-expanded") === "true";
      menuBtn.setAttribute("aria-expanded", String(!open)); navList.classList.toggle("open", !open);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && navList.classList.contains("open")) { navList.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus(); } });
  }

  /* ---------- theme (light / dark) ---------- */
  var THEME_KEY = "theme";
  function storedTheme() { try { var t = localStorage.getItem(THEME_KEY); return t === "light" || t === "dark" ? t : null; } catch (e) { return null; } }
  function osTheme() { return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark"; }
  function currentTheme() { return doc.getAttribute("data-theme") === "light" ? "light" : "dark"; }
  function syncThemeUI() {
    var t = currentTheme(), next = t === "light" ? "dark" : "light";
    document.querySelectorAll("[data-theme-toggle]").forEach(function (b) { b.setAttribute("aria-label", "Switch to " + next + " theme"); b.setAttribute("title", "Switch to " + next + " theme"); });
    var m = document.querySelector('meta[name="theme-color"]'); if (m) m.setAttribute("content", t === "light" ? "#f3f5f8" : "#06080c");
  }
  function applyTheme(t, persist) {
    if (t !== "light" && t !== "dark") return;
    var change = function () {
      doc.setAttribute("data-theme", t);
      if (persist) { try { localStorage.setItem(THEME_KEY, t); } catch (e) {} }
      syncThemeUI();
      window.dispatchEvent(new CustomEvent("themechange", { detail: t }));
    };
    if (reduce) { change(); return; }
    doc.classList.add("theme-anim"); change();
    setTimeout(function () { doc.classList.remove("theme-anim"); }, 420);
  }
  if (!doc.getAttribute("data-theme")) doc.setAttribute("data-theme", storedTheme() || osTheme());
  syncThemeUI();
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () { applyTheme(currentTheme() === "light" ? "dark" : "light", true); });
  });
  if (window.matchMedia) {
    var mqTheme = window.matchMedia("(prefers-color-scheme: light)");
    var onOs = function () { if (!storedTheme()) applyTheme(osTheme(), false); };
    if (mqTheme.addEventListener) mqTheme.addEventListener("change", onOs); else if (mqTheme.addListener) mqTheme.addListener(onOs);
  }
  window.addEventListener("storage", function (e) { if (e.key === THEME_KEY && (e.newValue === "light" || e.newValue === "dark")) applyTheme(e.newValue, false); });

  /* ---------- background: DevOps motifs ----------
     Two fixed canvases behind the content. #net holds the still layer (dot grid, circuit traces, pipeline rails),
     drawn once per resize/theme. #bgfx holds what moves: helm wheels, pod hexagons, containers and YAML/terminal
     snippets drifting slowly, plus packets running along the traces. ~30 fps, paused when the tab is hidden,
     drawn once and left still under prefers-reduced-motion. */
  (function bg() {
    var sc = document.getElementById("net"); if (!sc || !sc.getContext) return;
    var dc = document.createElement("canvas"); dc.id = "bgfx"; dc.setAttribute("aria-hidden", "true");
    sc.parentNode.insertBefore(dc, sc.nextSibling);
    var sx = sc.getContext("2d"), dx = dc.getContext("2d");
    var W = 0, H = 0, dpr = 1, items = [], rails = [], traces = [], packets = [], col = {};
    var running = !document.hidden, raf = 0, last = 0, tm = 0;
    var mouse = { x: 0, y: 0, cx: 0, cy: 0 };
    var SNIPS = [
      ["apiVersion: apps/v1", "kind: Deployment", "spec:", "  replicas: 3"],
      ["$ kubectl rollout status", "deployment/api successfully rolled out"],
      ["on:", "  push:", "    branches: [main]"],
      ["$ docker build -t api:ci .", "=> exporting to image"],
      ["FROM python:3.12-slim", "EXPOSE 8080"],
      ["- uses: actions/checkout@v4"],
      ["$ kustomize build infra/k8s/base"],
      ["status:", "  phase: Running", "  ready: 1/1"],
      ["scrape_interval: 15s", "rule_files: [alerts.yml]"],
      ["$ ansible-playbook site.yml", "ok=12  changed=3  failed=0"],
      ["$ kubeconform -strict -summary"],
      ["livenessProbe:", "  httpGet: { path: /healthz }"]
    ];
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function pick(a) { return a[(Math.random() * a.length) | 0]; }
    function readColors() {
      var light = currentTheme() === "light", cs = getComputedStyle(doc);
      col.light = light;
      col.g = cs.getPropertyValue("--g-rgb").trim() || "62,224,143";
      col.c = cs.getPropertyValue("--c-rgb").trim() || "56,214,245";
      col.v = light ? "109,40,217" : "167,139,250";
      col.ink = light ? "30,41,59" : "148,163,184";
      col.k = light ? 0.95 : 1;   // light theme: darker hues, slightly lower alpha
    }
    function rgba(rgb, a) { return "rgba(" + rgb + "," + (a * col.k).toFixed(3) + ")"; }

    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 1.75);
      W = window.innerWidth; H = window.innerHeight;
      [sc, dc].forEach(function (c) { c.width = Math.round(W * dpr); c.height = Math.round(H * dpr); });
      sx.setTransform(dpr, 0, 0, dpr, 0, 0); dx.setTransform(dpr, 0, 0, dpr, 0, 0);
      build();
    }
    function far(x, y, list, d) { for (var i = 0; i < list.length; i++) { var a = list[i]; if (Math.abs(a.x - x) < d && Math.abs(a.y - y) < d) return false; } return true; }
    function build() {
      var mobile = W < 700;
      // rails: CI pipelines crossing the screen, with stage boxes
      rails = [];
      var ys = mobile ? [76, H * 0.95] : [H * 0.16, H * 0.62, H * 0.9];
      ys.forEach(function (y, i) {
        var gap = mobile ? 120 : 170, off = rnd(0, gap), st = [];
        for (var x = off; x < W + gap; x += gap) st.push(x);
        rails.push({ y: Math.round(y) + 0.5, stages: st, dir: i % 2 ? -1 : 1 });
      });
      // circuit traces: 45-degree routed lines with pads
      traces = [];
      var G = 28, n = mobile ? 7 : 14;
      for (var t = 0; t < n; t++) {
        var x0 = Math.round(rnd(0, W) / G) * G, y0 = Math.round(rnd(0, H) / G) * G, pts = [[x0, y0]];
        var dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]], d = pick(dirs), segs = 3 + ((Math.random() * 3) | 0);
        for (var s = 0; s < segs; s++) {
          var len = G * (2 + ((Math.random() * 4) | 0)), p = pts[pts.length - 1];
          pts.push([p[0] + d[0] * len, p[1] + d[1] * len]);
          var turn = Math.random() < 0.5 ? 1 : -1; // 45-degree jog then straight
          var nd = d[0] ? [d[0], turn] : [turn, d[1]];
          p = pts[pts.length - 1]; var j = G * (1 + ((Math.random() * 2) | 0));
          pts.push([p[0] + nd[0] * j, p[1] + nd[1] * j]);
        }
        var L = 0; for (var k = 1; k < pts.length; k++) L += Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]);
        traces.push({ pts: pts, len: L });
      }
      // packets
      packets = [];
      rails.forEach(function (r) { var c = mobile ? 1 : 2; for (var i = 0; i < c; i++) packets.push({ rail: r, p: rnd(0, W), v: rnd(0.55, 0.85) }); });
      traces.forEach(function (tr, i) { if (i % 2 === 0) packets.push({ tr: tr, p: rnd(0, tr.len), v: rnd(0.35, 0.6) }); });
      // drifting motifs
      items = [];
      var want = Math.round(Math.max(7, Math.min(mobile ? 9 : 20, (W * H) / 60000)));
      var kinds = mobile ? ["helm", "hex", "box", "hex", "box", "helm"] : ["helm", "hex", "box", "text", "hex", "text", "box", "helm", "text"];
      var tries = 0;
      while (items.length < want && tries++ < 400) {
        var x = rnd(0, W), y = rnd(0, H);
        if (!far(x, y, items, mobile ? 120 : 170)) continue;
        var kind = kinds[items.length % kinds.length], z = rnd(0.55, 1);
        items.push({ kind: kind, x: x, y: y, z: z, vx: rnd(-1, 1) * 0.12 * z, vy: rnd(-0.12, -0.04) * z, rot: rnd(0, 6.28), vr: (kind === "helm" ? rnd(0.0015, 0.004) : rnd(-0.001, 0.001)) * (Math.random() < 0.5 ? -1 : 1),
          r: kind === "helm" ? rnd(22, 40) * z : kind === "hex" ? rnd(14, 26) * z : kind === "box" ? rnd(14, 22) * z : 0,
          snip: kind === "text" ? pick(SNIPS) : null, ph: rnd(0, 6.28), hue: Math.random() < 0.5 ? "c" : (kind === "hex" ? "v" : "g") });
      }
      drawStatic();
    }

    function drawStatic() {
      sx.clearRect(0, 0, W, H);
      // dot grid, fading toward the centre so it sits behind the content
      var G = 28, cxm = W / 2, cym = H * 0.45, maxd = Math.hypot(W, H) / 2;
      sx.fillStyle = rgba(col.ink, col.light ? 0.16 : 0.13);
      for (var x = G / 2; x < W; x += G) for (var y = G / 2; y < H; y += G) {
        var f = Math.hypot(x - cxm, y - cym) / maxd; if (f < 0.25) continue;
        sx.globalAlpha = Math.min(1, (f - 0.25) * 1.6); sx.fillRect(x - 0.6, y - 0.6, 1.2, 1.2);
      }
      sx.globalAlpha = 1;
      // circuit traces
      sx.lineWidth = 1; sx.lineJoin = "round";
      traces.forEach(function (tr) {
        sx.strokeStyle = rgba(col.c, col.light ? 0.16 : 0.13);
        sx.beginPath(); sx.moveTo(tr.pts[0][0] + 0.5, tr.pts[0][1] + 0.5);
        for (var i = 1; i < tr.pts.length; i++) sx.lineTo(tr.pts[i][0] + 0.5, tr.pts[i][1] + 0.5);
        sx.stroke();
        [tr.pts[0], tr.pts[tr.pts.length - 1]].forEach(function (p) { sx.beginPath(); sx.arc(p[0] + 0.5, p[1] + 0.5, 2.6, 0, 6.283); sx.stroke(); });
      });
      // CI rails: dashed flow line, stage boxes, arrowheads
      rails.forEach(function (r) {
        sx.strokeStyle = rgba(col.g, col.light ? 0.17 : 0.13); sx.setLineDash([5, 7]);
        sx.beginPath(); sx.moveTo(0, r.y); sx.lineTo(W, r.y); sx.stroke(); sx.setLineDash([]);
        r.stages.forEach(function (x, i) {
          sx.strokeStyle = rgba(col.g, col.light ? 0.22 : 0.17); sx.fillStyle = col.light ? "rgba(243,245,248,.9)" : "rgba(6,8,12,.9)";
          roundRect(sx, x - 8, r.y - 8, 16, 16, 4); sx.fill(); sx.stroke();
          var ax = x + (r.dir > 0 ? 30 : -30);
          sx.beginPath(); sx.moveTo(ax - 4 * r.dir, r.y - 4); sx.lineTo(ax, r.y); sx.lineTo(ax - 4 * r.dir, r.y + 4); sx.stroke();
        });
      });
    }
    function roundRect(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }

    function helm(c, r) {
      c.beginPath(); c.arc(0, 0, r, 0, 6.283); c.stroke();
      c.beginPath(); c.arc(0, 0, r * 0.3, 0, 6.283); c.stroke();
      for (var i = 0; i < 7; i++) {
        var a = i / 7 * 6.283, ca = Math.cos(a), sa = Math.sin(a);
        c.beginPath(); c.moveTo(ca * r * 0.3, sa * r * 0.3); c.lineTo(ca * r * 1.28, sa * r * 1.28); c.stroke();
        c.beginPath(); c.arc(ca * r * 1.36, sa * r * 1.36, r * 0.09, 0, 6.283); c.stroke();
      }
    }
    function hex(c, r) {
      c.beginPath(); for (var i = 0; i < 6; i++) { var a = i / 6 * 6.283 - Math.PI / 2; c[i ? "lineTo" : "moveTo"](Math.cos(a) * r, Math.sin(a) * r); } c.closePath(); c.stroke();
      c.setLineDash([2, 4]); c.beginPath(); for (var j = 0; j < 6; j++) { var b = j / 6 * 6.283 - Math.PI / 2; c[j ? "lineTo" : "moveTo"](Math.cos(b) * r * 0.62, Math.sin(b) * r * 0.62); } c.closePath(); c.stroke(); c.setLineDash([]);
    }
    function box(c, s) { // isometric container with ribs
      var h = s * 0.58;
      c.beginPath(); c.moveTo(0, -s); c.lineTo(s, -s + h); c.lineTo(0, -s + 2 * h); c.lineTo(-s, -s + h); c.closePath(); c.stroke();
      c.beginPath(); c.moveTo(-s, -s + h); c.lineTo(-s, h); c.lineTo(0, 2 * h); c.lineTo(s, h); c.lineTo(s, -s + h); c.moveTo(0, -s + 2 * h); c.lineTo(0, 2 * h); c.stroke();
      for (var i = 1; i < 4; i++) { var t = i / 4; c.beginPath(); c.moveTo(-s * t, -s + h + h * t); c.lineTo(-s * t, h + h * t); c.moveTo(s * t, -s + h + h * t); c.lineTo(s * t, h + h * t); c.stroke(); }
    }
    function along(tr, p) {
      var pts = tr.pts, acc = 0;
      for (var i = 1; i < pts.length; i++) {
        var a = pts[i - 1], b = pts[i], l = Math.hypot(b[0] - a[0], b[1] - a[1]);
        if (acc + l >= p) { var t = (p - acc) / l; return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]; }
        acc += l;
      }
      return pts[pts.length - 1];
    }

    function frame(now) {
      raf = 0;
      if (!reduce && running) raf = requestAnimationFrame(frame);
      if (!reduce && now - last < 32) return; // ~30 fps is plenty for slow drift
      var dt = last ? Math.min(3, (now - last) / 33) : 1; last = now; tm += dt;
      mouse.cx += (mouse.x - mouse.cx) * 0.05; mouse.cy += (mouse.y - mouse.cy) * 0.05;
      dx.clearRect(0, 0, W, H);
      dx.lineWidth = 1.1; dx.lineCap = "round"; dx.lineJoin = "round";
      var A = col.light ? 0.2 : 0.17;
      for (var i = 0; i < items.length; i++) {
        var it = items[i];
        if (!reduce) {
          it.x += it.vx * dt; it.y += it.vy * dt; it.rot += it.vr * dt;
          var m = 90;
          if (it.x < -m) it.x = W + m; else if (it.x > W + m) it.x = -m;
          if (it.y < -m) it.y = H + m; else if (it.y > H + m) it.y = -m;
        }
        var px = it.x - mouse.cx * 0.02 * it.z, py = it.y - mouse.cy * 0.02 * it.z;
        // fade toward the centre column, where the content and its text sit
        var cxf = Math.min(1, Math.abs(px + (it.kind === "text" ? 110 : 0) - W / 2) / (W * 0.42));
        var fade = it.kind === "text" ? 0.12 + 0.88 * cxf * cxf : 0.45 + 0.55 * cxf;
        var rgb = it.hue === "c" ? col.c : it.hue === "v" ? col.v : col.g;
        dx.save(); dx.translate(px, py);
        if (it.kind === "text") {
          dx.font = "500 " + Math.round(10.5 + it.z * 2) + "px 'JetBrains Mono', ui-monospace, monospace";
          for (var l = 0; l < it.snip.length; l++) {
            var s = it.snip[l];
            dx.fillStyle = rgba(s.charAt(0) === "$" ? col.g : col.ink, (s.charAt(0) === "$" ? 0.24 : 0.2) * it.z * fade);
            dx.fillText(s, 0, l * (15 + it.z * 2));
          }
        } else {
          dx.rotate(it.rot);
          dx.strokeStyle = rgba(rgb, A * (0.6 + it.z * 0.5) * fade);
          if (it.kind === "helm") helm(dx, it.r); else if (it.kind === "hex") hex(dx, it.r); else box(dx, it.r);
          if (it.kind === "hex") { // pod status light
            var pulse = reduce ? 0.6 : 0.5 + 0.5 * Math.sin(tm / 20 + it.ph);
            dx.fillStyle = rgba(col.g, (0.25 + pulse * 0.35) * it.z * fade); dx.beginPath(); dx.arc(0, 0, 2.6, 0, 6.283); dx.fill();
          }
        }
        dx.restore();
      }
      // packets on rails and traces
      for (var k = 0; k < packets.length; k++) {
        var pk = packets[k], x, y, rgbp;
        if (!reduce) pk.p += pk.v * dt;
        if (pk.rail) {
          if (pk.p > W + 20) pk.p = -20;
          x = pk.rail.dir > 0 ? pk.p : W - pk.p; y = pk.rail.y; rgbp = col.g;
          // light up the stage the packet is passing
          for (var q = 0; q < pk.rail.stages.length; q++) {
            var sx0 = pk.rail.stages[q], dd = Math.abs(sx0 - x);
            if (dd < 26) { dx.strokeStyle = rgba(col.g, 0.5 * (1 - dd / 26)); roundRect(dx, sx0 - 8, y - 8, 16, 16, 4); dx.stroke(); }
          }
        } else {
          if (pk.p > pk.tr.len) pk.p = 0;
          var pt = along(pk.tr, pk.p); x = pt[0] + 0.5; y = pt[1] + 0.5; rgbp = col.c;
        }
        var g = dx.createRadialGradient(x, y, 0, x, y, 9);
        g.addColorStop(0, rgba(rgbp, col.light ? 0.5 : 0.55)); g.addColorStop(1, rgba(rgbp, 0));
        dx.fillStyle = g; dx.beginPath(); dx.arc(x, y, 9, 0, 6.283); dx.fill();
        dx.fillStyle = rgba(rgbp, 0.8); dx.beginPath(); dx.arc(x, y, 1.6, 0, 6.283); dx.fill();
      }
    }
    function kick() { if (!raf && running && !reduce) { last = 0; raf = requestAnimationFrame(frame); } }
    readColors(); size();
    var rt = 0;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { size(); if (reduce) frame(0); }, 120); }, { passive: true });
    if (finePointer && !reduce) window.addEventListener("pointermove", function (e) { mouse.x = e.clientX - W / 2; mouse.y = e.clientY - H / 2; }, { passive: true });
    window.addEventListener("themechange", function () { readColors(); drawStatic(); if (reduce || !running) frame(performance.now()); });
    document.addEventListener("visibilitychange", function () {
      running = !document.hidden;
      if (!running) { cancelAnimationFrame(raf); raf = 0; } else kick();
    });
    if (reduce) frame(0); else kick();
    window.__bg = { running: function () { return running && !!raf; }, items: function () { return items.length; } };
  })();

  /* ---------- scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".reveal, .tl-item");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0 });
    revealEls.forEach(function (el, i) { el.style.transitionDelay = (el.getAttribute("data-delay") || 0) + "ms"; io.observe(el); });
    var revealRest = function () {
      var de = document.documentElement;
      if (window.innerHeight + window.scrollY >= de.scrollHeight - 80) revealEls.forEach(function (el) { el.classList.add("in"); });
    };
    window.addEventListener("scroll", revealRest, { passive: true }); window.addEventListener("resize", revealRest);
  } else { revealEls.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- timeline progress ---------- */
  var tl = document.querySelector(".timeline");
  if (tl) {
    var prog = tl.querySelector(".prog");
    var upd = function () {
      var r = tl.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * 0.75 - r.top) / r.height));
      if (prog) prog.style.setProperty("--p", (reduce ? 100 : p * 100).toFixed(1) + "%");
    };
    window.addEventListener("scroll", upd, { passive: true }); window.addEventListener("resize", upd); upd();
  }

  /* ---------- tilt cards ---------- */
  if (finePointer && !reduce) {
    document.querySelectorAll(".tilt").forEach(function (el) {
      var g = document.createElement("span"); g.className = "glare"; g.setAttribute("aria-hidden", "true"); el.appendChild(g);
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        el.classList.add("is-tilting");
        el.style.transform = "perspective(900px) rotateX(" + ((0.5 - py) * 7).toFixed(2) + "deg) rotateY(" + ((px - 0.5) * 9).toFixed(2) + "deg) translateY(-3px)";
        el.style.setProperty("--gx", (px * 100).toFixed(1) + "%"); el.style.setProperty("--gy", (py * 100).toFixed(1) + "%");
      });
      el.addEventListener("pointerleave", function () { el.classList.remove("is-tilting"); el.style.transform = ""; });
    });
  }

  /* ---------- hero terminal ---------- */
  (function hero() {
    var body = document.getElementById("hero-term"); if (!body) return;
    var PS = '<span class="ps">navin@prod:~$</span> ';
    var script = [
      { cmd: "whoami", out: '<span class="hi">navin-jairam-m</span>  <span class="o"># B.Tech IT · Chennai</span>' },
      { cmd: "kubectl get pods -n portfolio", out:
        '<span class="o">NAME                 READY   STATUS</span>\n' +
        'aegisdeploy          1/1     <span class="ok">Running</span>\n' +
        'portfolio-platform   1/1     <span class="ok">Running</span>\n' +
        'digicrave-os         1/1     <span class="ok">Running</span>' },
      { cmd: "deploy navin --env=prod", out:
        '<span class="o">» building image</span> <span class="vi">navin:2027</span><span class="o"> … done</span>\n' +
        '<span class="o">» rolling out to</span> <span class="am">production</span><span class="o"> … done</span>\n' +
        '<span class="ok">✓ deployed</span>\n\n' +
        '  <span class="big">Navin Jairam M</span>\n' +
        '  <span class="hi">DevOps &amp; Cloud Engineer</span>\n' +
        '  <span class="o">AWS · Kubernetes · Docker · GitHub Actions</span>\n' +
        '  <span class="o">Prometheus · Grafana · Ansible · Linux</span>' }
    ];
    var html = "", done = false, timer = 0;
    var skipBtn = document.getElementById("hero-skip"), replayBtn = document.getElementById("hero-replay");
    function render(extra) { body.innerHTML = html + (extra || "") + (done ? PS + '<span class="caret"></span>' : ""); }
    function finish() {
      clearTimeout(timer); html = ""; script.forEach(function (s) { html += PS + '<span class="cmd">' + s.cmd + "</span>\n" + s.out + "\n"; });
      done = true; render(); if (skipBtn) skipBtn.hidden = true; if (replayBtn) replayBtn.hidden = false;
    }
    function play() {
      html = ""; done = false; var si = 0;
      if (skipBtn) skipBtn.hidden = false; if (replayBtn) replayBtn.hidden = true;
      function nextCmd() {
        if (si >= script.length) { done = true; render(); if (skipBtn) skipBtn.hidden = true; if (replayBtn) replayBtn.hidden = false; return; }
        var s = script[si], ci = 0;
        (function type() {
          if (ci <= s.cmd.length) {
            render(PS + '<span class="cmd">' + s.cmd.slice(0, ci) + '</span><span class="caret"></span>');
            ci++; timer = setTimeout(type, 38 + Math.random() * 55);
          } else {
            html += PS + '<span class="cmd">' + s.cmd + "</span>\n";
            render('<span class="caret"></span>');
            timer = setTimeout(function () { html += s.out + "\n"; render(); si++; timer = setTimeout(nextCmd, 650); }, 380);
          }
        })();
      }
      timer = setTimeout(nextCmd, 450);
    }
    if (skipBtn) skipBtn.addEventListener("click", finish);
    if (replayBtn) replayBtn.addEventListener("click", function () { clearTimeout(timer); play(); });
    if (reduce) finish(); else play();
  })();

  /* ---------- project filters ---------- */
  var filterBar = document.querySelector(".filters");
  if (filterBar) {
    var cards = document.querySelectorAll("[data-tags]");
    filterBar.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      filterBar.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      var f = b.getAttribute("data-filter"), shown = 0;
      cards.forEach(function (c) { var on = f === "all" || c.getAttribute("data-tags").split(" ").indexOf(f) > -1; c.hidden = !on; if (on) shown++; });
      var st = document.getElementById("filter-status"); if (st) st.textContent = shown + " project" + (shown === 1 ? "" : "s") + " shown";
    });
  }

  /* ---------- CI pipeline ---------- */
  (function pipeline() {
    var wrap = document.getElementById("pipe"); if (!wrap) return;
    var stages = wrap.querySelectorAll(".stage"), log = wrap.querySelector(".pipe-log"), btn = wrap.querySelector("[data-run]"), stateTxt = wrap.querySelector(".run-txt");
    var LOGS = [
      ["config", "$ python3 scripts/validate_yaml.py\n$ docker compose config --quiet", "YAML parses · compose config valid"],
      ["k8s manifests", "$ kubeconform -strict -summary infra/k8s/**\n$ kustomize build infra/k8s/base", "manifests valid · kustomize base assembles"],
      ["docs links", "$ check every link in docs/**/*.md", "All docs links: OK"],
      ["backend", "$ ruff check backend demoapp\n$ mypy --strict backend/… demoapp/…\n$ pytest backend/… demoapp/…", "style, types and tests passed"],
      ["docker build", "$ docker build demoapp/aegisshop/catalog-service\n$ docker build backend/services/registry-service", "images built"],
      ["frontend build", "$ cd frontend && npm ci && npm run build", "console production build ok"]
    ];
    var timers = [], ran = false;
    function clear() { timers.forEach(clearTimeout); timers = []; }
    function line(h) { if (!log) return; log.insertAdjacentHTML("beforeend", h + "\n"); log.scrollTop = log.scrollHeight; }
    function reset() { clear(); stages.forEach(function (s) { s.classList.remove("running", "passed"); s.querySelector(".st-state").textContent = "queued"; }); if (log) log.innerHTML = ""; wrap.setAttribute("data-state", "idle"); }
    function run() {
      reset(); ran = true; wrap.setAttribute("data-state", "running"); if (stateTxt) stateTxt.textContent = "running";
      if (btn) btn.disabled = true;
      line('<span class="hi">▶ workflow "CI" triggered by push to main</span>');
      var t = 300, step = reduce ? 60 : 1150;
      stages.forEach(function (s, i) {
        timers.push(setTimeout(function () {
          s.classList.add("running"); s.querySelector(".st-state").textContent = "running";
          line('<span class="cmd">' + LOGS[i][1] + "</span>");
        }, t));
        t += step;
        timers.push(setTimeout(function () {
          s.classList.remove("running"); s.classList.add("passed"); s.querySelector(".st-state").textContent = "passed";
          line('<span class="ok">✓ ' + LOGS[i][0] + "</span> " + LOGS[i][2]);
        }, t));
        t += reduce ? 20 : 180;
      });
      timers.push(setTimeout(function () {
        wrap.setAttribute("data-state", "passed"); if (stateTxt) stateTxt.textContent = "all 6 jobs passed";
        line('<span class="ok">✓ all 6 jobs green — ready to merge</span>'); if (btn) btn.disabled = false;
      }, t + 100));
    }
    if (btn) btn.addEventListener("click", run);
    if ("IntersectionObserver" in window) {
      var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting && !ran) { run(); o.disconnect(); } }, { threshold: 0.35 });
      o.observe(wrap);
    } else run();
  })();

  /* ---------- k8s service boot ---------- */
  document.querySelectorAll(".svcs").forEach(function (grid) {
    var svcs = grid.querySelectorAll(".svc");
    function boot() { svcs.forEach(function (s, i) { setTimeout(function () { s.classList.add("up"); }, reduce ? 0 : i * 140); }); }
    if ("IntersectionObserver" in window && !reduce) {
      var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { boot(); o.disconnect(); } }, { threshold: 0.3 }); o.observe(grid);
    } else boot();
  });

  /* ---------- clickable architecture nodes ---------- */
  document.querySelectorAll(".diagram").forEach(function (d) {
    var info = d.querySelector(".info"); if (!info) return;
    var nodes = d.querySelectorAll(".node[data-info]");
    nodes.forEach(function (n) {
      n.addEventListener("click", function () {
        nodes.forEach(function (x) { x.setAttribute("aria-pressed", String(x === n)); });
        info.innerHTML = "<b>" + n.querySelector("b").textContent + "</b> — " + n.getAttribute("data-info");
      });
    });
  });

  /* ---------- skills node pool ---------- */
  (function skills() {
    var cluster = document.getElementById("cluster"); if (!cluster) return;
    var out = document.getElementById("inspect-out"), pods = cluster.querySelectorAll(".pod"), usage = document.getElementById("usage");
    var WHERE = window.__SKILL_WHERE || {};
    function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }
    function describe(p) {
      pods.forEach(function (x) { x.setAttribute("aria-pressed", String(x === p)); });
      var name = p.getAttribute("data-name"), pool = p.closest(".pool").getAttribute("data-pool"), used = (p.getAttribute("data-used") || "").split("|").filter(Boolean);
      var lines = '<span class="ps">$</span> kubectl describe pod <span class="hi">' + esc(p.getAttribute("data-id")) + "</span>\n" +
        "Name:        " + esc(name) + "\n" + "Node pool:   " + esc(pool) + "\n" + "Status:      <span class=\"ok\">Running</span>\n" + "Shows up in: ";
      if (!used.length) lines += '<span class="o">listed in my skills</span>';
      else lines += used.map(function (u, i) { return (i ? "\n             " : "") + esc(u); }).join("");
      out.innerHTML = lines;
    }
    pods.forEach(function (p) { p.addEventListener("click", function () { describe(p); }); });
    if (usage) {
      usage.addEventListener("click", function (e) {
        var b = e.target.closest("button"); if (!b) return;
        var key = b.getAttribute("data-key"), on = b.getAttribute("aria-pressed") !== "true";
        usage.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        if (!on || key === "all") { cluster.classList.remove("filtering"); pods.forEach(function (p) { p.classList.remove("dim", "lit"); }); if (key === "all") b.setAttribute("aria-pressed", "true"); out.innerHTML = '<span class="ps">$</span> kubectl get pods --all-namespaces\n<span class="o">' + pods.length + " pods across 6 node pools. Tap a pod to describe it.</span>"; return; }
        b.setAttribute("aria-pressed", "true"); cluster.classList.add("filtering"); var n = 0;
        pods.forEach(function (p) { var hit = (" " + (p.getAttribute("data-keys") || "") + " ").indexOf(" " + key + " ") > -1; p.classList.toggle("lit", hit); p.classList.toggle("dim", !hit); if (hit) n++; });
        out.innerHTML = '<span class="ps">$</span> kubectl get pods -l used-in=<span class="hi">' + esc(key) + '</span>\n<span class="o">' + n + " pods matched: " + esc(b.textContent) + "</span>";
      });
    }
    var poolsEl = cluster;
    if ("IntersectionObserver" in window && !reduce) {
      poolsEl.classList.add("pool-boot");
      pods.forEach(function (p, i) { p.style.transitionDelay = (i * 35) + "ms"; });
      var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { poolsEl.classList.add("booted"); o.disconnect(); setTimeout(function () { pods.forEach(function (p) { p.style.transitionDelay = ""; }); }, 2200); } }, { threshold: 0.1 });
      o.observe(poolsEl);
    }
  })();

  /* ---------- command palette ---------- */
  (function palette() {
    var dlg = document.getElementById("palette"); if (!dlg || typeof dlg.showModal !== "function") return;
    var out = dlg.querySelector(".pal-out"), input = dlg.querySelector("input"), chips = dlg.querySelector(".pal-chips");
    var hist = [], hi = -1, greeted = false;
    var CMDS = ["help", "whoami", "projects", "skills", "experience", "about", "contact", "resume", "email", "github", "linkedin", "ls", "kubectl get pods", "open aegisdeploy", "open portfolio", "open digicrave", "open java", "sudo hire navin", "theme light", "theme dark", "home", "clear", "exit"];
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function print(h) { out.insertAdjacentHTML("beforeend", h + "\n"); out.scrollTop = out.scrollHeight; }
    function go(path, label) { print('<span class="ok">→ opening ' + esc(label) + "…</span>"); setTimeout(function () { window.location.href = ROOT + path; }, reduce ? 0 : 380); }
    function ext(url, label) { print('<span class="ok">→ opening ' + esc(label) + '</span> <a href="' + url + '" target="_blank" rel="noopener">' + esc(url.replace(/^https?:\/\//, "")) + "</a>"); var w = window.open(url, "_blank", "noopener"); return w; }
    function greet() {
      print('<span class="dim">navin-sh 1.0 — an interactive shell for this site.</span>');
      print('Type <span class="hi">help</span> to see commands. <span class="dim">Tab completes, ↑↓ history, Esc closes.</span>');
    }
    var H = {
      help: function () {
        print([
          '<span class="hi">whoami</span>        who is Navin',
          '<span class="hi">projects</span>      go to projects  ·  <span class="hi">ls</span> list pages',
          '<span class="hi">kubectl get pods</span>  projects, as pods',
          '<span class="hi">open &lt;name&gt;</span>   aegisdeploy · portfolio · digicrave · java',
          '<span class="hi">skills</span>        the node-pool view of my stack',
          '<span class="hi">experience</span>    internships timeline',
          '<span class="hi">resume</span>        download my resume (PDF)',
          '<span class="hi">contact</span>       contact page  ·  <span class="hi">email</span> copy my email',
          '<span class="hi">github</span> · <span class="hi">linkedin</span>  open profiles',
          '<span class="hi">theme light|dark</span>  switch the colour theme',
          '<span class="hi">clear</span> · <span class="hi">exit</span>'
        ].join("\n"));
      },
      whoami: function () { print('<span class="hi">Navin Jairam M</span> — DevOps &amp; Cloud Engineer\nFinal-year B.Tech IT (2023–2027), Chennai\n2 DevOps internships: Rapture Twelve, Adroit Technologies\nSeeking DevOps, SRE, and cloud roles starting in 2027'); },
      ls: function () { print("index.html  about.html  projects.html  skills.html  contact.html\nprojects/aegisdeploy.html  projects/portfolio-platform.html\nprojects/digicrave-os.html  projects/distributed-java-webapp.html"); },
      projects: function () { go(PAGES.projects, "projects"); },
      skills: function () { go(PAGES.skills, "skills"); },
      experience: function () { go(PAGES.experience, "experience"); },
      about: function () { go(PAGES.about, "about"); },
      contact: function () { go(PAGES.contact, "contact"); },
      home: function () { go(PAGES.home, "home"); },
      resume: function () {
        print('<span class="ok">→ downloading resume</span> <a href="' + LINKS.resume + '" download>Navin_Jairam_M_Resume.pdf</a>');
        var a = document.createElement("a"); a.href = LINKS.resume; a.download = "Navin_Jairam_M_Resume.pdf"; document.body.appendChild(a); a.click(); a.remove();
      },
      email: function () { copyText(EMAIL).then(function (ok) { print(ok ? '<span class="ok">✓ copied</span> ' + EMAIL + ' to clipboard · <a href="mailto:' + EMAIL + '">write now</a>' : 'my email: <a href="mailto:' + EMAIL + '">' + EMAIL + "</a>"); }); },
      github: function () { ext(LINKS.github, "GitHub"); },
      linkedin: function () { ext(LINKS.linkedin, "LinkedIn"); },
      theme: function () { print("theme: " + currentTheme() + '  ·  usage: <span class="hi">theme light</span> | <span class="hi">theme dark</span> | <span class="hi">theme toggle</span>'); },
      clear: function () { out.innerHTML = ""; },
      exit: function () { dlg.close(); },
      "kubectl get pods": function () {
        var short = ["aegisdeploy", "portfolio-platform", "digicrave-os", "java-webapp", "kaizen"];
        var rows = '<span class="dim">NAME                STATUS</span>';
        PROJECTS.forEach(function (p, i) {
          var href = p.page ? ROOT + p.page : p.repo;
          rows += "\n" + (short[i] + "                    ").slice(0, 20) + '<span class="ok">Running</span>  <a href="' + href + '"' + (p.page ? "" : ' target="_blank" rel="noopener"') + ">" + (p.page ? "open" : "repo") + "</a>";
        });
        print(rows);
      },
      "sudo hire navin": function () {
        print("[sudo] password for recruiter: ********");
        setTimeout(function () { print('<span class="ok">✓ access granted.</span> Great call. Opening an email to Navin…'); setTimeout(function () { window.location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Let's talk: DevOps role"); }, reduce ? 0 : 700); }, reduce ? 0 : 600);
      }
    };
    var OPEN = { aegisdeploy: 0, aegis: 0, portfolio: 1, "portfolio-platform": 1, digicrave: 2, "digicrave-os": 2, java: 3, "distributed-java-webapp": 3, kaizen: 4 };
    function exec(raw) {
      var cmd = raw.trim().replace(/\s+/g, " "); if (!cmd) return;
      hist.unshift(cmd); hi = -1;
      print('<span class="ps">visitor@navin:~$</span> ' + esc(cmd));
      var low = cmd.toLowerCase();
      if (H[low]) return H[low]();
      if (/^(cd|goto|go) /.test(low)) { var t = low.split(" ")[1].replace(/\.html$/, "").replace(/^\/|\/$/g, ""); if (t === "~" || t === "") t = "home"; if (PAGES[t]) return go(PAGES[t], t); }
      if (/^(open|cat) /.test(low)) { var k = low.split(" ")[1]; if (k in OPEN) { var p = PROJECTS[OPEN[k]]; return p.page ? go(p.page, p.name) : ext(p.repo, p.name + " repo"); } print('<span class="er">no such project: ' + esc(k) + '</span> · try <span class="hi">kubectl get pods</span>'); return; }
      if (/^deploy navin/.test(low)) { print('<span class="ok">✓ already deployed to prod.</span> Next step: <span class="hi">contact</span>'); return; }
      var tm = low.match(/^theme\s+(light|dark|toggle|auto)$/);
      if (tm) {
        if (tm[1] === "auto") { try { localStorage.removeItem(THEME_KEY); } catch (e) {} applyTheme(osTheme(), false); print('<span class="ok">✓ theme follows your system</span> (' + currentTheme() + ")"); return; }
        var to = tm[1] === "toggle" ? (currentTheme() === "light" ? "dark" : "light") : tm[1];
        applyTheme(to, true); print('<span class="ok">✓ theme set to ' + to + "</span>"); return;
      }
      if (/^theme\b/.test(low)) { print('usage: <span class="hi">theme light</span> | <span class="hi">theme dark</span> | <span class="hi">theme toggle</span> | <span class="hi">theme auto</span>'); return; }
      if (/^kubectl/.test(low)) return H["kubectl get pods"]();
      if (/^sudo/.test(low)) { print('visitor is not in the sudoers file. Try <span class="hi">sudo hire navin</span>'); return; }
      if (/^echo /.test(low)) { print(esc(cmd.slice(5))); return; }
      if (low === "history") { print(hist.slice(1).reverse().map(function (h, i) { return (i + 1) + "  " + esc(h); }).join("\n") || "(empty)"); return; }
      if (low === "date") { print(new Date().toString()); return; }
      if (low === "pwd") { print("/home/visitor/" + (location.pathname.split("/").pop() || "index.html")); return; }
      if (low === "uname" || low === "uname -a") { print("navin-sh 1.0 static-html x86_64 (no backend, still fast)"); return; }
      print('<span class="er">command not found: ' + esc(cmd.split(" ")[0]) + '</span> · type <span class="hi">help</span>');
    }
    function open(prefill) {
      if (dlg.open) return;
      dlg.showModal(); if (!greeted) { greet(); greeted = true; }
      if (prefill) { input.value = prefill; }
      setTimeout(function () { input.focus(); }, 30);
    }
    window.__openPalette = open;
    document.querySelectorAll("[data-palette]").forEach(function (b) { b.addEventListener("click", function () { open(); }); });
    document.addEventListener("keydown", function (e) {
      var k = e.key ? e.key.toLowerCase() : "";
      if ((e.metaKey || e.ctrlKey) && k === "k") { e.preventDefault(); dlg.open ? dlg.close() : open(); return; }
      if (k === "/" && !dlg.open) { var t = e.target; if (!(t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable))) { e.preventDefault(); open(); } }
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); var v = input.value; input.value = ""; exec(v); }
      else if (e.key === "ArrowUp") { if (hist.length) { e.preventDefault(); hi = Math.min(hi + 1, hist.length - 1); input.value = hist[hi]; } }
      else if (e.key === "ArrowDown") { e.preventDefault(); hi = Math.max(hi - 1, -1); input.value = hi < 0 ? "" : hist[hi]; }
      else if (e.key === "Tab") {
        var v2 = input.value.toLowerCase(); if (!v2) return; e.preventDefault();
        var m = CMDS.filter(function (c) { return c.indexOf(v2) === 0; });
        if (m.length === 1) input.value = m[0]; else if (m.length > 1) print('<span class="dim">' + m.join("   ") + "</span>");
      }
    });
    if (chips) chips.addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; exec(b.getAttribute("data-cmd")); input.focus(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    var closeBtn = dlg.querySelector("[data-close]"); if (closeBtn) closeBtn.addEventListener("click", function () { dlg.close(); });
  })();

  /* footer year */
  var y = document.getElementById("year"); if (y) y.textContent = String(new Date().getFullYear());
})();
