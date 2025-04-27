# Creating AMIs for all running instances in an AWS account.

import boto3
from datetime import datetime

# Input variables
AWS_PROFILE = "aws-profile-name"
REGION      = "aws-region"
TICKET      = "ticket-number"

# Internal variables
TODAY_DATE  = datetime.today().strftime('%Y-%m-%d')

# Starting boto3 with a specific aws credentials profile
session = boto3.Session(profile_name=AWS_PROFILE)

# Starting ec2 client
ec2 = session.client('ec2', region_name=REGION)

# Function to get the ID of all running instances
def get_running_instances_ids():
    print("Searching for running instances...")
    # Describe instances and filter only running ones
    response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    # Extract instance IDs
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])

    print(f'Found total of {len(instances)} instances in running state.')

    return instances

# Function to get Name tag of an instance
def get_instance_name(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            tags = instance.get('Tags', [])
            for tag in tags:
                if tag['Key'] == 'Name':
                    return tag['Value']
    # returns instance ID if no Name tag is found
    return instance_id

# Function to create AMI
def create_ami(instance):
    # Get instance name
    instance_name = get_instance_name(instance)

    # Create AMI
    response = ec2.create_image(
        InstanceId=instance,
        Name=f"{TODAY_DATE}-patching-{instance_name}",
        NoReboot=True
    )
    ami_id = response['ImageId']

    # Tag the AMI
    ec2.create_tags(
        Resources =[ami_id],  # Target the AMI ID
        Tags = [
            {"Key": "AT_Ticket", "Value": TICKET},
            {"Key": "AWS_Account", "Value": AWS_PROFILE},
            {"Key": "InstanceName", "Value": instance_name},
            {"Key": "CreationDate", "Value": TODAY_DATE},
            {"Key": "Name", "Value": f"{TODAY_DATE}-patching-{instance_name}"}
        ]
    )

    print(f"AMI created for instance {instance_name}: {ami_id}")

# ----- Running the script -----
instances = get_running_instances_ids()

# Checking full list of instances
print_instances = input('Type (y) to see full list of instances, anything else for not:  ')
if print_instances == "y":
    print("Any instances without the Name tag will have only its ID displayed.")
    for instance in instances:
        name = get_instance_name(instance)
        print(f"{instance} - {name}")

# Confirm before taking snapshots
confirm_snapshot = input('Type (y) to create AMIs for all running instances, or type anything else to abort: ')
if confirm_snapshot == "y":
    for instance in instances:
        create_ami(instance)
else:
    print('Aborted')
