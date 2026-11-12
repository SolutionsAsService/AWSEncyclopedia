#!/usr/bin/env python3
"""Build the AWS Encyclopedia into site/.   python3 _src/build.py

All counts come from _src/data/aws.json (written by _src/fetch_aws.py from the AWS SDK's own models). The build fails
on a dead local link, a service id missing from the data, or deploy config that disagrees with the DADA website rule.
"""
import html
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
sys.path.insert(0, str(Path(__file__).parent))
import content as K  # noqa: E402

SITE_URL = "https://awsencyclopedia.shadw.app"
e = html.escape
D = json.loads((ROOT / "_src" / "data" / "aws.json").read_text())
SV = sorted(D["services"], key=lambda s: s["id"])
BY = {s["id"]: s for s in SV}
N = len(SV)
OPS = sum(s["ops"] for s in SV)
RANK = {s["id"]: i + 1 for i, s in enumerate(sorted(SV, key=lambda s: (-s["ops"], s["id"])))}
MAXOPS = max(s["ops"] for s in SV)
PARTS = D["partitions"]
REGIONS = sum(len(p["regions"]) for p in PARTS)
STD = next(p for p in PARTS if p["partition"] == "aws")
BEGIN = {x["id"] for x in K.SERVICES}


def name(sid):
    return BY[sid]["full"] or sid


_Q = sorted(x["ops"] for x in SV)
CUTS = [_Q[len(_Q) * k // 4] for k in (1, 2, 3)]  # quartiles of operation count


def level(ops):
    """Four shades by quartile of operation count."""
    return sum(ops >= c for c in CUTS)


NAV = [("services.html", f"All {N} services"), ("why.html", "Why it's complicated"), ("start.html", "The 13 basics"), ("shadw.html", "Use Shadw")]


def page(path, title, body, desc, active=None, js=False):
    links = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{e(l)}</a></li>' for h, l in NAV)
    full = K.SITE if title is None else f"{title} · {K.SITE}"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}/og.png">
<meta property="og:site_name" content="{K.SITE}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
{'<script src="js/site.js" defer></script>' if js else ''}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="brand" href="index.html"><span class="mark" aria-hidden="true"></span><span>AWS <b>Encyclopedia</b></span></a>
  <nav class="nav-wide" aria-label="Site"><ul>{links}</ul></nav>
  <details class="nav-menu"><summary>Menu</summary><nav aria-label="Site menu"><ul>{links}</ul></nav></details>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <p><strong>{K.SITE}.</strong> Counts from the AWS SDK for Python (botocore {D["botocore"]}, read {D["fetched"]}). Not affiliated with Amazon Web Services. <a href="about.html">About</a> · <a href="https://github.com/SolutionsAsService/AWSEncyclopedia">Source</a> · MIT licence.</p>
</footer>
</body>
</html>
"""
    (OUT / path).write_text(doc)


def wall(compact=False):
    cells = "".join(f'<i class="w{level(s["ops"])}{" b" if s["id"] in BEGIN else ""}" title="{e(name(s["id"]))}"></i>' for s in SV)
    return f'<div class="wall{" compact" if compact else ""}" aria-hidden="true">{cells}</div>'


def header(kicker, title, lede):
    return f'<header class="pg-head"><p class="kicker">{kicker}</p><h1>{title}</h1><p class="lede">{lede}</p></header>'


# ------------------------------------------------------------------ home
def build_home():
    top = sorted(SV, key=lambda s: -s["ops"])[0]
    groups = len(K.GROUPS[0][1])
    cards = "".join(f'<li><a href="{x["file"]}"><span class="c-k">{e(x["kind"])}</span><span class="c-t">{e(x["short"])}</span><span class="c-n">{BY[x["id"]]["ops"]} operations</span></a></li>' for x in K.SERVICES)
    body = f"""<section class="hero" aria-labelledby="h1">
  <div class="hero-text">
    <p class="kicker">A field guide to Amazon Web Services</p>
    <h1 id="h1"><span class="big">{N}</span> services.<br>Your website needs <em>one file</em>.</h1>
    <p class="lede">Every square is one AWS service, counted from Amazon's own SDK: {OPS:,} API operations in all. This guide explains the {len(K.SERVICES)} you meet first and why the rest exist. Then it tells you the shortcut.</p>
    <div class="ctas"><a class="btn" href="services.html">See all {N}</a><a class="btn ghost" href="shadw.html">Or use Shadw →</a></div>
  </div>
  <figure class="hero-fig">
    {wall()}
    <figcaption><span class="lg"><i class="w0"></i><i class="w1"></i><i class="w2"></i><i class="w3"></i> one square per service, darker = more API operations (quartiles)</span><span class="lg"><i class="w2 b"></i> the {len(K.SERVICES)} basics</span><a class="one" href="shadw.html"><i></i><span><b>fluid.json</b> one file on Shadw →</span></a></figcaption>
  </figure>
</section>
<section class="band" aria-labelledby="why-h">
  <h2 id="why-h">Why it feels like this</h2>
  <ul class="facts">
    <li><b>{N}</b><span>services in the SDK, each its own API</span></li>
    <li><b>{OPS:,}</b><span>API operations across them; {name(top["id"])} alone has {top["ops"]}</span></li>
    <li><b>{groups}</b><span>different services that can run your code</span></li>
    <li><b>{REGIONS}</b><span>regions in {len(PARTS)} separate partitions</span></li>
  </ul>
  <p><a class="more" href="why.html">Why AWS is this complicated →</a></p>
</section>
<section class="band" aria-labelledby="basics-h">
  <h2 id="basics-h">The {len(K.SERVICES)} you meet first</h2>
  <ol class="cards">{cards}</ol>
</section>
<section class="band shadw-band" aria-labelledby="sh-h">
  <h2 id="sh-h">Or skip all of it</h2>
  <p class="lede">To put a website online on AWS you would wire S3, CloudFront, Route 53, a certificate and IAM together. On Shadw this whole site deploys from one small file:</p>
  <pre class="code"><code>{e((ROOT / "fluid.json").read_text().strip())}</code></pre>
  <p><a class="btn" href="shadw.html">How Shadw does it →</a></p>
</section>"""
    page("index.html", None, body, f"AWS has {N} services and {OPS:,} API operations, counted from its own SDK. A field guide to the ones you meet first, and why a website needs only one file on Shadw.")


# ------------------------------------------------------------------ all services
def build_services():
    rows = []
    for s in SV:
        w = max(0.6, 100 * s["ops"] / MAXOPS)
        rows.append(f'<li data-n="{e((s["full"] or "").lower())} {s["id"]}" data-ops="{s["ops"]}"><span class="s-name">{e(name(s["id"]))}</span>'
                    f'<code class="s-id">{s["id"]}</code><span class="s-ops"><span class="bar" style="width:{w:.1f}%"></span><span class="num">{s["ops"]}</span></span></li>')
    body = f"""<div class="wrap">
{header(f"All {N}, from the SDK", f"Every AWS service", f"The AWS SDK for Python ships one model per service API: {N} of them, with {OPS:,} operations between them. The bar is each service's number of API operations.")}
<div class="tools" role="search">
  <label>Find a service <input type="search" data-role="q" placeholder="queue, database, S3…" autocomplete="off"></label>
  <div class="sort" role="group" aria-label="Sort"><button type="button" data-sort="az" aria-pressed="true">A–Z</button><button type="button" data-sort="ops" aria-pressed="false">Largest first</button></div>
</div>
<p class="count" data-role="count" role="status">{N} services</p>
<ol class="svc" data-role="list">{"".join(rows)}</ol>
<p class="note">Names are the SDK's own <code>serviceFullName</code>. Some services have more than one API (for example <code>ses</code> and <code>sesv2</code>), so this counts APIs, not products.</p>
</div>"""
    page("services.html", "Every AWS service", body, f"All {N} AWS service APIs from the AWS SDK, searchable, with their operation counts.", active="services.html", js=True)


# ------------------------------------------------------------------ why
def build_why():
    top = sorted(SV, key=lambda s: -s["ops"])[:12]
    bars = "".join(f'<li><span class="b-l">{e(name(s["id"]))}</span><span class="b-v"><span class="bar" style="width:{100 * s["ops"] / MAXOPS:.1f}%"></span><span class="num">{s["ops"]}</span></span></li>' for s in top)
    groups = ""
    for label, ids in K.GROUPS:
        chips = "".join(f'<li><span>{e(name(i))}</span> <code>{i}</code></li>' for i in ids)
        groups += f'<div class="grp"><h3>{len(ids)} ways to {e(label)}</h3><ul class="chips">{chips}</ul></div>'
    parts = "".join(f'<li><b>{len(p["regions"])}</b> {e(p["name"])}</li>' for p in PARTS)
    std = " ".join(f"<code>{r}</code>" for r in STD["regions"])
    iam = BY["iam"]["ops"]
    body = f"""<div class="wrap">
{header("The honest answer", "Why AWS is this complicated", "Four reasons, each counted from the AWS SDK, and one reason it is not a mistake.")}
<section class="sec"><h2><span class="num">01</span>There is a service for everything</h2>
<p>{N} services, {OPS:,} operations. The twelve largest APIs alone have {sum(s["ops"] for s in top):,} operations between them:</p>
<ol class="bars">{bars}</ol></section>
<section class="sec"><h2><span class="num">02</span>Many ways to do one thing</h2>
<p>For each everyday job there are several services, each with its own pricing, limits and API. Every name below is in the SDK today.</p>
{groups}</section>
<section class="sec"><h2><span class="num">03</span>Where your things live</h2>
<p>Resources live in a region, and regions are grouped into partitions that do not share accounts: {REGIONS} regions in {len(PARTS)} partitions.</p>
<ul class="parts">{parts}</ul>
<p class="regions">{std}</p></section>
<section class="sec"><h2><span class="num">04</span>Permission for every action</h2>
<p>Nothing works until IAM allows it. Each service defines its own actions, and a policy has to name the right ones on the right resources. IAM's own API has {iam} operations, more than {sum(1 for s in SV if s["ops"] < iam)} of the {N} services.</p></section>
<section class="sec"><h2><span class="num">05</span>Not a mistake</h2>
<p>{e(K.WHY_FAIR)}</p>
<p><a class="btn" href="shadw.html">The shortcut for websites →</a></p></section>
</div>"""
    page("why.html", "Why it's complicated", body, f"Why AWS is complicated, counted: {N} services, {OPS:,} operations, {REGIONS} regions, and several services for every job.", active="why.html")


# ------------------------------------------------------------------ the 13 basics
def build_start():
    cards = "".join(f'<li><a href="{x["file"]}"><span class="c-k">{e(x["kind"])}</span><span class="c-t">{e(x["short"])}</span><span class="c-l">{e(x["what"])}</span><span class="c-n">{BY[x["id"]]["ops"]} operations · #{RANK[x["id"]]} of {N}</span></a></li>' for x in K.SERVICES)
    body = f"""<div class="wrap">
{header("Start here", f"The {len(K.SERVICES)} basics", f"Out of {N}, these are the services almost every AWS account touches. Each page says what it is, what it is for, the catch, and whether a website needs it.")}
<ol class="cards cards-wide">{cards}</ol></div>"""
    page("start.html", f"The {len(K.SERVICES)} basics", body, f"The {len(K.SERVICES)} AWS services you meet first, in plain words.", active="start.html")


def build_service(i, x):
    s = BY[x["id"]]
    prev_ = K.SERVICES[i - 1] if i else None
    next_ = K.SERVICES[i + 1] if i + 1 < len(K.SERVICES) else None
    pager = '<nav class="pager" aria-label="Previous and next">' + \
        (f'<a href="{prev_["file"]}" rel="prev"><small>← Previous</small><span>{e(prev_["short"])}</span></a>' if prev_ else '<span></span>') + \
        (f'<a class="nx" href="{next_["file"]}" rel="next"><small>Next →</small><span>{e(next_["short"])}</span></a>' if next_ else '<a class="nx" href="shadw.html"><small>Then →</small><span>Use Shadw</span></a>') + "</nav>"
    body = f"""<div class="wrap">
{header(f'{e(x["kind"])} · {i + 1} of {len(K.SERVICES)} basics', e(x["short"]), e(s["full"] or x["short"]))}
<dl class="stats"><div><dt>SDK name</dt><dd><code>{s["id"]}</code></dd></div><div><dt>API operations</dt><dd>{s["ops"]}</dd></div><div><dt>Size rank</dt><dd>#{RANK[s["id"]]} of {N}</dd></div></dl>
<section class="sec"><h2>What it is</h2><p>{e(x["what"])}</p></section>
<section class="sec"><h2>What it is for</h2><p>{e(x["use"])}</p></section>
<section class="sec"><h2>The catch</h2><p>{e(x["catch"])}</p></section>
<aside class="web"><h2>For a website</h2><p>{e(x["web"])} <a href="shadw.html">A whole site on Shadw is one file →</a></p></aside>
{pager}</div>"""
    page(x["file"], x["short"], body, f'{x["short"]} ({s["full"]}): {x["what"]}', active="start.html")


# ------------------------------------------------------------------ shadw
def build_shadw():
    fj = (ROOT / "fluid.json").read_text().strip()
    facts = "".join(f"<li><h3>{e(t)}</h3><p>{d}</p></li>" for t, d in K.SHADW_FACTS)
    aws_web = ["s3", "cloudfront", "route53", "acm", "iam"]
    aws_list = "".join(f'<li>{e(name(i))} <code>{i}</code> <span>{BY[i]["ops"]} ops</span></li>' for i in aws_web)
    body = f"""<div class="wrap">
{header("The shortcut", "Just use Shadw", f"If what you want is a website online, you do not need {N} services. You need a folder of pages and one file.")}
<div class="vs">
  <div class="vs-a"><h2>A static site on AWS</h2><ul class="vs-list">{aws_list}</ul><p class="vs-n">{len(aws_web)} services · {sum(BY[i]["ops"] for i in aws_web)} API operations to learn your way around</p></div>
  <div class="vs-b"><h2>The same site on Shadw</h2><pre class="code"><code>{e(fj)}</code></pre><p class="vs-n">1 file · this site's own <code>fluid.json</code>, as deployed</p></div>
</div>
<ul class="shfacts">{facts}</ul>
<section class="sec"><h2>When you do need AWS</h2><p>Databases at scale, machine learning, video pipelines, strict compliance, or anything that needs its own servers: that is what the other services are for. For pages, a blog, a portfolio or a docs site, start simple.</p></section>
<p class="go"><a class="btn big" href="{K.SHADW_URL}">Go to Shadw →</a></p>
</div>"""
    page("shadw.html", "Just use Shadw", body, "Why a website does not need AWS's services: the same site deploys on Shadw from one fluid.json file.", active="shadw.html")


def build_about():
    body = f"""<div class="wrap">
{header("About", "About this guide", "A plain field guide to AWS, rebuilt in 2026.")}
<section class="sec"><h2>Where the numbers come from</h2><p>Every count on the site is read from the AWS SDK for Python (botocore {D["botocore"]}, read {D["fetched"]}): one model per service API, the operations in each model, and the regions in its endpoint data. <code>_src/fetch_aws.py</code> refreshes them; <code>_src/build.py</code> writes the pages and fails if a service it names is missing.</p></section>
<section class="sec"><h2>Not affiliated</h2><p>AWS and the service names are trademarks of Amazon.com, Inc. or its affiliates. This guide is independent.</p></section>
<section class="sec"><h2>Earlier version</h2><p>Version 1 had thirteen hand-written pages; their addresses still work, and the misspelt <code>lamda.html</code> now goes to <a href="lambda.html">lambda.html</a>.</p></section></div>"""
    page("about.html", "About", body, "Where the numbers come from.")


def build_404():
    page("404.html", "Not found", f'<div class="wrap">{header("404", "Not one of the " + str(N), "This page does not exist. <a href=\"index.html\">Back to the guide</a>.")}</div>', "Page not found.")


def build_redirects():
    for old, new in K.OLD_URLS.items():
        (OUT / old).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved · {K.SITE}</title><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="canonical" href="{new}"><meta http-equiv="refresh" content="0; url={new}"></head><body><p>Moved to <a href="{new}">{new}</a>.</p></body></html>\n')


# ------------------------------------------------------------------ checks
def check_ids():
    named = [i for _, ids in K.GROUPS for i in ids] + [x["id"] for x in K.SERVICES] + ["s3", "cloudfront", "route53", "acm", "iam"]
    return [f"service id not in the SDK data: {i}" for i in named if i not in BY]


def check_links():
    bad = []
    for f in OUT.glob("*.html"):
        for href in re.findall(r'href="([^"#]+)(?:#[^"]*)?"', f.read_text()):
            if not href.startswith(("http", "mailto:")) and not (f.parent / href).exists():
                bad.append(f"{f.name} -> {href}")
    return bad


def check_deploy():
    try:
        root = json.loads((ROOT / "vercel.json").read_text())
        inner = json.loads((OUT / "vercel.json").read_text())
        fluid = json.loads((ROOT / "fluid.json").read_text())
    except (OSError, ValueError) as err:
        return [f"deploy config: {err}"]
    ok = (root.get("outputDirectory") == "site" and root.get("fluid") and inner.get("outputDirectory") == "."
          and fluid.get("project") == "awsencyclopedia" and fluid.get("static_dir") == "site"
          and fluid.get("routes") == [{"pattern": "/", "target": "static"}])
    return [] if ok else ["deploy config: vercel.json, site/vercel.json and fluid.json must follow the DADA website rule"]


def main():
    problems = check_ids()
    if problems:
        print(*problems, sep="\n")
        sys.exit(1)
    for f in OUT.glob("*.html"):
        f.unlink()
    build_home()
    build_services()
    build_why()
    build_start()
    for i, x in enumerate(K.SERVICES):
        build_service(i, x)
    build_shadw()
    build_about()
    build_404()
    build_redirects()
    problems = check_links() + check_deploy() + ([] if (OUT / "og.png").exists() else ["site/og.png missing: run node _src/og.cjs"])
    print(f"built {len(list(OUT.glob('*.html')))} pages: {N} services, {OPS:,} operations, {REGIONS} regions (botocore {D['botocore']})")
    if problems:
        print("problems:", *problems, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
