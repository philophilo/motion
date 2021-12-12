import json
import os
import pytest
import boto3

from moto import mock_dynamodb2
from time import time

REGION = os.environ.get('REGION')
DB_TABLE_NAME = os.environ.get('DB_TABLE_NAME')
print('..............................', DB_TABLE_NAME)

@pytest.fixture
def use_moto():
    @mock_dynamodb2
    def dynamodb_client():
        dynamodb = boto3.resource('dynamodb', region_name=REGION)

        # Create the table
        print(">>>>>>>>>>>>>>>>>>>>>>", DB_TABLE_NAME)
        dynamodb.create_table(
            TableName=DB_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        return dynamodb
    return dynamodb_client

@mock_dynamodb2
def test_get_handler(use_moto):
    from motion import handler
    use_moto()
    get_event = {
        'httpMethod': 'GET',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"username": "xyzi", "password": "xyzi"}'
    }

    print(get_event, ">>>>>>>>>>>>>>>>>")
    result = handler(get_event, "")
    print(result)
    assert result['statusCode'] == 400
    body = json.loads(result.get('body'))
    assert body.get('httpMethod') ==  'GET'
    assert body.get('message') == 'The username does not exist'

@mock_dynamodb2
def test_post_handler(use_moto):
    use_moto()
    from motion import handler
    table = boto3.resource('dynamodb', region_name=REGION).Table(DB_TABLE_NAME)
    post_event = {
        'httpMethod': 'POST',
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"username": "user-' + str(int(time())) + '", "password": "xyzi"}'
    }

    result = handler(post_event, "")
    body = json.loads(result['body'])
    assert result.get('statusCode') == 200
    assert result.get('headers') == {'Content-Type': 'application/json'}
    assert body['message'] == {"username": "user-" + str(int(time())), "password": "xyzi"}
