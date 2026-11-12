# AWS Encyclopedia

**https://awsencyclopedia.shadw.app**

A field guide to Amazon Web Services: all 436 service APIs in the AWS SDK, why AWS is this complicated, the 13
services you meet first, and the shortcut for websites (Shadw: one `fluid.json`). Every number is counted from the
SDK's own models (botocore), never typed.

```bash
python3 _src/build.py                                   # writes site/
python3 -m venv /tmp/v && /tmp/v/bin/pip install botocore && /tmp/v/bin/python _src/fetch_aws.py   # refresh the counts
```

Deployed from `site/` on Shadw and Vercel. Not affiliated with Amazon Web Services. MIT licence.
