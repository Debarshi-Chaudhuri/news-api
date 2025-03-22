from typing import Optional, List
import logging
from datetime import datetime

from app.db.user_repository import UserSubscriptionRepository
from app.models.user import UserSubscription, UserSubscriptionCreate, UserSubscriptionUpdate
from app.services.event_service import EventService

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
        
        else:
            # First, create or update the user profile in WebEngage
            result = await UserSubscriptionRepository.create(subscription)

            user_id = subscription.mobile_number
            
            await EventService.create_user(
                user_id=user_id,
                phone=subscription.mobile_number,
                sms_opt_in=subscription.is_subscribed,
                email_opt_in=subscription.is_subscribed,
                whatsapp_opt_in=subscription.is_subscribed,
                attributes={
                    "is_subscribed": subscription.is_subscribed,
                    "subscription_created_at": result.created_at.isoformat(),
                    "subscription_updated_at": result.updated_at.isoformat(),
                    "source": "news_api"
                }
            )
            
            # Then track the subscription event
            event_name = "hackathon_user_subscribed" if subscription.is_subscribed else "hackathon_user_unsubscribed"
            
            await EventService.track_event(
                user_id=user_id,
                event_name=event_name,
                event_data={
                    "mobile_number": "91"+subscription.mobile_number,
                    "subscription_status": "active" if subscription.is_subscribed else "inactive",
                    "timestamp": datetime.utcnow().isoformat(),
                    "created_at": result.created_at.isoformat(),
                    "updated_at": result.updated_at.isoformat()
                }
            )
        
        # If no existing subscription, create a new one
        logger.info(f"Creating new subscription for mobile {subscription.mobile_number}")
        return result
    
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