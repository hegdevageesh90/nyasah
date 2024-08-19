import boto3
from app.config import config


def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        region_name=config.DYNAMODB_REGION,
        endpoint_url=config.DYNAMODB_ENDPOINT_URL
    )


def get_reviews_table():
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(config.DYNAMODB_TABLE_NAME)
