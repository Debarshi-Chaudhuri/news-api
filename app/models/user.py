from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserSubscription(BaseModel):
    mobile_number: str
    is_subscribed: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserSubscriptionCreate(BaseModel):
    mobile_number: str
    is_subscribed: bool = True

class UserSubscriptionUpdate(BaseModel):
    is_subscribed: Optional[bool] = None