from typing import Optional, List
import logging
from datetime import datetime

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
        """
        Create a new user subscription or update existing one
        
        If a subscription with the same mobile number already exists,
        it will update that subscription instead of creating a new one,
        ensuring no duplicate entries.
        """
        # Check if the subscription already exists
        existing_subscription = await UserSubscriptionRepository.get_by_mobile(subscription.mobile_number)
        
        if existing_subscription:
            logger.info(f"Found existing subscription for mobile {subscription.mobile_number}, updating instead of creating new")
            
            # Update the existing subscription
            updated = await UserSubscriptionRepository.update(
                subscription.mobile_number,
                UserSubscriptionUpdate(is_subscribed=subscription.is_subscribed)
            )
            
            if updated:
                return updated
                
            # If update failed for some reason, return the existing subscription
            logger.warning(f"Update failed for subscription {subscription.mobile_number}, returning existing")
            return existing_subscription
        
        # If no existing subscription, create a new one
        logger.info(f"Creating new subscription for mobile {subscription.mobile_number}")
        return await UserSubscriptionRepository.create(subscription)
    
    @staticmethod
    async def update_subscription(mobile_number: str, subscription: UserSubscriptionUpdate) -> Optional[UserSubscription]:
        """Update an existing user subscription"""
        existing = await UserSubscriptionRepository.get_by_mobile(mobile_number)
        if not existing:
            logger.warning(f"Attempted to update non-existent subscription for {mobile_number}")
            return None
            
        return await UserSubscriptionRepository.update(mobile_number, subscription)
    
    @staticmethod
    async def delete_subscription(mobile_number: str) -> bool:
        """Delete a user subscription"""
        existing = await UserSubscriptionRepository.get_by_mobile(mobile_number)
        if not existing:
            logger.warning(f"Attempted to delete non-existent subscription for {mobile_number}")
            return False
            
        return await UserSubscriptionRepository.delete(mobile_number)
        
    @staticmethod
    async def get_all_active_subscriptions() -> List[UserSubscription]:
        """Get all active user subscriptions"""
        return await UserSubscriptionRepository.get_all_active()