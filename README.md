# AWS Partner Central API Poller for AWS Billing Events

This solution provides a Lambda function that automatically processes AWS Billing events from EventBridge and calls the AWS Partner Central ListEngagements API.

## Overview

When any AWS Billing event occurs and is published to EventBridge, this Lambda function:

1. Receives the event notification via EventBridge
2. Extracts the billing event details
3. Calls the AWS Partner Central `ListEngagements` API
4. Processes the engagement data (with customizable business logic)

## Architecture

```
EventBridge Event → EventBridge Rule → Lambda Function → Partner Central API
(AWS Billing           (Pattern Match)    (Process Event)   (ListEngagements)
 Events)
```

## Components

- **Lambda Function**: Processes AWS Billing events and calls Partner Central API
- **EventBridge Rule**: Filters and routes AWS Billing events to Lambda
- **IAM Role**: Provides necessary permissions to Lambda
- **CloudWatch Logs**: Stores Lambda execution logs

## Prerequisites

- AWS Account with Partner Central access
- AWS CLI configured with appropriate credentials
- CloudFormation permissions to deploy the stack
- Partner Central Selling API access (available in us-east-1)

## Deployment Options

### Option 1: Deploy with CloudFormation (Recommended)

```bash
aws cloudformation create-stack \
  --stack-name partner-central-engagement-processor \
  --template-body file://cloudformation_template.yaml \
  --parameters \
    ParameterKey=Catalog,ParameterValue=AWS \
    ParameterKey=LambdaFunctionName,ParameterValue=PartnerCentralEngagementProcessor \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

**Parameters:**
- `Catalog`: Choose `AWS` for production or `Sandbox` for testing (default: AWS)
- `LambdaFunctionName`: Name for the Lambda function (default: PartnerCentralEngagementProcessor)
- `EventBridgeRuleName`: Name for the EventBridge rule (default: PartnerCentralBillingEventRule)

**Monitor deployment:**
```bash
aws cloudformation describe-stacks \
  --stack-name partner-central-engagement-processor \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus'
```

### Option 2: Manual Deployment

#### Step 1: Create IAM Role

Create an IAM role with the policy from `lambda_iam_policy.json`:

```bash
# Create trust policy
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name PartnerCentralEngagementProcessorRole \
  --assume-role-policy-document file://trust-policy.json

# Attach the policy
aws iam put-role-policy \
  --role-name PartnerCentralEngagementProcessorRole \
  --policy-name PartnerCentralAPIAccess \
  --policy-document file://lambda_iam_policy.json

# Attach AWS managed policy for basic Lambda execution
aws iam attach-role-policy \
  --role-name PartnerCentralEngagementProcessorRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

#### Step 2: Create Lambda Function

```bash
# Zip the Lambda code
zip lambda_function.zip lambda_function.py

# Get the role ARN
ROLE_ARN=$(aws iam get-role --role-name PartnerCentralEngagementProcessorRole --query 'Role.Arn' --output text)

# Create the Lambda function
aws lambda create-function \
  --function-name PartnerCentralEngagementProcessor \
  --runtime python3.12 \
  --role $ROLE_ARN \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 300 \
  --memory-size 256 \
  --environment Variables={CATALOG=AWS} \
  --region us-east-1 \
  --description "Processes Engagement Invitation Created events and calls ListEngagements API"
```

#### Step 3: Create EventBridge Rule

```bash
# Create the EventBridge rule
aws events put-rule \
  --name PartnerCentralBillingEventRule \
  --event-pattern file://eventbridge_rule_pattern.json \
  --state ENABLED \
  --description "Triggers Lambda when AWS Billing events are received" \
  --region us-east-1

# Get Lambda function ARN
LAMBDA_ARN=$(aws lambda get-function --function-name PartnerCentralEngagementProcessor --region us-east-1 --query 'Configuration.FunctionArn' --output text)

# Add Lambda as target
aws events put-targets \
  --rule PartnerCentralBillingEventRule \
  --targets "Id"="1","Arn"="$LAMBDA_ARN" \
  --region us-east-1

# Grant EventBridge permission to invoke Lambda
aws lambda add-permission \
  --function-name PartnerCentralEngagementProcessor \
  --statement-id AllowEventBridgeInvoke \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn $(aws events describe-rule --name PartnerCentralBillingEventRule --region us-east-1 --query 'Arn' --output text) \
  --region us-east-1
```

## Testing

### Test with Sample Event

Create a test event file `test_event.json`:

```json
{
  "version": "0",
  "id": "12345678-1234-1234-1234-123456789012",
  "detail-type": "AWS API Call via CloudTrail",
  "source": "aws.billing",
  "account": "123456789012",
  "time": "2024-01-15T12:00:00Z",
  "region": "us-east-1",
  "resources": [],
  "detail": {
    "eventVersion": "1.08",
    "userIdentity": {
      "type": "IAMUser",
      "principalId": "AIDAI23HXS4EXAMPLE",
      "arn": "arn:aws:iam::123456789012:user/billing-user",
      "accountId": "123456789012",
      "userName": "billing-user"
    },
    "eventTime": "2024-01-15T12:00:00Z",
    "eventSource": "billing.amazonaws.com",
    "eventName": "GetCostAndUsage",
    "awsRegion": "us-east-1",
    "sourceIPAddress": "192.0.2.1",
    "userAgent": "aws-cli/2.0.0",
    "requestParameters": {
      "timePeriod": {
        "start": "2024-01-01",
        "end": "2024-01-15"
      },
      "granularity": "DAILY",
      "metrics": ["UnblendedCost"]
    },
    "responseElements": null,
    "requestID": "abc123def456ghi789",
    "eventID": "11111111-2222-3333-4444-555555555555",
    "readOnly": true,
    "eventType": "AwsApiCall",
    "managementEvent": true,
    "recipientAccountId": "123456789012"
  }
}
```

Invoke the Lambda function:

```bash
aws lambda invoke \
  --function-name PartnerCentralEngagementProcessor \
  --payload file://test_event.json \
  --region us-east-1 \
  response.json

cat response.json
```

### Check CloudWatch Logs

```bash
# Get latest log stream
LOG_STREAM=$(aws logs describe-log-streams \
  --log-group-name /aws/lambda/PartnerCentralEngagementProcessor \
  --order-by LastEventTime \
  --descending \
  --max-items 1 \
  --region us-east-1 \
  --query 'logStreams[0].logStreamName' \
  --output text)

# View logs
aws logs get-log-events \
  --log-group-name /aws/lambda/PartnerCentralEngagementProcessor \
  --log-stream-name $LOG_STREAM \
  --region us-east-1
```

## Customization

### Adding Custom Business Logic

The `process_engagements()` function in the Lambda code is designed for customization. You can:

1. **Store engagement data in DynamoDB:**
```python
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Engagements')

for engagement in engagement_summaries:
    table.put_item(Item={
        'Id': engagement['Id'],
        'Title': engagement['Title'],
        'CreatedAt': engagement['CreatedAt'],
        'MemberCount': engagement['MemberCount']
    })
```

2. **Send SNS notifications:**
```python
sns = boto3.client('sns')
sns.publish(
    TopicArn='arn:aws:sns:us-east-1:123456789012:BillingNotifications',
    Subject='New AWS Billing Event',
    Message=f"New billing event received: {detail_type}"
)
```

3. **Update external CRM:**
```python
import requests

crm_api_url = os.environ.get('CRM_API_URL')
requests.post(
    f"{crm_api_url}/engagements",
    json={'billing_event': detail_type, 'engagements': engagement_summaries},
    headers={'Authorization': f'Bearer {api_token}'}
)
```

### Filtering Engagements

You can modify the `list_engagements()` function to add filters:

```python
params = {
    'Catalog': catalog,
    'MaxResults': max_results,
    'CreatedBy': ['123456789012'],  # Filter by creator
    'Sort': {
        'SortBy': 'CreatedDate',
        'SortOrder': 'DESCENDING'
    }
}
```

## Monitoring

### CloudWatch Metrics

Monitor Lambda performance:
- Invocations
- Duration
- Errors
- Throttles

### CloudWatch Alarms

Create an alarm for Lambda errors:

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name PartnerCentralLambdaErrors \
  --alarm-description "Alert on Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=PartnerCentralEngagementProcessor \
  --evaluation-periods 1 \
  --region us-east-1
```

## Troubleshooting

### Common Issues

1. **Access Denied errors:**
   - Verify IAM role has `partnercentral-selling:ListEngagements` permission
   - Check that you're using the correct AWS region (us-east-1)
   - Ensure your account has Partner Central access

2. **No events received:**
   - Verify EventBridge rule is enabled
   - Check event pattern matches the aws.billing source
   - Confirm Lambda has permission to be invoked by EventBridge
   - Ensure CloudTrail is configured to capture billing events

3. **Timeout errors:**
   - Increase Lambda timeout (currently set to 300 seconds)
   - Consider implementing pagination limits

### Enable Debug Logging

Update Lambda environment variable:
```bash
aws lambda update-function-configuration \
  --function-name PartnerCentralEngagementProcessor \
  --environment Variables={CATALOG=AWS,LOG_LEVEL=DEBUG} \
  --region us-east-1
```

## API Reference

### AWS Partner Central Selling API

- **ListEngagements**: [Documentation](https://docs.aws.amazon.com/partner-central/latest/APIReference/API_ListEngagements.html)
- **GetEngagement**: [Documentation](https://docs.aws.amazon.com/partner-central/latest/APIReference/API_GetEngagement.html)
- **AWS Billing and EventBridge**: [EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event.html)

## Security Considerations

1. **Least Privilege**: The IAM policy grants only necessary Partner Central API permissions
2. **Encryption**: Use environment variables encryption for sensitive data
3. **VPC**: Consider deploying Lambda in VPC if accessing internal resources
4. **Secrets**: Use AWS Secrets Manager for API keys and credentials

## Cost Optimization

- Lambda invocations: Charged per request and duration
- CloudWatch Logs: Consider log retention period (currently 30 days)
- EventBridge: No additional cost for rules and event delivery
- Partner Central API: Check for any API usage limits or quotas

## Cleanup

### Delete CloudFormation Stack

```bash
aws cloudformation delete-stack \
  --stack-name partner-central-engagement-processor \
  --region us-east-1
```

### Manual Cleanup

```bash
# Delete Lambda function
aws lambda delete-function \
  --function-name PartnerCentralEngagementProcessor \
  --region us-east-1

# Delete EventBridge rule
aws events remove-targets \
  --rule PartnerCentralBillingEventRule \
  --ids 1 \
  --region us-east-1

aws events delete-rule \
  --name PartnerCentralBillingEventRule \
  --region us-east-1

# Delete IAM role and policies
aws iam detach-role-policy \
  --role-name PartnerCentralEngagementProcessorRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam delete-role-policy \
  --role-name PartnerCentralEngagementProcessorRole \
  --policy-name PartnerCentralAPIAccess

aws iam delete-role \
  --role-name PartnerCentralEngagementProcessorRole

# Delete CloudWatch log group
aws logs delete-log-group \
  --log-group-name /aws/lambda/PartnerCentralEngagementProcessor \
  --region us-east-1
```

## Additional Resources

- [AWS Partner Central Documentation](https://docs.aws.amazon.com/partner-central/)
- [Partner Central API Reference](https://docs.aws.amazon.com/partner-central/latest/APIReference/)
- [AWS Partner Central Blog: CRM Integration](https://aws.amazon.com/blogs/awsmarketplace/integrate-crm-system-aws-partner-central-using-api-for-selling/)
- [EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)

## Support

For issues related to:
- **AWS Partner Central API**: Contact AWS Partner Support
- **Lambda/EventBridge**: Open an AWS Support case
- **This Solution**: Review CloudWatch logs and the troubleshooting section

## License

This solution is provided as-is for AWS Partners to integrate with Partner Central.
