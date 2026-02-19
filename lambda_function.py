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
    Lambda function handler for processing AWS Billing events.
    
    This function is triggered by EventBridge when any event is received 
    from aws.billing source.
    
    Args:
        event: EventBridge event containing the billing event details
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
        
        # Validate event source - must be from AWS Billing
        if source != 'aws.billing':
            logger.warning(f"Unexpected event source: {source}. Expected 'aws.billing'")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid event source. Expected aws.billing'})
            }
        
        # Log the event details (generic for any billing event type)
        logger.info(f"Processing AWS Billing event: DetailType={detail_type}, Source={source}")
        logger.info(f"Event detail: {json.dumps(detail)}")
        
        # Get the catalog from environment variable or default to 'AWS'
        catalog = os.environ.get('CATALOG', 'AWS')
        
        # Call ListEngagements API
        logger.info(f"Calling ListEngagements API with catalog: {catalog}")
        engagements_response = list_engagements(catalog)
        
        # Log the results
        engagement_count = len(engagements_response.get('EngagementSummaryList', []))
        logger.info(f"Successfully retrieved {engagement_count} engagements")
        
        # Process the engagements with the billing event details
        process_engagements(engagements_response, detail_type, detail)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully processed AWS Billing event',
                'source': source,
                'detailType': detail_type,
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


def process_engagements(engagements_response, detail_type=None, event_detail=None):
    """
    Process the retrieved engagements.
    
    This is a placeholder for custom business logic. You can:
    - Filter engagements based on criteria
    - Correlate billing events with engagements
    - Store engagement data in a database
    - Send notifications
    - Update external systems
    
    Args:
        engagements_response: Response from ListEngagements API
        detail_type: The detail-type of the billing event (optional)
        event_detail: The detail payload of the billing event (optional)
    """
    
    engagement_summaries = engagements_response.get('EngagementSummaryList', [])
    
    logger.info(f"Processing {len(engagement_summaries)} engagements")
    logger.info(f"Triggered by billing event: {detail_type}")
    
    # Log information about the billing event that triggered this
    if event_detail:
        logger.info(f"Billing event details: {json.dumps(event_detail)}")
        
        # Check if this is an engagement-related billing event
        engagement_id = event_detail.get('engagementId')
        if engagement_id:
            # Find the engagement related to this billing event
            matching_engagement = None
            for engagement in engagement_summaries:
                if engagement.get('Id') == engagement_id:
                    matching_engagement = engagement
                    break
            
            if matching_engagement:
                logger.info(f"Found matching engagement: {json.dumps(matching_engagement)}")
                logger.info(f"Engagement Title: {matching_engagement.get('Title')}")
                logger.info(f"Member Count: {matching_engagement.get('MemberCount')}")
                logger.info(f"Created At: {matching_engagement.get('CreatedAt')}")
            else:
                logger.warning(f"No engagement found with ID {engagement_id} in current list")
    
    # Log summary information about all engagements
    for engagement in engagement_summaries:
        logger.debug(f"Engagement: ID={engagement.get('Id')}, Title={engagement.get('Title')}, Members={engagement.get('MemberCount')}")
    
    # Add your custom processing logic here
    # Examples:
    # - Store engagements in DynamoDB
    # - Send SNS notifications
    # - Update a CRM system
    # - Trigger additional workflows
    # - Correlate billing events with partner engagements
    
    return True
