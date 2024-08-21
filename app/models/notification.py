from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4
from pydantic import BaseModel, Field
from app.models.notification_status import NotificationStatus
from app.models.notification_type import NotificationType
from app.models.urgency_level import UrgencyLevel


class Notification(BaseModel):
    notification_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the "
                                                                                   "notification")
    user_id: str = Field(..., description="The user to whom the notification is targeted")
    content: str = Field(..., description="Content of the notification")
    notification_type: NotificationType = Field(..., description="The type of notification (e.g., email, real-time, "
                                                                 "SMS, etc.)")
    status: NotificationStatus = Field(default=NotificationStatus.PENDING, description="Current status of the "
                                                                                       "notification")
    urgency: UrgencyLevel = Field(default=UrgencyLevel.MEDIUM, description="Level of urgency of the notification")
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict, description="Additional metadata related to the "
                                                                                 "notification")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the notification was "
                                                                              "created")
    sent_at: Optional[datetime] = Field(None, description="Timestamp when the notification was sent")
    delivered_at: Optional[datetime] = Field(None, description="Timestamp when the notification was delivered")
    retries: int = Field(default=0, description="The number of retries attempted to send the notification")
    is_read: bool = Field(default=False, description="Whether the notification has been read (for real-time "
                                                     "notifications)")
