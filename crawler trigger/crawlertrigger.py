import json
import boto3

glue = boto3.client('glue')


def lambda_handler(event, context):
    print('Event :', event)
    # TODO implement
    response = glue.start_crawler(
        Name='demoserverlesstriggerbasedtechnique'
    )
    print('Response Crawler : ', response)

    return {
        'statusCode': 200,
        'body': json.dumps('Function executed successfully')
    }
