import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')

def create(event, context):
    ts = time.gmtime()
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", ts)
    
    data = json.loads(event['body'])

    if 'text' not in data:
        logging.error('Validation Failed')
        return {'statusCode': 422,
                "headers": {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error_message': 'Couldn\'t create the item.'})}

    if not data['text']:
        logging.error('Validation Failed - text was empty. %s', data)
        return {'statusCode': 422,
                "headers": {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error_message': 'Couldn\'t create the item. As text was empty.'})}

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE_POSTS'])
    id = str(uuid.uuid1())
    item = {
        'id':         id,
        'date':       timestamp,
        'userName':   data['userName'],
        'text':       data['text'],
        'x-array':    data['x-array'],
        'y-array':    data['y-array'],
        'likes':      0,
        'chartType':  data['chartType'],
    }
    
    # write the post to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "headers": {
          'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(item)
    }

    return response
