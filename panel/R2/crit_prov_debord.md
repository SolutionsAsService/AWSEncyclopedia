| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
|---|---|---|---|---|
| Critic: Provocateur (Debord) | The Society of the Spectacle (Guy Debord): the number shown in place of the thing; the comparison staged so that only one outcome can be seen | 9 of my 10 R1 items are fixed in the live copy: "service APIs" everywhere, honest groups (5 ways to put a site online, 11 to send a message), the comparison relabelled "by hand, on your own domain", Amplify Hosting named as the fairer comparison, "as committed" and "by that rule", the shadw-MCP link moved to the GitHub repository (checked: it exists), the build claim cut back to the evidence, and the five AWS description errors corrected. One item is half fixed: "one file" survives in the home hero and five other places, and the repo still requires vercel.json alongside fluid.json. The new copy adds two claims that EVIDENCE.md does not support: "Your own domain is extra" and "Push the repository" as the deploy step. | OBJECT | Fix the 3 defects below. All are copy changes in `_src/build.py` and `_src/content.py`. |

## Remaining defects

1. **"One file" survives outside shadw.html (R1 item 4, half fixed).**
   File: `_src/build.py`. Line 115: "Your website needs <em>one file</em>." Line 116: "serves a repository from one <code>fluid.json</code> file". Line 122: "<b>fluid.json</b> one file on Shadw →". Line 97: aria-label "Shadw: one file, fluid.json". Line 145 meta: "why a website needs only one file on Shadw". Line 226: "A whole site on Shadw is one file →". Line 248 meta: "deploys on Shadw from one fluid.json file".
   Problem: The pages are files too. `check_deploy()` (lines 286–294) still requires `vercel.json` with `"fluid": true` and `site/vercel.json` alongside fluid.json. Nothing shows Shadw ignores them.
   Replacement: Use "one config file" in each place. For example: "Your website needs <em>one config file</em>." / "serves a folder of pages from one <code>fluid.json</code> config file" / "A whole site on Shadw is one config file →". There are two ways to settle vercel.json: confirm Shadw deploys without it and drop it from `check_deploy`, or name it on shadw.html ("this repo also carries a vercel.json for …").

2. **"Your own domain is extra" claims a feature that has not been verified.**
   File: `_src/content.py` SHADW_FACTS[1].
   Exact: "Each project is served at <code>&lt;name&gt;.shadw.app</code>; by that rule this one is <code>awsencyclopedia.shadw.app</code>. Your own domain is extra."
   Problem: EVIDENCE.md verifies only the `<name>.shadw.app` address. "Extra" implies Shadw supports custom domains, maybe for a fee. That has not been verified.
   Replacement: "… by that rule this one is <code>awsencyclopedia.shadw.app</code>. This guide has not checked custom domains on Shadw."

3. **The new "Three steps" step 3 states a deploy mechanism that has not been verified.**
   File: `_src/build.py` line 244.
   Exact: "Push the repository; by Shadw's rule it is served at <code>&lt;name&gt;.shadw.app</code>."
   Problem: The evidence says only that "a repo with fluid.json deploys to <name>.shadw.app". It does not say that a push alone triggers the deploy. Connecting the repo to Shadw, or calling the shadw-MCP deploy tool, may be needed.
   Replacement: "Deploy the repository to Shadw (for example with shadw-MCP's deploy tool); by Shadw's rule it is served at <code>&lt;name&gt;.shadw.app</code>."

These now pass: R1 items 1, 2, 3, 5, 6, 7, 8, 9 and 10, the home intro clause apart from "one file", three-step items 1 and 2, the "When you do need AWS" section, and "Go to shadw.app →".
