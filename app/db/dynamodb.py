import logging
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)
dynamodb_client = None
dynamodb_resource = None

def get_dynamodb_client():
    return dynamodb_client

def get_dynamodb_resource():
    return dynamodb_resource

def init_dynamodb():
    global dynamodb_client, dynamodb_resource
    try:
        # Set up connection parameters for DynamoDB
        dynamodb_config = {
            'endpoint_url': settings.DYNAMODB_ENDPOINT,
            'region_name': settings.AWS_REGION,  # Always include region
        }
        
        # Only add AWS credentials if we're connecting to a real AWS instance
        if not settings.USE_LOCAL_DYNAMODB:
            dynamodb_config.update({
                'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
                'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            })
        else:
            # For local DynamoDB, add dummy credentials
            dynamodb_config.update({
                'aws_access_key_id': 'dummy',
                'aws_secret_access_key': 'dummy'
            })
        
        # Initialize the DynamoDB client and resource
        dynamodb_client = boto3.client('dynamodb', **dynamodb_config)
        dynamodb_resource = boto3.resource('dynamodb', **dynamodb_config)
        
        logger.info("Connected to DynamoDB")
        return dynamodb_client, dynamodb_resource
    except Exception as e:
        logger.error(f"Error connecting to DynamoDB: {e}")
        raise e

async def create_user_subscriptions_table_if_not_exists():
    """Create the UserSubscriptions table if it doesn't exist"""
    client = get_dynamodb_client()
    
    # Check if table exists
    try:
        client.describe_table(TableName=settings.USER_SUBSCRIPTIONS_TABLE)
        logger.info(f"Table {settings.USER_SUBSCRIPTIONS_TABLE} already exists")
        return
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            logger.error(f"Error checking if table exists: {e}")
            raise e
    
    # Table doesn't exist, create it
    try:
        client.create_table(
            TableName=settings.USER_SUBSCRIPTIONS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'mobile_number',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'mobile_number',
                    'AttributeType': 'S'  # String type
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # On-demand capacity mode
        )
        logger.info(f"Created table: {settings.USER_SUBSCRIPTIONS_TABLE}")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise e