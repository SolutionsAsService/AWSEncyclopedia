# R1 evidence: AWS Encyclopedia (rebuilt from scratch)
- Brief (owner): make it pretty; explain why AWS is too complicated by showing all the services; then tell people to use Shadw anyway and link to it.
- Site: /home/user/awsencyclopedia/site/, served at http://localhost:8769/site/ (Playwright: require('playwright')). 21 pages.
- Source: _src/build.py (pages), _src/content.py (all copy), _src/data/aws.json (botocore 1.44.1: 436 service models, 19,571 operations, 46 regions in 8 partitions), site/css/site.css, site/js/site.js (search and sort).
- Design intent: DESIGN-LOG.md. Screenshots here: <page>-1280.png and <page>-375.png.
- measure.json: every page at 1280x800, 375x812, 390x844, 320x640, light and dark: no overflow, no text under 12 px, no target under 44 px.
- Shadw facts the site may state (verified in this project): a repo with fluid.json deploys to <name>.shadw.app; builds run as host processes in the checkout; the shadw-MCP server (portfolio) has 15 tools to deploy, check health and roll back. shadw.app itself was not reachable from the build machine.
