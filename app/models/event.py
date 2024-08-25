from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import uuid4


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique event identifier")
    tenant_id: str = Field(default_factory=lambda: str(uuid4()), description="The tenant using the platform")
    product_id: str = Field(..., description="Product ID being viewed or purchased")
    user_id: str = Field(..., description="User ID who triggered the event")
    event_type: str = Field(..., description="Type of event: view or purchase")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the event")
    location: Optional[str] = Field(None, description="Location of the user (if applicable for purchase)")

    def to_dynamodb_item(self):
        item = self.dict()
        # Convert datetime to ISO format string
        item['timestamp'] = item['timestamp'].isoformat() if isinstance(item['timestamp'], datetime) else item['timestamp']
        return item
