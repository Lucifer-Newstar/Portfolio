# Page bodies. Executed by build.py (shares its namespace: page, write, tags, ICON, EMAIL, GH, LI, html).
R = "https://github.com/Lucifer-Newstar/"
PP_SRC = R + PORTFOLIO_PLATFORM_REPO if PORTFOLIO_PLATFORM_REPO else ""  # set the repo name in build.py

def node(name, sub, info, color=None, glow=False):
    c = f' style="--c:var(--{color})"' if color else ""
    g = " glow" if glow else ""
    return f'<button type="button" class="node{g}"{c} aria-pressed="false" data-info="{html.escape(info)}"><b>{html.escape(name)}</b><small>{html.escape(sub)}</small></button>'

def wire(color=None):
    c = f' style="--c:var(--{color})"' if color else ""
    return f'<span class="wire" aria-hidden="true"{c}></span>'

def lane(label, parts, color="cyan"):
    out = []
    for i, p in enumerate(parts):
        if i: out.append(wire(color))
        if isinstance(p, list):
            out.append('<div class="fan">' + "".join(node(*n, color=color) for n in p) + "</div>")
        else:
            out.append(node(*p, color=color))
    return f'<p class="lane-label">{html.escape(label)}</p><div class="lane" role="group" aria-label="{html.escape(label)}">' + "".join(out) + "</div>"

def diagram(title, lanes_html, hint="Tap any box to see what it does."):
    return f'<figure class="diagram reveal" aria-label="{html.escape(title)}">{lanes_html}<figcaption class="info" aria-live="polite"><span class="hint">▸ {html.escape(hint)}</span></figcaption></figure>'

def pcard(href, title, kind, desc, tg, data_tags, external=False, feature=False, delay=0, hl="h3", arch=None):
    tgt = ' target="_blank" rel="noopener"' if external else ""
    go = "View repo on GitHub" if external else "Open case study"
    f = " feature" if feature else ""
    corner = "github ↗" if external else "case study"
    if arch:
        return f'''<div class="card tilt pcard reveal{f}" data-tags="{data_tags}" data-delay="{delay}">
  <div class="ptop"><span class="badge">{html.escape(kind)}</span><span>{corner}</span></div>
  <{hl}><a class="pcard-title" href="{href}">{html.escape(title)}</a></{hl}>
  <p>{html.escape(desc)}</p>
  {tags(tg)}
  <div class="pcard-foot">
    <a class="go" href="{href}">{go} <span class="arr" aria-hidden="true">→</span></a>
    <button type="button" class="arch-btn" data-arch-open="{arch}">View architecture</button>
  </div>
</div>'''
    return f'''<a class="card tilt pcard reveal{f}" href="{href}"{tgt} data-tags="{data_tags}" data-delay="{delay}">
  <div class="ptop"><span class="badge">{html.escape(kind)}</span><span>{corner}</span></div>
  <{hl}>{html.escape(title)}</{hl}>
  <p>{html.escape(desc)}</p>
  {tags(tg)}
  <span class="go">{go} <span class="arr" aria-hidden="true">→</span></span>
</a>'''

def wcard(href, title, meta, desc, delay=0, badge="write-up", cta="Read", external=False):
    tgt = ' target="_blank" rel="noopener"' if external else ''
    arrow = '↗' if external else '→'
    return f'''<a class="card tilt pcard reveal" href="{href}"{tgt} data-delay="{delay}">
  <div class="ptop"><span class="badge">{badge}</span><span>{html.escape(meta)}</span></div>
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(desc)}</p>
  <span class="go">{cta} <span class="arr" aria-hidden="true">{arrow}</span></span>
</a>'''

def detail_head(root, kind, title, lead, tg, links):
    btns = "".join(links)
    slug = html.escape(title.lower().replace(" ", "-"))
    return f'''<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="{root}projects.html">~/projects</a> / {slug}</p>
  <p class="eyebrow">{html.escape(kind)}</p>
  <h1>{html.escape(title)}</h1>
  <p class="lead">{lead}</p>
  <div style="margin:18px 0 24px">{tags(tg)}</div>
  <div class="btns">{btns}</div>
</div></section>'''

def gh_btn(repo):
    return f'<a class="btn" href="{R}{repo}" target="_blank" rel="noopener">{ICON["gh"]} Source on GitHub</a>'

def src_btn(url):
    """Source button for a full repo URL, or a non-clickable "private" state when url is empty."""
    if url:
        return f'<a class="btn" href="{url}" target="_blank" rel="noopener">{ICON["gh"]} Source on GitHub</a>'
    return f'<span class="btn btn-off" data-source="private">{ICON["gh"]} Source: private, available on request</span>'

def next_nav(root, prev, nxt):
    return f'''<section style="padding-top:20px"><div class="wrap next">
  <a class="btn" href="{root}{prev[0]}">← {html.escape(prev[1])}</a>
  <a class="btn" href="{root}{nxt[0]}">{html.escape(nxt[1])} →</a>
</div></section>'''

def CTA(root):
    return f'''<section><div class="wrap"><div class="cta reveal">
  <div><h2>Hiring for DevOps, SRE or Cloud?</h2><p>I'm graduating in 2027 and seeking DevOps, SRE, or cloud roles. Let's talk.</p></div>
  <div class="btns"><a class="btn primary" href="mailto:{EMAIL}">{ICON["mail"]} Email me</a><a class="btn" href="{root}assets/Navin_Jairam_M_Resume.pdf" download>{ICON["dl"]} Download resume</a></div>
</div></div></section>'''

# ---------------- HOME ----------------
home = f'''<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <div class="podcard">
      <div class="avatar">{photo("", eager=True)}</div>
      <div class="podmeta">
        <span class="pod-name">pod/<b>navin-jairam-m</b> <span>· ns: chennai</span></span>
        <span class="pod-status"><span class="pill"><i aria-hidden="true"></i>Running</span> open to DevOps / SRE roles · 2027</span>
      </div>
    </div>
    <h1>Navin Jairam M<span class="role">DevOps &amp; Cloud Engineer who likes software that <span class="grad">ships reliably</span>.</span></h1>
  </div>
  <div class="hero-actions">
    <p class="lead">Final-year B.Tech IT student in Chennai with two DevOps internships on live projects. I build with AWS, Docker, Kubernetes, GitHub Actions, Ansible, and Prometheus with Grafana.</p>
    <div class="btns">
      <a class="btn primary" href="projects.html">See my projects <span aria-hidden="true">→</span></a>
      <a class="btn" href="assets/Navin_Jairam_M_Resume.pdf" download>{ICON["dl"]} Resume</a>
      <button class="btn" type="button" data-palette>{ICON["term"]} Terminal</button>
    </div>
    <p class="hero-meta"><span>Chennai, India</span><span>B.Tech IT 2023–2027</span><span>Seeking DevOps / SRE / Cloud roles</span></p>
  </div>
  <div class="term" role="group" aria-label="Animated terminal: whoami prints navin-jairam-m; kubectl get pods lists the projects AegisSRE, ColdBox Pentest and DineSmart as running; deploy navin to prod prints Navin Jairam M, DevOps and Cloud Engineer.">
    <div class="term-bar" aria-hidden="true"><i></i><i></i><i></i><span>navin@prod: ~ — zsh</span></div>
    <div class="term-body" id="hero-term" aria-hidden="true"></div>
    <div class="term-foot"><span aria-hidden="true"><span class="hint-desk">press ⌘K or / for the real shell</span><span class="hint-touch">tap &gt;_ for the real shell</span></span><button type="button" id="hero-skip">skip ⏭</button><button type="button" id="hero-replay" hidden>replay ↻</button></div>
  </div>
</div></section>

<section style="padding-top:20px"><div class="wrap">
  <div class="grid g3">
    <div class="card reveal"><div class="stat">2<small>DevOps internships on live projects: Rapture Twelve and Adroit Technologies</small></div></div>
    <div class="card reveal" data-delay="80"><div class="stat">6-job<small>GitHub Actions CI pipeline guarding every push to AegisSRE</small></div></div>
    <div class="card reveal" data-delay="160"><div class="stat">9<small>security findings documented, fixed and re-tested in my ColdBox pentest</small></div></div>
  </div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow reveal">what I work on</p>
  <h2 class="reveal">Cloud, containers, pipelines and the dashboards that watch them</h2>
  <div class="grid g3" style="margin-top:26px">
    <div class="card reveal"><h3>Cloud on AWS</h3><p class="muted">IAM roles and policies, cloud architecture and deployment strategy at Rapture Twelve, and a serverless portfolio on S3, CloudFront, Lambda and DynamoDB.</p></div>
    <div class="card reveal" data-delay="80"><h3>Containers &amp; Kubernetes</h3><p class="muted">Dockerised services, Kubernetes manifests managed with Kustomize, and manifests validated in CI with kubeconform.</p></div>
    <div class="card reveal" data-delay="160"><h3>CI/CD &amp; observability</h3><p class="muted">GitHub Actions pipelines, plus Prometheus alert rules, Grafana dashboards, Loki logs, Tempo traces and OpenTelemetry.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap">
    <div><p class="eyebrow reveal">featured work</p><h2 class="reveal" style="margin:0">Projects</h2></div>
    <a class="btn reveal" href="projects.html">All projects →</a>
  </div>
  <a class="card tilt pcard reveal feature-flag" href="projects/aegissre.html" style="margin-top:26px">
    <div class="ptop"><span class="badge">SRE platform · personal flagship</span><span>case study</span></div>
    <div class="ff-grid">
      <div>
        <h3>AegisSRE</h3>
        <p>SRE platform, phase 2 built and tested: a 4-service demo shop watched by a service registry, deployments API and a Next.js console, with Prometheus, Grafana, Loki, Tempo and OpenTelemetry. AI incident detection and auto-remediation are next on the roadmap.</p>
        {tags(["Kubernetes","FastAPI","GitHub Actions","Prometheus","Grafana"])}
        <span class="go">Open case study <span class="arr" aria-hidden="true">→</span></span>
      </div>
      <div class="mini-pipe-wrap">
        <span class="mp-label">6-job CI · guards every push</span>
        <div class="mini-pipe"><span>config</span><i>→</i><span>k8s manifests</span><i>→</i><span>docs links</span><i>→</i><span>backend</span><i>→</i><span>docker build</span><i>→</i><span>frontend build</span></div>
      </div>
    </div>
  </a>
  <div class="grid g2" style="margin-top:18px">
    {pcard("projects/coldbox-pentesting.html","ColdBox Pentest","DevSecOps","A full penetration-test engagement on a CFML banking app: 9 findings documented and fixed, proven with executed ZAP, Semgrep, Gitleaks, Trivy and TestBox runs.",["OWASP ZAP","Semgrep","Gitleaks","Trivy","TestBox"],"security cicd",delay=80)}
    {pcard("projects/codomax-internship.html","Codomax DevOps","AWS · CI/CD","A GitHub Actions pipeline with OIDC auth really deployed to EC2 over SSM, verified the running code matched the commit, then tore everything down for about $0.03.",["AWS EC2","OIDC","SSM","GitHub Actions","Docker"],"aws cicd",delay=160)}
  </div>
</div></section>

<section id="writing"><div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap">
    <div><p class="eyebrow reveal">writing</p><h2 class="reveal" style="margin:0">Build write-ups</h2></div>
    <a class="btn reveal" href="writing.html">All writing →</a>
  </div>
  <div class="grid g3" style="margin-top:26px">
    {wcard("writing/deploying-to-ec2-with-oidc-and-ssm.html","Deploying to EC2 with OIDC and SSM, and proving it worked","AWS · CI/CD","The codomax capstone: a GitHub Actions pipeline that authenticates without stored keys, deploys over SSM, and verifies the running code matches the commit.")}
    {wcard("writing/coldbox-nine-findings.html","Nine findings in a ColdBox banking app, and how I fixed them","security","A full penetration-test engagement against my own CFML banking app, with every fix proven by executed scans and tests.",delay=80)}
    {wcard("writing/building-an-sre-platform.html","Building an SRE platform: what is real today, what is next","SRE · Kubernetes","AegisSRE, my personal flagship: an honest tour of what phase 2 built and tested, and what is still on the roadmap.",delay=160)}
  </div>
</div></section>

<section id="experience"><div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:end;gap:16px;flex-wrap:wrap">
    <div><p class="eyebrow reveal">experience</p><h2 class="reveal" style="margin:0">Two internships, both on live projects</h2></div>
    <a class="btn reveal" href="about.html#experience">Full timeline →</a>
  </div>
  <div class="wf reveal" data-delay="80" role="img" aria-label="Career timeline styled like a distributed-trace waterfall: B.Tech IT from 2023 to 2027, Adroit Technologies from December 2025 to February 2026, Rapture Twelve from May to October 2026, and three certifications in October 2025.">
    <div class="wf-axis"><span></span><div class="wf-ticks"><span style="left:0%">2023</span><span style="left:20%">2024</span><span style="left:40%">2025</span><span style="left:60%">2026</span><span style="left:80%">2027</span></div></div>
    <div class="wf-rows">
      <div class="wf-row">
        <p class="wf-name">B.Tech IT<small>Meenakshi College of Engineering</small></p>
        <div class="wf-track"><button type="button" class="wf-span c-cyan" style="left:13.3%;width:75%" aria-label="B.Tech IT, 2023 to 2027. Final year now; the base everything else builds on."></button></div>
        <div class="wf-detail"><p>2023 – 2027 · final year now — the base everything else builds on.</p></div>
      </div>
      <div class="wf-row">
        <p class="wf-name">Adroit Technologies<small>Software Deployment Intern</small></p>
        <div class="wf-track"><button type="button" class="wf-span c-amber" style="left:58.3%;width:5%" aria-label="Adroit Technologies, December 2025 to February 2026. Helped optimise payroll-system deployment."></button></div>
        <div class="wf-detail"><p>Dec 2025 – Feb 2026 · helped optimise payroll-system deployment.</p></div>
      </div>
      <div class="wf-row">
        <p class="wf-name">Rapture Twelve<small>DevOps Intern</small></p>
        <div class="wf-track"><button type="button" class="wf-span" style="left:66.7%;width:8.3%" aria-label="Rapture Twelve, May to October 2026. AWS IAM, CI/CD automation and DigiCraveOS; Certificate of Exceptional Contribution."></button></div>
        <div class="wf-detail"><p>May – Oct 2026 · AWS IAM, CI/CD and DigiCraveOS — Certificate of Exceptional Contribution.</p></div>
      </div>
      <div class="wf-row">
        <p class="wf-name">Certifications<small>Oracle ×2 · Forage</small></p>
        <div class="wf-track"><button type="button" class="wf-cert" style="left:55%" aria-label="Certifications, October 2025: OCI Foundations Associate, Oracle Database at AWS Architect Professional, and the AWS Solutions Architecture job simulation."></button></div>
        <div class="wf-detail"><p>Oct 2025 · OCI Foundations, Oracle Database@AWS Architect Pro, AWS job sim (Forage).</p></div>
      </div>
    </div>
  </div>
</div></section>
<section><div class="wrap">
  <p class="eyebrow reveal">certifications</p>
  <h2 class="reveal">Certified, and counting</h2>
  <div class="grid g3" style="margin-top:22px">
    <a class="card cert reveal" href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=3E5A5A8C90DB6F61272E7662EF777663C3316544D516C47E054F2357741AC09A" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">OCI</span><span><b>OCI 2025 Foundations Associate</b><span>Oracle · view badge ↗</span></span></a>
    <a class="card cert reveal" data-delay="80" href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=CA28460C14F975E596709C7D3B622CE567A942B04EF082EF61C6C213894FA234" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">DB</span><span><b>Oracle Database@AWS Certified Architect Professional</b><span>Oracle · view badge ↗</span></span></a>
    <a class="card cert reveal" data-delay="160" href="https://www.linkedin.com/posts/navin-jairam_forage-certificate-activity-7383053776896770048-CnHV" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">AWS</span><span><b>AWS Solutions Architecture Job Simulation</b><span>Forage · view post ↗</span></span></a>
  </div>
</div></section>
{CTA("")}
'''
write("index.html", page("index.html","home","Home",DESC,home))

# ---------------- ABOUT ----------------
about = f'''<section class="page-head"><div class="wrap head-grid">
  <div>
  <p class="crumb">~/about</p>
  <p class="eyebrow">about &amp; experience</p>
  <h1>I make software <span class="grad">ship reliably</span>.</h1>
  <p class="lead">I'm a final-year B.Tech IT student at Meenakshi College of Engineering in Chennai. I've completed two DevOps internships on live projects, and I build projects such as AegisSRE, an SRE platform with a full observability stack. I'm seeking DevOps, SRE, or cloud engineering roles starting in 2027.</p>
  </div>
  <figure class="photo-frame">
    <div class="term-bar" aria-hidden="true"><i></i><i></i><i></i><span>kubectl describe pod navin</span></div>
    <div class="shot"><span class="scan" aria-hidden="true"></span>{photo("")}<span class="tag" aria-hidden="true"><i></i>Running · 1/1</span></div>
    <pre aria-hidden="true"><b>Name:</b>   <em>navin-jairam-m</em>
<b>Role:</b>   <em>DevOps &amp; Cloud Engineer</em>
<b>Node:</b>   <em>chennai</em>
<b>Status:</b>  <em>seeking roles in 2027</em></pre>
    <figcaption class="sr-only">Navin Jairam M, framed as a running Kubernetes pod.</figcaption>
  </figure>
</div></section>

<section style="padding-top:10px"><div class="wrap about-grid">
  <div class="card reveal">
    <h2 class="h3">Quick facts</h2>
    <dl class="kv">
      <dt>based</dt><dd>Chennai, India</dd>
      <dt>studying</dt><dd>B.Tech Information Technology, Meenakshi College of Engineering (2023–2027), CGPA 7.61</dd>
      <dt>stack</dt><dd>AWS, Docker, Kubernetes, GitHub Actions, Ansible, Prometheus, Grafana</dd>
      <dt>looking for</dt><dd>DevOps / SRE / Cloud roles starting in 2027</dd>
      <dt>languages</dt><dd>English (professional), Tamil (native)</dd>
    </dl>
  </div>
  <div class="card reveal" data-delay="100">
    <h2 class="h3">Earlier education</h2>
    <dl class="kv"><dt>higher sec.</dt><dd>68%</dd><dt>secondary</dt><dd>81%</dd></dl>
    <div class="btns" style="margin-top:20px"><a class="btn primary" href="assets/Navin_Jairam_M_Resume.pdf" download>{ICON["dl"]} Download resume</a></div>
  </div>
</div></section>

<section id="experience"><div class="wrap">
  <p class="eyebrow reveal">experience</p>
  <h2 class="reveal">Timeline</h2>
  <div class="timeline" style="margin-top:30px">
    <span class="prog" aria-hidden="true"></span>
    <ol style="list-style:none;margin:0;padding:0">
    <li class="tl-item">
      <span class="tl-node" aria-hidden="true"></span>
      <p class="tl-when">May 2026 – Oct 2026</p>
      <h3>DevOps Intern</h3>
      <p class="tl-org"><a href="https://lnkd.in/p/gB7U-ycr" target="_blank" rel="noopener">Rapture Twelve Pvt. Ltd.</a></p>
      <ul>
        <li>Set up AWS IAM roles and policies to control access for live project environments.</li>
        <li>Designed cloud architectures and deployment strategies for live projects on AWS, built for scalability.</li>
        <li>Automated build and release with CI/CD pipelines and containerised applications for repeatable deployments.</li>
        <li>Contributed to building and deploying <a href="projects/digicrave-os.html">DigiCrave OS</a>, a MERN-stack restaurant POS &amp; operations system.</li>
      </ul>
      <div class="award">{ICON["award"]}<div><b>Certificate of Exceptional Contribution · Sep 2026</b><span>For work across cloud infrastructure, AWS IAM, scalability, containerisation and CI/CD automation. <a href="https://lnkd.in/p/gHc3NYDa" target="_blank" rel="noopener">See the post</a></span></div></div>
    </li>
    <li class="tl-item">
      <span class="tl-node" aria-hidden="true"></span>
      <p class="tl-when">Dec 2025 – Feb 2026</p>
      <h3>Software Deployment Intern</h3>
      <p class="tl-org"><a href="https://lnkd.in/p/gAGeuRe9" target="_blank" rel="noopener">Adroit Technologies Innovative Solutions Pvt. Ltd.</a></p>
      <ul>
        <li>Helped optimise the deployment strategy of a Payroll Management System.</li>
        <li>Introduced DevOps practices into the team's software deployment and operations workflow.</li>
      </ul>
    </li>
    <li class="tl-item">
      <span class="tl-node" aria-hidden="true"></span>
      <p class="tl-when">2023 – 2027</p>
      <h3>B.Tech, Information Technology</h3>
      <p class="tl-org">Meenakshi College of Engineering, Chennai · CGPA 7.61</p>
    </li>
    </ol>
  </div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow reveal">certifications</p>
  <h2 class="reveal">Certified</h2>
  <div class="grid g3" style="margin-top:24px">
    <a class="card cert reveal" href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=3E5A5A8C90DB6F61272E7662EF777663C3316544D516C47E054F2357741AC09A" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">OCI</span><span><b>OCI 2025 Foundations Associate</b><span>Oracle · view badge ↗</span></span></a>
    <a class="card cert reveal" data-delay="80" href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=CA28460C14F975E596709C7D3B622CE567A942B04EF082EF61C6C213894FA234" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">DB</span><span><b>Oracle Database@AWS Certified Architect Professional</b><span>Oracle · view badge ↗</span></span></a>
    <a class="card cert reveal" data-delay="160" href="https://www.linkedin.com/posts/navin-jairam_forage-certificate-activity-7383053776896770048-CnHV" target="_blank" rel="noopener"><span class="ic" aria-hidden="true">AWS</span><span><b>AWS Solutions Architecture Job Simulation</b><span>Forage · view post ↗</span></span></a>
  </div>
</div></section>
{CTA("")}
'''
write("about.html", page("about.html","about","About & Experience","Navin Jairam M's internships at Rapture Twelve and Adroit Technologies, education and certifications.",about))

# ---------------- PROJECTS ----------------
ARCH_SVG_AEGIS = '''<svg class="arch-svg" viewBox="0 0 700 300" role="img" aria-label="AegisSRE architecture: four shop services register with a service registry, a deployments API drives deploys to a Next.js console, and Prometheus with Grafana, Loki and Tempo watch the services.">
<defs><marker id="am-c" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker><marker id="am-g" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah g"/></marker></defs>
<text class="lbl" x="20" y="26">REQUEST FLOW</text>
<rect class="box" x="20" y="42" width="150" height="64" rx="10"/>
<text class="t" x="95" y="68" text-anchor="middle">AegisShop</text>
<text class="s" x="95" y="88" text-anchor="middle">4 services</text>
<line class="ln" x1="172" y1="74" x2="202" y2="74" marker-end="url(#am-c)"/>
<rect class="box" x="205" y="42" width="150" height="64" rx="10"/>
<text class="t" x="280" y="68" text-anchor="middle">Service Registry</text>
<text class="s" x="280" y="88" text-anchor="middle">discovery</text>
<line class="ln" x1="357" y1="74" x2="387" y2="74" marker-end="url(#am-c)"/>
<rect class="box" x="390" y="42" width="150" height="64" rx="10"/>
<text class="t" x="465" y="68" text-anchor="middle">Deployments API</text>
<text class="s" x="465" y="88" text-anchor="middle">FastAPI</text>
<line class="ln" x1="542" y1="74" x2="572" y2="74" marker-end="url(#am-c)"/>
<rect class="box" x="575" y="42" width="105" height="64" rx="10"/>
<text class="t" x="627" y="68" text-anchor="middle">Console</text>
<text class="s" x="627" y="88" text-anchor="middle">Next.js</text>
<text class="lbl" x="20" y="156">OBSERVABILITY</text>
<rect class="box" x="20" y="172" width="150" height="64" rx="10"/>
<text class="t" x="95" y="198" text-anchor="middle">Prometheus</text>
<text class="s" x="95" y="218" text-anchor="middle">metrics + alerts</text>
<line class="ln g" x1="172" y1="204" x2="202" y2="204" marker-end="url(#am-g)"/>
<rect class="box" x="205" y="172" width="230" height="64" rx="10"/>
<text class="t" x="320" y="198" text-anchor="middle">Grafana · Loki · Tempo</text>
<text class="s" x="320" y="218" text-anchor="middle">dashboards · logs · traces</text>
<line class="ln g" x1="150" y1="108" x2="150" y2="168" marker-end="url(#am-g)"/>
</svg>'''

ARCH_SVG_COLDBOX = '''<svg class="arch-svg" viewBox="0 0 700 180" role="img" aria-label="ColdBox pentest flow: the CFML app in vulnerable and hardened builds, scanned by ZAP, Semgrep, Gitleaks and Trivy, nine findings fixed and re-scanned, proven by TestBox suites and a differential matrix.">
<defs><marker id="cm-c" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<text class="lbl" x="15" y="26">ENGAGEMENT FLOW</text>
<rect class="box" x="15" y="52" width="150" height="64" rx="10"/>
<text class="t" x="90" y="78" text-anchor="middle">ColdBox app</text>
<text class="s" x="90" y="98" text-anchor="middle">vuln + hardened builds</text>
<line class="ln" x1="167" y1="84" x2="195" y2="84" marker-end="url(#cm-c)"/>
<rect class="box" x="198" y="52" width="160" height="64" rx="10"/>
<text class="t" x="278" y="78" text-anchor="middle">Scanners</text>
<text class="s" x="278" y="98" text-anchor="middle">ZAP · Semgrep · Trivy</text>
<line class="ln" x1="360" y1="84" x2="388" y2="84" marker-end="url(#cm-c)"/>
<rect class="box" x="391" y="52" width="150" height="64" rx="10"/>
<text class="t" x="466" y="78" text-anchor="middle">9 findings</text>
<text class="s" x="466" y="98" text-anchor="middle">fixed + re-scanned</text>
<line class="ln" x1="543" y1="84" x2="571" y2="84" marker-end="url(#cm-c)"/>
<rect class="box" x="574" y="52" width="111" height="64" rx="10"/>
<text class="t" x="629" y="78" text-anchor="middle">Proof</text>
<text class="s" x="629" y="98" text-anchor="middle">44/44 · 18/18</text>
</svg>'''

ARCH_SVG_CODOMAX = '''<svg class="arch-svg" viewBox="0 0 700 180" role="img" aria-label="Codomax deploy pipeline: a push to main runs GitHub Actions with OIDC auth, deploys to EC2 over SSM with Docker Compose, verifies the running commit, then tears everything down for about three cents.">
<defs><marker id="xm-c" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>
<text class="lbl" x="15" y="26">DEPLOY PIPELINE</text>
<rect class="box" x="15" y="52" width="120" height="64" rx="10"/>
<text class="t" x="75" y="78" text-anchor="middle">git push</text>
<text class="s" x="75" y="98" text-anchor="middle">to main</text>
<line class="ln" x1="137" y1="84" x2="148" y2="84" marker-end="url(#xm-c)"/>
<rect class="box" x="151" y="52" width="120" height="64" rx="10"/>
<text class="t" x="211" y="78" text-anchor="middle">Actions</text>
<text class="s" x="211" y="98" text-anchor="middle">OIDC auth</text>
<line class="ln" x1="273" y1="84" x2="284" y2="84" marker-end="url(#xm-c)"/>
<rect class="box" x="287" y="52" width="120" height="64" rx="10"/>
<text class="t" x="347" y="78" text-anchor="middle">EC2 + SSM</text>
<text class="s" x="347" y="98" text-anchor="middle">compose up</text>
<line class="ln" x1="409" y1="84" x2="420" y2="84" marker-end="url(#xm-c)"/>
<rect class="box" x="423" y="52" width="120" height="64" rx="10"/>
<text class="t" x="483" y="78" text-anchor="middle">verify</text>
<text class="s" x="483" y="98" text-anchor="middle">git_sha match</text>
<line class="ln" x1="545" y1="84" x2="556" y2="84" marker-end="url(#xm-c)"/>
<rect class="box" x="559" y="52" width="120" height="64" rx="10"/>
<text class="t" x="619" y="78" text-anchor="middle">teardown</text>
<text class="s" x="619" y="98" text-anchor="middle">≈ $0.03</text>
</svg>'''

ARCH_MODAL = '''<div class="arch-modal" hidden role="dialog" aria-modal="true" aria-labelledby="arch-title">
  <div class="arch-dialog">
    <div class="arch-head"><h2 id="arch-title" class="arch-title">Architecture</h2><button type="button" class="arch-close" aria-label="Close architecture view">✕</button></div>
    <div data-arch-panel="aegissre" data-title="AegisSRE · architecture" hidden>
      <p class="arch-sub">request flow + observability, simplified · the case study has the full interactive diagram</p>
      ''' + ARCH_SVG_AEGIS + '''
      <p class="arch-more"><a href="projects/aegissre.html">Open the full case study →</a></p>
    </div>
    <div data-arch-panel="coldbox" data-title="ColdBox Pentest · architecture" hidden>
      <p class="arch-sub">assess → harden → prove, simplified · the case study has the full interactive diagram</p>
      ''' + ARCH_SVG_COLDBOX + '''
      <p class="arch-more"><a href="projects/coldbox-pentesting.html">Open the full case study →</a></p>
    </div>
    <div data-arch-panel="codomax" data-title="Codomax DevOps · architecture" hidden>
      <p class="arch-sub">the deploy pipeline, simplified · the case study has the full interactive diagram</p>
      ''' + ARCH_SVG_CODOMAX + '''
      <p class="arch-more"><a href="projects/codomax-internship.html">Open the full case study →</a></p>
    </div>
  </div>
</div>'''

projects = f'''<section class="page-head"><div class="wrap">
  <p class="crumb">~/projects</p>
  <p class="eyebrow">ls -la ~/projects</p>
  <h1>Things I've built and shipped</h1>
  <p class="lead">From an SRE platform and a full penetration-test engagement to a proven AWS deploy pipeline and a restaurant POS. Each case study has an interactive architecture diagram.</p>
</div></section>
<section style="padding-top:6px"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter projects">
    <button type="button" data-filter="all" aria-pressed="true">all</button>
    <button type="button" data-filter="k8s" aria-pressed="false">kubernetes</button>
    <button type="button" data-filter="aws" aria-pressed="false">aws</button>
    <button type="button" data-filter="cicd" aria-pressed="false">ci/cd</button>
    <button type="button" data-filter="security" aria-pressed="false">security</button>
    <button type="button" data-filter="obs" aria-pressed="false">observability</button>
    <button type="button" data-filter="infra" aria-pressed="false">infra</button>
    <button type="button" data-filter="web" aria-pressed="false">full-stack</button>
  </div>
  <p id="filter-status" class="sr-only" aria-live="polite"></p>
  <div class="grid g3">
    {pcard("projects/aegissre.html","AegisSRE","SRE platform · personal flagship · MIT","SRE platform, phase 2 built and tested: a 4-service demo shop watched by a service registry, deployments API and a Next.js console. 6-job CI pipeline, 7 Dockerfiles, Kubernetes manifests for 7 services, terraform, and Prometheus, Grafana, Loki, Tempo and OpenTelemetry. AI incident detection and auto-remediation are next on the roadmap.",["Python","FastAPI","Docker","Kubernetes","Kustomize","Terraform","GitHub Actions","Prometheus","Grafana","Loki","Tempo","OpenTelemetry"],"k8s cicd obs",feature=True,hl="h2",arch="aegissre")}
    {pcard("projects/coldbox-pentesting.html","ColdBox Pentest","DevSecOps","A full penetration-test engagement on a CFML banking app: 9 findings documented and fixed, proven with executed ZAP, Semgrep, Gitleaks, Trivy and cfscan runs, TestBox suites and 7 quality gates.",["OWASP ZAP","Semgrep","Gitleaks","Trivy","TestBox","CFML"],"security cicd",delay=80,hl="h2",arch="coldbox")}
    {pcard("projects/codomax-internship.html","Codomax DevOps Internship","AWS · CI/CD","7 modules capped by a real AWS deploy: GitHub Actions with OIDC auth deployed to EC2 over SSM, verified the running code matched the commit, then tore everything down for about $0.03.",["AWS EC2","OIDC","SSM","GitHub Actions","Docker","CloudWatch"],"aws cicd",hl="h2",arch="codomax")}
    {pcard("projects/dinesmart.html","DineSmart","Full-stack SaaS","Restaurant-operations platform with incident intelligence (product name: Andhrimnir). Next.js 16 + Express 5 + MongoDB; 524/524 backend and 137/137 frontend tests passing, CI green.",["Next.js","React","Express","TypeScript","MongoDB","Playwright"],"web cicd",delay=80,hl="h2")}
    {pcard("projects/ascend.html","Ascend","Desktop app · team lead","Offline Windows fitness RPG: Electron + React with a local FastAPI sidecar and deterministic training and diet engines. 612 + 1,228 tests passing locally.",["Electron","React","FastAPI","Python","SQLite","DVC"],"web",hl="h2")}
    {pcard("projects/portfolio-platform.html","Portfolio Platform","Serverless AWS · previously live","Serverless portfolio on AWS: S3 + CloudFront hosting, API Gateway + Lambda APIs, DynamoDB, Cognito auth and SES email, deployed by a GitHub Actions workflow. A previous version was live; it is not currently live.",["S3","CloudFront","API Gateway","Lambda","DynamoDB","Cognito","SES"],"aws cicd",delay=80,hl="h2")}
    {pcard("projects/digicrave-os.html","DigiCrave OS","MERN stack · Rapture Twelve","Restaurant POS & operations system. I helped build and deploy it during my internship at Rapture Twelve.",["MongoDB","Express","React","Node.js"],"web",hl="h2")}
    {pcard("projects/distributed-java-webapp.html","Distributed Java Web App","Multi-VM infra","A multi-VM Java app environment provisioned with Vagrant: Tomcat, MySQL, Memcached, RabbitMQ and an Nginx load balancer.",["Vagrant","Tomcat","MySQL","Memcached","RabbitMQ","Nginx"],"infra",delay=80,hl="h2")}
    {pcard(R+"Productivity-App","Kaizen – Productivity OS","CI/CD · MLOps","A productivity OS with automated CI/CD releases and basic MLOps workflows.",["CI/CD","MLOps"],"cicd",external=True,delay=160,hl="h2")}
  </div>
</div></section>
{CTA("")}
{ARCH_MODAL}
'''
write("projects.html", page("projects.html","projects","Projects","AegisSRE, a ColdBox penetration test, a proven AWS deploy pipeline, DineSmart, Ascend, a serverless AWS portfolio platform, DigiCrave OS, a distributed Java web app on Vagrant, and Kaizen.",projects))

# ---------------- SKILLS ----------------
POOLS = [
 ("cloud","Cloud","amber",[
   ("aws-iam","AWS IAM",["rapture|Rapture Twelve: set up IAM roles and policies for live environments"]),
   ("aws-ec2","AWS EC2",["codomax|Codomax capstone: deployed to a real EC2 instance"]),
   ("aws-s3","AWS S3",["portfolio|Portfolio Platform: static hosting on S3","codomax|Codomax: module-4 AWS stack"]),
   ("aws-lambda","AWS Lambda",["portfolio|Portfolio Platform: API Gateway + Lambda APIs"]),
   ("aws-cloudwatch","AWS CloudWatch",["codomax|Codomax capstone: container logs and availability metrics"]),
   ("aws-ssm","AWS SSM",["codomax|Codomax capstone: deploy commands to EC2 over Systems Manager"]),
   ("cloudfront","CloudFront",["portfolio|Portfolio Platform: CDN in front of S3"]),
   ("api-gateway","API Gateway",["portfolio|Portfolio Platform: the API front door"]),
   ("dynamodb","DynamoDB",["portfolio|Portfolio Platform: data store"]),
   ("cognito","Cognito",["portfolio|Portfolio Platform: authentication"]),
   ("ses","SES",["portfolio|Portfolio Platform: email"]),
   ("oci","Oracle Cloud (OCI)",["cert|OCI 2025 Foundations Associate","cert|Oracle Database@AWS Certified Architect Professional"]),
 ]),
 ("containers","Containers & Orchestration","cyan",[
   ("docker","Docker",["aegis|AegisSRE: 7 Dockerfiles, 15-container Compose stack","codomax|Codomax: Compose stacks and smoke tests on a real Docker host","rapture|Rapture Twelve: containerised applications"]),
   ("kubernetes","Kubernetes",["aegis|AegisSRE: manifests for 7 services"]),
   ("kustomize","Kustomize",["aegis|AegisSRE: one Kustomize base for all 7 services"]),
 ]),
 ("cicd","CI/CD","green",[
   ("github-actions","GitHub Actions",["aegis|AegisSRE: 6-job CI pipeline","codomax|Codomax capstone: OIDC-authenticated deploy pipeline","dinesmart|DineSmart: unit, Playwright e2e and CodeQL checks","portfolio|Portfolio Platform: deploy workflow"]),
   ("git","Git",["aegis|AegisSRE","coldbox|ColdBox Pentest","codomax|Codomax","dinesmart|DineSmart","ascend|Ascend","portfolio|Portfolio Platform","java|Distributed Java Web App","digicrave|DigiCrave OS","kaizen|Kaizen"]),
   ("oidc","OIDC federation",["codomax|Codomax capstone: keyless AWS auth from GitHub Actions"]),
   ("ci-cd","CI/CD pipelines",["rapture|Rapture Twelve: automated build and release","kaizen|Kaizen: automated CI/CD releases"]),
   ("kubeconform","kubeconform",["aegis|AegisSRE: validates K8s manifests in CI"]),
 ]),
 ("security","Security","red",[
   ("owasp-zap","OWASP ZAP",["coldbox|ColdBox Pentest: baseline + active scan matrix, executed"]),
   ("semgrep","Semgrep",["coldbox|ColdBox Pentest: static analysis"]),
   ("gitleaks","Gitleaks",["coldbox|ColdBox Pentest: secret scanning"]),
   ("trivy","Trivy",["coldbox|ColdBox Pentest: dependency and image scanning"]),
   ("testbox","TestBox",["coldbox|ColdBox Pentest: CFML suites, 31/31 and 44/44"]),
 ]),
 ("iac","IaC & Config","violet",[
   ("terraform","Terraform",["aegis|AegisSRE: cloud infrastructure as code"]),
   ("cloudformation","CloudFormation",["codomax|Codomax: module-4 AWS stack templates, cfn-lint clean"]),
   ("ansible","Ansible",[]),
   ("vagrant","Vagrant",["java|Distributed Java Web App: multi-VM environment"]),
   ("nginx","Nginx",["java|Distributed Java Web App: load balancer"]),
   ("tomcat","Tomcat",["java|Distributed Java Web App: app server"]),
   ("rabbitmq","RabbitMQ",["java|Distributed Java Web App: message queue"]),
   ("memcached","Memcached",["java|Distributed Java Web App: cache"]),
   ("mysql","MySQL",["java|Distributed Java Web App: database"]),
 ]),
 ("observability","Observability","amber",[
   ("prometheus","Prometheus",["aegis|AegisSRE: metrics and alert rules"]),
   ("grafana","Grafana",["aegis|AegisSRE: dashboards"]),
   ("loki","Loki",["aegis|AegisSRE: logs"]),
   ("tempo","Tempo",["aegis|AegisSRE: traces"]),
   ("opentelemetry","OpenTelemetry",["aegis|AegisSRE: instrumentation"]),
 ]),
 ("languages","Languages & OS","cyan",[
   ("python","Python",["aegis|AegisSRE: services, checked with mypy and pytest","ascend|Ascend: FastAPI sidecar engine"]),
   ("typescript","TypeScript",["dinesmart|DineSmart: backend and frontend","kaizen|Kaizen"]),
   ("fastapi","FastAPI",["aegis|AegisSRE: registry and deployments services","ascend|Ascend: sidecar engine"]),
   ("electron","Electron",["ascend|Ascend: Windows desktop app shell"]),
   ("cfml","CFML",["coldbox|ColdBox Pentest: banking app target"]),
   ("bash","Bash",["codomax|Codomax: scripting and smoke tests"]),
   ("linux","Linux",["codomax|Codomax: server administration and cron"]),
   ("mern","MERN stack",["digicrave|DigiCrave OS: MongoDB, Express, React, Node.js"]),
 ]),
]
pool_html = ""
total = 0
for pid, pname, color, skl in POOLS:
    pods = ""
    for sid, sname, used in skl:
        total += 1
        keys = " ".join(sorted(set(u.split("|")[0] for u in used)))
        texts = "|".join(u.split("|", 1)[1] for u in used)
        pods += f'<button type="button" class="pod" aria-pressed="false" data-id="{sid}" data-name="{html.escape(sname)}" data-keys="{keys}" data-used="{html.escape(texts)}">{html.escape(sname)}</button>'
    pool_html += f'<section class="pool" style="--c:var(--{color})" data-pool="{pid}" aria-label="{html.escape(pname)} node pool"><header><h2>{html.escape(pname)}</h2><span>{len(skl)} pods</span></header><div class="pods">{pods}</div></section>'
usage_btns = '<button type="button" data-key="all" aria-pressed="true">everything</button>' + "".join(f'<button type="button" data-key="{k}" aria-pressed="false">{html.escape(v)}</button>' for k, v in [("aegis","AegisSRE"),("coldbox","ColdBox Pentest"),("codomax","Codomax"),("dinesmart","DineSmart"),("ascend","Ascend"),("portfolio","Portfolio Platform"),("java","Java Web App"),("digicrave","DigiCrave OS"),("rapture","Rapture Twelve"),("cert","Certifications")])
skills = f'''<section class="page-head"><div class="wrap">
  <p class="crumb">~/skills</p>
  <p class="eyebrow">kubectl get nodes</p>
  <h1>My stack, as a cluster</h1>
  <p class="lead">Each node pool is one area of my stack, and each pod is a tool. No made-up skill percentages: tap a pod to see exactly where I've used it, or filter by project.</p>
</div></section>
<section style="padding-top:6px"><div class="wrap">
  <p class="lane-label">show pods used in</p>
  <div class="usage" id="usage" role="group" aria-label="Filter skills by where they are used">{usage_btns}</div>
  <div class="cluster" id="cluster" style="margin-top:16px">{pool_html}</div>
  <div class="inspect" aria-live="polite">
    <div class="term-bar" aria-hidden="true"><i></i><i></i><i></i><span>kubectl — inspector</span></div>
    <div class="term-body" id="inspect-out"><span class="ps">$</span> kubectl get pods --all-namespaces
<span class="o">{total} pods across 7 node pools. Tap a pod to describe it.</span></div>
  </div>
</div></section>
{CTA("")}
'''
write("skills.html", page("skills.html","skills","Skills","Navin Jairam M's stack grouped by Cloud, Containers, CI/CD, Security, IaC, Observability and Languages, with where each tool was used.",skills))

# ---------------- CONTACT ----------------
contact = f'''<section class="page-head"><div class="wrap">
  <p class="crumb">~/contact</p>
  <p class="eyebrow">ssh navin@inbox</p>
  <h1>Let's <span class="grad">talk</span>.</h1>
  <p class="lead">I'm graduating in 2027 and seeking DevOps, SRE, or cloud roles. Email is the fastest way to reach me.</p>
</div></section>
<section style="padding-top:6px"><div class="wrap">
  <div class="card email-box reveal">
    <code>{EMAIL}</code>
    <div class="btns">
      <button class="btn" type="button" data-copy="{EMAIL}">{ICON["copy"]} <span class="lbl">Copy email</span></button>
      <a class="btn primary" href="mailto:{EMAIL}">{ICON["mail"]} Write to me</a>
    </div>
  </div>
  <div class="contact-grid" style="margin-top:16px">
    <a class="card ccard tilt reveal" href="{LI}" target="_blank" rel="noopener"><span class="ic">{ICON["li"]}</span><span><b>LinkedIn</b><span>linkedin.com/in/navin-jairam</span></span></a>
    <a class="card ccard tilt reveal" data-delay="80" href="{GH}" target="_blank" rel="noopener"><span class="ic">{ICON["gh"]}</span><span><b>GitHub</b><span>github.com/Lucifer-Newstar</span></span></a>
    <a class="card ccard tilt reveal" href="assets/Navin_Jairam_M_Resume.pdf" download><span class="ic">{ICON["dl"]}</span><span><b>Resume (PDF)</b><span>One page, A4</span></span></a>
    <button class="card ccard tilt reveal" data-delay="80" type="button" data-palette style="text-align:left;font:inherit;cursor:pointer"><span class="ic">{ICON["term"]}</span><span><b>Prefer a terminal?</b><span>Open the shell and try sudo hire navin</span></span></button>
  </div>
</div></section>
'''
write("contact.html", page("contact.html","contact","Contact","Email, LinkedIn and GitHub for Navin Jairam M, DevOps & Cloud Engineer.",contact))

# ---------------- AEGISSRE ----------------
STAGES = [("config","YAML + compose valid","M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8zM14 3v5h5M9 13h6M9 17h4"),("k8s manifests","kubeconform + kustomize","M12 2 3 7v10l9 5 9-5V7z"),("docs links","every docs link resolves","M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1"),("backend","ruff · mypy · pytest","M8 4 4 12l4 8M16 4l4 8-4 8"),("docker build","container images","M3 9h18v10H3zM7 9V5h4v4M13 9V5h4v4"),("frontend build","console production build","M3 4h18v12H3zM8 20h8M12 16v4")]
st_html = ""
for name, sub, d in STAGES:
    st_html += f'<li class="stage"><span class="st-ic" aria-hidden="true"><svg class="base" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg><svg class="chk" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5 9-10"/></svg></span><span class="st-txt"><span class="st-name">{name}</span><span class="st-sub">{sub} · <span class="st-state">queued</span></span></span></li>'
SVCS = [("registry-service","platform"),("deployments-service","platform"),("console","platform · frontend"),("catalog-service","aegisshop demo"),("cart-service","aegisshop demo"),("order-service","aegisshop demo"),("payment-service","aegisshop demo")]
svc_html = "".join(f'<div class="svc{" demo" if "demo" in g else ""}">{n}<small>{g}</small></div>' for n, g in SVCS)
obs = diagram("AegisSRE observability flow",
  lane("metrics", [("6 services","OpenTelemetry instrumented","The six Python services (registry, deployments and the four AegisShop services) are instrumented with OpenTelemetry, so metrics, logs and traces come from the same code. The console isn't instrumented."),("Prometheus","metrics + alert rules","Prometheus holds the services' metrics and evaluates alert rules, so problems raise an alert instead of hiding."),("Grafana","dashboards","Grafana dashboards bring metrics, logs and traces into one place.")], "red") +
  lane("logs", [("6 services","logs","The same six services send their logs."),("Loki","log aggregation","Loki stores and indexes the logs so they can be searched from Grafana."),("Grafana","explore logs","Logs show up beside the metrics in Grafana.")], "amber") +
  lane("traces", [("6 services","OpenTelemetry spans","OpenTelemetry records spans for the requests each service handles."),("Tempo","trace storage","Tempo stores each service's traces, so a slow request can be looked up and inspected."),("Grafana","trace view","Traces open in Grafana next to the logs and metrics for the same moment.")], "violet"))
aegis_body = detail_head("../","case study · SRE platform · personal flagship · MIT licensed","AegisSRE",
  "My personal flagship: an SRE platform (platform codename: AegisDeploy). Phase 2 is built and tested: AegisShop, a 4-service demo shop, watched by a service registry, a deployments API and a live Next.js console, with Prometheus, Grafana, Loki, Tempo and OpenTelemetry. A 6-job CI pipeline guards every push, and all 54 backend tests pass. AI anomaly detection, root-cause analysis and automated remediation are designed and next on the roadmap.",
  ["Python","FastAPI","Docker","Kubernetes","Kustomize","Terraform","GitHub Actions","Prometheus","Grafana","Loki","Tempo","OpenTelemetry"],
  [gh_btn("AegisSRE")]) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid g3">
  <div class="card reveal"><div class="stat">6<small>CI jobs on GitHub Actions</small></div></div>
  <div class="card reveal" data-delay="80"><div class="stat">7<small>Dockerfiles</small></div></div>
  <div class="card reveal" data-delay="160"><div class="stat">7<small>Kubernetes services, one Kustomize base</small></div></div>
</div></div></section>

<section><div class="wrap">
  <p class="eyebrow reveal">status</p>
  <h2 class="reveal">What's built, and what's next</h2>
  <div class="split" style="margin-top:20px">
    <div class="card reveal"><h3>Built and tested today (phase 2)</h3><ul class="list-check"><li>AegisShop demo: catalog, cart, order and payment services</li><li>Service registry, deployments API and a live Next.js console</li><li>7 Dockerfiles, a 15-container Docker Compose stack, and Kubernetes manifests for 7 services with Kustomize</li><li>Terraform for the cloud infrastructure</li><li>A 6-job GitHub Actions CI pipeline; 54/54 backend tests pass</li><li>Prometheus, Grafana, Loki, Tempo and OpenTelemetry across the 6 Python services</li></ul></div>
    <div class="card reveal" data-delay="80"><h3>On the roadmap</h3><ul class="list-check planned"><li>AI anomaly detection and root-cause analysis</li><li>Automated remediation, with a human approving risky actions</li><li>A chaos lab to test it</li></ul><p class="muted" style="margin-top:14px">One name note: the repo is AegisSRE, while the README, code and containers use the platform's codename, AegisDeploy. Same project.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow reveal">.github/workflows/ci.yml</p>
  <h2 class="reveal">The CI pipeline</h2>
  <p class="muted reveal" style="max-width:66ch">Every push and pull request to main runs six CI jobs, and all of them must pass before a merge: YAML and compose validation, Kubernetes manifests (kubeconform + kustomize), a docs link check, the backend (ruff, mypy, pytest), Docker image builds and the frontend build. This animation walks through them. It's an illustration, not live build status.</p>
  <div class="pipe-wrap reveal" id="pipe" data-state="idle" style="margin-top:22px">
    <div class="pipe-head"><span class="run-state"><i aria-hidden="true"></i> CI · main · <span class="run-txt">queued</span></span><button class="btn" type="button" data-run style="padding:8px 14px;font-size:14px">↻ Run pipeline</button></div>
    <ol class="pipeline" aria-label="CI jobs">{st_html}</ol>
    <div class="pipe-log" role="log" aria-label="Pipeline log"></div>
  </div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow reveal">infra/k8s/base</p>
  <h2 class="reveal">7 services on Kubernetes</h2>
  <p class="muted reveal" style="max-width:66ch">Each service has its own Deployment and Service manifest, assembled by one Kustomize base and validated with kubeconform in CI. Three make up the platform; four make up AegisShop, a demo shop for the platform to watch.</p>
  <div class="k8s reveal" style="margin-top:20px">
    <div class="k8s-top"><span>⎈ kustomize build infra/k8s/base</span><span>■ platform  <span style="color:var(--violet)">■</span> demo app</span></div>
    <div class="svcs">{svc_html}</div>
  </div>
</div></section>

<section><div class="wrap">
  <p class="eyebrow reveal">observability</p>
  <h2 class="reveal">Metrics, logs and traces</h2>
  <p class="muted reveal" style="max-width:66ch">OpenTelemetry instruments the six Python services, Prometheus, Loki and Tempo each take one signal, and Grafana puts it all on one screen.</p>
  <div style="margin-top:20px">{obs}</div>
</div></section>
''' + next_nav("../",("projects/distributed-java-webapp.html","Distributed Java Web App"),("projects/coldbox-pentesting.html","ColdBox Pentest")) + CTA("../")
write("projects/aegissre.html", page("projects/aegissre.html","projects","AegisSRE","AegisSRE, an SRE platform with phase 2 built and tested: a demo shop watched by a service registry, deployments API and Next.js console, a 6-job CI pipeline, 7 Kubernetes services and Prometheus, Grafana, Loki, Tempo and OpenTelemetry.",aegis_body,root="../"))

# ---------------- COLDBOX PENTEST ----------------
cb = diagram("ColdBox pentest engagement",
  lane("assess", [("CFML banking app","ColdBox target","Two builds of the same ColdBox (CFML) banking app: one deliberately vulnerable, one hardened to fix every finding."),("OWASP ZAP","baseline + active scans","ZAP ran a real baseline and active scan matrix against the app, not a demo config."),("9 findings","documented","Nine vulnerabilities documented with evidence, including SQL injection, cross-site scripting and session fixation.")], "red") +
  lane("harden", [("fixes","hardened build","Each finding got a fix in the hardened build of the app."),("Semgrep + Gitleaks","code + secrets","Semgrep scans the code for vulnerable patterns; Gitleaks hunts for committed secrets."),("Trivy + cfscan","deps + CFML","Trivy checks dependencies and images; cfscan checks the CFML code itself.")], "amber") +
  lane("prove", [("TestBox","31/31 + 44/44","TestBox suites pass on the vulnerable baseline (31/31) and the hardened build (44/44)."),("differential matrix","18/18","An 18-case differential matrix proves behaviour changed exactly where the fixes intended."),("gates G1–G7","PASS","Seven quality gates, all passing, backed by 14 evidence screenshots in the repo.")], "green"))
cb_body = detail_head("../","case study · DevSecOps · penetration test","ColdBox Pentest",
  "A full penetration-test engagement on a ColdBox (CFML) banking app: a vulnerable build and a hardened build, nine findings documented with evidence, and every fix proven with executed scanners and test suites, not claimed.",
  ["OWASP ZAP","Semgrep","Gitleaks","Trivy","cfscan","TestBox","CFML","Docker"],
  [gh_btn("ColdBox-Pentesting")]) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid g3">
  <div class="card reveal"><div class="stat">9<small>findings documented and fixed</small></div></div>
  <div class="card reveal" data-delay="80"><div class="stat">G1–G7<small>quality gates, all PASS</small></div></div>
  <div class="card reveal" data-delay="160"><div class="stat">14<small>evidence screenshots in the repo</small></div></div>
</div></div></section>
<section><div class="wrap">
  <p class="eyebrow reveal">method</p>
  <h2 class="reveal">Assess, harden, prove</h2>
  <div style="margin-top:20px">{cb}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>The engagement</h3><ul class="list-check"><li>Two builds of the same CFML banking app: deliberately vulnerable, and hardened</li><li>Nine findings, each written up with evidence and a fix</li><li>OWASP ZAP baseline and active scan matrix actually executed</li><li>Semgrep, Gitleaks, Trivy and cfscan all run, with output captured</li></ul></div>
  <div class="card reveal" data-delay="80"><h3>Proof, not promises</h3><ul class="list-check"><li>TestBox: 31/31 on the vulnerable baseline, 44/44 on the hardened build</li><li>Differential matrix: 18/18 cases behave exactly as intended</li><li>Seven quality gates (G1–G7) all pass</li><li>14 evidence screenshots committed alongside the reports</li></ul></div>
</div></section>
''' + next_nav("../",("projects/aegissre.html","AegisSRE"),("projects/codomax-internship.html","Codomax DevOps Internship")) + CTA("../")
write("projects/coldbox-pentesting.html", page("projects/coldbox-pentesting.html","projects","ColdBox Pentest","A DevSecOps penetration test of a ColdBox CFML banking app: 9 findings documented and fixed, ZAP, Semgrep, Gitleaks, Trivy and cfscan executed, TestBox 31/31 and 44/44, differential 18/18, gates G1-G7 PASS.",cb_body,root="../"))

# ---------------- CODOMAX ----------------
cx = diagram("codomax capstone deploy pipeline",
  lane("pipeline", [("git push","main","A push to main starts the deploy workflow."),("GitHub Actions","OIDC auth","The workflow authenticates to AWS with OIDC federation: no long-lived AWS keys stored anywhere."),("EC2 + SSM","real deploy","Deploy commands reach a real EC2 instance over AWS Systems Manager and bring the stack up with Docker Compose.")], "cyan") +
  lane("proof", [("verify step","git_sha match","A verification step checks the running containers match the pushed commit, so a green run means the deploy really happened."),("CloudWatch","logs + metrics","Container logs and a healthcheck-driven availability metric land in CloudWatch."),("teardown","about $0.03 total","After the proof, the whole stack was torn down: stack deleted, IAM key removed, nothing left running.")], "green"))
cx_body = detail_head("../","case study · DevOps internship · AWS","Codomax DevOps Internship",
  "Seven modules of DevOps work, ending in a capstone that really deploys: a GitHub Actions pipeline authenticates to AWS with OIDC, deploys to EC2 over SSM, verifies the running code matches the commit, then tears everything down. 43 evidence screenshots document the runs.",
  ["AWS EC2","OIDC","SSM","GitHub Actions","Docker","CloudWatch","CloudFormation","pytest"],
  [gh_btn("codomax-internship")]) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid g3">
  <div class="card reveal"><div class="stat">7<small>modules, from Linux to a capstone deploy</small></div></div>
  <div class="card reveal" data-delay="80"><div class="stat">43<small>evidence screenshots in the repo</small></div></div>
  <div class="card reveal" data-delay="160"><div class="stat">$0.03<small>total AWS cost after full teardown</small></div></div>
</div></div></section>
<section><div class="wrap">
  <p class="eyebrow reveal">capstone</p>
  <h2 class="reveal">A pipeline that deploys for real</h2>
  <p class="muted reveal" style="max-width:66ch">Earlier pipeline runs silently skipped the deploy step. The final pipeline doesn't: it deploys to EC2 and proves the running code matches the commit. That's the difference between CI that exists and CI that works.</p>
  <div class="diff reveal" data-delay="80" role="img" aria-label="Before: earlier runs silently skipped the deploy step and nothing proved the running code matched the commit. After: OIDC-authenticated deploys over SSM with a verified git SHA match, torn down to about three cents.">
    <p class="d-h">git diff capstone</p>
    <p class="d-l del"><span class="d-s" aria-hidden="true">-</span><span>deploy step silently skipped on earlier runs</span></p>
    <p class="d-l del"><span class="d-s" aria-hidden="true">-</span><span>no proof the running code matched the commit</span></p>
    <p class="d-l add"><span class="d-s" aria-hidden="true">+</span><span>OIDC auth, zero stored keys, real deploy over SSM</span></p>
    <p class="d-l add"><span class="d-s" aria-hidden="true">+</span><span>git_sha match verified, then full teardown ≈ $0.03</span></p>
  </div>
  <div style="margin-top:20px">{cx}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>The seven modules</h3><ul class="list-check"><li>Linux, Git and shell scripting fundamentals</li><li>Docker: images, Compose stacks and smoke tests on a real Docker host</li><li>CI/CD with GitHub Actions</li><li>AWS infrastructure: EC2, RDS, S3 and CloudFormation templates, checked with cfn-lint</li><li>Monitoring with CloudWatch logs and metrics</li><li>A capstone that ties them together</li></ul></div>
  <div class="card reveal" data-delay="80"><h3>Bugs found by running it for real</h3><ul class="list-check"><li>A healthcheck that failed under cron (PATH) and probed the wrong routes</li><li>All container logs landing in one literal log stream</li><li>An OIDC trust policy that was referenced but never committed, then broke on GitHub's new token format</li></ul><p class="muted" style="margin-top:14px">Each was diagnosed from real evidence (CloudTrail, logs) and fixed; every test suite in the repo was executed, none skipped.</p></div>
</div></section>
''' + next_nav("../",("projects/coldbox-pentesting.html","ColdBox Pentest"),("projects/dinesmart.html","DineSmart")) + CTA("../")
write("projects/codomax-internship.html", page("projects/codomax-internship.html","projects","Codomax DevOps Internship","A 7-module DevOps internship with a real AWS capstone: OIDC-authenticated GitHub Actions deploys to EC2 over SSM, verified against the commit, then torn down. 43 evidence screenshots.",cx_body,root="../"))

# ---------------- DINESMART ----------------
dm = diagram("DineSmart architecture",
  lane("app", [("Restaurant staff","browser","Restaurant teams use DineSmart to run operations and track incidents."),("Next.js 16","React 19 frontend","The frontend is a Next.js 16 app on React 19."),("Express 5","TypeScript API","The backend is an Express 5 API written in TypeScript."),("MongoDB","database","MongoDB stores the platform's data.")], "green") +
  lane("quality", [("524 tests","backend","The backend suite passes 524 of 524 tests."),("137 tests","frontend","The frontend suite passes 137 of 137 tests."),("CI green","tests · e2e · CodeQL","GitHub CI runs the unit suites, 21 Playwright end-to-end specs with a real MongoDB service, and CodeQL, all green.")], "cyan"))
dm_body = detail_head("../","case study · full-stack SaaS","DineSmart",
  "A SaaS platform for restaurant operations with incident intelligence at its core (product name: Andhrimnir). Next.js 16 + React 19 frontend, Express 5 + TypeScript backend, MongoDB. Implemented and tested locally and in CI; the first cloud deploy is next.",
  ["Next.js","React","Express","TypeScript","MongoDB","Playwright","Docker"],
  [gh_btn("DineSmart")]) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid g3">
  <div class="card reveal"><div class="stat">524/524<small>backend tests passing</small></div></div>
  <div class="card reveal" data-delay="80"><div class="stat">137/137<small>frontend tests passing</small></div></div>
  <div class="card reveal" data-delay="160"><div class="stat">3<small>CI checks green: unit, Playwright e2e, CodeQL</small></div></div>
</div></div></section>
<section><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">How it fits together</h2>
  <div style="margin-top:20px">{dm}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>What it does</h3><p class="muted">DineSmart helps restaurant teams stay on top of operations: menu, bookings and a dashboard, with incident intelligence to spot and triage problems. AI-assisted features are implemented and being verified against live services.</p></div>
  <div class="card reveal" data-delay="80"><h3>Where it stands</h3><p class="muted">Every suite passes locally and GitHub CI is green, including 21 Playwright end-to-end specs that run against a real MongoDB service in CI. Deployment comes next: a deployment checklist already exists in the repo.</p></div>
</div></section>
''' + next_nav("../",("projects/codomax-internship.html","Codomax DevOps Internship"),("projects/ascend.html","Ascend")) + CTA("../")
write("projects/dinesmart.html", page("projects/dinesmart.html","projects","DineSmart","DineSmart (Andhrimnir), a restaurant-operations SaaS with incident intelligence: Next.js 16, Express 5, MongoDB; 524/524 backend and 137/137 frontend tests passing, CI green.",dm_body,root="../"))

# ---------------- ASCEND ----------------
asc = diagram("Ascend architecture",
  lane("desktop", [("Electron + React","Windows app","An offline-first Windows desktop app: a fitness RPG where training and diet drive character progression."),("FastAPI sidecar","local engine","A FastAPI sidecar with SQLite runs the deterministic training and diet engines."),("MLOps","DVC pipeline","An MLOps pipeline managed with DVC versions the data and models.")], "violet") +
  lane("quality", [("612 tests","passing locally","The desktop-side suite passes 612 of 612 tests locally."),("1,228 tests","passing locally","The engine-side suite passes 1,228 of 1,228 tests locally."),("CI","repair in progress","GitHub CI is mid-repair: three small environment breaks, with the suites themselves green locally.")], "amber"))
asc_body = detail_head("../","case study · desktop app · team lead","Ascend",
  "An offline Windows desktop fitness RPG: an Electron + React app driven by a local FastAPI sidecar with deterministic training and diet engines, plus a DVC-managed MLOps pipeline. A team project that I lead.",
  ["Electron","React","FastAPI","Python","SQLite","DVC"],
  [gh_btn("Ascend")]) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid g3">
  <div class="card reveal"><div class="stat">612/612<small>desktop-side tests passing locally</small></div></div>
  <div class="card reveal" data-delay="80"><div class="stat">1,228/1,228<small>engine-side tests passing locally</small></div></div>
  <div class="card reveal" data-delay="160"><div class="stat">offline<small>no account, no server, all local data</small></div></div>
</div></div></section>
<section><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">A desktop app with a real engine</h2>
  <div style="margin-top:20px">{asc}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>What it does</h3><p class="muted">Ascend turns fitness into an RPG: training and diet choices drive character progression, computed by deterministic engines so results are explainable and reproducible. Everything runs offline on Windows.</p></div>
  <div class="card reveal" data-delay="80"><h3>Where it stands</h3><p class="muted">Both suites are green locally (612 + 1,228 tests). GitHub CI is being repaired: a missing system package in the ML workflow, a test that assumes a path depth, and a Windows file-lock in a fixture. Small, known breaks with fixes in flight.</p></div>
</div></section>
''' + next_nav("../",("projects/dinesmart.html","DineSmart"),("projects/portfolio-platform.html","Portfolio Platform")) + CTA("../")
write("projects/ascend.html", page("projects/ascend.html","projects","Ascend","Ascend, an offline Windows fitness RPG: Electron + React with a FastAPI sidecar and deterministic engines; 612 + 1,228 tests passing locally.",asc_body,root="../"))

# ---------------- PORTFOLIO PLATFORM ----------------
pp = diagram("Portfolio Platform architecture",
  lane("static site", [("Visitor","browser","A visitor opens the site in their browser."),("CloudFront","CDN","CloudFront serves the site from the edge and caches it."),("S3","static files","The site's files live in an S3 bucket behind CloudFront.")], "cyan") +
  lane("api", [("Frontend","API calls","The site calls its own API for anything dynamic."),("API Gateway","HTTP API","API Gateway is the API's front door and routes each request to a function."),("Lambda","serverless functions","Lambda functions run the API's logic with no servers to manage."),[("DynamoDB","data","DynamoDB stores the platform's data."),("SES","email","SES sends the platform's email.")]], "green") +
  lane("auth", [("User","sign in","A user signs in."),("Cognito","authentication","Cognito handles sign-in and tokens for the platform."),("API Gateway","authorised calls","Signed-in requests reach the API.")], "violet") +
  lane("delivery", [("git push","main","A push to the repo starts a deploy."),("GitHub Actions","deploy workflow","A GitHub Actions workflow automates the deployment to AWS."),("AWS","new version live","The new version goes out.")], "amber"))
pp_body = detail_head("../","case study · serverless AWS","Portfolio Platform",
  "A serverless portfolio platform on AWS: S3 + CloudFront hosting, API Gateway + Lambda APIs, DynamoDB, Cognito auth and SES email, with deployment automated by GitHub Actions. A previous version was live; it is not currently live, and the repo is private as it contains AWS secrets.",
  ["S3","CloudFront","API Gateway","Lambda","DynamoDB","Cognito","SES","GitHub Actions"],[src_btn(PP_SRC)]) + f'''
<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">How it fits together</h2>
  <div style="margin-top:20px">{pp}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>What I built</h3><ul class="list-check"><li>Static hosting on S3 behind CloudFront</li><li>APIs on API Gateway + Lambda</li><li>DynamoDB for data, Cognito for auth, SES for email</li><li>Automated deployment with a GitHub Actions workflow</li></ul></div>
  <div class="card reveal" data-delay="80"><h3>Why serverless</h3><p class="muted">No servers to patch or keep running: each piece is a managed AWS service, and the whole thing deploys from a git push.</p></div>
</div></section>
''' + next_nav("../",("projects/ascend.html","Ascend"),("projects/digicrave-os.html","DigiCrave OS")) + CTA("../")
write("projects/portfolio-platform.html", page("projects/portfolio-platform.html","projects","Portfolio Platform","A serverless AWS platform: S3, CloudFront, API Gateway, Lambda, DynamoDB, Cognito and SES, deployed with GitHub Actions.",pp_body,root="../"))

# ---------------- DIGICRAVE ----------------
dc = diagram("DigiCrave OS architecture",
  lane("request path", [("Restaurant staff","browser","Staff use DigiCrave OS in the browser for point of sale and day-to-day restaurant operations."),("React","frontend","The React frontend of the POS."),("Express + Node.js","API","The Express API on Node.js handles the POS and operations logic."),("MongoDB","database","MongoDB stores the restaurant's data.")], "green"))
dc_body = detail_head("../","case study · MERN stack · Rapture Twelve","DigiCrave OS",
  "A MERN-stack restaurant POS and operations system. I contributed to building and deploying it during my DevOps internship at Rapture Twelve.",
  ["MongoDB","Express","React","Node.js"],
  [gh_btn("DigiCraveOS")]) + f'''
<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">The MERN stack, end to end</h2>
  <div style="margin-top:20px">{dc}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>My part</h3><p class="muted">I contributed to building and deploying it at Rapture Twelve, as part of the work that earned my Certificate of Exceptional Contribution (Sep 2026).</p></div>
</div></section>
''' + next_nav("../",("projects/portfolio-platform.html","Portfolio Platform"),("projects/distributed-java-webapp.html","Distributed Java Web App")) + CTA("../")
write("projects/digicrave-os.html", page("projects/digicrave-os.html","projects","DigiCrave OS","DigiCrave OS: a MERN-stack restaurant POS and operations system Navin helped build and deploy at Rapture Twelve.",dc_body,root="../"))

# ---------------- JAVA ----------------
jv = diagram("Distributed Java web app architecture",
  lane("vagrant up → multi-VM stack", [("User","HTTP","A user opens the app."),("Nginx","load balancer","Nginx sits in front and load-balances traffic to the app server."),("Tomcat","Java app server","Tomcat runs the Java web app."),[("Memcached","cache","Memcached caches data so the database isn't hit for every request."),("RabbitMQ","message queue","RabbitMQ queues messages for the app."),("MySQL","database","MySQL is the app's database.")]], "violet"))
jv_body = detail_head("../","case study · multi-VM infrastructure","Distributed Java Web App",
  "A multi-VM Java app environment provisioned with Vagrant: Tomcat, MySQL, Memcached, RabbitMQ and an Nginx load balancer.",
  ["Vagrant","Nginx","Tomcat","MySQL","Memcached","RabbitMQ"],[gh_btn("distributed-java-webapp")]) + f'''
<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">One command, a whole stack</h2>
  <div style="margin-top:20px">{jv}</div>
</div></section>
''' + next_nav("../",("projects/digicrave-os.html","DigiCrave OS"),("projects/aegissre.html","AegisSRE")) + CTA("../")
write("projects/distributed-java-webapp.html", page("projects/distributed-java-webapp.html","projects","Distributed Java Web App","A multi-VM Java app environment provisioned with Vagrant: Nginx, Tomcat, MySQL, Memcached and RabbitMQ.",jv_body,root="../"))

# ---------------- 404 ----------------
nf_root = BASE_PATH  # absolute, e.g. /Portfolio/: GitHub Pages serves 404.html at any depth
nf = f'''<section class="page-head"><div class="wrap">
  <p class="eyebrow">exit code 404</p>
  <h1>Pod not found.</h1>
  <p class="lead">That page doesn't exist. Head home, or open the terminal and type <b>help</b>.</p>
  <div class="btns"><a class="btn primary" href="{nf_root}index.html">Back home</a><button class="btn" type="button" data-palette>Open terminal</button></div>
</div></section>'''
write("404.html", page("404.html","none","Not found","Page not found.",nf,root=nf_root,noindex=True))

# ---------------- WRITING ----------------
def post_head(slug, tag, title, standfirst, repo_btn):
    return f'''<section class="page-head"><div class="wrap">
  <p class="crumb"><a href="../writing.html">~/writing</a> / {html.escape(slug)}</p>
  <p class="eyebrow">write-up · {html.escape(tag)}</p>
  <h1>{html.escape(title)}</h1>
  <p class="lead">{standfirst}</p>
  <div class="btns">{repo_btn}</div>
</div></section>'''

writing = f'''<section class="page-head"><div class="wrap">
  <p class="crumb">~/writing</p>
  <p class="eyebrow">ls -la ~/writing</p>
  <h1>Build write-ups</h1>
  <p class="lead">Short posts on how the projects actually work: the pipeline that really deploys, the pentest that proves its fixes, and the SRE platform I build in the open. Everything here matches what is in the repos.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="grid g3">
    {wcard("writing/deploying-to-ec2-with-oidc-and-ssm.html","Deploying to EC2 with OIDC and SSM, and proving it worked","AWS · CI/CD","The codomax capstone: a GitHub Actions pipeline that authenticates without stored keys, deploys over SSM, and verifies the running code matches the commit.")}
    {wcard("writing/coldbox-nine-findings.html","Nine findings in a ColdBox banking app, and how I fixed them","security","A full penetration-test engagement against my own CFML banking app, with every fix proven by executed scans and tests.",delay=80)}
    {wcard("writing/building-an-sre-platform.html","Building an SRE platform: what is real today, what is next","SRE · Kubernetes","AegisSRE, my personal flagship: an honest tour of what phase 2 built and tested, and what is still on the roadmap.",delay=160)}
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow reveal">elsewhere · LinkedIn</p>
  <h2 class="reveal">Build posts on LinkedIn</h2>
  <div class="grid g3" style="margin-top:22px">
    {wcard("https://www.linkedin.com/feed/update/urn:li:activity:7529778282771443713/","From finding vulnerabilities to fixing them","LinkedIn · Nov 2026 · security","The post behind the ColdBox write-up: what the pentest covered, the validation numbers, and what a first SecOps project actually taught me.",badge="linkedin",cta="Read on LinkedIn",external=True)}
    {wcard("https://www.linkedin.com/feed/update/urn:li:activity/7529779038500872192/","Six modules, one real deploy: Codomax","LinkedIn · Nov 2026 · AWS · CI/CD","The internship completion post: Linux and networking to servers, AWS, Docker, and a capstone pipeline that deploys for real.",delay=80,badge="linkedin",cta="Read on LinkedIn",external=True)}
    {wcard("https://www.linkedin.com/feed/update/urn:li:activity:7522983178719125504/","Six months of DevOps at Rapture Twelve","LinkedIn · Nov 2026 · internship","The wrap-up post: AWS IAM and least-privilege, cloud architecture exposure, containerised deployments, and building DigiCraveOS.",delay=160,badge="linkedin",cta="Read on LinkedIn",external=True)}
  </div>
</div></section>
''' + CTA("")
write("writing.html", page("writing.html","writing","Writing","Build write-ups by Navin Jairam M: deploying to EC2 with OIDC and SSM, nine ColdBox pentest findings, and building the AegisSRE platform.",writing))

p1_body = post_head("deploying-to-ec2-with-oidc-and-ssm","AWS · CI/CD",
  "Deploying to EC2 with OIDC and SSM, and proving it worked",
  "The capstone of my Codomax internship: a GitHub Actions pipeline that authenticates to AWS without stored keys, deploys to EC2 over SSM, verifies the running code matches the commit, and rolls back if it does not.",
  gh_btn("codomax-internship")) + '''
<section style="padding-top:0"><div class="wrap"><div class="post">
  <p>Most student pipelines are CI only: lint, test, build, green tick, done. For the capstone of my Codomax Linux, Cloud and DevOps internship I wanted the second half too. Seven modules build up to it, starting with Linux CLI, networking and server deployment, then AWS, Docker and CI/CD, all around one application (CloudOps, a small notes platform with a UI, a REST API and PostgreSQL) instead of throwaway exercises. The capstone deploys that application to a real EC2 host.</p>
  <p>The part I am most glad I did properly is authentication. The pipeline never touches a stored AWS key. GitHub Actions mints a short-lived OIDC token, and an IAM role trusts it for exactly this repository and branch. The trust policy and permission policy live in the repo under module 6. This bit me early on: the trust policy was referenced in my docs but never actually committed, and then GitHub's new token format broke the old claim I had copied. Keyless auth only works if the federation setup itself is treated as code.</p>
  <p>The deploy path on a push to main is: build the image, push it to GHCR, then reach the EC2 host over AWS Systems Manager. SSM Run Command is the control channel, so there are no SSH keys to manage and no inbound port to justify in the security group. The host pulls the new image and restarts the Compose stack.</p>
  <p>Shipping is the easy half; proving it worked is the point. The application reports the commit it was built from, and the pipeline's verify step compares that git_sha with the commit that triggered the run, plus health checks. Earlier versions of this pipeline quietly skipped the deploy step and still went green. Running it for real surfaced bugs CI alone would never catch: a healthcheck that failed under cron because PATH was different, probes pointed at the wrong routes, and every container's logs landing in one literal log stream. Each one was diagnosed from CloudTrail and logs, then fixed.</p>
  <p>The evidence is committed: 43 screenshots in the capstone's screenshots folder. The platform was deployed live on AWS and verified on 21 November 2026, then torn down on purpose, because a student budget is a real constraint. Total AWS cost for the whole exercise was about $0.03. Everything is in the repo: the workflows, the OIDC policies, the deploy scripts and the runbook.</p>
</div></div></section>
''' + next_nav("../",("writing/building-an-sre-platform.html","Building an SRE platform"),("writing/coldbox-nine-findings.html","Nine findings in a ColdBox banking app")) + CTA("../")
write("writing/deploying-to-ec2-with-oidc-and-ssm.html", page("writing/deploying-to-ec2-with-oidc-and-ssm.html","writing","Deploying to EC2 with OIDC and SSM","How the Codomax capstone pipeline deploys to EC2: OIDC keyless auth, SSM Run Command, git_sha verification and rollback, with 43 evidence screenshots.",p1_body,root="../"))

p2_body = post_head("coldbox-nine-findings","security",
  "Nine findings in a ColdBox banking app, and how I fixed them",
  "A full penetration-test engagement against my own application: SecureBank, a small ColdBox banking app built twice, once vulnerable and once hardened, with every fix proven by executed tooling.",
  gh_btn("ColdBox-Pentesting")) + '''
<section style="padding-top:0"><div class="wrap"><div class="post">
  <p>SecureBank is a deliberately small simulated banking application on the ColdBox/CFML stack (ColdBox 8.3, Lucee 6.2, MariaDB 11.8), implemented twice: a vulnerable build and a hardened build with the same features. Everything runs on loopback only, all accounts and balances are synthetic fixtures, and the test harness refuses non-loopback targets. The point was never the app. The point was running the complete application-security lifecycle on it: develop, test, scan, identify, remediate, verify, automate.</p>
  <p>The findings cover four classes. SQL injection in the login and search flows, where the queries were concatenated strings, fixed with cfqueryparam and proper validation. Reflected and stored cross-site scripting from raw output, fixed with context-aware encoding and a Content Security Policy. Session fixation, where the session identifier never rotated at login, fixed by rotating it and invalidating the old token. And a transfer endpoint that did not verify account ownership, fixed so both accounts must belong to the caller, with the transfer bounded and atomic.</p>
  <p>A fix you cannot demonstrate is just a claim, so the repo is built around proof. A differential harness sends the same 18 requests to both builds: 18 out of 18, the vulnerable build fails and the secured build holds. The TestBox suites pass 31/31 on one side and 44/44 on the other, and seven environment gates (G1 to G7: boot, database, BCrypt, sessions, TestBox, datasource) run before any of the security tooling starts.</p>
  <p>The scanner story is honest about its limits. OWASP ZAP runs baseline and active scans, Gitleaks hunts secrets, Trivy covers dependencies and containers. Semgrep has no CFML parser, so instead of pretending it scanned anything, I wrote cfscan, a small in-repository CFML scanner, with its heuristic rules labelled as heuristics. A severity-based quality gate reads the reports, and the one accepted exception lives in a written ledger as EX-001 rather than being quietly ignored.</p>
  <p>What I took from the engagement is that security work is evidence work. The findings index has a chapter per finding, including what the evidence does not prove, and the limitations doc lists the gaps, like untested concurrency. Reports distinguish executed checks from checks with no results. Fourteen screenshots capture the running applications. It is all in the repo, MIT licensed, for local and isolated educational use.</p>
</div></div></section>
''' + next_nav("../",("writing/deploying-to-ec2-with-oidc-and-ssm.html","Deploying to EC2 with OIDC and SSM"),("writing/building-an-sre-platform.html","Building an SRE platform")) + CTA("../")
write("writing/coldbox-nine-findings.html", page("writing/coldbox-nine-findings.html","writing","Nine findings in a ColdBox banking app","A penetration-test engagement on a ColdBox CFML banking app: 9 findings documented and fixed, proven with ZAP, Semgrep, Gitleaks, Trivy, cfscan and TestBox runs.",p2_body,root="../"))

p3_body = post_head("building-an-sre-platform","SRE · Kubernetes",
  "Building an SRE platform: what is real today, what is next",
  "AegisSRE is my personal flagship: an SRE platform that watches a deployed application, collects its telemetry and keeps a human in control. Here is what phase 2 actually built and tested, and what is still design.",
  gh_btn("AegisSRE")) + '''
<section style="padding-top:0"><div class="wrap"><div class="post">
  <p>One name note first: the platform's codename is AegisDeploy, and the repository is AegisSRE. Same project. I started it because every project I had built stopped at deployment, and I wanted to work on the part that comes after: watching a running system, noticing when it misbehaves, and understanding why.</p>
  <p>What exists today, built and tested, is phase 2. AegisShop is a four-service demo shop (catalog, cart, order and payment) that exists to be watched. Around it sit a service registry, a deployments API and a live Next.js console. Observability is not an afterthought: Prometheus for metrics with alert rules, Grafana dashboards, Loki for logs, Tempo for traces, and OpenTelemetry instrumentation across the six Python services.</p>
  <p>The engineering discipline around it matters as much as the features. Every push runs a six-job CI pipeline, and all six must pass before a merge: YAML and Compose validation, Kubernetes manifests checked with kubeconform and kustomize, a link check across every doc, the backend (ruff, mypy, pytest), Docker image builds and the frontend build. All 54 backend tests pass. The platform ships with 7 Dockerfiles, a 15-container Compose stack, manifests for 7 Kubernetes services managed with Kustomize, and Terraform for the cloud infrastructure. It is MIT licensed.</p>
  <p>What is next is designed, documented, and not built yet, and I try to keep that line bright. The roadmap covers anomaly detection with Isolation Forest models and statistical baselines, an AI reasoning layer that combines logs, metrics, traces, deployments and runbooks into evidence-backed root-cause explanations, and remediation where low-risk reversible actions can execute automatically while anything risky waits for a human to approve. A deployment-intelligence tier (risk scoring, bad-rollout detection, change-incident correlation, DI-1 through DI-7) is specced in the architecture docs.</p>
  <p>The biggest lesson so far: instrument one demo application end to end before reaching for any intelligence. A platform that cannot show you a clean trace of a boring request has no business detecting anomalies. The repo has the docs, the roadmap and the working phase 2 code, and the CI pipeline keeps both honest.</p>
</div></div></section>
''' + next_nav("../",("writing/coldbox-nine-findings.html","Nine findings in a ColdBox banking app"),("writing/deploying-to-ec2-with-oidc-and-ssm.html","Deploying to EC2 with OIDC and SSM")) + CTA("../")
write("writing/building-an-sre-platform.html", page("writing/building-an-sre-platform.html","writing","Building an SRE platform","AegisSRE, a personal flagship SRE platform: what phase 2 built and tested (registry, deployments API, console, 6-job CI, observability) and what is still on the roadmap.",p3_body,root="../"))
