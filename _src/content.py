"""Words for the AWS Encyclopedia. Every number comes from _src/data/aws.json (the AWS SDK's own models), never from here."""

SITE = "AWS Encyclopedia"
SHADW_URL = "https://shadw.app"

# Ways to do one thing. Each id must exist in the SDK data; the build fails if one does not.
GROUPS = [
    ("run your code", ["ec2", "lambda", "ecs", "eks", "lightsail", "elasticbeanstalk", "apprunner", "batch", "amplify", "emr-serverless", "sagemaker", "gamelift"]),
    ("store your data", ["s3", "dynamodb", "rds", "docdb", "neptune", "redshift", "elasticache", "memorydb", "keyspaces", "timestream-write", "opensearch", "efs", "fsx", "glacier", "dsql", "s3tables"]),
    ("send a message", ["sqs", "sns", "events", "kinesis", "firehose", "mq", "kafka", "pipes", "pinpoint", "ses", "scheduler"]),
    ("put a website online", ["s3", "amplify", "lightsail", "elasticbeanstalk", "apprunner"]),
]

# The services a beginner meets first. file: the page (old URLs kept); id: the SDK model.
SERVICES = [
    {"file": "ec2.html", "id": "ec2", "short": "EC2", "kind": "Compute",
     "what": "Virtual servers you rent by the second. You choose the size, the operating system and the network, and you look after everything on it.",
     "use": "Anything that needs a full computer: a long-running app server, a game server, a build machine.",
     "catch": "You own the server: patches, scaling, backups, and the security group that decides who can reach it. Its API is the largest in AWS.",
     "web": "A static website does not need a server at all."},
    {"file": "s3.html", "id": "s3", "short": "S3", "kind": "Storage",
     "what": "Object storage: files (“objects”) in named “buckets”, reached by URL or API, stored across several data centres.",
     "use": "Uploads, backups, logs, data for analytics, and the files of static websites.",
     "catch": "A bucket is private by default; making a website public means bucket policies, Block Public Access settings and usually CloudFront in front for HTTPS on your own domain.",
     "web": "By hand, a static site on your own domain uses up to five services: S3, CloudFront, a certificate from ACM, DNS (Route 53 or any other) and IAM permissions. Amplify Hosting bundles most of that into one service."},
    {"file": "lambda.html", "id": "lambda", "short": "Lambda", "kind": "Compute",
     "what": "Functions that run when something happens (a web request, a file upload, a message) without a server you manage. You pay per request and per millisecond.",
     "use": "Small pieces of backend logic, glue between services, scheduled jobs.",
     "catch": "Each function needs an IAM role, a trigger and limits (time, memory); a web API usually adds API Gateway or a function URL. Debugging spans CloudWatch logs.",
     "web": "Not needed for a site that is only pages."},
    {"file": "dynamodb.html", "id": "dynamodb", "short": "DynamoDB", "kind": "Database",
     "what": "A key-value and document database that scales without servers. You design tables around the questions you will ask.",
     "use": "High-traffic apps with simple, predictable lookups.",
     "catch": "You must plan access patterns and keys up front; questions you did not plan for are slow or expensive.",
     "web": "Only if your site stores data."},
    {"file": "rds.html", "id": "rds", "short": "RDS", "kind": "Database",
     "what": "Managed relational databases: PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, IBM Db2, and Amazon Aurora.",
     "use": "Apps that need SQL, joins and transactions.",
     "catch": "You still choose instance sizes, storage, backups, Multi-AZ, networking (a VPC and subnets) and maintenance windows.",
     "web": "Only if your site stores data."},
    {"file": "iam.html", "id": "iam", "short": "IAM", "kind": "Security",
     "what": "Identity and Access Management: users, roles and JSON policies that say who may do what to which resource.",
     "use": "Every AWS account, from the first day.",
     "catch": "Every service has its own actions to allow or deny, and a wrong policy is either a security hole or an access-denied error. IAM's own API has more operations than most services.",
     "web": "Needed the moment you use any of the others."},
    {"file": "sns.html", "id": "sns", "short": "SNS", "kind": "Messaging",
     "what": "Simple Notification Service: publish one message, deliver it to many subscribers (queues, functions, email, SMS, HTTP).",
     "use": "Fan-out: one event, many reactions.",
     "catch": "Delivery retries, filters and permissions per subscriber; easy to confuse with SQS and EventBridge.",
     "web": "Not needed for a site that is only pages."},
    {"file": "sqs.html", "id": "sqs", "short": "SQS", "kind": "Messaging",
     "what": "Simple Queue Service: a queue that holds messages until a worker takes them.",
     "use": "Smoothing out bursts of work and decoupling parts of an app.",
     "catch": "Standard or FIFO, visibility timeouts, dead-letter queues: each choice changes how failures behave.",
     "web": "Not needed for a site that is only pages."},
    {"file": "cloudfront.html", "id": "cloudfront", "short": "CloudFront", "kind": "Delivery",
     "what": "A content delivery network: copies of your files served from locations near your visitors, with HTTPS.",
     "use": "Speed and HTTPS in front of S3, load balancers or any origin.",
     "catch": "Distributions, origins, behaviours, cache policies, invalidations, and a certificate that must live in us-east-1.",
     "web": "The usual front door for an S3 site."},
    {"file": "beanstalk.html", "id": "elasticbeanstalk", "short": "Elastic Beanstalk", "kind": "Compute",
     "what": "AWS Elastic Beanstalk: upload an app and it creates the servers, load balancer and scaling for you, on EC2.",
     "use": "Running a familiar web app (Node, Python, Java, …) without wiring every piece by hand.",
     "catch": "The pieces it creates are still yours to pay for and understand when something breaks.",
     "web": "More than a static site needs."},
    {"file": "elasticache.html", "id": "elasticache", "short": "ElastiCache", "kind": "Database",
     "what": "Managed in-memory caches (Valkey, Redis OSS, Memcached).",
     "use": "Making reads fast and taking load off a database.",
     "catch": "Node types, clusters and replication (ElastiCache Serverless hides those), and a VPC to reach it from.",
     "web": "Not needed for a site that is only pages."},
    {"file": "efs.html", "id": "efs", "short": "EFS", "kind": "Storage",
     "what": "Elastic File System: a shared network file system many servers can mount at once.",
     "use": "Files shared between EC2 instances, containers or functions.",
     "catch": "A mount target per Availability Zone, security groups, throughput modes and storage classes.",
     "web": "Not needed for a site that is only pages."},
    {"file": "ebs.html", "id": "ebs", "short": "EBS", "kind": "Storage",
     "what": "Elastic Block Store: virtual disks for EC2 servers, usually attached to one (io1 and io2 volumes can attach to several).",
     "use": "The hard drive of an EC2 instance; snapshots for backup.",
     "catch": "Volume types, sizes, IOPS and snapshots. Most EBS actions live in the EC2 API; the separate EBS API reads and writes snapshot data directly.",
     "web": "Only if you run servers."},
]
OLD_URLS = {"lamda.html": "lambda.html"}  # the old site's misspelt page

WHY_FAIR = ("This complexity is not a mistake. AWS serves banks, streaming services and space agencies, and each "
            "service exists because some customer needed exactly that. The cost lands on everyone else: to put a few "
            "pages online, you meet the same menu.")

SHADW_FACTS = [
    ("One config file", "A Shadw project is a repository with a <code>fluid.json</code> that names the project and the folder of pages to serve. This site's is printed above, as committed."),
    ("A predictable address", "Each project is served at <code>&lt;name&gt;.shadw.app</code>; by that rule this one is <code>awsencyclopedia.shadw.app</code>."),
    ("Built where it lives", "Shadw runs builds as host processes in your checkout. This site ships its pages already built, in <code>site/</code>."),
    ("Deploy, check, roll back", "The <a href=\"https://github.com/SolutionsAsService/shadw-MCP\">shadw-MCP</a> server gives an AI agent fifteen tools to deploy a project, check its health and roll it back."),
]
