from datetime import datetime
from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field
from app.models.notification import Notification


class NotificationBatch(BaseModel):
    batch_id: str = Field(default_factory=lambda: str(uuid4()), description="Batch identifier for a group of "
                                                                            "notifications")
    notifications: List[Notification] = Field(..., description="List of notifications in the batch")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the batch was created")
