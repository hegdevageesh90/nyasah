import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
from decimal import Decimal


class UserGeneratedContent(BaseModel):
    content_id: str = uuid.uuid4().hex
    user_id: str
    content_type: str  # e.g., 'review', 'comment'
    content_data: Optional[Dict[str, Any]] = None  # Flexible storage for content
    created_at: str = datetime.utcnow().isoformat()

    def to_dynamodb_item(self):
        """Converts the Pydantic model to a DynamoDB-compatible dictionary."""
        return {
            'content_id': self.content_id,
            'user_id': self.user_id,
            'content_type': self.content_type,
            'content_data': self.content_data or {},
            'created_at': self.created_at
        }

    @staticmethod
    def from_dynamodb_item(item: Dict[str, Any]) -> 'UserGeneratedContent':
        return UserGeneratedContent(
            content_id=item.get('content_id'),
            user_id=item.get('user_id'),
            content_type=item.get('content_type'),
            content_data=item.get('content_data'),
            created_at=item.get('created_at')
        )
