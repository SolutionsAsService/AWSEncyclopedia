#!/usr/bin/env python3
"""Regenerate _src/data/aws.json from the AWS SDK's own service models (botocore).

    python3 -m venv /tmp/v && /tmp/v/bin/pip install botocore && /tmp/v/bin/python _src/fetch_aws.py

Every count on the site comes from this file: services are the API models botocore ships, operations are the
operations in each model, regions are the regions in botocore's endpoint data. Nothing is typed by hand.
"""
import datetime, json, os, pathlib
import botocore, botocore.session

s = botocore.session.get_session()
services = []
for n in s.get_available_services():
    m = s.get_service_model(n)
    services.append({"id": n, "full": m.metadata.get("serviceFullName"), "ops": len(m.operation_names)})
ep = json.load(open(os.path.join(os.path.dirname(botocore.__file__), "data", "endpoints.json")))
parts = [{"partition": p["partition"], "name": p.get("partitionName"), "regions": sorted(p["regions"])} for p in ep["partitions"]]
out = {"botocore": botocore.__version__, "fetched": datetime.date.today().isoformat(), "services": services, "partitions": parts}
pathlib.Path(__file__).with_name("data").joinpath("aws.json").write_text(json.dumps(out, indent=1) + "\n")
print(f"botocore {botocore.__version__}: {len(services)} services, {sum(x['ops'] for x in services)} operations")
