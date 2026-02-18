# AWS Partner Central API and HubSpot Integration - Comprehensive Task List

## Overview
This document provides a comprehensive list of tasks required to ensure complete integration between AWS Partner Central API and HubSpot CRM. Each AWS Partner Central API endpoint should have corresponding code implementation, and all necessary HubSpot webhooks and functions should be defined.

---

## 1. AWS Partner Central API - Opportunity Management

### 1.1 Create Opportunity
**Task ID:** APC-OPP-001  
**Description:** Implement handler for creating new opportunities in AWS Partner Central  
**AWS API Method:** `create_opportunity`  
**HubSpot Integration:** Map to HubSpot Deal creation  
**Requirements:**
- Create Lambda function or handler to call `create_opportunity`
- Map HubSpot Deal properties to AWS Partner Central Opportunity fields
- Handle required fields: Catalog, ClientToken, CustomerOrigin, LifeCycle, NationalSecurity, OpportunityType, PartnerOpportunityIdentifier, PrimaryNeedsFromAws, Project
- Store mapping between HubSpot Deal ID and AWS Opportunity ID
- Implement error handling and retry logic

### 1.2 Update Opportunity
**Task ID:** APC-OPP-002  
**Description:** Implement handler for updating existing opportunities  
**AWS API Method:** `update_opportunity`  
**HubSpot Integration:** Sync Deal property changes to AWS Partner Central  
**Requirements:**
- Create Lambda function to call `update_opportunity`
- Track and identify which fields changed in HubSpot
- Map updated HubSpot Deal properties to AWS Partner Central fields
- Handle partial updates efficiently
- Implement conflict resolution strategy

### 1.3 Get Opportunity
**Task ID:** APC-OPP-003  
**Description:** Implement handler to retrieve single opportunity details  
**AWS API Method:** `get_opportunity`  
**HubSpot Integration:** Fetch AWS Partner Central data to enrich HubSpot Deal  
**Requirements:**
- Create function to retrieve opportunity by Catalog and Identifier
- Parse and format response for HubSpot consumption
- Cache frequently accessed opportunities
- Update HubSpot Deal with latest AWS data

### 1.4 List Opportunities
**Task ID:** APC-OPP-004  
**Description:** Implement handler to list and sync all opportunities  
**AWS API Method:** `list_opportunities`  
**HubSpot Integration:** Bulk sync opportunities to HubSpot Deals  
**Requirements:**
- Implement pagination handling (NextToken)
- Filter opportunities by various criteria (Customer, LifeCycleStatus, etc.)
- Batch process opportunity list
- Identify new, updated, and deleted opportunities
- Sync changes to HubSpot in batches

### 1.5 Assign Opportunity
**Task ID:** APC-OPP-005  
**Description:** Implement handler to assign opportunities to team members  
**AWS API Method:** `assign_opportunity`  
**HubSpot Integration:** Sync Deal owner assignment  
**Requirements:**
- Map HubSpot users to AWS Partner Central users
- Handle assignment changes triggered from either system
- Implement bidirectional sync for ownership changes

### 1.6 Submit Opportunity
**Task ID:** APC-OPP-006  
**Description:** Implement handler to submit opportunities for AWS review  
**AWS API Method:** `submit_opportunity`  
**HubSpot Integration:** Trigger on specific Deal stage changes  
**Requirements:**
- Define trigger conditions (e.g., Deal reaches specific stage)
- Validate opportunity data before submission
- Handle submission status and feedback
- Update HubSpot Deal with submission results

---

## 2. AWS Partner Central API - Engagement Management

### 2.1 Create Engagement
**Task ID:** APC-ENG-001  
**Description:** Implement handler for creating engagements  
**AWS API Method:** `create_engagement`  
**HubSpot Integration:** Create engagement records linked to Deals  
**Requirements:**
- Define engagement creation triggers
- Map HubSpot data to engagement fields
- Link engagements to opportunities

### 2.2 Get Engagement
**Task ID:** APC-ENG-002  
**Description:** Implement handler to retrieve engagement details  
**AWS API Method:** `get_engagement`  
**HubSpot Integration:** Fetch and display engagement data in HubSpot  
**Requirements:**
- Retrieve engagement by Catalog and Identifier
- Format data for HubSpot display
- Store in custom HubSpot properties or notes

### 2.3 List Engagements
**Task ID:** APC-ENG-003  
**Description:** Implement handler to list all engagements (CURRENTLY IMPLEMENTED)  
**AWS API Method:** `list_engagements`  
**HubSpot Integration:** Sync engagement list to HubSpot  
**Requirements:**
- ✅ Already implemented in `lambda_function.py`
- Add HubSpot sync functionality to existing implementation
- Implement pagination handling
- Filter and sort engagements

### 2.4 Create Engagement Invitation
**Task ID:** APC-ENG-004  
**Description:** Implement handler for creating engagement invitations  
**AWS API Method:** `create_engagement_invitation`  
**HubSpot Integration:** Track invitation status in HubSpot  
**Requirements:**
- Create invitations for partner collaboration
- Track invitation lifecycle
- Notify HubSpot when invitations are sent

### 2.5 Get Engagement Invitation
**Task ID:** APC-ENG-005  
**Description:** Implement handler to retrieve invitation details  
**AWS API Method:** `get_engagement_invitation`  
**HubSpot Integration:** Display invitation details in HubSpot  
**Requirements:**
- Fetch invitation by Catalog and Identifier
- Update HubSpot with invitation status

### 2.6 List Engagement Invitations
**Task ID:** APC-ENG-006  
**Description:** Implement handler to list all engagement invitations  
**AWS API Method:** `list_engagement_invitations`  
**HubSpot Integration:** Sync invitation list to HubSpot  
**Requirements:**
- Implement pagination
- Filter by status, date, engagement
- Display pending invitations prominently in HubSpot

### 2.7 Accept Engagement Invitation
**Task ID:** APC-ENG-007  
**Description:** Implement handler to accept invitations  
**AWS API Method:** `start_engagement_by_accepting_invitation_task`  
**HubSpot Integration:** Allow acceptance from HubSpot UI  
**Requirements:**
- Create workflow to accept invitations
- Update status in both systems
- Trigger follow-up actions

### 2.8 Reject Engagement Invitation
**Task ID:** APC-ENG-008  
**Description:** Implement handler to reject invitations  
**AWS API Method:** `reject_engagement_invitation`  
**HubSpot Integration:** Allow rejection from HubSpot UI  
**Requirements:**
- Create workflow to reject invitations
- Update status and add rejection reason
- Archive invitation in HubSpot

### 2.9 Start Engagement from Opportunity
**Task ID:** APC-ENG-009  
**Description:** Implement handler to create engagement from opportunity  
**AWS API Method:** `start_engagement_from_opportunity_task`  
**HubSpot Integration:** Create engagement when Deal reaches specific stage  
**Requirements:**
- Define trigger conditions
- Create engagement automatically
- Link to parent opportunity/deal

### 2.10 List Engagement Members
**Task ID:** APC-ENG-010  
**Description:** Implement handler to list engagement team members  
**AWS API Method:** `list_engagement_members`  
**HubSpot Integration:** Display team members in HubSpot  
**Requirements:**
- Retrieve member list for engagements
- Map to HubSpot contacts/users
- Display member roles and responsibilities

### 2.11 List Engagement Resource Associations
**Task ID:** APC-ENG-011  
**Description:** Implement handler to list associated resources  
**AWS API Method:** `list_engagement_resource_associations`  
**HubSpot Integration:** Display linked resources in HubSpot  
**Requirements:**
- Retrieve resource associations
- Display in HubSpot Deal timeline or notes

### 2.12 List Engagement By Accepting Invitation Tasks
**Task ID:** APC-ENG-012  
**Description:** Implement handler to track invitation acceptance tasks  
**AWS API Method:** `list_engagement_by_accepting_invitation_tasks`  
**HubSpot Integration:** Track task status in HubSpot  
**Requirements:**
- List all invitation acceptance tasks
- Monitor task progress
- Update HubSpot task records

### 2.13 List Engagement From Opportunity Tasks
**Task ID:** APC-ENG-013  
**Description:** Implement handler to track engagement creation tasks  
**AWS API Method:** `list_engagement_from_opportunity_tasks`  
**HubSpot Integration:** Track task status in HubSpot  
**Requirements:**
- List all engagement creation tasks
- Monitor task progress
- Update HubSpot accordingly

---

## 3. AWS Partner Central API - Entity Association

### 3.1 Associate Opportunity
**Task ID:** APC-ASSOC-001  
**Description:** Implement handler to associate opportunities with solutions/products  
**AWS API Method:** `associate_opportunity`  
**HubSpot Integration:** Link Deals to Products or Companies  
**Requirements:**
- Associate opportunities with AWS solutions
- Map to HubSpot Products or Line Items
- Support multiple associations per opportunity

### 3.2 Disassociate Opportunity
**Task ID:** APC-ASSOC-002  
**Description:** Implement handler to remove opportunity associations  
**AWS API Method:** `disassociate_opportunity`  
**HubSpot Integration:** Remove Deal-Product links  
**Requirements:**
- Remove associations when no longer valid
- Sync disassociation to HubSpot
- Handle cascading effects

---

## 4. AWS Partner Central API - AWS Referrals and Solutions

### 4.1 Get AWS Opportunity Summary
**Task ID:** APC-AWS-001  
**Description:** Implement handler to retrieve AWS opportunity insights  
**AWS API Method:** `get_aws_opportunity_summary`  
**HubSpot Integration:** Display AWS insights in HubSpot  
**Requirements:**
- Fetch real-time AWS opportunity data
- Display AWS-specific metrics and stages
- Show AWS account team involvement

### 4.2 List Solutions
**Task ID:** APC-AWS-002  
**Description:** Implement handler to list available partner solutions  
**AWS API Method:** `list_solutions`  
**HubSpot Integration:** Sync solutions to HubSpot Products  
**Requirements:**
- Retrieve partner solution catalog
- Create/update HubSpot Products
- Maintain solution-product mapping

---

## 5. AWS Partner Central API - Snapshot and Resource Management

### 5.1 Create Resource Snapshot
**Task ID:** APC-SNAP-001  
**Description:** Implement handler to create resource snapshots  
**AWS API Method:** `create_resource_snapshot`  
**HubSpot Integration:** Create backups of HubSpot data state  
**Requirements:**
- Define snapshot triggers and schedules
- Create snapshots for audit and compliance
- Store snapshot metadata

### 5.2 Create Resource Snapshot Job
**Task ID:** APC-SNAP-002  
**Description:** Implement handler to create snapshot jobs  
**AWS API Method:** `create_resource_snapshot_job`  
**HubSpot Integration:** Schedule automated snapshots  
**Requirements:**
- Create recurring snapshot jobs
- Configure job parameters
- Monitor job status

### 5.3 Get Resource Snapshot
**Task ID:** APC-SNAP-003  
**Description:** Implement handler to retrieve snapshots  
**AWS API Method:** `get_resource_snapshot`  
**HubSpot Integration:** Retrieve historical data state  
**Requirements:**
- Fetch specific snapshots by ID
- Enable data recovery and comparison

### 5.4 Get Resource Snapshot Job
**Task ID:** APC-SNAP-004  
**Description:** Implement handler to retrieve snapshot job details  
**AWS API Method:** `get_resource_snapshot_job`  
**HubSpot Integration:** Monitor job execution  
**Requirements:**
- Retrieve job status and results
- Display in monitoring dashboard

### 5.5 List Resource Snapshots
**Task ID:** APC-SNAP-005  
**Description:** Implement handler to list all snapshots  
**AWS API Method:** `list_resource_snapshots`  
**HubSpot Integration:** Display snapshot history  
**Requirements:**
- List snapshots with pagination
- Filter by date, type, status
- Enable snapshot browsing

### 5.6 List Resource Snapshot Jobs
**Task ID:** APC-SNAP-006  
**Description:** Implement handler to list all snapshot jobs  
**AWS API Method:** `list_resource_snapshot_jobs`  
**HubSpot Integration:** Display job history  
**Requirements:**
- List all jobs with status
- Filter and sort jobs
- Monitor job performance

### 5.7 Delete Resource Snapshot Job
**Task ID:** APC-SNAP-007  
**Description:** Implement handler to delete snapshot jobs  
**AWS API Method:** `delete_resource_snapshot_job`  
**HubSpot Integration:** Clean up completed/failed jobs  
**Requirements:**
- Delete obsolete jobs
- Implement retention policies

### 5.8 Start Resource Snapshot Job
**Task ID:** APC-SNAP-008  
**Description:** Implement handler to manually start snapshot jobs  
**AWS API Method:** `start_resource_snapshot_job`  
**HubSpot Integration:** Trigger on-demand snapshots  
**Requirements:**
- Start jobs on demand
- Handle immediate snapshot needs

### 5.9 Stop Resource Snapshot Job
**Task ID:** APC-SNAP-009  
**Description:** Implement handler to stop running jobs  
**AWS API Method:** `stop_resource_snapshot_job`  
**HubSpot Integration:** Cancel long-running jobs  
**Requirements:**
- Stop jobs gracefully
- Handle partial snapshots

---

## 6. AWS Partner Central API - System Settings and Configuration

### 6.1 Get Selling System Settings
**Task ID:** APC-SYS-001  
**Description:** Implement handler to retrieve system configuration  
**AWS API Method:** `get_selling_system_settings`  
**HubSpot Integration:** Configure integration behavior  
**Requirements:**
- Retrieve current settings
- Display in admin configuration panel
- Enable settings management

### 6.2 Put Selling System Settings
**Task ID:** APC-SYS-002  
**Description:** Implement handler to update system configuration  
**AWS API Method:** `put_selling_system_settings`  
**HubSpot Integration:** Update integration settings  
**Requirements:**
- Update settings programmatically
- Validate configuration changes
- Apply settings immediately

---

## 7. AWS Partner Central API - Resource Tagging

### 7.1 List Tags for Resource
**Task ID:** APC-TAG-001  
**Description:** Implement handler to retrieve resource tags  
**AWS API Method:** `list_tags_for_resource`  
**HubSpot Integration:** Display tags as HubSpot properties  
**Requirements:**
- Retrieve tags for opportunities, engagements
- Map to HubSpot custom properties
- Display in Deal/Contact views

### 7.2 Tag Resource
**Task ID:** APC-TAG-002  
**Description:** Implement handler to add tags to resources  
**AWS API Method:** `tag_resource`  
**HubSpot Integration:** Sync HubSpot tags to AWS  
**Requirements:**
- Add tags to opportunities/engagements
- Bidirectional tag sync
- Handle tag validation

### 7.3 Untag Resource
**Task ID:** APC-TAG-003  
**Description:** Implement handler to remove tags from resources  
**AWS API Method:** `untag_resource`  
**HubSpot Integration:** Remove tags from AWS when removed in HubSpot  
**Requirements:**
- Remove specific tags
- Sync tag removal
- Handle tag lifecycle

---

## 8. AWS EventBridge - Real-Time Event Subscriptions

### 8.1 Opportunity Created Event
**Task ID:** APC-EVENT-001  
**Description:** Implement EventBridge handler for Opportunity Created events  
**AWS Event:** `Opportunity Created`  
**HubSpot Integration:** Create Deal in HubSpot when opportunity created in AWS  
**Requirements:**
- Subscribe to opportunity created events
- Parse event payload
- Create corresponding HubSpot Deal
- Link to AWS opportunity ID

### 8.2 Opportunity Updated Event
**Task ID:** APC-EVENT-002  
**Description:** Implement EventBridge handler for Opportunity Updated events  
**AWS Event:** `Opportunity Updated`  
**HubSpot Integration:** Update Deal in HubSpot when opportunity updated in AWS  
**Requirements:**
- Subscribe to opportunity updated events
- Identify changed fields
- Update HubSpot Deal properties
- Handle conflict resolution

### 8.3 Engagement Invitation Created Event
**Task ID:** APC-EVENT-003  
**Description:** Implement EventBridge handler for Engagement Invitation Created (CURRENTLY IMPLEMENTED)  
**AWS Event:** `Engagement Invitation Created`  
**HubSpot Integration:** Notify in HubSpot when new invitation received  
**Requirements:**
- ✅ Already implemented in `lambda_function.py` and `eventbridge_rule_pattern.json`
- Add HubSpot notification functionality
- Create HubSpot task or activity
- Alert deal owner

### 8.4 Engagement Invitation Accepted Event
**Task ID:** APC-EVENT-004  
**Description:** Implement EventBridge handler for invitation acceptance  
**AWS Event:** `Engagement Invitation Accepted`  
**HubSpot Integration:** Update Deal status when invitation accepted  
**Requirements:**
- Subscribe to acceptance events
- Update HubSpot Deal stage
- Create follow-up tasks

### 8.5 Engagement Invitation Rejected Event
**Task ID:** APC-EVENT-005  
**Description:** Implement EventBridge handler for invitation rejection  
**AWS Event:** `Engagement Invitation Rejected`  
**HubSpot Integration:** Update Deal status when invitation rejected  
**Requirements:**
- Subscribe to rejection events
- Mark invitation as rejected
- Archive or close related activities

---

## 9. HubSpot Webhooks - Inbound Integration

### 9.1 Deal Created Webhook
**Task ID:** HS-WEBHOOK-001  
**Description:** Implement HubSpot webhook handler for new Deals  
**HubSpot Event:** `deal.creation`  
**AWS Integration:** Create opportunity in AWS Partner Central  
**Requirements:**
- Configure webhook subscription in HubSpot app
- Create HTTPS endpoint to receive webhook
- Validate webhook signature (X-HubSpot-Signature)
- Extract Deal properties
- Call `create_opportunity` API
- Store Deal ID to Opportunity ID mapping

### 9.2 Deal Property Changed Webhook
**Task ID:** HS-WEBHOOK-002  
**Description:** Implement HubSpot webhook handler for Deal updates  
**HubSpot Event:** `deal.propertyChange`  
**AWS Integration:** Update opportunity in AWS Partner Central  
**Requirements:**
- Subscribe to deal property change events
- Identify which properties changed
- Map changed properties to AWS fields
- Call `update_opportunity` API
- Handle partial updates

### 9.3 Deal Deleted Webhook
**Task ID:** HS-WEBHOOK-003  
**Description:** Implement HubSpot webhook handler for Deal deletion  
**HubSpot Event:** `deal.deletion`  
**AWS Integration:** Archive or mark opportunity inactive in AWS  
**Requirements:**
- Subscribe to deletion events
- Handle soft delete vs hard delete
- Update AWS opportunity status
- Maintain audit trail

### 9.4 Contact Created Webhook
**Task ID:** HS-WEBHOOK-004  
**Description:** Implement HubSpot webhook handler for new Contacts  
**HubSpot Event:** `contact.creation`  
**AWS Integration:** Associate contact with opportunities  
**Requirements:**
- Subscribe to contact creation
- Link contacts to engagement members
- Sync contact details to AWS if needed

### 9.5 Contact Property Changed Webhook
**Task ID:** HS-WEBHOOK-005  
**Description:** Implement HubSpot webhook handler for Contact updates  
**HubSpot Event:** `contact.propertyChange`  
**AWS Integration:** Update engagement member information  
**Requirements:**
- Track contact property changes
- Update AWS engagement members
- Sync critical contact fields

### 9.6 Company Property Changed Webhook
**Task ID:** HS-WEBHOOK-006  
**Description:** Implement HubSpot webhook handler for Company updates  
**HubSpot Event:** `company.propertyChange`  
**AWS Integration:** Update opportunity customer information  
**Requirements:**
- Subscribe to company changes
- Update AWS opportunity customer fields
- Sync company details

### 9.7 Deal Stage Changed Webhook
**Task ID:** HS-WEBHOOK-007  
**Description:** Implement specialized handler for Deal stage changes  
**HubSpot Event:** `deal.propertyChange` (dealstage property)  
**AWS Integration:** Update opportunity lifecycle status  
**Requirements:**
- Detect stage transitions
- Map HubSpot stages to AWS lifecycle stages
- Trigger stage-specific actions (e.g., submit opportunity)
- Create audit trail

---

## 10. HubSpot API - Outbound Integration Functions

### 10.1 Create Deal Function
**Task ID:** HS-API-001  
**Description:** Implement function to create Deals in HubSpot  
**HubSpot API:** `POST /crm/v3/objects/deals`  
**Trigger:** AWS opportunity created event  
**Requirements:**
- Map AWS opportunity fields to Deal properties
- Set Deal name, amount, stage, owner
- Create associations to Contacts/Companies
- Return Deal ID for mapping storage

### 10.2 Update Deal Function
**Task ID:** HS-API-002  
**Description:** Implement function to update Deals in HubSpot  
**HubSpot API:** `PATCH /crm/v3/objects/deals/{dealId}`  
**Trigger:** AWS opportunity updated event  
**Requirements:**
- Update specific Deal properties
- Handle partial updates efficiently
- Avoid overwriting unchanged fields

### 10.3 Get Deal Function
**Task ID:** HS-API-003  
**Description:** Implement function to retrieve Deal details  
**HubSpot API:** `GET /crm/v3/objects/deals/{dealId}`  
**Trigger:** On-demand or for validation  
**Requirements:**
- Retrieve Deal with all properties
- Fetch associations (contacts, companies)
- Cache for performance

### 10.4 Search Deals Function
**Task ID:** HS-API-004  
**Description:** Implement function to search for Deals  
**HubSpot API:** `POST /crm/v3/objects/deals/search`  
**Trigger:** Find existing Deals before creating  
**Requirements:**
- Search by custom properties (AWS opportunity ID)
- Filter by multiple criteria
- Handle pagination for large result sets

### 10.5 Create Contact Function
**Task ID:** HS-API-005  
**Description:** Implement function to create Contacts in HubSpot  
**HubSpot API:** `POST /crm/v3/objects/contacts`  
**Trigger:** AWS engagement member added  
**Requirements:**
- Create contact records
- Set email, name, company
- Link to relevant Deals

### 10.6 Update Contact Function
**Task ID:** HS-API-006  
**Description:** Implement function to update Contacts  
**HubSpot API:** `PATCH /crm/v3/objects/contacts/{contactId}`  
**Trigger:** Engagement member information updated  
**Requirements:**
- Update contact properties
- Maintain data accuracy

### 10.7 Create Company Function
**Task ID:** HS-API-007  
**Description:** Implement function to create Companies in HubSpot  
**HubSpot API:** `POST /crm/v3/objects/companies`  
**Trigger:** AWS opportunity with new customer  
**Requirements:**
- Create company records
- Set company name, domain, industry
- Link to Deals and Contacts

### 10.8 Create Association Function
**Task ID:** HS-API-008  
**Description:** Implement function to create object associations  
**HubSpot API:** `PUT /crm/v4/objects/{objectType}/{objectId}/associations/default/{toObjectType}/{toObjectId}`  
**Trigger:** Linking entities across systems  
**Requirements:**
- Associate Deals with Contacts
- Associate Deals with Companies
- Associate Contacts with Companies

### 10.9 Create Task/Activity Function
**Task ID:** HS-API-009  
**Description:** Implement function to create Tasks in HubSpot  
**HubSpot API:** `POST /crm/v3/objects/tasks`  
**Trigger:** Engagement invitation requires action  
**Requirements:**
- Create tasks for invitation actions
- Assign to deal owner
- Set due dates and priorities

### 10.10 Create Note Function
**Task ID:** HS-API-010  
**Description:** Implement function to create Notes on Deals  
**HubSpot API:** `POST /crm/v3/objects/notes`  
**Trigger:** AWS events or updates  
**Requirements:**
- Log AWS events as Deal notes
- Store engagement details
- Maintain audit trail

### 10.11 Create Product Function
**Task ID:** HS-API-011  
**Description:** Implement function to create Products in HubSpot  
**HubSpot API:** `POST /crm/v3/objects/products`  
**Trigger:** AWS solution list sync  
**Requirements:**
- Create product records from AWS solutions
- Set product properties
- Enable line item associations

### 10.12 Create Line Item Function
**Task ID:** HS-API-012  
**Description:** Implement function to create Line Items on Deals  
**HubSpot API:** `POST /crm/v3/objects/line_items`  
**Trigger:** Opportunity-solution association  
**Requirements:**
- Create line items for associated solutions
- Link to Deals and Products
- Set quantity and price

---

## 11. Data Mapping and Transformation

### 11.1 Opportunity to Deal Field Mapping
**Task ID:** MAP-001  
**Description:** Define and implement field mapping between AWS Opportunity and HubSpot Deal  
**Requirements:**
- Map all AWS opportunity fields to HubSpot properties
- Handle custom field creation in HubSpot
- Document field mapping schema
- Implement transformation logic for data type differences

### 11.2 Engagement to Activity Mapping
**Task ID:** MAP-002  
**Description:** Define mapping for engagements to HubSpot activities  
**Requirements:**
- Map engagement types to HubSpot activity types
- Track engagement lifecycle as tasks
- Store engagement members as associations

### 11.3 Contact/Member Mapping
**Task ID:** MAP-003  
**Description:** Map AWS engagement members to HubSpot Contacts  
**Requirements:**
- Match contacts by email
- Create contacts when not found
- Sync member roles and responsibilities

### 11.4 Stage/Lifecycle Mapping
**Task ID:** MAP-004  
**Description:** Map AWS lifecycle stages to HubSpot Deal stages  
**Requirements:**
- Define stage equivalency table
- Handle bidirectional stage changes
- Document stage transition rules

---

## 12. Infrastructure and Configuration

### 12.1 Lambda Functions Setup
**Task ID:** INFRA-001  
**Description:** Create and configure all required Lambda functions  
**Requirements:**
- One Lambda per API endpoint or logical grouping
- Configure appropriate timeouts and memory
- Set up IAM roles and permissions
- Configure environment variables

### 12.2 EventBridge Rules Configuration
**Task ID:** INFRA-002  
**Description:** Configure EventBridge rules for all AWS events  
**Requirements:**
- Create rules for each event type
- Configure event patterns and filters
- Link rules to appropriate Lambda targets

### 12.3 API Gateway Setup
**Task ID:** INFRA-003  
**Description:** Set up API Gateway for HubSpot webhooks  
**Requirements:**
- Create REST API endpoints
- Configure authentication and authorization
- Implement request validation
- Set up throttling and rate limiting

### 12.4 DynamoDB Tables
**Task ID:** INFRA-004  
**Description:** Create DynamoDB tables for ID mapping and state management  
**Requirements:**
- Table for AWS-HubSpot ID mappings
- Table for sync state and timestamps
- Table for error logs and retry queue
- Configure indexes for efficient queries

### 12.5 Secrets Manager Configuration
**Task ID:** INFRA-005  
**Description:** Store and manage sensitive credentials  
**Requirements:**
- Store HubSpot API key/access token
- Store AWS Partner Central credentials
- Implement credential rotation
- Set up access policies

### 12.6 CloudWatch Alarms and Monitoring
**Task ID:** INFRA-006  
**Description:** Set up comprehensive monitoring  
**Requirements:**
- Alarms for Lambda errors
- Alarms for API rate limiting
- Alarms for webhook failures
- Dashboard for sync status

---

## 13. Error Handling and Retry Logic

### 13.1 AWS API Error Handling
**Task ID:** ERROR-001  
**Description:** Implement robust error handling for AWS API calls  
**Requirements:**
- Handle throttling (429 errors)
- Implement exponential backoff
- Log errors with context
- Queue failed requests for retry

### 13.2 HubSpot API Error Handling
**Task ID:** ERROR-002  
**Description:** Implement error handling for HubSpot API calls  
**Requirements:**
- Handle rate limits (429 errors)
- Implement retry with backoff
- Handle 4xx client errors
- Queue failed requests

### 13.3 Webhook Validation and Security
**Task ID:** ERROR-003  
**Description:** Implement webhook signature validation  
**Requirements:**
- Validate X-HubSpot-Signature header
- Reject invalid requests
- Log security events
- Implement request timeout

### 13.4 Dead Letter Queue
**Task ID:** ERROR-004  
**Description:** Set up DLQ for failed messages  
**Requirements:**
- Create SQS dead letter queues
- Configure Lambda DLQ settings
- Implement DLQ processing
- Alert on DLQ messages

---

## 14. Testing and Validation

### 14.1 Unit Tests
**Task ID:** TEST-001  
**Description:** Write unit tests for all functions  
**Requirements:**
- Test each Lambda function independently
- Mock external API calls
- Test error scenarios
- Achieve >80% code coverage

### 14.2 Integration Tests
**Task ID:** TEST-002  
**Description:** Write integration tests for end-to-end flows  
**Requirements:**
- Test AWS to HubSpot sync
- Test HubSpot to AWS sync
- Test bidirectional updates
- Test with sandbox environments

### 14.3 Event Simulation Tests
**Task ID:** TEST-003  
**Description:** Test with simulated EventBridge events  
**Requirements:**
- Create test events for each event type
- Test event processing logic
- Validate HubSpot updates
- Test error scenarios

---

## 15. Documentation and Maintenance

### 15.1 API Documentation
**Task ID:** DOC-001  
**Description:** Document all API integrations  
**Requirements:**
- Document each Lambda function
- Document field mappings
- Document error codes and handling
- Create troubleshooting guide

### 15.2 Deployment Guide
**Task ID:** DOC-002  
**Description:** Create comprehensive deployment documentation  
**Requirements:**
- Step-by-step setup instructions
- Configuration requirements
- HubSpot app setup guide
- CloudFormation templates

### 15.3 Runbook
**Task ID:** DOC-003  
**Description:** Create operational runbook  
**Requirements:**
- Common issues and solutions
- Monitoring and alerting guide
- Escalation procedures
- Maintenance procedures

---

## Summary

### Total Tasks: 82
- AWS API Endpoints: 38 tasks
- EventBridge Events: 5 tasks
- HubSpot Webhooks: 7 tasks
- HubSpot API Functions: 12 tasks
- Data Mapping: 4 tasks
- Infrastructure: 6 tasks
- Error Handling: 4 tasks
- Testing: 3 tasks
- Documentation: 3 tasks

### Priority Classification:
- **P0 (Critical):** Opportunity and Engagement core operations, primary webhooks
- **P1 (High):** EventBridge events, data mapping, error handling
- **P2 (Medium):** Snapshot management, tagging, advanced features
- **P3 (Low):** Documentation, monitoring enhancements

### Recommended Implementation Order:
1. Infrastructure setup (INFRA-001 to INFRA-006)
2. Data mapping definitions (MAP-001 to MAP-004)
3. Core opportunity management (APC-OPP-001 to APC-OPP-006)
4. HubSpot Deal webhooks (HS-WEBHOOK-001, HS-WEBHOOK-002, HS-WEBHOOK-007)
5. HubSpot API functions (HS-API-001 to HS-API-004)
6. Engagement management (APC-ENG-001 to APC-ENG-013)
7. EventBridge event handlers (APC-EVENT-001 to APC-EVENT-005)
8. Association and tagging (APC-ASSOC-001, APC-ASSOC-002, APC-TAG-001 to APC-TAG-003)
9. Error handling and monitoring (ERROR-001 to ERROR-004)
10. Testing and validation (TEST-001 to TEST-003)
11. Documentation (DOC-001 to DOC-003)

