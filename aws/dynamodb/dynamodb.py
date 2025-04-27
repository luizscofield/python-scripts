# Checking if all DynamoDB tables are global tables and have point in time recovery

import boto3

# Input variables
AWS_PROFILE = "aws-profile-name"
REGION      = "aws-region"

# Static variables
FILE = "dynamodb.csv"

# Creating csv file
#with open(FILE, 'w') as file:
#    file.write('Table Name, Global Table, Replication Region, Point-in-Time Recovery\n')

# Starting boto3 with a specific aws credentials profile
session = boto3.Session(profile_name=AWS_PROFILE)

# Starting DynamoDB client
dynamodb_client = session.client('dynamodb', region_name=REGION)

# Get all tables
tables = []
response = dynamodb_client.list_tables()

while True:
    tables.extend(response['TableNames'])  # Add tables to the list
    
    # Check if there are more tables to fetch
    if 'LastEvaluatedTableName' in response:
        response = dynamodb_client.list_tables(ExclusiveStartTableName=response['LastEvaluatedTableName'])
    else:
        break

# Check if each table is a global table
for table_name in tables:
    if table_name == "Audits-6df34b8c-64af-4849-a734-ed405bfbc61b":
        print(dynamodb_client.describe_continuous_backups(TableName=table_name))
    """
    response = dynamodb_client.describe_table(TableName=table_name)
    
    # A table is global if it has the "Replicas" key with one or more items
    replicas = response['Table'].get('Replicas', [])
    
    if len(replicas) > 0:
        global_table = True
        regions = []
        for replica in replicas:
            regions.append(replica['RegionName'])
    else:
        global_table = False
        regions = 'N/A'

    # Check if Point-in-Time Recovery (PITR) is enabled
    backup_response = dynamodb_client.describe_continuous_backups(TableName=table_name)
    backup_status = backup_response['ContinuousBackupsDescription']['PointInTimeRecoveryDescription']['PointInTimeRecoveryStatus']
    
    # Writing to CSV file
    with open(FILE, 'a') as file:
        file.write(f'{table_name}, {'yes' if global_table == True else 'no'}, {regions}, {backup_status}\n')
    """