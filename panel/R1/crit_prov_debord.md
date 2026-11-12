| Critic | Anchor used | Observed in the work | Verdict PASS/OBJECT | Requested change |
|---|---|---|---|---|
| Critic: Provocateur (Debord) | The Society of the Spectacle (Guy Debord): the number shown in place of the thing; the comparison staged so that only one outcome can be seen | The counting is real (botocore 1.44.1) and the service pages are mostly accurate. The sell turns counts into a show: 436 SDK *APIs* are presented as 436 *services*. Components are listed as alternatives ("11 ways to put a website online"). A custom-domain, CDN-fronted AWS site is set against a Shadw subdomain and called "the same site". "As deployed" and a shadw-mcp URL are stated although shadw.app was never reached. And "1 file" sits beside a build check that requires three config files. | OBJECT | Fix the 10 defects below. Each one is a copy change in `_src/content.py` or `_src/build.py`. |

## Defects

1. **The 436 APIs are called "services" (this inflates the headline number).**
   File: `_src/build.py` (build_home, NAV, build_why, build_shadw, build_start, 404).
   Exact: "Every square is one AWS service, counted from Amazon's own SDK" / "<b>436</b> services in the SDK, each its own API" / nav "All 436 services" / why.html "436 services, 19,571 operations." / shadw.html "you do not need 436 services".
   Problem: The data has 436 models but only 432 distinct full names. ses/sesv2 and the split data-plane, runtime, read and write APIs (for example timestream-write, iot-data) are counted separately. services.html admits this ("this counts APIs, not products"), but the home page, nav and why.html do not.
   Replacement: Use "service APIs" wherever the 436 figure appears. For example: "Every square is one AWS service API, counted from Amazon's own SDK" and "<b>436</b> service APIs in the SDK (some products have more than one)". The nav would read "All 436 APIs". On why.html: "436 service APIs, 19,571 operations."

2. **"Ways to do one thing" lists components and unrelated tools as alternatives.**
   File: `_src/content.py` GROUPS, rendered by `_src/build.py` build_why as "{n} ways to {label}".
   Exact: "11 ways to put a website online" (it includes route53, acm, apigateway, codepipeline, codebuild). "14 ways to send a message" includes ses *and* sesv2 (one product), stepfunctions (workflow orchestration) and iot-data. "12 ways to run your code" includes sagemaker, gamelift and emr-serverless, which are specialist platforms.
   Problem: Route 53, ACM, CodeBuild and CodePipeline are not ways to put a site online. They are parts you combine. Counting them as rival options inflates the "too many choices" argument.
   Replacement: Remove `route53`, `acm`, `apigateway`, `codepipeline` and `codebuild` from the website group. That leaves "6 ways to put a website online": s3, cloudfront, amplify, lightsail, elasticbeanstalk, apprunner. Also remove `sesv2` (or `ses`) and `stepfunctions` from the message group. Alternatively, change the heading template to "{n} services involved in {label}" and the lede to "For each everyday job, several services are involved, some as alternatives and some as parts you combine."

3. **The AWS-vs-Shadw comparison is not like for like.**
   File: `_src/build.py` build_shadw (and build_home "Or skip all of it").
   Exact: "A static site on AWS" [S3, CloudFront, Route 53, ACM, IAM] "5 services · 574 API operations to learn your way around" vs "The same site on Shadw … 1 file".
   Problem: The AWS column includes a custom domain (Route 53), a custom-domain certificate (ACM) and a global CDN (CloudFront). The Shadw column serves `<name>.shadw.app`. Nothing in EVIDENCE.md says Shadw offers a custom domain or a CDN, so this is not "the same site". Nobody learns 574 API operations to host pages. AWS's closest equivalent, Amplify Hosting (connect a repo, get HTTPS at `*.amplifyapp.com`), is left out entirely.
   Replacement: Rename the AWS column "A static site on your own domain, wired by hand on AWS". Replace the count line with "5 services to configure (574 API operations between them; the console hides most)". Rename the Shadw column "This site on Shadw, at awsencyclopedia.shadw.app". Below both, add: "AWS also has a shorter path: Amplify Hosting connects a repository and serves it over HTTPS. The comparison above is the hand-built route the S3 docs describe."

4. **The "1 file" claim conflicts with the repo's own deploy config.**
   File: `_src/build.py` build_shadw / build_home; `_src/content.py` SHADW_FACTS[0].
   Exact: "1 file · this site's own fluid.json, as deployed" / "On Shadw this whole site deploys from one small file" / "Your website needs one file."
   Problem: `check_deploy()` fails the build unless `vercel.json` (with `"fluid": true`), `site/vercel.json` *and* `fluid.json` are present. The site also needs its folder of pages. EVIDENCE.md verifies only that "a repo with fluid.json deploys"; it does not verify that fluid.json alone is enough.
   Replacement: Either (a) show that Shadw deploys with only fluid.json and drop the vercel.json requirement, or (b) change the copy to "a folder of pages plus one config file, fluid.json" and the hero to "Your website needs <em>one config file</em>." If the vercel.json files are needed by Shadw, say so.

5. **"As deployed" and "This one is awsencyclopedia.shadw.app" assert a deployment nobody verified.**
   File: `_src/content.py` SHADW_FACTS[0], SHADW_FACTS[1]; `_src/build.py` build_shadw.
   Exact: "This site's is printed above, exactly as deployed." / "This one is <code>awsencyclopedia.shadw.app</code>." / "this site's own <code>fluid.json</code>, as deployed".
   Problem: EVIDENCE.md says "shadw.app itself was not reachable from the build machine".
   Replacement: "This site's own fluid.json is printed above, exactly as committed." / "By that rule, this one is served at <code>awsencyclopedia.shadw.app</code>." / "1 config file · this site's own <code>fluid.json</code>, as committed". Restore "as deployed" only after the URL has been fetched successfully.

6. **The shadw-MCP link points at an unverified host.**
   File: `_src/content.py` SHADW_FACTS[3].
   Exact: `The <a href="https://shadw-mcp.shadw.app">shadw-MCP</a> server gives an AI agent fifteen tools…`
   Problem: shadw.app was unreachable, so this URL is unverified. The verified source is the portfolio repository.
   Replacement: Link to the verified portfolio/source location of shadw-MCP, or drop the link: "The shadw-MCP server (in the same portfolio) gives an AI agent fifteen tools to deploy a project, check its health and roll it back."

7. **"Needs no build step at all" goes beyond the evidence.**
   File: `_src/content.py` SHADW_FACTS[2].
   Exact: "Shadw runs builds as plain processes in your checkout, so a site that is already built needs no build step at all."
   Problem: The evidence covers only "builds run as host processes in the checkout". It says nothing about skipping builds.
   Replacement: "Shadw runs builds as plain processes in your checkout, not in a separate build image."

8. **Straw man on the Shadw page header.**
   File: `_src/build.py` build_shadw.
   Exact: "If what you want is a website online, you do not need 436 services. You need a folder of pages and one file."
   Problem: No AWS user needs 436 services for a website. The site itself names 5.
   Replacement: "If what you want is a website online, you do not need to wire five AWS services together. You need a folder of pages and a fluid.json."

9. **S3 page overstates what a static site requires.**
   File: `_src/content.py` SERVICES[s3]["web"] (also echoed in build_home "you would wire S3, CloudFront, Route 53, a certificate and IAM together").
   Exact: "Hosting a static site well takes S3, CloudFront, Route 53, a certificate from ACM and IAM permissions for each: five services."
   Problem: Route 53 is optional, because any DNS provider works. Amplify Hosting or Lightsail can do the job as a single service.
   Replacement: "The hand-built route for a static site on your own domain is S3 and CloudFront, with a certificate from ACM, DNS (Route 53 or any provider) and IAM permissions: up to five services. Amplify Hosting packages this as one."
   For the home page: "To put a website online on AWS by hand you would wire S3, CloudFront, a certificate, DNS and IAM together."

10. **Errors in the AWS service descriptions.**
    - `_src/content.py` SERVICES[efs]["catch"]: "Mount targets per subnet, …". A mount target is created per Availability Zone, one per AZ in a subnet you choose. Replace with: "A mount target in each Availability Zone, security groups, throughput modes and storage classes."
    - `_src/content.py` SERVICES[ebs]["what"]: "virtual disks attached to one EC2 server." io1/io2 Multi-Attach allows several instances. Replace with: "Elastic Block Store: virtual disks attached to an EC2 instance (usually one at a time; io1/io2 volumes can be multi-attached)."
    - `_src/content.py` SERVICES[elasticache]["catch"]: "Node types, clusters, replication and a VPC to reach it from." This ignores ElastiCache Serverless, which has no node types to pick. Replace with: "Serverless or node-based, clusters and replication, and a VPC to reach it from."
    - `_src/build.py` build_why §03: "Resources live in a region, …". IAM, Route 53 and CloudFront are global. Replace with: "Most resources live in a region (IAM, Route 53 and CloudFront are global), and regions are grouped into partitions that do not share accounts". Optionally add: "most people only ever use the 34 in AWS Standard."
    - `_src/build.py` build_start lede: "these are the services almost every AWS account touches." This is not true of ElastiCache, EFS, Elastic Beanstalk or SNS. Replace with: "these are the services a beginner meets first."

These descriptions were checked and are accurate: EC2 (per-second billing is broadly correct, and its API is the largest at 811 operations), Lambda, DynamoDB, RDS engine list, IAM, SNS, SQS, CloudFront (the certificate must be in us-east-1), Elastic Beanstalk, and the EBS direct API note. The WHY_FAIR paragraph and the "When you do need AWS" section are fair and should stay.
