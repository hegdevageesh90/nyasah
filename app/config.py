import os


class Config:
    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'Reviews')
    DYNAMODB_REGION = os.getenv('DYNAMODB_REGION', 'us-west-2')
    DYNAMODB_ENDPOINT_URL = os.getenv('DYNAMODB_ENDPOINT_URL', None)  # Optional, for local development


config = Config()
