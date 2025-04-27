"""
Author:      Luiz Scofield
Date:        01/16/2025
Description: Use this script to register an S3 bucket as an Opensearch Snapshot repository.
"""

import boto3
import requests
from requests_aws4auth import AWS4Auth

# Opensearch Information
host = 'opensearch-url'
region = 'aws-region'
service = 'es'

# S3 bucket information
bucket = "bucket-name"
bucket_path = "snapshots"
role_arn = "arn-of-role-with-access-to-bucket"

# AWS authentication
session = boto3.Session(profile_name='aws-profile-name') # AWS Profile
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Register repository
path = f'/_snapshot/{bucket}' # the OpenSearch API endpoint
url = host + path

payload = {
  "type": "s3",
  "settings": {
    "bucket": bucket,
    "base_path": bucket_path,
    "region": region,
    "role_arn": role_arn
  }
}

headers = {"Content-Type": "application/json"}

response = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(response.status_code)
print(response.text)