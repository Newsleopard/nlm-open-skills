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
6. [SMS Event Query](#sms-event-query)
7. [Sender Domain Authentication](#sender-domain-authentication)
8. [Webhook Signature Verification](#webhook-signature-verification)
9. [Variable System](#variable-system)
10. [Error Messages](#error-messages)

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
| `recipients[].address` | string | Recipient email |

**Optional fields:**

| Field | Type | Description |
|-------|------|-------------|
| `fromName` | string | Sender display name |
| `unsubscribedLink` | string | Unsubscribe URL |
| `recipients[].variables` | object | Per-recipient variables (max 100 chars each) |

**Request example:**

```json
{
  "subject": "Order Confirmation {{order_id}}",
  "fromAddress": "noreply@example.com",
  "fromName": "Example Store",
  "content": "<h1>Hi {{name}}</h1><p>Order {{order_id}} confirmed.</p>",
  "recipients": [
    {
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
  "failure": {}
}
```

The `success[].id` is the message ID used for event tracking.

---

## Email Webhooks

### Create/Update Webhook

```
POST /v1/webhooks
```

**Request body:**

```json
{
  "url": "https://your-server.com/webhook",
  "events": [3, 4, 5, 6, 7]
}
```

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

### Delete Webhook

```
DELETE /v1/webhooks
```

---

## Email Event Query

```
GET /v1/events
```

**Query parameters:**

| Parameter | Description |
|-----------|-------------|
| `id` | Message ID (from send response) |
| `recipient` | Recipient email address |
| `from` | Start date (UTC+0 format) |
| `to` | End date (UTC+0 format) |
| `status` | Filter: `accept`, `retry`, `delivery`, `open`, `click`, `bounce`, `complaint` |

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
| `recipients[].address` | string | Phone number (numeric only) |
| `recipients[].country_code` | string | Country code (e.g., `"886"` for Taiwan) |

**Optional fields:**

| Field | Type | Description |
|-------|------|-------------|
| `from` | string | Sender phone (dedicated number only) |
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
- SMS content must include company/brand name in【】brackets (NCC regulation).
- URLs in SMS require whitelist approval — email service@newsleopard.tw to request.
- Phone numbers must be numeric only (no dashes, spaces, or `+` prefix).

---

## SMS Webhooks

### Create/Update SMS Webhook

```
POST /v1/sms/webhooks
```

**SMS event types:**

| Type | Event |
|------|-------|
| 3 | delivery |
| 6 | bounce |

### Query SMS Webhooks

```
GET /v1/sms/webhooks
```

### Delete SMS Webhook

```
DELETE /v1/sms/webhooks
```

---

## SMS Event Query

```
GET /v1/sms/events
```

**Query parameters:** `id`, `recipient`, `country_code`, `from`, `to`, `status`

**Status values:** `accept`, `delivery`, `bounce`

---

## Sender Domain Authentication

### Create Authentication Records

```
POST /v1/domains/{domain}
```

Returns DNS records (TXT or CNAME) to configure for SPF/DKIM.

### Verify DNS Records

```
PUT /v1/domains/{domain}
```

Call after DNS records are configured. Returns verification status.

### Remove Domain Authentication

```
DELETE /v1/domains/{domain}
```

**Setup flow:**
1. `POST /v1/domains/example.com` → get DNS records
2. Configure DNS records with your domain registrar
3. Wait for DNS propagation (up to 48 hours)
4. `PUT /v1/domains/example.com` → verify

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

**Constraints:** Each variable value max 100 characters.

---

## Error Messages

| Error | Cause |
|-------|-------|
| `"Invalid: address is not a valid email format"` | Malformed recipient email |
| `"Invalid: sender domain unverified"` | `fromAddress` domain not authenticated |
| `"Invalid: the value of recipient variables should under 100 characters"` | Variable exceeds 100 char limit |
| `"address is not a valid format"` | Invalid SMS phone number |
| `"content length exceeds the limit"` | SMS content too long |
| `{"message": "Forbidden"}` | Missing or invalid API key |
