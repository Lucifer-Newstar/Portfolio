# Page bodies. Executed by build.py (shares its namespace: page, write, tags, ICON, EMAIL, GH, LI, html).
R = "https://github.com/Lucifer-Newstar/"
DIGI_LIVE = "https://digi-crave-os.vercel.app"

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

def pcard(href, title, kind, desc, tg, data_tags, external=False, feature=False, delay=0):
    tgt = ' target="_blank" rel="noopener"' if external else ""
    go = "View repo on GitHub" if external else "Open case study"
    f = " feature" if feature else ""
    corner = "github ↗" if external else "case study"
    return f'''<a class="card tilt pcard reveal{f}" href="{href}"{tgt} data-tags="{data_tags}" data-delay="{delay}">
  <div class="ptop"><span class="badge">{html.escape(kind)}</span><span>{corner}</span></div>
  <h3>{html.escape(title)}</h3>
  <p>{html.escape(desc)}</p>
  {tags(tg)}
  <span class="go">{go} <span class="arr" aria-hidden="true">→</span></span>
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
  <div class="term" role="img" aria-label="Animated terminal: whoami prints navin-jairam-m; kubectl get pods lists the projects AegisDeploy, Portfolio Platform and DigiCrave OS as running; deploy navin to prod prints Navin Jairam M, DevOps and Cloud Engineer.">
    <div class="term-bar" aria-hidden="true"><i></i><i></i><i></i><span>navin@prod: ~ — zsh</span></div>
    <div class="term-body" id="hero-term" aria-hidden="true"></div>
    <div class="term-foot"><span aria-hidden="true"><span class="hint-desk">press ⌘K or / for the real shell</span><span class="hint-touch">tap &gt;_ for the real shell</span></span><button type="button" id="hero-skip">skip ⏭</button><button type="button" id="hero-replay" hidden>replay ↻</button></div>
  </div>
</div></section>

<section style="padding-top:20px"><div class="wrap">
  <div class="grid g3">
    <div class="card reveal"><div class="stat">2<small>DevOps internships on live projects: Rapture Twelve and Adroit Technologies</small></div></div>
    <div class="card reveal" data-delay="80"><div class="stat">6-job<small>GitHub Actions CI pipeline guarding every push to AegisDeploy</small></div></div>
    <div class="card reveal" data-delay="160"><div class="stat">7<small>Kubernetes services in AegisDeploy, managed with Kustomize</small></div></div>
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
  <div class="grid g3" style="margin-top:26px">
    {pcard("projects/aegisdeploy.html","AegisDeploy","SRE platform","AI-powered autonomous SRE platform for monitoring, incident detection, root-cause analysis and automated remediation.",["Kubernetes","Kustomize","GitHub Actions","Prometheus","Grafana"],"k8s cicd obs")}
    {pcard("projects/portfolio-platform.html","Portfolio Platform","Serverless AWS","S3 + CloudFront hosting, API Gateway + Lambda APIs, DynamoDB, Cognito auth and SES email, deployed by GitHub Actions.",["S3","CloudFront","Lambda","DynamoDB","Cognito"],"aws cicd",delay=80)}
    {pcard("projects/digicrave-os.html","DigiCrave OS","Live product","MERN-stack restaurant POS and operations system I helped build and deploy at Rapture Twelve. It's live.",["MongoDB","Express","React","Node.js"],"web",delay=160)}
  </div>
</div></section>

<section><div class="wrap split">
  <div class="reveal">
    <p class="eyebrow">experience</p>
    <h2>Two internships, both on live projects</h2>
    <p class="muted">At Rapture Twelve I set up AWS IAM, designed cloud architecture and automated CI/CD, and received a Certificate of Exceptional Contribution. At Adroit Technologies I helped optimise how a payroll system was deployed.</p>
    <a class="btn" href="about.html#experience">See the timeline →</a>
  </div>
  <div class="term reveal" data-delay="100">
    <div class="term-bar" aria-hidden="true"><i></i><i></i><i></i><span>git log --oneline career</span></div>
    <div class="term-body" style="min-height:0"><span class="am">a7f3e21</span> <span class="o">(HEAD → main)</span> Rapture Twelve · DevOps Intern
        <span class="o">May 2026 – Oct 2026</span>
<span class="am">c41d0b9</span> 🏅 Certificate of Exceptional Contribution
        <span class="o">Sep 2026</span>
<span class="am">9be2a54</span> Adroit Technologies · Software Deployment Intern
        <span class="o">Dec 2025 – Feb 2026</span>
<span class="am">3d1f7c0</span> init: B.Tech IT, Meenakshi College of Engineering
        <span class="o">2023</span></div>
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
  <p class="lead">I'm a final-year B.Tech IT student at Meenakshi College of Engineering in Chennai. I've completed two DevOps internships on live projects, and I build projects such as AegisDeploy, an SRE platform with a full observability stack. I'm seeking DevOps, SRE, or cloud engineering roles starting in 2027.</p>
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
    <h3>Quick facts</h3>
    <dl class="kv">
      <dt>based</dt><dd>Chennai, India</dd>
      <dt>studying</dt><dd>B.Tech Information Technology, Meenakshi College of Engineering (2023–2027), CGPA 7.61</dd>
      <dt>stack</dt><dd>AWS, Docker, Kubernetes, GitHub Actions, Ansible, Prometheus, Grafana</dd>
      <dt>looking for</dt><dd>DevOps / SRE / Cloud roles starting in 2027</dd>
      <dt>languages</dt><dd>English (professional), Tamil (native)</dd>
    </dl>
  </div>
  <div class="card reveal" data-delay="100">
    <h3>Earlier education</h3>
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
        <li>Automated build and release with CI/CD pipelines and containerized applications for repeatable deployments.</li>
        <li>Contributed to building and deploying <a href="projects/digicrave-os.html">DigiCrave OS</a>, a MERN-stack restaurant POS &amp; operations system, now live.</li>
      </ul>
      <div class="award">{ICON["award"]}<div><b>Certificate of Exceptional Contribution · Sep 2026</b><span>For work across cloud infrastructure, AWS IAM, scalability, containerization and CI/CD automation. <a href="https://lnkd.in/p/gHc3NYDa" target="_blank" rel="noopener">See the post</a></span></div></div>
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
projects = f'''<section class="page-head"><div class="wrap">
  <p class="crumb">~/projects</p>
  <p class="eyebrow">ls -la ~/projects</p>
  <h1>Things I've built and shipped</h1>
  <p class="lead">From a Kubernetes-ready SRE platform to a serverless AWS stack and a live restaurant POS. Each case study has an interactive architecture diagram.</p>
</div></section>
<section style="padding-top:6px"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter projects">
    <button type="button" data-filter="all" aria-pressed="true">all</button>
    <button type="button" data-filter="k8s" aria-pressed="false">kubernetes</button>
    <button type="button" data-filter="aws" aria-pressed="false">aws</button>
    <button type="button" data-filter="cicd" aria-pressed="false">ci/cd</button>
    <button type="button" data-filter="obs" aria-pressed="false">observability</button>
    <button type="button" data-filter="infra" aria-pressed="false">infra</button>
    <button type="button" data-filter="web" aria-pressed="false">full-stack</button>
  </div>
  <p id="filter-status" class="sr-only" aria-live="polite"></p>
  <div class="grid g3">
    {pcard("projects/aegisdeploy.html","AegisDeploy","SRE platform · MIT","AI-powered autonomous SRE platform for monitoring, incident detection, root-cause analysis and automated remediation. 6-job CI pipeline, 6 Dockerfiles, Kubernetes manifests for 7 services, and a full observability stack.",["Python","Docker","Kubernetes","Kustomize","GitHub Actions","Prometheus","Grafana","Loki","Tempo","OpenTelemetry"],"k8s cicd obs",feature=True)}
    {pcard("projects/portfolio-platform.html","Portfolio Platform","Serverless AWS","Serverless portfolio on AWS: S3 + CloudFront hosting, API Gateway + Lambda APIs, DynamoDB, Cognito auth and SES email, deployed by a GitHub Actions workflow.",["S3","CloudFront","API Gateway","Lambda","DynamoDB","Cognito","SES"],"aws cicd",delay=80)}
    {pcard("projects/digicrave-os.html","DigiCrave OS","Live · Rapture Twelve","Restaurant POS & operations system. I helped build and deploy it during my internship at Rapture Twelve.",["MongoDB","Express","React","Node.js"],"web")}
    {pcard("projects/distributed-java-webapp.html","Distributed Java Web App","Multi-VM infra","A multi-VM Java app environment provisioned with Vagrant: Tomcat, MySQL, Memcached, RabbitMQ and an Nginx load balancer.",["Vagrant","Tomcat","MySQL","Memcached","RabbitMQ","Nginx"],"infra",delay=80)}
    {pcard(R+"Productivity-App","Kaizen – Productivity OS","CI/CD · MLOps","A productivity OS with automated CI/CD releases and basic MLOps workflows.",["CI/CD","MLOps"],"cicd",external=True,delay=160)}
  </div>
</div></section>
{CTA("")}
'''
write("projects.html", page("projects.html","projects","Projects","AegisDeploy, a serverless AWS portfolio platform, DigiCrave OS, a distributed Java web app on Vagrant, and Kaizen.",projects))

# ---------------- SKILLS ----------------
POOLS = [
 ("cloud","Cloud","amber",[
   ("aws-iam","AWS IAM",["rapture|Rapture Twelve: set up IAM roles and policies for live environments"]),
   ("aws-ec2","AWS EC2",[]),
   ("aws-s3","AWS S3",["portfolio|Portfolio Platform: static hosting on S3"]),
   ("aws-lambda","AWS Lambda",["portfolio|Portfolio Platform: API Gateway + Lambda APIs"]),
   ("aws-cloudwatch","AWS CloudWatch",[]),
   ("cloudfront","CloudFront",["portfolio|Portfolio Platform: CDN in front of S3"]),
   ("api-gateway","API Gateway",["portfolio|Portfolio Platform: the API front door"]),
   ("dynamodb","DynamoDB",["portfolio|Portfolio Platform: data store"]),
   ("cognito","Cognito",["portfolio|Portfolio Platform: authentication"]),
   ("ses","SES",["portfolio|Portfolio Platform: email"]),
   ("oci","Oracle Cloud (OCI)",["cert|OCI 2025 Foundations Associate","cert|Oracle Database@AWS Certified Architect Professional"]),
 ]),
 ("containers","Containers & Orchestration","cyan",[
   ("docker","Docker",["aegis|AegisDeploy: 6 Dockerfiles","rapture|Rapture Twelve: containerized applications"]),
   ("kubernetes","Kubernetes",["aegis|AegisDeploy: manifests for 7 services"]),
   ("kustomize","Kustomize",["aegis|AegisDeploy: one Kustomize base for all 7 services"]),
 ]),
 ("cicd","CI/CD","green",[
   ("github-actions","GitHub Actions",["aegis|AegisDeploy: 6-job CI pipeline","portfolio|Portfolio Platform: deploy workflow"]),
   ("git","Git",["aegis|AegisDeploy","portfolio|Portfolio Platform","java|Distributed Java Web App","digicrave|DigiCrave OS","kaizen|Kaizen"]),
   ("ci-cd","CI/CD pipelines",["rapture|Rapture Twelve: automated build and release","kaizen|Kaizen: automated CI/CD releases"]),
   ("kubeconform","kubeconform",["aegis|AegisDeploy: validates K8s manifests in CI"]),
 ]),
 ("iac","IaC & Config","violet",[
   ("ansible","Ansible",[]),
   ("vagrant","Vagrant",["java|Distributed Java Web App: multi-VM environment"]),
   ("nginx","Nginx",["java|Distributed Java Web App: load balancer"]),
   ("tomcat","Tomcat",["java|Distributed Java Web App: app server"]),
   ("rabbitmq","RabbitMQ",["java|Distributed Java Web App: message queue"]),
   ("memcached","Memcached",["java|Distributed Java Web App: cache"]),
   ("mysql","MySQL",["java|Distributed Java Web App: database"]),
 ]),
 ("observability","Observability","red",[
   ("prometheus","Prometheus",["aegis|AegisDeploy: metrics and alert rules"]),
   ("grafana","Grafana",["aegis|AegisDeploy: dashboards"]),
   ("loki","Loki",["aegis|AegisDeploy: logs"]),
   ("tempo","Tempo",["aegis|AegisDeploy: traces"]),
   ("opentelemetry","OpenTelemetry",["aegis|AegisDeploy: instrumentation"]),
 ]),
 ("languages","Languages & OS","cyan",[
   ("python","Python",["aegis|AegisDeploy: services, checked with mypy and pytest"]),
   ("bash","Bash",[]),
   ("linux","Linux",[]),
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
    pool_html += f'<section class="pool" style="--c:var(--{color})" data-pool="{pid}" aria-label="{html.escape(pname)} node pool"><header><h3>{html.escape(pname)}</h3><span>{len(skl)} pods</span></header><div class="pods">{pods}</div></section>'
usage_btns = '<button type="button" data-key="all" aria-pressed="true">everything</button>' + "".join(f'<button type="button" data-key="{k}" aria-pressed="false">{html.escape(v)}</button>' for k, v in [("aegis","AegisDeploy"),("portfolio","Portfolio Platform"),("java","Java Web App"),("digicrave","DigiCrave OS"),("rapture","Rapture Twelve"),("cert","Certifications")])
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
<span class="o">{total} pods across 6 node pools. Tap a pod to describe it.</span></div>
  </div>
</div></section>
{CTA("")}
'''
write("skills.html", page("skills.html","skills","Skills","Navin Jairam M's stack grouped by Cloud, Containers, CI/CD, IaC, Observability and Languages, with where each tool was used.",skills))

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

# ---------------- AEGISDEPLOY ----------------
STAGES = [("config","YAML + compose valid","M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8zM14 3v5h5M9 13h6M9 17h4"),("k8s manifests","kubeconform + kustomize","M12 2 3 7v10l9 5 9-5V7z"),("docs links","every docs link resolves","M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1 1M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1-1"),("backend","ruff · mypy · pytest","M8 4 4 12l4 8M16 4l4 8-4 8"),("docker build","container images","M3 9h18v10H3zM7 9V5h4v4M13 9V5h4v4"),("frontend build","console production build","M3 4h18v12H3zM8 20h8M12 16v4")]
st_html = ""
for name, sub, d in STAGES:
    st_html += f'<li class="stage"><span class="st-ic" aria-hidden="true"><svg class="base" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg><svg class="chk" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5 9-10"/></svg></span><span class="st-txt"><span class="st-name">{name}</span><span class="st-sub">{sub} · <span class="st-state">queued</span></span></span></li>'
SVCS = [("registry-service","platform"),("deployments-service","platform"),("console","platform · frontend"),("catalog-service","aegisshop demo"),("cart-service","aegisshop demo"),("order-service","aegisshop demo"),("payment-service","aegisshop demo")]
svc_html = "".join(f'<div class="svc{" demo" if "demo" in g else ""}">{n}<small>{g}</small></div>' for n, g in SVCS)
obs = diagram("AegisDeploy observability flow",
  lane("metrics", [("7 services","OpenTelemetry instrumented","The services are instrumented with OpenTelemetry, so metrics, logs and traces come from the same code."),("Prometheus","metrics + alert rules","Prometheus holds the services' metrics and evaluates alert rules, so problems raise an alert instead of hiding."),("Grafana","dashboards","Grafana dashboards bring metrics, logs and traces into one place.")], "red") +
  lane("logs", [("7 services","logs","The same services produce logs."),("Loki","log aggregation","Loki stores and indexes the logs so they can be searched from Grafana."),("Grafana","explore logs","Logs show up beside the metrics in Grafana.")], "amber") +
  lane("traces", [("7 services","OpenTelemetry spans","OpenTelemetry records a trace as a request moves between services."),("Tempo","distributed tracing","Tempo stores the traces so a slow request can be followed hop by hop."),("Grafana","trace view","Traces open in Grafana next to the logs and metrics for the same moment.")], "violet"))
aegis_body = detail_head("../","case study · SRE platform · MIT licensed","AegisDeploy",
  "An AI-powered autonomous SRE platform for monitoring, incident detection, root-cause analysis and automated remediation. Kubernetes-ready, checked by CI on every push, and observable end to end.",
  ["Python","Docker","Kubernetes","Kustomize","GitHub Actions","Prometheus","Grafana","Loki","Tempo","OpenTelemetry"],
  [gh_btn("AegisDeploy")]) + f'''
<section style="padding-top:0"><div class="wrap"><div class="grid g3">
  <div class="card reveal"><div class="stat">6<small>CI jobs on GitHub Actions</small></div></div>
  <div class="card reveal" data-delay="80"><div class="stat">6<small>Dockerfiles</small></div></div>
  <div class="card reveal" data-delay="160"><div class="stat">7<small>Kubernetes services, one Kustomize base</small></div></div>
</div></div></section>

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
  <p class="muted reveal" style="max-width:66ch">OpenTelemetry instruments the services, Prometheus, Loki and Tempo each take one signal, and Grafana puts it all on one screen.</p>
  <div style="margin-top:20px">{obs}</div>
</div></section>
''' + next_nav("../",("projects/distributed-java-webapp.html","Distributed Java Web App"),("projects/portfolio-platform.html","Portfolio Platform")) + CTA("../")
write("projects/aegisdeploy.html", page("projects/aegisdeploy.html","projects","AegisDeploy","AegisDeploy: AI-powered autonomous SRE platform with a 6-job CI pipeline, 7 Kubernetes services and a Prometheus/Grafana/Loki/Tempo/OpenTelemetry stack.",aegis_body,root="../"))

# ---------------- PORTFOLIO PLATFORM ----------------
pp = diagram("Portfolio Platform architecture",
  lane("static site", [("Visitor","browser","A visitor opens the site in their browser."),("CloudFront","CDN","CloudFront serves the site from the edge and caches it."),("S3","static files","The site's files live in an S3 bucket behind CloudFront.")], "cyan") +
  lane("api", [("Frontend","API calls","The site calls its own API for anything dynamic."),("API Gateway","HTTP API","API Gateway is the API's front door and routes each request to a function."),("Lambda","serverless functions","Lambda functions run the API's logic with no servers to manage."),[("DynamoDB","data","DynamoDB stores the platform's data."),("SES","email","SES sends the platform's email.")]], "green") +
  lane("auth", [("User","sign in","A user signs in."),("Cognito","authentication","Cognito handles sign-in and tokens for the platform."),("API Gateway","authorised calls","Signed-in requests reach the API.")], "violet") +
  lane("delivery", [("git push","main","A push to the repo starts a deploy."),("GitHub Actions","deploy workflow","A GitHub Actions workflow automates the deployment to AWS."),("AWS","new version live","The new version goes out.")], "amber"))
pp_body = detail_head("../","case study · serverless AWS","Portfolio Platform",
  "A serverless portfolio platform on AWS: S3 + CloudFront hosting, API Gateway + Lambda APIs, DynamoDB, Cognito auth and SES email, with deployment automated by GitHub Actions.",
  ["S3","CloudFront","API Gateway","Lambda","DynamoDB","Cognito","SES","GitHub Actions"],[gh_btn("portfolio")]) + f'''
<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">How it fits together</h2>
  <div style="margin-top:20px">{pp}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>What I built</h3><ul class="list-check"><li>Static hosting on S3 behind CloudFront</li><li>APIs on API Gateway + Lambda</li><li>DynamoDB for data, Cognito for auth, SES for email</li><li>Automated deployment with a GitHub Actions workflow</li></ul></div>
  <div class="card reveal" data-delay="80"><h3>Why serverless</h3><p class="muted">No servers to patch or keep running: each piece is a managed AWS service, and the whole thing deploys from a git push.</p></div>
</div></section>
''' + next_nav("../",("projects/aegisdeploy.html","AegisDeploy"),("projects/digicrave-os.html","DigiCrave OS")) + CTA("../")
write("projects/portfolio-platform.html", page("projects/portfolio-platform.html","projects","Portfolio Platform","A serverless AWS platform: S3, CloudFront, API Gateway, Lambda, DynamoDB, Cognito and SES, deployed with GitHub Actions.",pp_body,root="../"))

# ---------------- DIGICRAVE ----------------
dc = diagram("DigiCrave OS architecture",
  lane("request path", [("Restaurant staff","browser","Staff use DigiCrave OS in the browser for point of sale and day-to-day restaurant operations."),("React","frontend · live on Vercel","The React frontend is what's live at digi-crave-os.vercel.app."),("Express + Node.js","API","The Express API on Node.js handles the POS and operations logic."),("MongoDB","database","MongoDB stores the restaurant's data.")], "green"))
dc_body = detail_head("../","case study · live product · Rapture Twelve","DigiCrave OS",
  "A MERN-stack restaurant POS and operations system. I contributed to building and deploying it during my DevOps internship at Rapture Twelve, and it's live now.",
  ["MongoDB","Express","React","Node.js"],
  [f'<a class="btn primary" href="{DIGI_LIVE}" target="_blank" rel="noopener">{ICON["ext"]} Open live demo</a>', gh_btn("DigiCraveOS")]) + f'''
<section style="padding-top:0"><div class="wrap">
  <p class="eyebrow reveal">architecture</p>
  <h2 class="reveal">The MERN stack, end to end</h2>
  <div style="margin-top:20px">{dc}</div>
</div></section>
<section><div class="wrap split">
  <div class="card reveal"><h3>My part</h3><p class="muted">I contributed to building and deploying it at Rapture Twelve, as part of the work that earned my Certificate of Exceptional Contribution (Sep 2026).</p></div>
  <div class="card reveal" data-delay="80"><h3>Try it</h3><p class="muted">The live demo is at <a href="{DIGI_LIVE}" target="_blank" rel="noopener">digi-crave-os.vercel.app</a>.</p></div>
</div></section>
''' + next_nav("../",("projects/portfolio-platform.html","Portfolio Platform"),("projects/distributed-java-webapp.html","Distributed Java Web App")) + CTA("../")
write("projects/digicrave-os.html", page("projects/digicrave-os.html","projects","DigiCrave OS","DigiCrave OS: a live MERN-stack restaurant POS and operations system Navin helped build and deploy at Rapture Twelve.",dc_body,root="../"))

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
''' + next_nav("../",("projects/digicrave-os.html","DigiCrave OS"),("projects/aegisdeploy.html","AegisDeploy")) + CTA("../")
write("projects/distributed-java-webapp.html", page("projects/distributed-java-webapp.html","projects","Distributed Java Web App","A multi-VM Java app environment provisioned with Vagrant: Nginx, Tomcat, MySQL, Memcached and RabbitMQ.",jv_body,root="../"))

# ---------------- 404 ----------------
nf = '''<section class="page-head"><div class="wrap">
  <p class="eyebrow">exit code 404</p>
  <h1>Pod not found.</h1>
  <p class="lead">That page doesn't exist. Head home, or open the terminal and type <b>help</b>.</p>
  <div class="btns"><a class="btn primary" href="/index.html">Back home</a><button class="btn" type="button" data-palette>Open terminal</button></div>
</div></section>'''
write("404.html", page("404.html","none","Not found","Page not found.",nf,root="/"))
