# SureNotify API Reference

Base URL: `https://mail.surenotifyapi.com`

Authentication: `x-api-key` header on all requests.

---

## Table of Contents

1. [Email Sending](#email-sending)
2. [Email Webhooks](#email-webhooks)
3. [Email Event Query](#email-event-query)
4. [SMS Sending](#sms-sending)
5. [SMS Webhooks](#sms-webhooks)
6. [SMS Exclusive Number](#query-exclusive-number)
7. [SMS Event Query](#sms-event-query)
8. [Sender Domain Authentication](#sender-domain-authentication)
9. [Webhook Signature Verification](#webhook-signature-verification)
10. [Variable System](#variable-system)
11. [Error Messages](#error-messages)

---

## Email Sending

### Send Email

```
POST /v1/messages
```

**Required fields:**

| Field | Type | Description |
|-------|------|-------------|
| `subject` | string | Email subject |
| `fromAddress` | string | Verified sender email |
| `content` | string | HTML email body |
| `recipients` | array | Recipient list (max 100 per request) |
| `recipients[].name` | string | Recipient name |
| `recipients[].address` | string | Recipient email |

**Optional fields:**

| Field | Type | Description |
|-------|------|-------------|
| `fromName` | string | Sender display name (defaults to local part of fromAddress) |
| `unsubscribedLink` | string | Unsubscribe URL (displayed in email client header per MIME spec) |
| `recipients[].variables` | object | Per-recipient variables (max 100 chars each) |

**Important:** Per-recipient personalization variables (e.g., order_id, customer_name) MUST be placed inside a `recipients[].variables` object — do NOT put them as top-level fields in the recipient object. Only `name` and `address` are top-level required fields.

**Request example:**

```json
{
  "subject": "Order Confirmation {{order_id}}",
  "fromAddress": "noreply@example.com",
  "fromName": "Example Store",
  "content": "<h1>Hi {{name}}</h1><p>Order {{order_id}} confirmed.</p>",
  "recipients": [
    {
      "name": "Alice",
      "address": "user@example.com",
      "variables": {
        "name": "Alice",
        "order_id": "ORD-12345"
      }
    }
  ]
}
```

**Response:**

```json
{
  "id": "request-uuid",
  "success": [
    {
      "id": "message-uuid",
      "address": "user@example.com"
    }
  ],
  "failure": {
    "invalid-email": "Invalid: address is not a valid email format",
    "long_var@example.com": "Invalid: the value of recipient variables should under 100 characters"
  }
}
```

The `success[].id` is the message ID used for event tracking. `failure` is an object with addresses as keys and error messages as values.

---

## Email Webhooks

### Create/Update Webhook

```
POST /v1/webhooks
```

**Request body:**

```json
{
  "type": 3,
  "url": "https://your-server.com/webhook"
}
```

Each event type requires a separate webhook registration. When a record with the same `type` exists, the URL is updated; otherwise a new record is created.

**Event types:**

| Type | Event | Description |
|------|-------|-------------|
| 3 | delivery | Email delivered to recipient |
| 4 | open | Recipient opened email |
| 5 | click | Recipient clicked a link |
| 6 | bounce | Email bounced |
| 7 | complaint | Recipient marked as spam |

### Query Webhooks

```
GET /v1/webhooks
```

**Response fields per webhook:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | number | Event type code |
| `domain` | string | Domain name |
| `url` | string | Webhook URL |
| `createDate` | string | Created time |

### Delete Webhook

```
DELETE /v1/webhooks
```

**Request body:**

```json
{
  "type": 3
}
```

---

## Email Event Query

```
GET /v1/events
```

**Query parameters (choose one of `id` or `recipient`):**

| Parameter | Description |
|-----------|-------------|
| `id` | Message ID (from send response) |
| `recipient` | Recipient email address |
| `from` | Start date (UTC+0 format) |
| `to` | End date (UTC+0 format) |
| `status` | Filter: `accept`, `retry`, `delivery`, `open`, `click`, `bounce`, `complaint` |

**Note:** `id` and `recipient` are mutually exclusive — use one or the other, not both.

**Constraints:** 30-day history max, 50 results per query.

---

## SMS Sending

### Send SMS

```
POST /v1/sms/messages
```

**Required fields:**

| Field | Type | Description |
|-------|------|-------------|
| `content` | string | SMS text (must include company name per NCC regs) |
| `recipients` | array | Recipient list (max 100 per request) |
| `recipients[].address` | string | Phone number (numeric only, e.g. `0912345678` or `912345678`) |
| `recipients[].country_code` | string | Country code (e.g., `"886"` for Taiwan) |

**Optional fields:**

| Field | Type | Description |
|-------|------|-------------|
| `from` | string | Sender phone (dedicated/exclusive number only, omit if none) |
| `alive_mins` | integer | Retry duration 5-480 min (default 5) |
| `recipients[].variables` | object | Per-recipient variables |

**Request example:**

```json
{
  "content": "【Example Store】Your verification code is {{code}}",
  "recipients": [
    {
      "address": "0912345678",
      "country_code": "886",
      "variables": {
        "code": "123456"
      }
    }
  ]
}
```

**Important:**
- SMS content must include company/brand name in brackets (NCC regulation).
- URLs in SMS require whitelist approval — email service@newsleopard.tw to request.
- Phone numbers must be numeric only (no dashes, spaces, or `+` prefix).

---

## SMS Webhooks

### Create/Update SMS Webhook

```
POST /v1/sms/webhooks
```

**Request body:**

```json
{
  "type": 3,
  "url": "https://your-server.com/sms-webhook"
}
```

Each event type requires a separate webhook registration.

**SMS event types:**

| Type | Event |
|------|-------|
| 3 | delivery |
| 6 | bounce |

### Query SMS Webhooks

```
GET /v1/sms/webhooks
```

**Response fields per webhook:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | number | Event type code |
| `url` | string | Webhook URL |
| `createDate` | string | Created time |

### Delete SMS Webhook

```
DELETE /v1/sms/webhooks
```

**Request body:**

```json
{
  "type": 3
}
```

### Query Exclusive Number

```
GET /v1/sms/exclusive-number
```

Returns dedicated SMS phone numbers assigned to the account.

**Response:**

```json
{
  "phoneNumbers": [
    {
      "phoneNumber": "0912345678",
      "createDate": "2024-01-15T08:00:00Z",
      "updateDate": "2024-01-15T08:00:00Z"
    }
  ]
}
```

---

## SMS Event Query

```
GET /v1/sms/events
```

**Query parameters (choose one of `id` or `recipient`+`country_code`):**

| Parameter | Description |
|-----------|-------------|
| `id` | Message ID (from send response) |
| `recipient` | Recipient phone number |
| `country_code` | Country code (required with `recipient`) |
| `from` | Start date (UTC+0 format) |
| `to` | End date (UTC+0 format) |
| `status` | Filter: `accept`, `delivery`, `bounce` |

**Note:** `id` and `recipient`+`country_code` are mutually exclusive query methods.

**Constraints:** 30-day history max, 50 results per query.

---

## Sender Domain Authentication

### Create Authentication Records

```
POST /v1/domains/{domain}
```

**Response:** Returns an array of DNS records to configure:

```json
[
  {
    "name": "yours.domain.com",
    "value": "v=spf1 include:amazonses.com include:mailgun.org ?all",
    "record_type": 0,
    "valid": false
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | DNS record name |
| `value` | string | DNS record value |
| `record_type` | number | 0 = TXT, 1 = CNAME |
| `valid` | boolean | Whether verification passed |

### Verify DNS Records

```
PUT /v1/domains/{domain}
```

Call after DNS records are configured. Returns the same DNS records array with updated `valid` status.

### Remove Domain Authentication

```
DELETE /v1/domains/{domain}
```

Returns `{ "success": true }` or `{ "success": false }`.

**Setup flow:**
1. `POST /v1/domains/example.com` — get DNS records
2. Configure DNS records with your domain registrar
3. Wait for DNS propagation (up to 48 hours)
4. `PUT /v1/domains/example.com` — verify

---

## Webhook Signature Verification

Verify incoming webhook requests using HmacSHA256:

```python
import hmac
import hashlib

def verify_webhook(api_key, message_id, event_type, signature_header):
    """Verify SureNotify webhook signature."""
    payload = f"{message_id}{event_type}"
    expected = hmac.new(
        api_key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

**Steps:**
1. Extract `x-surenotify-signature` from request headers
2. Concatenate message `id` + `eventType` from the webhook body
3. Generate HMAC-SHA256 using your API key as the secret
4. Compare generated signature with header value

---

## Variable System

Use `{{variable_name}}` in email subject, content, and SMS content.

Variables are per-recipient and defined in the `recipients[].variables` object.

**Constraints:**
- Each variable value max 100 characters
- Variable names cannot contain special symbols (e.g., `{{#subject}}` is invalid)
- Variable names cannot start with a digit
- Variable names cannot be math expressions

---

## Error Messages

| Error | Cause |
|-------|-------|
| `"Invalid: address is not a valid email format"` | Malformed recipient email |
| `"Invalid: sender domain unverified"` | `fromAddress` domain not authenticated |
| `"Invalid: the value of recipient variables should under 100 characters"` | Variable exceeds 100 char limit |
| `"address is not a valid format"` | Invalid SMS phone number |
| `"content can not be empty"` | SMS content is empty |
| `"content length exceeds the limit"` | SMS content too long |
| `{"message": "Forbidden"}` | Missing or invalid API key |
