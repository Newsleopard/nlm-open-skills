# EDM API Reference

Base URL: `https://api.newsleopard.com`

Authentication: `x-api-key` header on all requests.

---

## Table of Contents

1. [Contacts Management](#contacts-management)
2. [Campaign Management](#campaign-management)
3. [A/B Testing Campaigns](#ab-testing-campaigns)
4. [Reporting](#reporting)
5. [Templates](#templates)
6. [Automation](#automation)
7. [Account](#account)
8. [Variable Substitution](#variable-substitution)
9. [Reserved System Fields](#reserved-system-fields)
10. [Rate Limits](#rate-limits)
11. [Error Codes](#error-codes)

---

## Contacts Management

### Create Group

```
POST /v1/contacts/lists/insert
```

**Request body:**
```json
{
  "name": "VIP Customers"
}
```

**Response:** Returns group code (`sn`) for use in other endpoints.

### Query Groups

```
GET /v1/contacts/lists?size=20&page=1
```

**Response fields per group:**

| Field | Type | Description |
|-------|------|-------------|
| `sn` | string | Group code |
| `name` | string | Group name |
| `subscribedCnt` | number | Active subscriber count |
| `excludeCnt` | number | Excluded/invalid count |
| `openedRate` | number | Average open rate |
| `clickedRate` | number | Average click rate |
| `status` | string | `GENERAL` (normal) or `PROCESSING` (importing) |
| `type` | number | 0 = regular group, 1 = auto-segment |
| `createDate` | string | Created time (UTC) |
| `updateDate` | string | Updated time (UTC) |

### Import Contacts (File Upload)

```
POST /v1/contacts/imports/{list_sn}/file
```

**Optional request body:**

| Field | Type | Description |
|-------|------|-------------|
| `webhookUrl` | string | URL to receive import result via POST when complete |

**Response:** Returns a pre-signed upload URL and import code (`import_sn`).

**Flow:**
1. Call endpoint to get upload URL + import_sn
2. Upload CSV/Excel file to the pre-signed URL via PUT (binary)
3. Poll import status with import_sn (or wait for webhook callback)

**Note:** Custom fields must be pre-configured in the dashboard before import.

### Import Contacts (Text/CSV)

```
POST /v1/contacts/imports/{list_sn}/text
```

**Request body:** CSV text with `EMAIL`, `NAME` headers plus custom fields.

**Constraints:**
- Payload limit: 10 MB
- Custom fields must exist in dashboard

### Check Import Status

```
GET /v1/contacts/imports/result/{import_sn}
```

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `import_sn` | string | Import code |
| `status` | string | See status values below |
| `fileCnt` | number | Total rows in file |
| `insertCnt` | number | Successfully imported count |
| `duplicateCnt` | number | Duplicate rows in file |
| `errCnt` | number | Failed rows count |
| `createDate` | string | Import created time |
| `completedDate` | string | Import completed time |
| `errorDownloadLink` | string | CSV download link for failed rows with reasons |

**Status values:**

| Status | Meaning |
|--------|---------|
| `PROCESSING` | Import in progress |
| `COMPLETE` | Import finished successfully |
| `DUPLICATE_HEADER` | CSV has duplicate column headers |
| `ERROR` | Import failed |
| `MISSING_REQUIRED_DATA` | Required fields missing |

**Note:** Query window is 30 days max.

### Remove Contacts

```
DELETE /v1/contacts/{list_sn}
```

**Filter parameters:**
- Fields: `NAME`, `MAIL_ADDRESS`, `DOMAIN`, `LISTSN`, or custom fields
- Operators: `EQ`, `NOT_EQ`, `LIKE`, `NOT_LIKE`

---

## Campaign Management

### Submit Campaign

```
POST /v1/campaign/normal/submit
```

**Request body uses nested structure:**

```json
{
  "form": {
    "name": "Campaign name",
    "selectedLists": ["group_sn_1", "group_sn_2"],
    "excludeLists": ["group_sn_3"]
  },
  "content": {
    "preheader": "Preview text (max 60 chars)",
    "subject": "Email subject (max 150 chars)",
    "fromName": "Sender name (max 50 chars)",
    "fromAddress": "verified@example.com",
    "htmlContent": "<html>...</html>",
    "footerLang": 1
  },
  "config": {
    "schedule": {
      "type": 0,
      "timezone": 21,
      "scheduleDate": "2024-07-05T06:00:28.000Z"
    },
    "ga": {
      "enable": false,
      "ecommerceEnable": false,
      "utmCampaign": "",
      "utmContent": ""
    }
  }
}
```

**Required parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `form.name` | string | Campaign name |
| `form.selectedLists` | array | Target group SNs (at least 1) |
| `form.excludeLists` | array | Excluded group SNs |
| `content.subject` | string | Email subject (max 150 chars) |
| `content.fromName` | string | Sender display name (max 50 chars) |
| `content.fromAddress` | string | Sender email (must be verified in dashboard) |
| `content.htmlContent` | string | HTML email body |
| `content.footerLang` | number | Footer language: `0` = English, `1` = Chinese |
| `config.schedule.type` | number | `0` = immediate, `1` = scheduled |
| `config.ga.enable` | boolean | Enable GA tracking |
| `config.ga.ecommerceEnable` | boolean | Enable GA e-commerce analytics |

**Optional parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `content.preheader` | string | Preview text (max 60 chars) |
| `config.schedule.timezone` | number | Timezone code (see timezone table) |
| `config.schedule.scheduleDate` | string | Scheduled send time (UTC+0), e.g. `2024-07-05T06:00:28.000Z` |
| `config.ga.utmCampaign` | string | utm_campaign value (required if GA enabled) |
| `config.ga.utmContent` | string | utm_content value (required if GA enabled) |

**Response:** Returns campaign code (`sn`).

### Single Upload Campaign

```
POST /v1/campaign/normal/once
```

For one-time sends without storing contacts. Returns campaign code + pre-signed upload URL for contact list. Contact list is discarded after sending.

### Delete Campaign

```
DELETE /v1/campaign/normal
```

**Request body:**

```json
{
  "campaignSnList": ["campaign_sn_1", "campaign_sn_2"]
}
```

**Response:** Returns `success`, `sendingCampaign`, `badCampaigns` arrays.

### Pause Campaign

```
PATCH /v1/campaign/normal/{campaign_sn}
```

**Response:** 204 No Content on success. 400 with error code on failure.

### Query Campaign Status

```
GET /v1/campaign/normal/{campaign_sn}
```

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `sn` | string | Campaign code |
| `name` | string | Campaign name |
| `hasContent` | array | Whether versions have content |
| `status` | string | See status values below |
| `channel` | number | 0 = Email, 1 = SMS |
| `sendTimeType` | string | `NOW` or `SCHEDULED` |
| `type` | string | `REGULAR` or `A_B_TEST` |
| `proportion` | number | A/B test proportion (%) |
| `scheduledDate` | string | Scheduled time (UTC) |
| `sentBeginDate` | string | Send start time (UTC) |
| `sentEndDate` | string | Send end time (UTC) |
| `updateDate` | string | Last updated (UTC) |

**Campaign status values:** `DRAFT`, `COMPLETE`, `STOP`, `SENDING`, `PREPARE`, `PREPARE_TO_SENT`, `OVER_LIMIT`, `TESTING`, `EMPTY_RECIPIENT`, `INSUFFICIENT_RECIPIENT_FOR_TESTING`, `UNAUTHENTICATED_SENDER`

---

## A/B Testing Campaigns

### Submit A/B Test

```
POST /v1/campaign/testing/submit
```

Uses the same nested structure as normal campaigns (`form`, `config`, `content`), with additional A/B testing fields in `content`:

**A/B testing parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `content.testingOn` | number | `1` = subject, `2` = sender, `3` = content |
| `content.testing.proportion` | number | Test percentage 0-100 |
| `content.testing.time` | number | Duration before picking winner |
| `content.testing.unit` | number | `0` = hours, `1` = days |

**A/B version fields (all in `content`):**

| Test type | Required A/B fields |
|-----------|-------------------|
| 1 (subject) | `subjectA`, `subjectB`, `preheaderA`, `preheaderB` (preheaders optional) |
| 2 (sender) | `fromNameA`, `fromNameB`, `fromAddressA`, `fromAddressB` |
| 3 (content) | `htmlContentA`, `htmlContentB` |

When `testingOn=1`, use shared `fromName`, `fromAddress`, `htmlContent`.
When `testingOn=2`, use shared `subject`, `htmlContent`.
When `testingOn=3`, use shared `subject`, `fromName`, `fromAddress`.

### Single Upload A/B Test

```
POST /v1/campaign/testing/once
```

Combines single-upload (no stored contacts) with A/B testing.

---

## Reporting

### Get Campaign Codes by Date Range

```
GET /v1/report/campaigns?startDate=YYYY-MM-DDTHH:mm:ss.SSZ&endDate=YYYY-MM-DDTHH:mm:ss.SSZ
```

Date format is UTC+0, e.g. `2024-04-01T08:38:32.00Z`.

### Campaign Performance

```
POST /v1/report/campaigns/metrics
```

**Request body:**

```json
{
  "campaignSns": ["campaign_sn_1", "campaign_sn_2"]
}
```

**Response fields per campaign:**

| Field | Type | Description |
|-------|------|-------------|
| `campaignSn` | string | Campaign code |
| `name` | string | Campaign name |
| `channel` | string | `MAIL` or `SMS` |
| `subject` | string | Email subject |
| `sentStartAt` | string | Send start time (UTC) |
| `sentEndAt` | string | Send end time (UTC) |
| `reportType` | string | `TOTAL`, `TEST_A`, `TEST_B`, or `WINNING` |
| `recipientCnt` | number | Total recipients |
| `delivered` | number | Delivered count |
| `bounced` | number | Bounced count |
| `opened` | number | Opened count |
| `clicked` | number | Clicked count |
| `distinctClickCnt` | number | Unique click count |
| `duplicateClickCnt` | number | Duplicate click count |
| `complained` | number | Complaint count |
| `unsubscribed` | number | Unsubscribe count |
| `transactions` | number | GA e-commerce order count (if GA integrated) |
| `transactionRevenue` | number | GA e-commerce revenue (if GA integrated) |

### Export Detailed Report

```
POST /v1/report/{campaign_sn}/export
```

Generates a CSV export for a specific campaign. Returns an `export_sn`.

**Rate limit:** 1 request per 10 seconds.

### Get Report Download URL

```
GET /v1/report/{campaign_sn}/link
```

Returns the download URL once the export is ready.

---

## Templates

### List All Templates

```
GET /v1/templates
```

### Get Specific Template

```
GET /v1/templates/{id}
```

Returns template HTML content and metadata.

---

## Automation

### Trigger or Stop Automation Script

```
POST /v1/automation/event
```

**Request body:**

```json
{
  "workflow": "automation_script_id",
  "event": "TRIGGER",
  "recipients": [
    {
      "name": "John",
      "address": "john@example.com",
      "variables": { "ORDER_ID": "A123" }
    }
  ]
}
```

| Parameter | Description |
|-----------|-------------|
| `workflow` | Automation script ID (created in dashboard) |
| `event` | `TRIGGER` to start, `TERMINATE` to stop |
| `recipients` | Array of recipients (max 100) |

**Response:**

```json
{
  "success": ["john@example.com"],
  "failure": {
    "invalid-email": "Invalid: address is not a valid email format",
    "long_var@example.com": "Invalid: the value of recipient variables should under 100 characters"
  }
}
```

`failure` is an object with addresses as keys and error messages as values.

---

## Account

### Check Balance

```
GET /v1/balance
```

**Response:**

```json
{
  "email": 10,
  "sms": 20
}
```

Returns remaining email credits and SMS credits.

---

## Variable Substitution

Use `${CUSTOM_FIELD_NAME}` in subject and HTML content for personalization.

Example:
```html
<p>Hello ${NAME}, your order ${ORDER_ID} has been confirmed.</p>
```

Custom fields must be configured in the dashboard and present in the imported contact data.

---

## Reserved System Fields

Cannot be used as custom field names during import (case-insensitive):

`NAME`, `EMAIL`, `GENDER`, `PHONE`, `COUNTRY_CODE`, `COUNTRY`, `CITY`, `ADDRESS`, `REGISTER_DATE`, `BIRTHDAY`, `LINE_UID`, `FACEBOOK_ID`, `SHOPLINE_ID`, `CYBERBIZ_ID`, `WACA_ID`, `EASYSTORE_ID`, `QDM_ID`, `LINE_DISPLAY_NAME`, `USER`, `REPORTTYPE`, `ONCEMODE`, `CAMPAIGN`, `APP_HOST`, `SUBJECT`, `CAMPAIGNNAME`, `MAIL_HASH`, `SCHEDULE_DATE`, `LINK_URL`, `LINK_TEXT`, `S__ID`, `S:WH`, `NL_IS_RECIPIENT_UNIQUE`, `NL_ESTIMATE_POINT`, `NL_SUBSCRIBE_FORM_SN`, `UNSUBSCRIBE`, `UNSUBSCRIBE_EN`, `UNSUBSCRIBE_JA`

---

## Rate Limits

| Limit | Value |
|-------|-------|
| General rate limit | 2 requests/second |
| Daily request limit | 300,000 requests/day |
| Report export rate limit | 1 request/10 seconds |

Rate limit responses:
- `{"message": "too many requests"}` — exceeded per-second limit
- `{"message": "Limit Exceeded"}` — exceeded daily limit

---

## Error Codes

| Code | Meaning |
|------|---------|
| `40001` | Field validation error |
| `40003` | Invalid email address |
| `40004` | Not allowed domain |
| `40007` | Invalid SN |
| `40008` | Unsupported file format |
| `40009` | Empty file content |
| `40010` | File size exceeds limit |
| `40011` | Unverified sender address |
| `40012` | Insufficient balance |
| `40013` | No sendable contacts in list |
| `40014` | Invalid campaign content |
| `40015` | Invalid send information |
| `40017` | Insufficient balance for testing |
| `40019` | Invalid schedule time |
| `40020` | Invalid date format |
