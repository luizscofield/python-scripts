"""
Author:      Luiz Scofield
Date:        01/17/2025
Description: Use this script to apply an Opensearch Index Policy to existing indices based on name.
"""

import boto3
import requests
from requests_aws4auth import AWS4Auth

# Opensearch Information
host = 'opensearch-url'
region = 'aws-region'
service = 'es'

# AWS authentication
session = boto3.Session(profile_name='aws-profile-name') # AWS Profile
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Index Pattern (contains indices that the policy will be applied to)
index_pattern = "index-pattern"

# Policy
policy = "policy-name"

# Index Settings Endpoint
url = f"{host}/_plugins/_ism/add/{index_pattern}"

# Applying the policy
payload = {
  "policy_id": policy
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, auth=awsauth, json=payload, headers=headers)

print(response.status_code)
print(response.text)