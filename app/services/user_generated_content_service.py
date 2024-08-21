import boto3
from boto3.dynamodb.conditions import Key
from typing import List, Dict, Any
from app.models.user_generated_content import UserGeneratedContent

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb',
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='local',
                          aws_secret_access_key='local',
                          region_name='us-west-2')
table = dynamodb.Table('UserGeneratedContent')


def add_user_generated_content(content: UserGeneratedContent) -> Dict[str, Any]:
    """Adds user-generated content to DynamoDB."""
    item = content.to_dynamodb_item()
    table.put_item(Item=item)
    return item


def update_ugc(content_id: str, updated_content: Dict[str, Any]) -> Dict[str, Any]:
    """Updates an existing user-generated content entry."""
    response = table.update_item(
        Key={'content_id': content_id},
        UpdateExpression="set content_data = :d, user_id = :u, created_at = :c",
        ExpressionAttributeValues={
            ':d': updated_content.get('content_data'),
            ':u': updated_content.get('user_id'),
            ':c': updated_content.get('created_at')
        },
        ReturnValues="UPDATED_NEW"
    )
    return response.get('Attributes')


def get_content_by_content_id(content_id: str) -> List[Dict[str, Any]]:
    """Fetches user-generated content by content_id."""
    response = table.query(
        IndexName='ContentIdIndex',
        KeyConditionExpression=Key('content_id').eq(content_id)
    )
    return response.get('Items', [])


def get_content_by_user(user_id: str) -> List[Dict[str, Any]]:
    """Fetches user-generated content by user_id."""
    response = table.query(
        IndexName='UserIdIndex',
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response.get('Items', [])


def get_content_by_type(content_type: str) -> List[Dict[str, Any]]:
    """Fetches user-generated content by content_type."""
    response = table.query(
        IndexName='ContentTypeIndex',
        KeyConditionExpression=Key('content_type').eq(content_type)
    )
    return response.get('Items', [])
