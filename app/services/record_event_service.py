import uuid
from datetime import datetime
import boto3
from app.models.event import Event
from app.utils.redis_utils import RedisUtils


class RecordEventService:
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

    def record_view(self, tenant_id: str, product_id: str, user_id: str, timestamp: str = None):
        if not timestamp:
            timestamp = datetime.utcnow()

        view_key = f"{tenant_id}:{product_id}:views"
        event_id = f"{user_id}:{str(uuid.uuid4())}"
        self.redis_utils.zadd(view_key, {event_id: timestamp.timestamp()})

        event = Event(
            tenant_id=tenant_id,
            product_id=product_id,
            user_id=user_id,
            event_type="view",
            timestamp=timestamp
        )
        self.table.put_item(Item=event.to_dynamodb_item())

        return {"status": "success", "message": "View recorded successfully"}

    def record_purchase(self, tenant_id: str, product_id: str, user_id: str, location: str, timestamp: str = None):
        if not timestamp:
            timestamp = datetime.utcnow()

        purchase_key = f"{tenant_id}:{product_id}:purchases"
        event_id = f"{user_id}:{str(uuid.uuid4())}"
        self.redis_utils.zadd(purchase_key, {event_id: timestamp.timestamp()})

        event = Event(
            tenant_id=tenant_id,
            product_id=product_id,
            user_id=user_id,
            location=location,
            event_type="purchase",
            timestamp=timestamp
        )
        self.table.put_item(Item=event.to_dynamodb_item())

        return {"status": "success", "message": "Purchase recorded successfully"}
