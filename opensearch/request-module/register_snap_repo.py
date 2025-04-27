from elk_request import opensearch_request

# S3 bucket information
bucket = "dr-workbench-opensearch-snaps"
bucket_path = "snapshots"
role_arn = "arn:aws:iam::194103089011:role/opensearch_s3_role"
region = 'us-west-2'

# Register repository
path = f'/_snapshot/{bucket}'

payload = {
  "type": "s3",
  "settings": {
    "bucket": bucket,
    "base_path": bucket_path,
    "region": region,
    "role_arn": role_arn,
    "server_side_encryption": True,
    "canned_acl": None
  }
}

response = opensearch_request(method='PUT', path=path, payload=payload)