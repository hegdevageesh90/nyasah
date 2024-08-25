from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, HttpUrl, Field


class Tenant(BaseModel):
    tenant_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique tenant identifier")
    website_address: HttpUrl = Field(..., description="Website address of the tenant")
    purchase_notification_message: str = Field(..., description="Message to display for purchase notifications")
    view_notification_message: str = Field(..., description="Message to display for view notifications")
    subscribed_for: List[str] = Field(..., description="List of subscribed events like view, purchase, UGC, reviews")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(),
                            description="Timestamp of tenant registration")

    class Config:
        schema_extra = {
            "example": {
                "tenant_id": "b57e8d94-3a0f-43d7-b8c2-9f9e6c2f1b58",
                "website_address": "https://example.com",
                "purchase_notification_message": "X people have bought this product.",
                "view_notification_message": "Y people are viewing this product right now.",
                "subscribed_for": ["view", "purchase", "ugc", "reviews"]
            }
        }
