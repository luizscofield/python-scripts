"""
Author:      Luiz Scofield
Date:        01/17/2025
Description: Use this script to create an AWSV4 authentication signature for Opensearch requests.
"""

from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# AWS Credentials 
AWS_ACCESS_KEY = "access-key"
AWS_SECRET_KEY = "secret-key"
AWS_REGION = "aws-region"  # Change this to your OpenSearch region
SERVICE = "es"

# AWS Authentication Signature V4
aws_auth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, SERVICE)

# URL
OPENSEARCH_HOST = "opensearch-url"
OPENSEARCH_PORT = "443"

# Testing
client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=aws_auth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

info = client.info()
print(info)
