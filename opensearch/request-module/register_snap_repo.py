from elk_request import opensearch_request

# S3 bucket information
bucket = "bucket-name"
bucket_path = "snapshots"
role_arn = "arn-of-role-with-access-to-bucket"
region = 'aws-region'

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