import boto3
import time
import requests
from datetime import datetime

# Initialazing boto3 for a specific aws credentials profile
session = boto3.Session(profile_name='aws-profile-name')

inspector = session.client('inspector')

template_arns = [
    "arn-of-template-1", # Example: CIS/SBP Assessment Template
    "arn-of-template-2" # Example: CVE Assessment Template
]

for index, template_arn in enumerate(template_arns):

    if index == 0:
        print('Searching through the CIS/SBP assessment runs...')
    elif index == 1:
        print('Searching through the CVE assessment runs...')

    assessment_runs_arns = []
    next_token = None

    while True:
        # Listing the runs, can't list more than 10 at a time, 
        if next_token:
            response = inspector.list_assessment_runs(
                assessmentTemplateArns=[template_arn],
                nextToken=next_token
            )
        else:
            response = inspector.list_assessment_runs(
                assessmentTemplateArns=[template_arn]
            )

        describe_response = inspector.describe_assessment_runs(
            assessmentRunArns=response['assessmentRunArns']
        )

        runs = describe_response['assessmentRuns']

        for run in runs:
            arn = run['arn']
            _date = run['createdAt']

            run_info = {
                'arn' : arn,
                'date': _date
            }

            assessment_runs_arns.append(run_info)

        # Checking if there are more runs, if not, breaking the loop
        next_token = response.get('nextToken')
        if not next_token:
            break

    most_recent_run = max(assessment_runs_arns, key=lambda x: x['date'])

    print(f'Found the most recent accessment run!\nARN: {most_recent_run['arn']}\nDATE: {most_recent_run['date']}')
    print('Generating findings report...')

    # Generating report

    response = inspector.get_assessment_report(
        assessmentRunArn=most_recent_run['arn'],
        reportFileFormat='PDF',
        reportType='FINDING'
    )
    status = response['status']

    # Checking if the report is already generated
    while status != 'COMPLETED':
        if status == 'FAILED':
            print("Report generation failed.")
            break
        print(f"Report generation in progress... Current status: {status}")
        time.sleep(5)  

        response = inspector.get_assessment_report(
            assessmentRunArn=most_recent_run['arn'],
            reportFileFormat='PDF',
            reportType='FINDING'
        )
        status = response['status']
        report_url = response['url']

    # Downloading the report once it is generated successfully
    if status == 'COMPLETED':

        #The generated report becomes available on a temporary S3 URL hosted by AWS
        report_url = response['url']
        report_content = requests.get(report_url).content

        # Setting the PDF file name
        current_date = datetime.now()
        formatted_date = current_date.strftime("%m%d%y")

        if index == 0:
            FILE = f'inspector_{formatted_date}_cissbp.pdf'
        elif index == 1:
            FILE = f'inspector_{formatted_date}_cve.pdf'

        with open(FILE, "wb") as file:
            file.write(report_content)

        if index == 0:
            print('CIS/SBP report downloaded successfully!')
        elif index == 1:
            print('CVE report downloaded successfully!')