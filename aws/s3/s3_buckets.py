# Checking if all buckets inside an AWS account have the backup tag and versioning enabled

import boto3

# Input variables
AWS_PROFILE = "aws-profile-name"
REGION      = "aws-region"

# Static variables
FILE = "s3.csv"

# Starting boto3 with a specific aws credentials profile
session = boto3.Session(profile_name=AWS_PROFILE)

# Starting S3 client
s3_client = session.client('s3')

# Get buckets
response = s3_client.list_buckets()

with open(FILE, 'w') as file:
    file.write('Bucket Name, Backup Tag, Versioning\n')

# Getting details of each bucket
for bucket in response['Buckets']:
    bucket_name = bucket['Name']

    # Checking if versioning is enabled
    try:
        response = s3_client.get_bucket_versioning(Bucket=bucket_name)
        versioning_status = response.get('Status', 'Disabled')

    except s3_client.exceptions.ClientError as e:
        print(f"Error checking versioning for {bucket_name}: {e}")

    # Checking bakup tag
    try:
        response = s3_client.get_bucket_tagging(Bucket=bucket_name)

        for tag in response['TagSet']:
            if tag['Key'] == 'backup':
                backup_tag_exists = True
                backup_tag_value = tag['Value']

    except s3_client.exceptions.ClientError as e:
        # In case no tags are present
        if e.response['Error']['Code'] == 'NoSuchTagSet':
            backup_tag_value = 'Tag Not Present'
        else:
            print(f"error - {bucket_name}: {e}")

    if not backup_tag_exists:
        backup_tag_value = 'Tag Not Present'

    with open(FILE, 'a') as file:
        file.writelines(f'{bucket_name}, {backup_tag_value}, {versioning_status}\n')