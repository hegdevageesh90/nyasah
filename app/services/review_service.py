import boto3
from boto3.dynamodb.conditions import Key
from typing import List, Dict, Any

from app.models.review import Review

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='local',
                          aws_secret_access_key='local',
                          region_name='us-west-2')
table = dynamodb.Table('Reviews')


def add_review(review: Review) -> Dict[str, Any]:
    """Adds a review to DynamoDB."""
    # Convert the model instance to a DynamoDB-compatible dictionary
    item = review.to_dynamodb_item()

    # Store the item in DynamoDB
    table.put_item(Item=item)

    return item


def get_reviews_by_product(product_id: str) -> List[Dict[str, Any]]:
    """Fetches reviews by product_id."""
    response = table.query(
        IndexName='ProductIndex',
        KeyConditionExpression=Key('product_id').eq(product_id)
    )
    return response.get('Items', [])


def get_reviews_by_source(source: str) -> List[Dict[str, Any]]:
    """Fetches reviews by source."""
    response = table.query(
        IndexName='SourceIndex',
        KeyConditionExpression=Key('source').eq(source)
    )
    return response.get('Items', [])
