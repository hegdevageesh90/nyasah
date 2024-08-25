from datetime import datetime, timedelta
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key

from app.utils.redis_utils import RedisUtils


class NotificationService:
    def __init__(self, redis_utils: RedisUtils):
        self.redis_utils = redis_utils
        self.dynamodb_resource = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8000',
            aws_access_key_id='local',
            aws_secret_access_key='local',
            region_name='us-west-2'
        )
        self.table = self.dynamodb_resource.Table("EventTable")

    def get_view_notification(self, tenant_id: str, product_id: str, start_time: Optional[str] = None,
                              end_time: Optional[str] = None):
        view_key = f"{tenant_id}:{product_id}:views"

        # If a time range is provided, handle the filtering accordingly
        if start_time and end_time:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            views = self.redis_utils.zrangebyscore(view_key, start_time.timestamp(), end_time.timestamp())
        else:
            default_start_time = datetime.utcnow() - timedelta(minutes=1)
            views = self.redis_utils.zrangebyscore(view_key, default_start_time.timestamp(),
                                                   datetime.utcnow().timestamp())

        if not views:
            views = self.fetch_views_from_dynamodb(tenant_id, product_id, start_time, end_time)

        return {"message": f"{views} people are viewing this product right now"}

    def get_purchase_notification(self, tenant_id: str, product_id: str, start_time: Optional[str] = None,
                                  end_time: Optional[str] = None):
        purchase_key = f"{tenant_id}:{product_id}:purchases"

        if start_time and end_time:
            start_time = datetime.fromisoformat(start_time)
            end_time = datetime.fromisoformat(end_time)
            purchases = self.redis_utils.zrangebyscore(purchase_key, start_time.timestamp(), end_time.timestamp())
        else:
            default_start_time = datetime.utcnow() - timedelta(days=1)
            purchases = self.redis_utils.zrangebyscore(purchase_key, default_start_time.timestamp(),
                                                       datetime.utcnow().timestamp())

        if not purchases:
            purchases = self.fetch_purchases_from_dynamodb(tenant_id, product_id, start_time, end_time)

        return {"message": f"{purchases} people have bought this product"}

    def fetch_views_from_dynamodb(self, tenant_id: str, product_id: str, start_time: Optional[str] = None,
                                  end_time: Optional[str] = None) -> int:
        """Fetch view counts from DynamoDB within the specified time range."""
        key_condition = Key('tenant_id').eq(tenant_id) & Key('product_id').eq(product_id)

        if start_time and end_time:
            filter_expression = Key('event_type').eq('view') & Key('timestamp').between(start_time, end_time)
        else:
            filter_expression = Key('event_type').eq('view')

        response = self.table.query(
            IndexName='TenantProductIndex',
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expression
        )

        items = response.get('Items', [])
        if not isinstance(items, list):
            raise TypeError(f"Expected list for 'Items', got {type(items).__name__}")

        return len(items)

    def fetch_purchases_from_dynamodb(self, tenant_id: str, product_id: str, start_time: Optional[str] = None,
                                      end_time: Optional[str] = None) -> int:
        """Fetch purchase counts from DynamoDB within the specified time range."""
        key_condition = Key('tenant_id').eq(tenant_id) & Key('product_id').eq(product_id)

        if start_time and end_time:
            filter_expression = Key('event_type').eq('purchase') & Key('timestamp').between(start_time, end_time)
        else:
            filter_expression = Key('event_type').eq('purchase')

        response = self.table.query(
            IndexName='TenantProductIndex',
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expression
        )

        items = response.get('Items', [])
        if not isinstance(items, list):
            raise TypeError(f"Expected list for 'Items', got {type(items).__name__}")

        return len(items)
