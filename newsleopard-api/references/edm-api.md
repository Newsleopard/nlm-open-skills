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
10. [Error Codes](#error-codes)

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

**Response fields per group:** sn, name, subscriber count, exclusion count, open rate, click rate.

### Import Contacts (File Upload)

```
POST /v1/contacts/imports/{list_sn}/file
```

**Response:** Returns a pre-signed upload URL and import code (`import_sn`).

**Flow:**
1. Call endpoint to get upload URL + import_sn
2. Upload CSV/Excel file to the pre-signed URL
3. Poll import status with import_sn

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

**Required parameters:**

| Parameter | Description |
|-----------|-------------|
| `name` | Campaign name |
| `lists` | Array of target list SNs (at least 1) |
| `excludeLists` | Array of excluded list SNs |
| `subject` | Email subject (max 150 chars) |
| `fromName` | Sender display name (max 50 chars) |
| `fromAddress` | Sender email (must be verified) |
| `htmlContent` | HTML email body |
| `footerLang` | Footer language code |
| `scheduleType` | `0` = immediate, `1` = scheduled |
| `timezone` | Timezone string (for scheduled) |
| `utcTimestamp` | UTC timestamp (for scheduled) |

**Optional parameters:**

| Parameter | Description |
|-----------|-------------|
| `preheader` | Preview text (max 60 chars) |
| `gaEnable` | Enable GA tracking |
| `utmSource` | GA utm_source |
| `utmMedium` | GA utm_medium |
| `utmCampaign` | GA utm_campaign |

### Single Upload Campaign

```
POST /v1/campaign/normal/once
```

For one-time sends without storing contacts. Returns campaign code + pre-signed upload URL for contact list. Contact list is discarded after sending.

### Delete Campaign

```
DELETE /v1/campaign/{campaign_sn}
```

### Pause Campaign

```
PATCH /v1/campaign/{campaign_sn}
```

### Query Campaign Status

```
GET /v1/campaign/{campaign_sn}
```

Returns current campaign state and delivery progress.

---

## A/B Testing Campaigns

### Submit A/B Test

```
POST /v1/campaign/testing/submit
```

**Additional parameters beyond normal campaign:**

| Parameter | Description |
|-----------|-------------|
| `testType` | `1` = subject, `2` = sender, `3` = content |
| `testProportion` | Percentage of list for test (0-100) |
| `testDuration` | Duration before picking winner |
| `testDurationUnit` | `0` = hours, `1` = days |

### Single Upload A/B Test

```
POST /v1/campaign/testing/once
```

Combines single-upload (no stored contacts) with A/B testing.

---

## Reporting

### Get Campaign Codes by Date Range

```
GET /v1/report/campaigns?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD
```

### Campaign Performance

```
POST /v1/report/performance
```

**Request body:** Array of campaign SNs.

**Response metrics per campaign:** delivered, opened, clicked, bounced, complained, unsubscribed counts.

### Export Detailed Report

```
POST /v1/report/export
```

Generates a CSV export. Returns an `export_sn`.

**Rate limit:** 1 request per 10 seconds.

### Get Report Download URL

```
GET /v1/report/export/{export_sn}
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
GET /v1/templates/{template_sn}
```

Returns template HTML content and metadata.

---

## Automation

### Trigger or Stop Automation Script

```
POST /v1/automation/{script_sn}
```

---

## Account

### Check Balance

```
GET /v1/account/balance
```

Returns remaining email credits.

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

Cannot be used as custom field names during import:

`NAME`, `EMAIL`, `GENDER`, `PHONE`, `COUNTRY_CODE`, `COUNTRY`, `CITY`, `ADDRESS`, `REGISTER_DATE`, `BIRTHDAY`, and various integration IDs.

---

## Error Codes

| Code | Meaning |
|------|---------|
| `40001` | Field validation error |
| `40003` | Invalid email address |
| `40011` | Unverified sender address |
| `40012` | Insufficient balance/credits |
| `40013` | No sendable contacts in list |
| `40019` | Invalid schedule time |

Rate limit responses:
- `{"message": "too many requests"}` — exceeded per-second limit
- `{"message": "Limit Exceeded"}` — exceeded daily limit
