import boto3


glue = boto3.client('glue')


def lambda_handler(event, context):
    response = glue.start_job_run(JobName="demoserverless")
    print("Lambda Invoke")
