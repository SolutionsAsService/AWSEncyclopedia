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
