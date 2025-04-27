"""
Author:      Luiz Scofield
Date:        01/17/2025
Description: Use this script to delete an Opensearch document.
"""

import boto3
import requests
from requests_aws4auth import AWS4Auth

# Opensearch Information
host = 'opensearch-url'
region = 'aws-region'
service = 'es'

# user
username = "username"
password = "password"

# index and document
index= "index-name"
doc = "document-id"

# Delete doc
path = f'/{index}/_doc/{doc}' # the OpenSearch API endpoint
url = host + path

headers = {"Content-Type": "application/json"}

response = requests.delete(url, auth=(username, password), headers=headers)

print(response.status_code)
print(response.text)