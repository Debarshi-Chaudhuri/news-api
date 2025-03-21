from datetime import datetime
from typing import Optional, List
import logging
from botocore.exceptions import ClientError

from app.db.dynamodb import get_dynamodb_resource
from app.core.config import settings
from app.models.user import UserSubscription, UserSubscriptionCreate, UserSubscriptionUpdate

logger = logging.getLogger(__name__)

class UserSubscriptionRepository:
    @staticmethod
    async def get_by_mobile(mobile_number: str) -> Optional[UserSubscription]:
        """Get a user subscription by mobile number"""
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(settings.USER_SUBSCRIPTIONS_TABLE)
        
        try:
            response = table.get_item(
                Key={'mobile_number': mobile_number}
            )
            
            item = response.get('Item')
            if not item:
                return None
                
            return UserSubscription(
                mobile_number=item['mobile_number'],
                is_subscribed=item['is_subscribed'],
                created_at=datetime.fromisoformat(item['created_at']),
                updated_at=datetime.fromisoformat(item['updated_at'])
            )
            
        except Exception as e:
            logger.error(f"Error getting user subscription: {e}")
            raise
    
    @staticmethod
    async def create(subscription: UserSubscriptionCreate) -> UserSubscription:
        """Create a new user subscription"""
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(settings.USER_SUBSCRIPTIONS_TABLE)
        
        now = datetime.utcnow().isoformat()
        
        try:
            # Check if the subscription already exists
            existing = await UserSubscriptionRepository.get_by_mobile(subscription.mobile_number)
            
            if existing:
                # Update the existing subscription
                return await UserSubscriptionRepository.update(
                    subscription.mobile_number,
                    UserSubscriptionUpdate(is_subscribed=subscription.is_subscribed)
                )
            
            # Create a new item
            item = {
                'mobile_number': subscription.mobile_number,
                'is_subscribed': subscription.is_subscribed,
                'created_at': now,
                'updated_at': now
            }
            
            table.put_item(Item=item)
            
            return UserSubscription(
                mobile_number=subscription.mobile_number,
                is_subscribed=subscription.is_subscribed,
                created_at=datetime.fromisoformat(now),
                updated_at=datetime.fromisoformat(now)
            )
            
        except Exception as e:
            logger.error(f"Error creating user subscription: {e}")
            raise
    
    @staticmethod
    async def update(mobile_number: str, subscription: UserSubscriptionUpdate) -> Optional[UserSubscription]:
        """Update an existing user subscription"""
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(settings.USER_SUBSCRIPTIONS_TABLE)
        
        now = datetime.utcnow().isoformat()
        
        try:
            # Check if the subscription exists
            existing = await UserSubscriptionRepository.get_by_mobile(mobile_number)
            if not existing:
                return None
            
            # Build the update expression
            update_expr = "SET updated_at = :updated_at"
            expr_attr_values = {
                ':updated_at': now
            }
            
            # Add is_subscribed to the update if it's provided
            if subscription.is_subscribed is not None:
                update_expr += ", is_subscribed = :is_subscribed"
                expr_attr_values[':is_subscribed'] = subscription.is_subscribed
            
            # Perform the update
            table.update_item(
                Key={'mobile_number': mobile_number},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues='ALL_NEW'
            )
            
            # Get the updated item
            return await UserSubscriptionRepository.get_by_mobile(mobile_number)
            
        except Exception as e:
            logger.error(f"Error updating user subscription: {e}")
            raise
    
    @staticmethod
    async def delete(mobile_number: str) -> bool:
        """Delete a user subscription"""
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(settings.USER_SUBSCRIPTIONS_TABLE)
        
        try:
            # Check if the subscription exists
            existing = await UserSubscriptionRepository.get_by_mobile(mobile_number)
            if not existing:
                return False
            
            # Delete the item
            table.delete_item(
                Key={'mobile_number': mobile_number}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user subscription: {e}")
            raise
            
    @staticmethod
    async def get_all_active() -> List[UserSubscription]:
        """Get all active user subscriptions"""
        dynamodb = get_dynamodb_resource()
        table = dynamodb.Table(settings.USER_SUBSCRIPTIONS_TABLE)
        
        try:
            # Query for active subscriptions
            response = table.scan(
                FilterExpression="is_subscribed = :is_subscribed",
                ExpressionAttributeValues={
                    ":is_subscribed": True
                }
            )
            
            items = response.get("Items", [])
            
            # Convert to UserSubscription objects
            subscriptions = []
            for item in items:
                subscription = UserSubscription(
                    mobile_number=item["mobile_number"],
                    is_subscribed=item["is_subscribed"],
                    created_at=datetime.fromisoformat(item["created_at"]),
                    updated_at=datetime.fromisoformat(item["updated_at"])
                )
                subscriptions.append(subscription)
                
            return subscriptions
            
        except Exception as e:
            logger.error(f"Error getting active subscriptions: {e}")
            raise