import json
import os

from ig import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def list(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_POSTS'])

    # fetch all posts from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "headers": {
          'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
