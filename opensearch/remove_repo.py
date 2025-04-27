"""
Author:      Luiz Scofield
Date:        01/16/2025
Description: Use this script to remove an Opensearch Snapshot repository.
"""

import boto3
import requests
from requests_aws4auth import AWS4Auth

# Opensearch Information
host = 'opensearch-url'
region = 'aws-region'
service = 'es'

# Repository name
repo_name = "my-snapshot-repo-name"

# AWS authentication
session = boto3.Session(profile_name='aws-profile-name') # AWS Profile
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# API endpoint
url = f"{host}/_snapshot/{repo_name}"

# Make the DELETE request
response = requests.delete(url, auth=awsauth)

print(response.status_code)
print(response.text)