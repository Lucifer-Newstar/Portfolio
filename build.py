#!/usr/bin/env python3
"""Builds the static site into ./site from the page bodies below. Run: python3 build.py [BASE_URL]"""
import sys, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://navin-jairam.sites.tab.bot/").rstrip("/") + "/"
TITLE = "Navin Jairam M — DevOps & Cloud Engineer"
DESC = "Final-year B.Tech IT student in Chennai building on AWS, Kubernetes, Docker, GitHub Actions and Prometheus/Grafana. Projects, internships and resume."
EMAIL = "navin.jairam@gmail.com"
GH = "https://github.com/Lucifer-Newstar"
LI = "https://www.linkedin.com/in/navin-jairam"

ICON = {
 "gh": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.56-.29-5.25-1.28-5.25-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.42-2.7 5.39-5.26 5.68.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/></svg>',
 "li": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13ZM7.12 20.45H3.56V9h3.56v11.45ZM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0Z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 "dl": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12m0 0-5-5m5 5 5-5M4 21h16"/></svg>',
 "copy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>',
 "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/></svg>',
 "term": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 7 5 5-5 5M12 18h7"/></svg>',
 "award": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="9" r="6"/><path d="m8.5 14.2-1.5 7.8 5-3 5 3-1.5-7.8"/></svg>',
}

NAV = [("index.html","Home","home"),("about.html","About","about"),("projects.html","Projects","projects"),("skills.html","Skills","skills"),("contact.html","Contact","contact")]

def page(fname, key, title, desc, body, root=""):
    canon = BASE + ("" if fname == "index.html" else fname)
    cur = ' aria-current="page"'
    links = "".join(f'<li><a href="{root}{h}"{cur if k==key else ""}>{t}</a></li>' for h,t,k in NAV)
    full_title = TITLE if key == "home" else f"{title} · Navin Jairam M"
    return f"""<!doctype html>
<html lang="en" class="no-js" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="Navin Jairam M">
<meta name="theme-color" content="#06080c">
<meta name="color-scheme" content="dark light">
<script src="{root}theme-init.js"></script>
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Navin Jairam M">
<meta property="og:title" content="{html.escape(TITLE if key=='home' else full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Navin Jairam M — DevOps &amp; Cloud Engineer">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(TITLE if key=='home' else full_title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}og.png">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}assets/fonts/jetbrains-mono.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}styles.css">
<script src="{root}script.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<canvas id="net" aria-hidden="true"></canvas>
<div class="grain" aria-hidden="true"></div>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="brand" href="{root}index.html" aria-label="Navin Jairam M, home"><span class="dot" aria-hidden="true"></span><span><b>navin</b>@prod:<span class="path">~</span>$</span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav-links" aria-label="Menu"><span></span><span></span><span></span></button>
    <ul class="nav-links" id="nav-links">{links}</ul>
    <button class="theme-btn" type="button" data-theme-toggle aria-label="Switch colour theme"><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg><svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg></button>
    <button class="kbtn" data-palette type="button" aria-label="Open command palette">{ICON['term']}<span>Command</span><kbd>⌘K</kbd></button>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <span>© <span id="year">2026</span> Navin Jairam M · built as static HTML, CSS &amp; JS</span>
    <nav aria-label="Footer"><a href="mailto:{EMAIL}">Email</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="{GH}" target="_blank" rel="noopener">GitHub</a><a href="{root}assets/Navin_Jairam_M_Resume.pdf" download>Resume</a></nav>
  </div>
</footer>
<button class="fab" type="button" data-palette aria-label="Open command terminal">{ICON['term']}</button>
<dialog class="palette" id="palette" aria-label="Command terminal">
  <div class="pal-head"><span>navin-sh — try <b>help</b></span><button type="button" data-close>esc</button></div>
  <div class="pal-out" aria-live="polite"></div>
  <div class="pal-chips" aria-label="Suggested commands">
    <button type="button" data-cmd="help">help</button><button type="button" data-cmd="whoami">whoami</button><button type="button" data-cmd="kubectl get pods">kubectl get pods</button><button type="button" data-cmd="projects">projects</button><button type="button" data-cmd="skills">skills</button><button type="button" data-cmd="experience">experience</button><button type="button" data-cmd="resume">resume</button><button type="button" data-cmd="email">email</button><button type="button" data-cmd="contact">contact</button><button type="button" data-cmd="theme toggle">theme toggle</button><button type="button" data-cmd="sudo hire navin">sudo hire navin</button>
  </div>
  <div class="pal-in"><label for="pal-input">visitor@navin:~$</label><input id="pal-input" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="go" placeholder="type a command…"></div>
</dialog>
</body>
</html>
"""

def photo(root, cls="", eager=False, size=600):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<picture><source srcset="{root}assets/img/navin.webp" type="image/webp"><img src="{root}assets/img/navin.jpg" width="{size}" height="{size}" alt="Photo of Navin Jairam M" decoding="async" {load}></picture>'

def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{html.escape(t)}</li>" for t in items) + "</ul>"

def write(path, s):
    p = os.path.join(SITE, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

exec(open(os.path.join(HERE, "pages.py"), encoding="utf-8").read())
print("built", BASE)
