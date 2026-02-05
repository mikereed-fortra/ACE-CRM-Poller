#!/bin/bash

# Deployment script for Partner Central Engagement Processor
# This script deploys the Lambda function and EventBridge rule using CloudFormation

set -e

# Configuration
STACK_NAME="${STACK_NAME:-partner-central-engagement-processor}"
CATALOG="${CATALOG:-AWS}"
LAMBDA_FUNCTION_NAME="${LAMBDA_FUNCTION_NAME:-PartnerCentralEngagementProcessor}"
EVENT_RULE_NAME="${EVENT_RULE_NAME:-PartnerCentralEngagementInvitationRule}"
REGION="us-east-1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Partner Central Engagement Processor${NC}"
echo -e "${GREEN}CloudFormation Deployment${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    echo "Please install AWS CLI: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if template file exists
if [ ! -f "cloudformation_template.yaml" ]; then
    echo -e "${RED}Error: cloudformation_template.yaml not found${NC}"
    exit 1
fi

echo -e "${YELLOW}Deployment Configuration:${NC}"
echo "  Stack Name: $STACK_NAME"
echo "  Catalog: $CATALOG"
echo "  Lambda Function: $LAMBDA_FUNCTION_NAME"
echo "  Event Rule: $EVENT_RULE_NAME"
echo "  Region: $REGION"
echo ""

# Validate template
echo -e "${YELLOW}Validating CloudFormation template...${NC}"
aws cloudformation validate-template \
    --template-body file://cloudformation_template.yaml \
    --region $REGION > /dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Template validation successful${NC}"
else
    echo -e "${RED}✗ Template validation failed${NC}"
    exit 1
fi

echo ""

# Check if stack already exists
echo -e "${YELLOW}Checking if stack exists...${NC}"
STACK_EXISTS=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    2>&1 | grep -c "does not exist" || true)

if [ $STACK_EXISTS -eq 0 ]; then
    echo -e "${YELLOW}Stack already exists. Updating stack...${NC}"
    OPERATION="update-stack"
    WAIT_CONDITION="stack-update-complete"
else
    echo -e "${YELLOW}Creating new stack...${NC}"
    OPERATION="create-stack"
    WAIT_CONDITION="stack-create-complete"
fi

echo ""

# Deploy stack
echo -e "${YELLOW}Deploying CloudFormation stack...${NC}"

if [ "$OPERATION" = "create-stack" ]; then
    aws cloudformation create-stack \
        --stack-name $STACK_NAME \
        --template-body file://cloudformation_template.yaml \
        --parameters \
            ParameterKey=Catalog,ParameterValue=$CATALOG \
            ParameterKey=LambdaFunctionName,ParameterValue=$LAMBDA_FUNCTION_NAME \
            ParameterKey=EventBridgeRuleName,ParameterValue=$EVENT_RULE_NAME \
        --capabilities CAPABILITY_NAMED_IAM \
        --region $REGION \
        --tags \
            Key=Project,Value=PartnerCentralIntegration \
            Key=ManagedBy,Value=CloudFormation
else
    aws cloudformation update-stack \
        --stack-name $STACK_NAME \
        --template-body file://cloudformation_template.yaml \
        --parameters \
            ParameterKey=Catalog,ParameterValue=$CATALOG \
            ParameterKey=LambdaFunctionName,ParameterValue=$LAMBDA_FUNCTION_NAME \
            ParameterKey=EventBridgeRuleName,ParameterValue=$EVENT_RULE_NAME \
        --capabilities CAPABILITY_NAMED_IAM \
        --region $REGION || {
        if [[ $? -eq 254 ]]; then
            echo -e "${YELLOW}No updates to perform${NC}"
            exit 0
        else
            echo -e "${RED}Stack update failed${NC}"
            exit 1
        fi
    }
fi

echo -e "${GREEN}✓ Stack operation initiated${NC}"
echo ""

# Wait for stack operation to complete
echo -e "${YELLOW}Waiting for stack operation to complete...${NC}"
echo "This may take a few minutes..."

aws cloudformation wait $WAIT_CONDITION \
    --stack-name $STACK_NAME \
    --region $REGION

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Stack operation completed successfully${NC}"
else
    echo -e "${RED}✗ Stack operation failed${NC}"
    
    # Get stack events to show errors
    echo -e "${YELLOW}Recent stack events:${NC}"
    aws cloudformation describe-stack-events \
        --stack-name $STACK_NAME \
        --region $REGION \
        --max-items 10 \
        --query 'StackEvents[].[Timestamp,ResourceStatus,ResourceType,ResourceStatusReason]' \
        --output table
    exit 1
fi

echo ""

# Get stack outputs
echo -e "${YELLOW}Stack Outputs:${NC}"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Test the Lambda function with a sample event:"
echo "   aws lambda invoke --function-name $LAMBDA_FUNCTION_NAME \\"
echo "     --payload file://test_event.json \\"
echo "     --region $REGION response.json"
echo ""
echo "2. View CloudWatch logs:"
echo "   aws logs tail /aws/lambda/$LAMBDA_FUNCTION_NAME --follow --region $REGION"
echo ""
echo "3. Monitor EventBridge rule:"
echo "   aws events describe-rule --name $EVENT_RULE_NAME --region $REGION"
echo ""
echo -e "${YELLOW}To delete this stack:${NC}"
echo "   aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION"
echo ""
