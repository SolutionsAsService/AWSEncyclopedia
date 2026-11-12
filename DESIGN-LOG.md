# DESIGN-LOG: AWS Encyclopedia, from scratch

DADA run, 2026-11-12. Mode: Adaptive. Run type: Full (the old site was thirteen unstyled pages; "next site", rebuilt).

## 1. Traversal Plan
**Brief (owner):** make it pretty, explain why AWS is too complicated by showing all the services, then tell people to use Shadw anyway and link to it.

### Seed (labels copied from the graph)
- Stance: **First Things First Manifesto (Ken Garland)**: the page is a claim before it is a decoration; the claim here is "for a website, you need one file".
- Rules: **The Visual Display of Quantitative Information (Edward Tufte)** (every number counted, never typed) and **WCAG 2.2 Contrast and Perceivability (W3C)**.
- Breaker: **Envisioning Information (Edward Tufte)**: small multiples at scale; the wall of 436 squares is the argument.
- Counterpoint: **How to Use Graphic Design to Sell Things, Explain Things, Make Things Look Better (Michael Bierut)**: the site sells Shadw, so it must explain first and say plainly that it is selling.

### Panel
From `pick_panel.py --mode adaptive --run-type full --project awsencyclopedia --data-graphic --money`: Debord, Shklovsky, Holmes, Mace, Cairo, Tufte, Papanek, Krug. **Override:** Greenberg added for craft (lesson 47: the owner's last grade named sloppiness).

## Frontier
| Candidate | Reached via | Status |
|---|---|---|
| Count everything from the SDK (botocore models and endpoint data) | Tufte, Garland | TAKEN (M1) |
| The wall: one square per service, one blue square for Shadw | Envisioning Information | TAKEN (M2) |
| Fair framing: why the complexity exists | Bierut, Debord | TAKEN (M3) |

## Move M1: Every number from the SDK (KEEP-THE-RULE)
`_src/fetch_aws.py` reads botocore 1.44.1: 436 service models, 19,571 operations, 46 regions in 8 partitions. `_src/build.py` fails if a service the copy names is not in the data.

## Move M2: The wall (BREAK)
The landing graphic is 436 grey squares, shaded by quartile of operation count, the 13 basics outlined, and one blue square: `fluid.json`. It fits the first screen at 1280x800 (bottom 542) and 375x812 (809).

## Move M3: Explain first, then sell (KEEP-THE-RULE)
Why it is complicated (four counted reasons and one fair one: "not a mistake"), the 13 basics with what each is for and its catch, then Shadw: the AWS static-site stack (5 services, 574 operations) beside this site's own `fluid.json`, and "when you do need AWS".

Step 2g measure: 21 pages at 1280x800, 375x812, 390x844 and 320x640, light and dark: no overflow, no text under 12 px, no target under 44 px.

### Panel, WHOLE, round R1 (verdicts in panel/R1/)
| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
|---|---|---|---|---|
| Critic: Provocateur (Debord) | The Society of the Spectacle (Guy Debord): the number shown in place of the thing; the comparison staged so that only one outcome can be seen | The counting is real (botocore 1.44.1) and the service pages are mostly accurate. The sell turns counts into a show: 436 SDK *APIs* are presented as 436 *services*. Components are listed as alternatives ("11 ways to put a website online"). A custom-domain, CDN-fronted AWS site is set against a Shadw subdomain and called "the same site". "As deployed" and a shadw-mcp URL are stated although shadw.app was never reached. And "1 file" sits beside a build check that requires three config files. | OBJECT | Fix the 10 defects below. Each one is a copy change in `_src/content.py` or `_src/build.py`. |
| Critic: Usability (Krug) | Don't Make Me Think (Steve Krug): five-second test, clear over clever, obvious starting point, self-evident clickables, search that meets expectations | Home reads as "a field guide to AWS", but the main button sends newcomers to the 436-item list rather than the 13 basics, and "Shadw" and "fluid.json" are never explained. The wall's 436 squares are `<i aria-hidden>` with native `title` tooltips only, so nothing appears on touch. The 13 outlined squares can't be clicked. The "one blue Shadw square" is not in the wall at all: it is only a chip in the caption. Searching services.html for "database" (the placeholder's own example) returns 2 results, and A–Z sorts by SDK id, not by the name shown. The 13 rows in the list are not linked. Prev/next and "N of 13" work. File names mix lower and upper case (ec2.html vs DynamoDB.html), so /dynamodb and /Lambda return 404. The path to Shadw is clear and not pushy, but the final off-site button gives no next step. | OBJECT | Items 1-8 below. They are small and mechanical: no redesign needed. |
| Critic: Evidence (Tufte) | The Visual Display of Quantitative Information (Edward Tufte): lie factor, data-ink, graphical integrity, label the data | Every figure checks out against aws.json: 436 services, 19,571 operations, 46 regions in 8 partitions, top 12 total 3,560, IAM 180 ops, ahead of 428. The graphics are less honest than the numbers. EC2's bar is clipped on services.html: lie factor 0.67 at 1280 and 0.50 at 375, where it draws the same length as SageMaker. why.html shrinks EC2 to lie factor 0.93 (0.90 at 375). The 13 basics are hollow, so their quartile is lost. The legend says "darker = more", but in dark mode more is lighter. The quartile breaks are never shown. | OBJECT | Draw the bars on a fixed track scaled by a `--v` ratio. Keep the shade of the basics squares. Label the legend with the operation ranges for each quartile and fix the wording for dark mode. Widen the grey steps. |

#### Resolutions, round R1
| Finding | Resolution |
|---|---|
| Debord: "436 'services' are 436 SDK APIs" | ADAPT: "service APIs" in the hero, nav, why and shadw pages |
| Debord: "'ways to do one thing' counts parts as alternatives" | ADAPT: 5 ways to put a website online; ses/sesv2, Step Functions and IoT Data removed from messaging |
| Debord: "the AWS vs Shadw comparison is not like for like" | ADAPT: "a static site on your own domain, by hand"; "up to five services"; Amplify Hosting named as the fairer comparison; the Shadw side says a shadw.app subdomain, own domain extra |
| Debord: "'1 file' and 'as deployed' overclaim" | ADAPT: "one config file, next to your pages", "as committed", "by that rule" |
| Debord: "unverified shadw-MCP host; build-step claim beyond the evidence" | ADAPT: the link goes to the GitHub repository; "builds run as host processes in your checkout; this site ships prebuilt" |
| Debord: "five AWS description errors" | ADAPT: EFS mount targets per AZ; EBS Multi-Attach; ElastiCache Serverless; global services named; "the ones a beginner meets first" |
| Tufte: "bars not to scale on services and why" | ADAPT: bar widths from a --v ratio on a fixed scale; "bar length is to scale" note |
| Tufte: "the 13 basics lose their shade; legend wrong in dark mode, no ranges, swatches overlap" | ADAPT: double inset outline keeps the shade; "stronger shade"; ranges 1–13, 14–28, 29–59, 60–811 |
| Tufte: "the lightest greys are indistinguishable" | ADAPT: new light and dark ramps (w0 1.9:1 on the page) |
| Tufte: "the alphabetical wall hides the distribution" | ADAPT: largest first |
| Krug: "no Shadw square in the wall; squares unnamed; basics not clickable" | ADAPT: a blue linked cell ends the wall; the 13 basics are links with 44 px hit areas; a live line names the square under hover, focus or touch |
| Krug: "'where do I start' fails" | ADAPT: primary "Start with the 13 basics", then "See all 436", then a text link to Shadw |
| Krug: "Shadw is never explained on the home page" | ADAPT: one clause in the intro |
| Krug: "search placeholder promises categories; A–Z sorts by SDK id" | ADAPT: "name or SDK id"; A–Z by visible name without Amazon/AWS |
| Krug: "the 13 are dead ends in the full list" | ADAPT: linked, with a "basic" tag |
| Krug: "mixed-case file names" | ADAPT: all 13 pages lowercase. DEFERRED: capitalised redirect stubs, which would collide with the lowercase files on case-insensitive filesystems |
| Krug: "'Go to Shadw' leaves no next step" | ADAPT: three steps; "Go to shadw.app →" |

Step 2g re-measure after R1: 21 pages at four sizes, light and dark: no overflow, no text under 12 px, no target under 44 px (the wall's links are 11–18 px squares with 44 px hit areas from ::after, which `measure.cjs` cannot see and so exempts by name); hero bottom 616 at 1280x800 and 800 at 375x812.

### Panel, WHOLE, round R2 (re-check; verdicts in panel/R2/)
| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
|---|---|---|---|---|
| Critic: Provocateur (Debord) | The Society of the Spectacle (Guy Debord): the number shown in place of the thing; the comparison staged so that only one outcome can be seen | 9 of my 10 R1 items are fixed in the live copy: "service APIs" everywhere, honest groups (5 ways to put a site online, 11 to send a message), the comparison relabelled "by hand, on your own domain", Amplify Hosting named as the fairer comparison, "as committed" and "by that rule", the shadw-MCP link moved to the GitHub repository (checked: it exists), the build claim cut back to the evidence, and the five AWS description errors corrected. One item is half fixed: "one file" survives in the home hero and five other places, and the repo still requires vercel.json alongside fluid.json. The new copy adds two claims that EVIDENCE.md does not support: "Your own domain is extra" and "Push the repository" as the deploy step. | OBJECT | Fix the 3 defects below. All are copy changes in `_src/build.py` and `_src/content.py`. |
| Critic: Usability (Krug) | Don't Make Me Think (Steve Krug): five-second test, obvious starting point, clickables that do what they look like | **Fixed:** All R1 items are resolved: the blue Shadw cell ends the wall (437th, links to shadw.html), the 13 basics are links, a live line names squares, "Start with the 13 basics" is the main button, Shadw is defined in the intro, the placeholder is honest, A–Z sorts by visible name, basic rows are linked and tagged, the 13 pages are lowercase with no broken internal links, and the Shadw page has three steps and "Go to shadw.app →". The deferral of capitalised redirect stubs is accepted (the old capitalised URLs only ever existed in the R1 build).<br>**New problem:** the 44 px hit areas added for the basics (`.wall a::after{inset:-13px}`, `-16px` under 860 px) now sit over their grey neighbours. At 1280x800, 78 of the 423 grey squares are covered: hovering SageMaker (2nd square) names it "EC2: 811 operations". At 375x812 with touch, 82 are covered, and Chromium's touch adjustment snaps taps near a link to that link. Tapping squares 1, 5 and 150 (SageMaker, AWS IoT, Lex Model Building) opened ec2.html, iam.html and efs.html, so 3 of the 6 squares sampled at 375 jumped to the wrong page. Only squares far from a basic get named. | OBJECT | **On the wall only, so a tap never lands on a page the visitor did not pick:**<br>- Remove the `::after` inset from `.wall a`.<br>- In `site.js`, have the first tap or hover on any cell, grey or basic, only update the name line (`preventDefault` on the first touch of an `a`).<br>- When the cell is a basic or Shadw, make the name line a link, e.g. "EC2: 811 operations. Open EC2 →", with `min-height:44px`. That link is the 44 px target, and the wall cells no longer need one.<br>- Update `measure.cjs`'s exemption to match.<br>The 13 cards and the nav remain the main ways in. |
| Critic: Evidence (Tufte) | The Visual Display of Quantitative Information (Edward Tufte): lie factor, graphical integrity, the legend must decode the graphic | **Fixed:** bars are now to scale at 1280 and 375, light and dark. On why.html every bar works out to the same px per operation (0.528 at 1280, 0.354 at 375), and services.html is the same (0.118 and 0.069), so EC2, at 811, is no longer clipped. Nothing overflows. The wall is sorted largest first (109 / 109 / 114 / 104 by quartile), and the 437th cell is the blue Shadw cell. The ranges 1–13, 14–28, 29–59, 60–811 match the cuts in aws.json. The new grey ramps can be told apart, and the "stronger shade" wording holds in both themes. **Not fixed:** the 13 basics are now `<a class="wN b">` elements, but the outline rule in `site/css/site.css` line 62 is `.wall i.b`. It no longer matches them (computed box-shadow is `none` in all four views), so the wall shows no basics, yet the legend still shows the outlined swatch. At 375, `.lg-t` and `.one` are hidden (line 184), so the phone legend gives ranges without saying what they count, and the blue cell is never explained. | OBJECT | Change site.css line 62 to `.wall .b,.lg i.b{box-shadow:inset 0 0 0 2px var(--ink),inset 0 0 0 3px var(--paper)}`. Recommended, not blocking: at 375, add "ops" to the ranges (`_src/build.py` line 108: `…{bounds[k + 1] - 1} ops`) and keep a short key for the blue cell (remove `.hero-fig figcaption .one` from site.css line 184, or add a 14px `sh` swatch saying "Shadw: one file"). |

#### Resolutions, round R2
| Finding | Resolution |
|---|---|
| Debord: "'one file' is still on the home page and every service page" | ADAPT: "one config file" everywhere; the Shadw page says the repository's vercel.json is only for Vercel |
| Debord: "'your own domain is extra' is unverified" | ADAPT: removed |
| Debord: "'push the repository' states an unverified trigger" | ADAPT: "deploy the repository to Shadw (for example with shadw-MCP's deploy tool)" |
| Tufte: "the basics lost their outline when they became links" | ADAPT: the rule matches `.wall .b`; checked in the computed style |
| Tufte: "no unit in the phone legend; the blue cell unexplained on phones" | ADAPT: "ops" on each range; a "Shadw: one config file" key on phones |
| Krug: "44 px hit areas cover neighbouring squares; taps open the wrong page" | ADAPT: no enlarged hit areas; a tap, hover or keyboard focus names the square, and for a basic or Shadw the name line becomes a 44 px "Open … →" link; a mouse click still opens directly. Tested on an iPhone 13 emulation and with a mouse |
| Krug: "basics last in search results; '1 operations'" | ADAPT: basics first among matches; singular |

Step 2g re-measure after R2: 21 pages, four sizes, light and dark: no overflow, small text or small target; hero bottom 627 at 1280x800 and 770 at 375x812.
