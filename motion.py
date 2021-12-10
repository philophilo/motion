import os
import logging
import boto3
import json


from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

DST_BUCKET = os.environ.get('DST_BUCKET')
REGION = os.environ.get('REGION')

s3 = boto3.resource('s3', region_name=REGION)

# DynamoDB
DB_TABLE_NAME = os.environ.get('DB_TABLE_NAME', 'workmotion_test_users')
DYNAMODB_CLIENT = boto3.resource('dynamodb', region_name=REGION)
DYNAMODB_TABLE = DYNAMODB_CLIENT.Table(DB_TABLE_NAME)

def check_key(data):
    """
    Check if key exists
    """
    response = DYNAMODB_TABLE.query(
            KeyConditionExpression=Key(
                'username').eq(
                    data.get('username'))
            )
    result = response.get('Items')
    if result:
        return response.get('Items')[0]
    else:
        return False

def save_data(data, method):
    """
    Save data to database
    """
    
    try:
        key_exists = check_key(data)
        if not key_exists:
            response = DYNAMODB_TABLE.put_item(Item=data)
            return {"statusCode": 200,
                "headers": headers,
                "body": json.dumps(
                {"headers": headers, "httpMethod": method,"message":data})}
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
            {"headers": headers, "httpMethod": method,
                "message": "The username already exists"})}
        
    except ClientError as e:
        LOGGER.exception(e)
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
            {"headers": headers, "httpMethod": method,
                "message": "make sure to use username and password for keys"})}
    
def get_data(data, method, headers):
    """
    Get data from the database
    """
    
    try:
        key_exists = check_key(data)
        if key_exists:
            return {"statusCode": 200,
                "headers": headers,
                "body": json.dumps({"headers": headers, "httpMethod": method,
                    "message":key_exists})}
            
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"headers": headers, "httpMethod": method,
                "message": "The username does not exist"})}
    except ClientError as e:
        LOGGER.exception(e)
        return {"statusCode": 400,
            "headers": headers,
            "body": json.dumps({"headers": headers, "httpMethod": method,
                "message": "There is no key match"})}
        

def handler(event, context):
    """
    Handle events
    """
    LOGGER.info('Event structure: %s', event)
    LOGGER.info('DST_BUCKET: %s', DST_BUCKET)
    
    if event.get('httpMethod') == "POST":
        result = save_data(json.loads(
            event.get('body')), event.get('httpMethod'))
        return result
    else:
        try:
            result = get_data(
                json.loads(event.get('body')), event.get('httpMethod'),
                event.get('headers'))
            return result
        except TypeError:
            return {
                "statusCode": 400,
                "body": json.dumps('Please provide the username and password')
            }
