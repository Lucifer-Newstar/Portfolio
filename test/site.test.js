// Reads the built site and checks the request's core content. Run: node --test test/
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const SITE = path.join(__dirname, "..", "site");
const PAGES = ["index.html", "about.html", "projects.html", "skills.html", "contact.html",
  "projects/aegisdeploy.html", "projects/portfolio-platform.html", "projects/digicrave-os.html", "projects/distributed-java-webapp.html", "404.html"];
const read = (p) => fs.readFileSync(path.join(SITE, p), "utf8");
const all = PAGES.map((p) => [p, read(p)]);
// The site's base path (e.g. "/Portfolio/"), read from the canonical URL build.py wrote.
const BASE_PATH = new URL(read("index.html").match(/rel="canonical" href="([^"]+)"/)[1]).pathname;

test("every page exists with a title, viewport meta, lang and main landmark", () => {
  for (const [p, h] of all) {
    assert.match(h, /<title>[^<]{5,}<\/title>/, p + " title");
    assert.match(h, /<meta name="viewport" content="width=device-width, initial-scale=1/, p + " viewport");
    assert.match(h, /<html lang="en"/, p + " lang");
    assert.match(h, /<main id="main">/, p + " main");
    assert.match(h, /<h1>/, p + " h1");
  }
});

test("home has the requested title and OG/Twitter preview tags with a real image", () => {
  const h = read("index.html");
  assert.match(h, /<title>Navin Jairam M — DevOps &amp; Cloud Engineer<\/title>/);
  assert.match(h, /property="og:title" content="Navin Jairam M — DevOps &amp; Cloud Engineer"/);
  assert.match(h, /property="og:image" content="https:\/\/[^"]+\/og\.png"/);
  assert.match(h, /name="twitter:card" content="summary_large_image"/);
  const png = fs.readFileSync(path.join(SITE, "og.png"));
  assert.equal(png.readUInt32BE(16), 1200); assert.equal(png.readUInt32BE(20), 630);
});

test("all local href/src references resolve to files", () => {
  for (const [p, h] of all) {
    const dir = path.dirname(path.join(SITE, p));
    const refs = [...h.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1])
      .filter((u) => !/^(https?:|mailto:|tel:|#|data:)/.test(u));
    for (const r of refs) {
      // 404.html uses base-path-absolute links (served at any depth); everything else is relative.
      if (p === "404.html") assert.ok(r.startsWith(BASE_PATH), `404.html -> ${r} is not under ${BASE_PATH}`);
      const clean = r.split("#")[0].split("?")[0];
      const file = clean.startsWith("/") ? path.join(SITE, clean.slice(BASE_PATH.length)) : path.resolve(dir, clean);
      assert.ok(fs.existsSync(file), `${p} -> ${r} missing`);
    }
  }
  for (const f of ["styles.css", "script.js", "favicon.svg", "apple-touch-icon.png", "assets/Navin_Jairam_M_Resume.pdf", "assets/fonts/inter.woff2", "assets/fonts/jetbrains-mono.woff2", "assets/fonts/space-grotesk.woff2"])
    assert.ok(fs.existsSync(path.join(SITE, f)), f);
  const css = read("styles.css");
  for (const m of css.matchAll(/url\("([^"]+)"\)/g)) assert.ok(fs.existsSync(path.join(SITE, m[1])), "css url " + m[1]);
});

test("required links are present", () => {
  const joined = all.map((x) => x[1]).join("\n");
  for (const u of ["https://github.com/Lucifer-Newstar", "https://www.linkedin.com/in/navin-jairam", "mailto:navin.jairam@gmail.com",
    "https://github.com/Lucifer-Newstar/AegisDeploy", "https://github.com/Lucifer-Newstar/DigiCraveOS",
    "https://github.com/Lucifer-Newstar/distributed-java-webapp", "https://github.com/Lucifer-Newstar/Productivity-App", "https://digi-crave-os.vercel.app"])
    assert.ok(joined.includes(u), "missing " + u);
  assert.match(joined, /href="(\.\.\/)?assets\/Navin_Jairam_M_Resume\.pdf" download/);
});

test("location references are removed from every page and the interactive terminal", () => {
  const files = [...all, ["script.js", read("script.js")]];
  for (const [p, h] of files) {
    assert.ok(!/bang(?:al|l)ore|bengaluru/i.test(h), p + " still mentions a removed location");
  }
  assert.match(read("contact.html"), /graduating in 2027 and seeking DevOps, SRE, or cloud roles/);
});

test("no dead domain, phone number, placeholders, or inline scripts", () => {
  const files = [...all, ["script.js", read("script.js")], ["styles.css", read("styles.css")]];
  for (const [p, h] of files) {
    assert.ok(!/lucifernewstar-2006/i.test(h), p + " links the dead domain");
    assert.ok(!/\b[6-9]\d{9}\b|tel:|\+91/.test(h), p + " exposes a phone number");
    assert.ok(!/lorem ipsum|TODO|\(github-link\)|placeholder text|\{\{/i.test(h), p + " placeholder");
    if (p.endsWith(".html")) {
      assert.ok(!/<script(?![^>]*\bsrc=)[^>]*>/.test(h), p + " inline <script>");
      assert.ok(!/\son[a-z]+="/i.test(h), p + " inline event handler");
    }
  }
});

test("core content: pipeline stages, services, observability, timeline, skill pools, palette", () => {
  const a = read("projects/aegisdeploy.html");
  const stages = [...a.matchAll(/class="st-name">([^<]+)</g)].map((m) => m[1]);
  assert.deepEqual(stages, ["config", "k8s manifests", "docs links", "backend", "docker build", "frontend build"]);
  for (const s of ["ruff · mypy · pytest", "kubeconform + kustomize", "YAML + compose valid", "every docs link resolves"]) assert.ok(a.includes(s), "stage sub " + s);
  assert.equal((a.match(/class="svc( demo)?"/g) || []).length, 7);
  for (const t of ["Prometheus", "Grafana", "Loki", "Tempo", "OpenTelemetry"]) assert.ok(a.includes(t), t);
  const pp = read("projects/portfolio-platform.html");
  for (const t of ["S3", "CloudFront", "API Gateway", "Lambda", "DynamoDB", "Cognito", "SES"]) assert.ok(pp.includes("<b>" + t + "</b>"), t);
  const ab = read("about.html");
  assert.ok(ab.includes("Rapture Twelve") && ab.includes("May 2026 – Oct 2026") && ab.includes("Certificate of Exceptional Contribution"));
  assert.ok(ab.includes("Adroit Technologies") && ab.includes("Dec 2025 – Feb 2026"));
  const sk = read("skills.html");
  assert.equal((sk.match(/class="pool"/g) || []).length, 6);
  assert.ok(!/\d+%/.test(sk.replace(/<style[\s\S]*?<\/style>/g, "").replace(/style="[^"]*"/g, "")), "no percentage levels on skills");
  for (const [p, h] of all) assert.ok(h.includes('id="palette"') && h.includes("data-palette"), p + " palette");
  const js = read("script.js");
  for (const c of ["help", "projects", "skills", "resume", "contact"]) assert.ok(js.includes(c + ":"), "command " + c);
  assert.ok(js.includes("prefers-reduced-motion"));
});

test("theme: toggle on every page, no-flash init script in head before CSS, light theme defined, palette command", () => {
  for (const [p, h] of all) {
    const head = h.split("</head>")[0];
    assert.ok(head.indexOf('theme-init.js"></script>') > -1 && head.indexOf('theme-init.js') < head.indexOf('styles.css'), p + " theme-init before CSS");
    assert.ok(!/theme-init\.js"[^>]*\b(defer|async)\b/.test(head), p + " theme-init must be blocking");
    assert.ok(h.includes("data-theme-toggle"), p + " toggle");
  }
  const init = read("theme-init.js");
  assert.ok(init.includes("localStorage") && init.includes("prefers-color-scheme: light") && init.includes("data-theme"));
  const css = read("styles.css");
  assert.ok(css.includes('[data-theme="light"]{'), "light vars");
  const js = read("script.js");
  assert.ok(js.includes("theme\\s+(light|dark|toggle|auto)") && js.includes("theme light|dark"), "theme command");
  assert.ok(js.includes("visibilitychange") && js.includes("helm(") && js.includes("hex(") && js.includes("SNIPS"), "background motifs + pause when hidden");
});

test("photo: optimised WebP + JPEG, square, used on home and about with alt text", () => {
  for (const f of ["assets/img/navin.webp", "assets/img/navin.jpg"]) {
    const b = fs.readFileSync(path.join(SITE, f)); assert.ok(b.length > 4000 && b.length < 120000, f + " size " + b.length);
  }
  const jpg = fs.readFileSync(path.join(SITE, "assets/img/navin.jpg"));
  let i = 2; let w = 0, h = 0;
  while (i < jpg.length) { if (jpg[i] !== 0xff) { i++; continue; } const m = jpg[i + 1]; if (m >= 0xc0 && m <= 0xc2) { h = jpg.readUInt16BE(i + 5); w = jpg.readUInt16BE(i + 7); break; } i += 2 + jpg.readUInt16BE(i + 2); }
  assert.equal(w, 600); assert.equal(h, 600);
  for (const p of ["index.html", "about.html"]) {
    const h2 = read(p);
    assert.match(h2, /<source srcset="assets\/img\/navin\.webp" type="image\/webp"><img src="assets\/img\/navin\.jpg" width="600" height="600" alt="Photo of Navin Jairam M"/, p);
  }
});

test("downloadable resume is the copy without the phone number", () => {
  const { execFileSync } = require("node:child_process");
  const txt = execFileSync("pdftotext", [path.join(SITE, "assets/Navin_Jairam_M_Resume.pdf"), "-"]).toString();
  assert.ok(txt.includes("Navin") || txt.includes("NAVIN"));
  assert.ok(!/\b[6-9]\d{9}\b|\+91/.test(txt), "phone in served resume");
  assert.ok(txt.includes("YAML/compose validation") && txt.includes("docs link check"), "corrected CI line in served resume");
  assert.ok(!fs.readFileSync(path.join(SITE, "assets/Navin_Jairam_M_Resume.pdf")).includes("tel:"), "tel link in PDF");
});

test("404 page works under the base path and is not indexed", () => {
  const h = read("404.html");
  assert.ok(h.includes(`href="${BASE_PATH}styles.css"`) && h.includes(`src="${BASE_PATH}script.js"`), "404 assets use " + BASE_PATH);
  assert.ok(h.includes(`data-root="${BASE_PATH}"`), "404 data-root");
  assert.ok(h.includes(`href="${BASE_PATH}index.html">Back home`), "404 back-home link");
  assert.match(h, /<meta name="robots" content="noindex">/);
  for (const [p, x] of all) if (p !== "404.html") assert.ok(!x.includes('name="robots"'), p + " must stay indexable");
});

test("Portfolio Platform never links the wrong or the abandoned repo", () => {
  const files = [...all, ["script.js", read("script.js")]];
  for (const [p, h] of files) {
    assert.ok(!/github\.com\/Lucifer-Newstar\/portfolio(?:-abandoned)?(?=["'\/?#\s]|$)/i.test(h), p + " links the portfolio / portfolio-abandoned repo");
  }
  const pp = read("projects/portfolio-platform.html");
  const repo = pp.match(/data-pp-repo="([^"]*)"/)[1];
  if (repo) assert.ok(pp.includes(`href="https://github.com/Lucifer-Newstar/${repo}"`), "source button links the configured repo");
  else assert.ok(pp.includes('data-source="private"') && pp.includes("Source: private, available on request"), "private source state");
});

test("AegisDeploy copy is honest: phase 2 built, AI on the roadmap, 7 Dockerfiles, 6 instrumented services", () => {
  const files = [...all, ["script.js", read("script.js")]];
  for (const [p, h] of files) {
    assert.ok(!/AI-powered|autonomous SRE|hop by hop/i.test(h), p + " overstates AegisDeploy");
    assert.ok(!/6 Dockerfiles|>6<small>Dockerfiles/.test(h), p + " says 6 Dockerfiles");
    // one spelling: British (-ise), as most of the site already uses
    assert.ok(!/\b(containeriz|optimiz|authoriz|organiz|customiz|visualiz|standardiz|prioritiz|recogniz|summariz|analyz|minimiz|maximiz|utiliz|categoriz)\w*/i.test(h), p + " uses American -ize spelling");
  }
  const a = read("projects/aegisdeploy.html");
  assert.ok(a.includes("phase 2") && /roadmap/i.test(a), "phase 2 + roadmap");
  assert.ok(a.includes('<div class="stat">7<small>Dockerfiles</small>'), "7 Dockerfiles stat");
  assert.ok(!a.includes("<b>7 services</b>"), "observability diagram says 7 services");
  assert.equal((a.match(/<b>6 services<\/b>/g) || []).length, 3, "6 instrumented services in each lane");
});

test("apple-touch-icon is a 180px PNG and is linked from every page", () => {
  const png = fs.readFileSync(path.join(SITE, "apple-touch-icon.png"));
  assert.equal(png.readUInt32BE(16), 180); assert.equal(png.readUInt32BE(20), 180);
  for (const [p, h] of all) assert.match(h, /<link rel="apple-touch-icon" href="[^"]*apple-touch-icon\.png">/, p);
});
