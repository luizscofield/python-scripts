import boto3
import requests
from requests_aws4auth import AWS4Auth

# AWS Profile
AWS_PROFILE = 'aws-profile-name'

# Opensearch Information
host = 'opensearch-url'
region = 'aws-region'
service = 'es'
headers = {"Content-Type": "application/json"}

# AWS authentication
session = boto3.Session(profile_name=AWS_PROFILE)
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def opensearch_request(method='GET', path='/', payload={}):
    url = host + path

    if method == 'GET':
        response = requests.get(url, auth=awsauth, json=payload, headers=headers)
    elif method == 'PUT':
        response = requests.put(url, auth=awsauth, json=payload, headers=headers)
    elif method == 'POST':
        response = requests.post(url, auth=awsauth, json=payload, headers=headers)
    else:
        raise Exception('Method not registered.')
    
    return response