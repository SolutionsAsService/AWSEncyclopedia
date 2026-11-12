| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
|---|---|---|---|---|
| Critic: Evidence (Tufte) | The Visual Display of Quantitative Information (Edward Tufte): lie factor, data-ink, graphical integrity, label the data | Every figure checks out against aws.json: 436 services, 19,571 operations, 46 regions in 8 partitions, top 12 total 3,560, IAM 180 ops, ahead of 428. The graphics are less honest than the numbers. EC2's bar is clipped on services.html: lie factor 0.67 at 1280 and 0.50 at 375, where it draws the same length as SageMaker. why.html shrinks EC2 to lie factor 0.93 (0.90 at 375). The 13 basics are hollow, so their quartile is lost. The legend says "darker = more", but in dark mode more is lighter. The quartile breaks are never shown. | OBJECT | Draw the bars on a fixed track scaled by a `--v` ratio. Keep the shade of the basics squares. Label the legend with the operation ranges for each quartile and fix the wording for dark mode. Widen the grey steps. |

1. **Verified figures (PASS).** I checked these with Python against `_src/data/aws.json`:
   - 436 services, all with unique ids and a full name.
   - 19,571 operations.
   - 46 regions, all distinct: 34 aws + 2 cn + 2 us-gov + 2 iso + 2 iso-b + 1 iso-e + 2 iso-f + 1 eusc.
   - Top 12: ec2 811, sagemaker 414, connect 404, glue 314, quicksight 301, iot 272, datazone 195, iam 180, bedrock-agentcore-control 172, rds 168, cloudfront 167, lightsail 162. They total 3,560, which matches why.html.
   - IAM has 180 ops, ranks #8 and is ahead of 428 services, so "more than 428 of the 436" is correct.
   - Quartile cuts are 14, 29 and 60. The bins hold 104, 114, 109 and 109 services, which is balanced enough to be honest.
   - The "12 ways to run your code" figure is a hand-picked list (`K.GROUPS[0]`), not something computed. It is acceptable as editorial content.
2. **services.html: EC2's bar is cut short (lie factor 0.67 / 0.50).** The bar width is a % of the 9rem cell, but `site/css/site.css` caps it at `max-width:6rem` on line 117 and `3.5rem` on line 162. Measured at 1280, EC2 draws at 96px where 144px would be true. At 375, ec2, sagemaker and connect all draw at about 56px, so 811, 414 and 404 look equal. Fix:
   - In `_src/build.py` lines 141 and 143, replace `style="width:{w:.1f}%"` with `style="--v:{s["ops"]/MAXOPS:.4f}"`.
   - In site.css line 117, change `.s-ops .bar{flex:none;max-width:6rem}` to `.s-ops .bar{flex:none;width:calc(var(--v)*6rem)}`.
   - In site.css line 162, change `max-width:3.5rem` to `.s-ops .bar{width:calc(var(--v)*3.5rem)}`.
   - Keep `min-width:2px` on line 116 so services with 1 operation stay visible.
3. **why.html: EC2's bar shrinks (lie factor 0.93 at 1280, 0.90 at 375).** `.b-v .bar` keeps the default `flex-shrink:1`. The longest bar, at 100%, gives way to make room for the number beside it: it draws at 451px where 484px would be true, and at 310px where 343px would be. Fix:
   - In `_src/build.py` line 160, emit `style="--v:{s["ops"]/MAXOPS:.4f}"`.
   - In site.css line 126, use `.b-v .bar{height:14px;flex:none;width:calc(var(--v)*(100% - 3.5rem))}`.
4. **The wall erases the data for the 13 basics.** `site/css/site.css` line 62 sets `.wall i.b{...;background:var(--paper)}`. The basics are 9 top-quartile services, 3 in the third quartile and EBS in the first, and every one is drawn as an empty box, so the most important squares carry no value. Fix: on line 62, delete `background:var(--paper)` and use `box-shadow:inset 0 0 0 2px var(--ink),inset 0 0 0 3px var(--paper)` so the ring sits over the quartile shade.
5. **The basics legend swatch misleads.** `_src/build.py` line 111 draws `<i class="w2 b"></i>`, which suggests the basics share one shade. Once fix 4 is in, change it to `<i class="w3 b"></i>`, so it shows a ring over a shade. Most basics are in the top quartile.
6. **The legend is wrong in dark mode.** `_src/build.py` line 111 says "darker = more API operations". The dark palette (site.css lines 12 and 13) runs `--w0:#2b2e34` to `--w3:#9aa0aa`, so in dark mode more is *lighter*, as the 1280-dark screenshot shows. Fix: change the wording to "stronger shade = more API operations". Better still, see fix 7.
7. **The legend has no numbers, so the reader cannot decode the quartiles.** Label each swatch with its range, computed from `CUTS` (build.py line 39). Today that reads: 1–13, 14–28, 29–59, 60–811 ops. In build.py line 111, emit `<span class="lg"><i class="w0"></i>1–{CUTS[0]-1}</span>` and so on for each bin. Also delete `.lg i+i{margin-left:-6px}` at site.css line 165. That rule makes the four swatches overlap into one strip, so no single shade can be read on its own.
8. **The lowest grey steps are hard to tell apart.**
   - Light mode: paper→w0 is 1.25:1 (L* 95.5→87.0), so a fourth of the wall almost disappears into the page. The steps after that are 1.42, 1.65 and 1.96.
   - Dark mode: paper→w0 is 1.37:1.
   - Fix (site.css line 10, light): `--w0:#b4b2aa;--w1:#8f9096;--w2:#6b6f77;--w3:#40444c`. That gives L* 72/60/47/29, 1.9:1 against paper for w0, and steps of 1.5/1.6/1.9.
   - Fix (site.css lines 12 and 13, dark): `--w0:#4a4e56;--w1:#6c717b;--w2:#9196a0;--w3:#c3c8d0`. That gives 2.2:1 against paper for w0 and steps of 1.7/1.65/1.8.
9. **The wall's order hides the distribution (recommended, not blocking).** `_src/build.py` line 89 draws `SV`, which is in alphabetical order by id, so the shading reads as salt-and-pepper noise. Drawing it by rank, using `sorted(SV, key=lambda s: (-s["ops"], s["id"]))`, shows the long tail at a glance. You can see 109 heavy services, then 109 lighter, 114, and 104. That is the "too complicated" argument shown in the picture itself. Alphabetical order adds nothing, because the wall is `aria-hidden` and has no labels.
10. **services.html ranks EC2 in its own text but not in its bars.** Once fix 2 is in, the bars are true to scale. Also add the scale reference to the note on build.py line 145: "bar length to scale; longest = EC2, 811".
