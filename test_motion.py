import json
import os
import unittest
import boto3
import mock

from moto import mock_s3
from moto import mock_dynamodb2
from time import time

from motion import handler



S3_BUCKET_NAME = 'test-bucket-' + str(int(time()))
DEFAULT_REGION = 'us-east-2'
DYNAMODB_TABLE_NAME = 'workmotion_test_users'

@mock_dynamodb2
@mock.patch.dict(os.environ, {'DB_TABLE_NAME': DYNAMODB_TABLE_NAME})
class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        # DynamoDB setup
        self.dynamodb = boto3.client('dynamodb')
        self.get_event = {
                    'httpMethod': 'GET',
                    "headers": {
                        'Content-Type': 'application/json',
                    },
                    'body': '{"username":"xyzi","password":"xyzi"}'
                }
        self.post_event = {
                    'httpMethod': 'POST',
                    'headers': {
                        'Content-Type': 'application/json',
                    },
                    'body': '{"username": "xyzi", "password": "xyzi"}'
                }
        try:
            self.table = self.dynamodb.create_table(
                    TableName=DYNAMODB_TABLE_NAME,
                KeySchema=[
                    {'KeyType': 'HASH', 'AttributeName': 'product'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'product', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
        except self.dynamodb.exceptions.ResourceInUseException:
            self.table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)
    def test_get_handler(self):
        result = handler(self.get_event, {})

        self.assertIn('headers', result)
        self.assertIn('body', result)
        self.assertIn('statusCode', result)

        self.assertEqual(result.get('statusCode'), 400)
        self.assertEqual(result.get('headers'),  {'Content-Type': 'application/json'})
        
        body = json.loads(result.get('body'))
        self.assertEqual(body.get('httpMethod'),  'GET')
        self.assertEqual(body.get('message'),  'The username does not exist')


    def test_post_handler(self):
        result = handler(self.post_event, {})

        self.assertIn('headers', result)
        self.assertIn('body', result)
        self.assertIn('statusCode', result)

        self.assertEqual(result.get('statusCode'), 200)
        self.assertEqual(result.get('headers'),  {'Content-Type': 'application/json'})
