import json
import logging
import httpx
import uuid
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)

# DTOs for Event Service
class CreateEventRequest(BaseModel):
    """Request model for creating a single event"""
    userId: str
    eventName: str
    eventTime: Optional[str] = None  # ISO-8601 format
    eventData: Optional[Dict[str, Any]] = {}

class CreateUserRequest(BaseModel):
    """Request model for creating/updating a user"""
    userId: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = {}
    smsOptIn: Optional[bool] = None
    emailOptIn: Optional[bool] = None
    whatsappOptIn: Optional[bool] = None

class EventClient:
    """Client for event tracking service"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not EventClient._initialized:
            self._initialize_client()
            EventClient._initialized = True
    
    def _initialize_client(self):
        """Initialize the HTTP client with configuration"""
        self.base_url = settings.EVENT_API_BASE_URL
        self.account_id = settings.EVENT_ACCOUNT_ID
        self.license_code = settings.EVENT_LICENSE_CODE

        self.api_timeout = 30.0  # seconds
        
        # Create client with default headers
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.api_timeout,
            headers={
                "Authorization": f"Bearer {settings.EVENT_ACCOUNT_ID}",
                "Content-Type": "application/json"
            }
        )
        
        # Enable debug in development environments
        self.debug = settings.DEBUG
        logger.info("Event client initialized")
    
    def _get_events_endpoint(self) -> str:
        """Get the events endpoint URL"""
        return f"/v1/accounts/{self.license_code}/events"
    
    def _get_users_endpoint(self) -> str:
        """Get the users endpoint URL"""
        return f"/v1/accounts/{self.license_code}/users"
    
    @staticmethod
    def _get_request_id() -> str:
        """Generate a random hex string for request ID"""
        return uuid.uuid4().hex
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def create_event(self, user_id: str, event_name: str, event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a single event
        
        Args:
            user_id: ID of the user
            event_name: Name of the event
            event_data: Additional event data/attributes
            
        Returns:
            Response from the event service
        """
        # ISO-8601 format with timezone info
        event_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+0000")
        
        request_data = CreateEventRequest(
            userId=user_id,
            eventName=event_name,
            eventTime=event_time,
            eventData=event_data or {}
        )
        
        request_id = self._get_request_id()
        
        try:
            endpoint = self._get_events_endpoint()
            
            if self.debug:
                logger.debug(f"Event API Request: POST {endpoint}")
                logger.debug(f"Request data: {request_data.dict()}")
            
            # Prepare curl command for debugging
            curl_command = f"""
            curl -X POST \\
              '{self.base_url}{endpoint}' \\
              -H 'Content-Type: application/json' \\
              -H 'x-request-id: {request_id}' \\
              -d '{json.dumps(request_data.dict())}'
            """
            logger.debug(f"Equivalent curl command: {curl_command}")
                
            # Make the actual request
            response = await self.client.post(
                endpoint,
                json=request_data.dict(),
                headers={"x-request-id": request_id}
            )
            
            if response.status_code >= 400:
                error_data = response.json() if response.text else {"message": "Empty response"}
                logger.error(f"Event API error: {error_data}")
                return {
                    "success": False,
                    "message": error_data.get("message", f"Error {response.status_code}"),
                    "status_code": response.status_code
                }
            
            result = response.json() if response.text else {"success": True}
            
            if self.debug:
                logger.debug(f"Event API Response: {result}")
                
            return {
                "success": True,
                "data": result,
                "status_code": response.status_code
            }
            
        except Exception as e:
            logger.exception(f"Error creating event: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    async def create_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a user
        
        Args:
            user_id: ID of the user
            user_data: User attributes and opt-in preferences
            
        Returns:
            Response from the event service
        """
        # Create request with user_id and other data
        request_data = CreateUserRequest(
            userId=user_id,
            **user_data
        )
        
        request_id = self._get_request_id()
        
        try:
            endpoint = self._get_users_endpoint()
            
            if self.debug:
                logger.debug(f"User API Request: POST {endpoint}")
                logger.debug(f"Request data: {request_data.dict(exclude_none=True)}")
            
            # Prepare request data for logging
            request_json = request_data.dict(exclude_none=True)
            
            # Log the equivalent curl command for debugging
            curl_command = f"curl -X POST '{self.base_url}{endpoint}' \\\n"
            curl_command += f"  -H 'Authorization: Bearer {self.account_id}' \\\n"
            curl_command += f"  -H 'Content-Type: application/json' \\\n"
            curl_command += f"  -H 'x-request-id: {request_id}' \\\n"
            curl_command += f"  -d '{request_json}'"
            

            logger.debug(f"Equivalent curl command:\n{curl_command}")
            
            # Make the actual request
            response = await self.client.post(
                endpoint,
                json=request_json,
                headers={"x-request-id": request_id}
            )
            
            if response.status_code >= 400:
                error_data = response.json() if response.text else {"message": "Empty response"}
                logger.error(f"User API error: {error_data}")
                return {
                    "success": False,
                    "message": error_data.get("message", f"Error {response.status_code}"),
                    "status_code": response.status_code
                }
            
            result = response.json() if response.text else {"success": True}
            
            if self.debug:
                logger.debug(f"User API Response: {result}")
                
            return {
                "success": True,
                "data": result,
                "status_code": response.status_code
            }
            
        except Exception as e:
            logger.exception(f"Error creating/updating user: {e}")
            return {
                "success": False,
                "message": str(e)
            }


class EventService:
    """Service for handling events"""
    
    # Class-level client that will be shared across all method calls
    _client = None
    
    @classmethod
    def initialize(cls):
        """Initialize the event client for the service"""
        if cls._client is None:
            cls._client = EventClient()
            logger.info("EventService initialized with global client")
    
    @classmethod
    async def shutdown(cls):
        """Close the event client"""
        if cls._client is not None:
            await cls._client.close()
            cls._client = None
            logger.info("EventService client closed")
    
    @classmethod
    async def track_event(cls, user_id: str, event_name: str, event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Track a single event
        
        Args:
            user_id: ID of the user (typically the mobile number in our implementation)
            event_name: Name of the event
            event_data: Additional event data/attributes
            
        Returns:
            Response indicating success or failure
        """
        if cls._client is None:
            cls.initialize()
        
        return await cls._client.create_event(user_id, event_name, event_data)
    
    @classmethod
    async def create_user(cls, user_id: str, first_name: Optional[str] = None, 
                         last_name: Optional[str] = None, phone: Optional[str] = None,
                         email: Optional[str] = None, sms_opt_in: Optional[bool] = None,
                         email_opt_in: Optional[bool] = None, 
                         whatsapp_opt_in: Optional[bool] = None,
                         attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create or update a user profile
        
        Args:
            user_id: ID of the user (typically the mobile number)
            first_name: User's first name
            last_name: User's last name  
            phone: User's phone number
            email: User's email address
            sms_opt_in: SMS opt-in status
            email_opt_in: Email opt-in status
            whatsapp_opt_in: WhatsApp opt-in status
            attributes: Additional user attributes
            
        Returns:
            Response indicating success or failure
        """
        if cls._client is None:
            cls.initialize()
        
        # Prepare user data
        user_data = {
            "firstName": first_name,
            "lastName": last_name,
            "phone": phone,
            "email": email,
            "smsOptIn": sms_opt_in,
            "emailOptIn": email_opt_in,
            "whatsappOptIn": whatsapp_opt_in,
            "attributes": attributes or {}
        }
        
        # Remove None values
        user_data = {k: v for k, v in user_data.items() if v is not None}
        
        return await cls._client.create_user(user_id, user_data)