import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
from decimal import Decimal  # Import Decimal


class Review(BaseModel):
    review_id: str = uuid.uuid4().hex
    product_id: str
    user_id: str
    rating: float
    source: str  # e.g., 'internal', 'google'
    review_data: Optional[Dict[str, Any]] = None  # Flexible storage for external reviews
    created_at: str = datetime.utcnow().isoformat()

    def to_dynamodb_item(self):
        """Converts the Pydantic model to a DynamoDB-compatible dictionary."""
        return {
            'review_id': self.review_id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'rating': Decimal(str(self.rating)),  # Convert float to Decimal
            'source': self.source,
            'review_data': self.review_data or {},
            'created_at': self.created_at
        }
