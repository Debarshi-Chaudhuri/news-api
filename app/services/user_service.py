from typing import Optional, List
import logging

from app.db.user_repository import UserSubscriptionRepository
from app.models.user import UserSubscription, UserSubscriptionCreate, UserSubscriptionUpdate

logger = logging.getLogger(__name__)

class UserSubscriptionService:
    @staticmethod
    async def get_subscription(mobile_number: str) -> Optional[UserSubscription]:
        """Get a user subscription by mobile number"""
        return await UserSubscriptionRepository.get_by_mobile(mobile_number)
    
    @staticmethod
    async def create_subscription(subscription: UserSubscriptionCreate) -> UserSubscription:
        """Create a new user subscription"""
        return await UserSubscriptionRepository.create(subscription)
    
    @staticmethod
    async def update_subscription(mobile_number: str, subscription: UserSubscriptionUpdate) -> Optional[UserSubscription]:
        """Update an existing user subscription"""
        return await UserSubscriptionRepository.update(mobile_number, subscription)
    
    @staticmethod
    async def delete_subscription(mobile_number: str) -> bool:
        """Delete a user subscription"""
        return await UserSubscriptionRepository.delete(mobile_number)