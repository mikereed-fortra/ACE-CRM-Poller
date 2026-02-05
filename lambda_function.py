import json
import boto3
import os
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the Partner Central Selling client
# The API is available in us-east-1 region
partner_central_client = boto3.client('partnercentral-selling', region_name='us-east-1')

def lambda_handler(event, context):
    """
    Lambda function handler for processing Engagement Invitation Created events.
    
    This function is triggered by EventBridge when an "Engagement Invitation Created" 
    event is received from aws.partnercentral-selling.
    
    Args:
        event: EventBridge event containing the engagement invitation details
        context: Lambda context object
        
    Returns:
        dict: Response with statusCode and body
    """
    
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract event details
        source = event.get('source')
        detail_type = event.get('detail-type')
        detail = event.get('detail', {})
        
        # Validate event source and type
        if source != 'aws.partnercentral-selling':
            logger.warning(f"Unexpected event source: {source}")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid event source'})
            }
        
        if detail_type != 'Engagement Invitation Created':
            logger.warning(f"Unexpected event type: {detail_type}")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid event detail-type'})
            }
        
        # Log the invitation details
        engagement_invitation_id = detail.get('engagementInvitationId')
        engagement_id = detail.get('engagementId')
        logger.info(f"Processing Engagement Invitation Created: InvitationId={engagement_invitation_id}, EngagementId={engagement_id}")
        
        # Get the catalog from environment variable or default to 'AWS'
        catalog = os.environ.get('CATALOG', 'AWS')
        
        # Call ListEngagements API
        logger.info(f"Calling ListEngagements API with catalog: {catalog}")
        engagements_response = list_engagements(catalog)
        
        # Log the results
        engagement_count = len(engagements_response.get('EngagementSummaryList', []))
        logger.info(f"Successfully retrieved {engagement_count} engagements")
        
        # Process the engagements (you can add custom logic here)
        process_engagements(engagements_response, engagement_id)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully processed Engagement Invitation Created event',
                'engagementInvitationId': engagement_invitation_id,
                'engagementId': engagement_id,
                'engagementsRetrieved': engagement_count
            })
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS API Error: {error_code} - {error_message}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error calling AWS Partner Central API',
                'error': error_message
            })
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal error processing event',
                'error': str(e)
            })
        }


def list_engagements(catalog, max_results=100):
    """
    Call the ListEngagements API to retrieve engagements.
    
    Args:
        catalog: The catalog to query (e.g., 'AWS' or 'Sandbox')
        max_results: Maximum number of results to return
        
    Returns:
        dict: Response from ListEngagements API
    """
    
    all_engagements = []
    next_token = None
    
    try:
        # Paginate through all engagements
        while True:
            params = {
                'Catalog': catalog,
                'MaxResults': max_results
            }
            
            if next_token:
                params['NextToken'] = next_token
            
            response = partner_central_client.list_engagements(**params)
            
            engagements = response.get('EngagementSummaryList', [])
            all_engagements.extend(engagements)
            
            logger.info(f"Retrieved {len(engagements)} engagements in this page")
            
            # Check if there are more results
            next_token = response.get('NextToken')
            if not next_token:
                break
        
        return {
            'EngagementSummaryList': all_engagements,
            'TotalCount': len(all_engagements)
        }
        
    except ClientError as e:
        logger.error(f"Error calling ListEngagements: {e}")
        raise


def process_engagements(engagements_response, related_engagement_id=None):
    """
    Process the retrieved engagements.
    
    This is a placeholder for custom business logic. You can:
    - Filter engagements based on criteria
    - Find the specific engagement related to the invitation
    - Store engagement data in a database
    - Send notifications
    - Update external systems
    
    Args:
        engagements_response: Response from ListEngagements API
        related_engagement_id: The engagement ID from the event (optional)
    """
    
    engagement_summaries = engagements_response.get('EngagementSummaryList', [])
    
    logger.info(f"Processing {len(engagement_summaries)} engagements")
    
    # Find the engagement related to this invitation if engagement_id was provided
    if related_engagement_id:
        matching_engagement = None
        for engagement in engagement_summaries:
            if engagement.get('Id') == related_engagement_id:
                matching_engagement = engagement
                break
        
        if matching_engagement:
            logger.info(f"Found matching engagement: {json.dumps(matching_engagement)}")
            logger.info(f"Engagement Title: {matching_engagement.get('Title')}")
            logger.info(f"Member Count: {matching_engagement.get('MemberCount')}")
            logger.info(f"Created At: {matching_engagement.get('CreatedAt')}")
        else:
            logger.warning(f"Engagement {related_engagement_id} not found in list")
    
    # Log summary information about all engagements
    for engagement in engagement_summaries:
        logger.debug(f"Engagement: ID={engagement.get('Id')}, Title={engagement.get('Title')}, Members={engagement.get('MemberCount')}")
    
    # Add your custom processing logic here
    # Examples:
    # - Store engagements in DynamoDB
    # - Send SNS notifications
    # - Update a CRM system
    # - Trigger additional workflows
    
    return True
