# Debugging & QA Guide

## Table of Contents

1. [Common Issues & Solutions](#common-issues--solutions)
2. [Debugging Workflows](#debugging-workflows)
3. [QA Checklist — EDM API](#qa-checklist--edm-api)
4. [QA Checklist — SureNotify API](#qa-checklist--surenotify-api)
5. [Integration Testing Patterns](#integration-testing-patterns)
6. [Monitoring & Alerting](#monitoring--alerting)

---

## Common Issues & Solutions

### Authentication

| Symptom | Cause | Fix |
|---------|-------|-----|
| `{"message": "Forbidden"}` | Missing/invalid `x-api-key` | Verify key is set and valid. Check for trailing whitespace. |
| 403 on all requests | Key expired or revoked | Request new key from NewsLeopard support. |

### Rate Limiting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `{"message": "too many requests"}` | Exceeded 2 req/sec | Add request throttling (e.g., 500ms delay between calls). |
| `{"message": "Limit Exceeded"}` | Exceeded 300K req/day | Batch operations; review if polling is too aggressive. |

### Campaign Errors (EDM)

| Error Code | Meaning | Debugging Steps |
|------------|---------|-----------------|
| `40001` | Field validation error | Check all required fields. Verify field lengths (subject ≤150, preheader ≤60, fromName ≤50). |
| `40003` | Invalid email | Validate `fromAddress` format. Check for typos. |
| `40004` | Not allowed domain | Use a permitted sender domain. |
| `40007` | Invalid SN | Verify campaign/group SN exists and is correct. |
| `40008` | Unsupported file format | Use CSV or supported Excel format for import. |
| `40009` | Empty file content | Ensure uploaded file has data rows. |
| `40010` | File size exceeds limit | Reduce file size or split into batches. |
| `40011` | Unverified sender | Go to dashboard → verify sender address first. |
| `40012` | Insufficient balance | Call `GET /v1/balance`. Top up credits. |
| `40013` | No sendable contacts | Check target list has active subscribers. Verify list SN is correct. |
| `40014` | Invalid campaign content | Review HTML content for errors. |
| `40015` | Invalid send information | Check schedule/sender configuration. |
| `40017` | Insufficient balance for testing | Need enough credits for both A/B test versions. |
| `40019` | Invalid schedule time | Ensure `config.schedule.scheduleDate` is in the future (UTC+0). Check timezone value. |
| `40020` | Invalid date format | Use ISO 8601 format: `YYYY-MM-DDTHH:mm:ss.SSZ` (UTC+0). |

### Contact Import Errors (EDM)

| Status | Fix |
|--------|-----|
| `DUPLICATE_HEADER` | Remove duplicate column names from CSV. |
| `MISSING_REQUIRED_DATA` | Ensure EMAIL column exists and is populated. |
| `ERROR` | Check CSV encoding (UTF-8), payload size (≤10MB), custom field names match dashboard. |

### SureNotify Email Errors

| Error | Fix |
|-------|-----|
| `"sender domain unverified"` | Complete domain auth flow: POST → DNS config → PUT to verify. |
| `"address is not a valid email format"` | Validate recipient email format before sending. |
| `"variables should under 100 characters"` | Truncate or split variable values. |

### SureNotify SMS Errors

| Error | Fix |
|-------|-----|
| `"address is not a valid format"` | Use numeric-only phone numbers. Remove `+`, `-`, spaces. |
| `"content length exceeds the limit"` | Shorten SMS text. CJK characters count as 2-3 bytes. |
| SMS not delivered | Verify company name in content (NCC req). Check country_code. |
| URLs blocked | Apply for URL whitelist via service@newsleopard.tw. |

---

## Debugging Workflows

### "Campaign sent but no opens/clicks"

```
1. GET /v1/campaign/normal/{sn}       → confirm status is SENT
2. POST /v1/report/campaigns/metrics  → check delivered vs bounced counts
3. If high bounce rate:
   a. Check sender domain SPF/DKIM records
   b. Review contact list quality (remove invalid addresses)
4. If delivered but no opens:
   a. Check subject line and preheader
   b. Verify tracking pixel is not stripped by HTML
   c. Check if emails land in spam folder
```

### "SureNotify email not arriving"

```
1. Check send response → was recipient in success[] or failure{}?
2. If in success[]:
   a. GET /v1/events?id={message_id}  → check event status
   b. Status progression: accept → delivery (or bounce/complaint)
   c. If no events after 5 min, check sender domain auth
3. If in failure{}:
   a. Read error message in failure object
   b. Common: invalid email format, unverified domain
4. Verify webhook is receiving events (if configured)
```

### "SMS not delivered"

```
1. Check send response for success/failure
2. GET /v1/sms/events?id={message_id}
3. If status=bounce:
   a. Verify phone number format (numeric only)
   b. Check country_code is correct
   c. Ensure content includes company name
4. If no events:
   a. Check alive_mins setting (default 5 min retry)
   b. Verify phone number is a valid mobile number
```

### "Webhook not receiving events"

```
1. GET /v1/webhooks (or /v1/sms/webhooks)  → confirm webhook URL and events
2. Check webhook URL is publicly accessible (not localhost)
3. Verify SSL certificate is valid
4. Test endpoint with curl to confirm it accepts POST
5. Check webhook signature verification logic
6. Review server logs for incoming requests
```

---

## QA Checklist — EDM API

### Authentication & Account
- [ ] Requests without `x-api-key` return 403
- [ ] Invalid API key returns `{"message": "Forbidden"}`
- [ ] `GET /v1/balance` returns valid balance

### Contacts
- [ ] Create group returns valid SN
- [ ] List groups with pagination works
- [ ] Import contacts (text) with valid CSV succeeds
- [ ] Import contacts with duplicate headers returns `DUPLICATE_HEADER`
- [ ] Import contacts with missing EMAIL returns `MISSING_REQUIRED_DATA`
- [ ] Import status polling returns final state within expected time
- [ ] Remove contacts with filter works correctly
- [ ] Custom fields match dashboard configuration

### Campaigns
- [ ] Submit campaign with all required fields succeeds
- [ ] Missing required fields returns `40001`
- [ ] Unverified sender returns `40011`
- [ ] Insufficient balance returns `40012`
- [ ] Empty list returns `40013`
- [ ] Past schedule time returns `40019`
- [ ] Subject > 150 chars rejected
- [ ] Preheader > 60 chars rejected
- [ ] Campaign status transitions: QUEUED → SENDING → SENT
- [ ] Pause campaign works on SENDING status
- [ ] Delete campaign works
- [ ] Variable substitution `${FIELD}` renders correctly in delivered email

### A/B Testing
- [ ] Each test type (1=subject, 2=sender, 3=content) creates valid test
- [ ] Test proportion 0-100 accepted
- [ ] Winner is selected after test duration

### Reporting
- [ ] Campaign codes query with date range returns expected campaigns
- [ ] Performance report returns all metric fields
- [ ] Report export returns export_sn
- [ ] Export download URL is accessible
- [ ] Report export respects 1 req/10 sec rate limit

### Templates
- [ ] List templates returns available templates
- [ ] Get template by SN returns HTML content

---

## QA Checklist — SureNotify API

### Email
- [ ] Send single email succeeds, returns message ID
- [ ] Send batch (up to 100 recipients) succeeds
- [ ] 101+ recipients in single request rejected
- [ ] Variables render correctly in delivered email
- [ ] Variable > 100 chars returns error
- [ ] Invalid recipient email returns in `failure` object
- [ ] Unverified sender domain returns error
- [ ] Event query returns delivery status for sent message

### SMS
- [ ] Send SMS with valid number succeeds
- [ ] Company name in content is required
- [ ] Non-numeric phone number rejected
- [ ] Invalid country code handled
- [ ] Variable substitution works in SMS content
- [ ] Event query returns SMS delivery status
- [ ] alive_mins parameter affects retry behavior

### Webhooks (Email & SMS)
- [ ] Create webhook with valid URL succeeds
- [ ] Query webhooks returns configured webhooks
- [ ] Delete webhook removes it
- [ ] Webhook receives events for subscribed types
- [ ] Webhook signature verification passes for valid requests
- [ ] Tampered signature rejected
- [ ] Webhook handles duplicate events idempotently

### Domain Authentication
- [ ] Create domain returns DNS records
- [ ] Verify succeeds after DNS propagation
- [ ] Delete domain removes authentication
- [ ] Sending from verified domain works
- [ ] Sending from unverified domain fails

---

## Integration Testing Patterns

### Mock API Responses

For CI/CD pipelines, mock the NewsLeopard APIs to avoid hitting production:

```python
# Example: pytest fixture for mocking EDM API
import responses

@responses.activate
def test_create_campaign():
    responses.add(
        responses.POST,
        "https://api.newsleopard.com/v1/campaign/normal/submit",
        json={"sn": "campaign-123", "status": "QUEUED"},
        status=200
    )
    # ... test code
```

### End-to-End Test Flow (EDM)

```python
def test_campaign_e2e():
    # 1. Check balance
    balance = api.get_balance()
    assert balance > 0

    # 2. Create test group
    group_sn = api.create_group("E2E Test Group")

    # 3. Import test contacts
    import_sn = api.import_contacts_text(group_sn, "EMAIL\ntest@example.com")
    wait_for_import(import_sn)

    # 4. Submit campaign
    campaign_sn = api.submit_campaign(
        lists=[group_sn],
        subject="E2E Test",
        html_content="<p>Test</p>"
    )

    # 5. Verify campaign status
    status = api.get_campaign_status(campaign_sn)
    assert status in ["QUEUED", "SENDING", "SENT"]

    # 6. Cleanup
    api.delete_campaign(campaign_sn)
```

### Webhook Testing

```python
def test_webhook_signature():
    """Verify webhook signature validation logic."""
    api_key = "test-key"
    message_id = "msg-123"
    event_type = "3"  # delivery

    payload = f"{message_id}{event_type}"
    expected_sig = hmac.new(
        api_key.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()

    assert verify_webhook(api_key, message_id, event_type, expected_sig)
    assert not verify_webhook(api_key, message_id, event_type, "tampered")
```

---

## Monitoring & Alerting

### Key Metrics to Track

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| API error rate | Response status codes | > 5% errors in 5 min |
| Delivery rate | Report performance | < 90% delivery |
| Bounce rate | Report performance | > 10% bounces |
| Balance | Account balance | < 1000 credits |
| Webhook failures | Webhook endpoint logs | > 3 consecutive failures |
| Rate limit hits | API responses | Any occurrence |

### Health Check Pattern

```python
def health_check():
    """Periodic health check for NewsLeopard integration."""
    checks = {}

    # EDM API connectivity
    try:
        balance = edm_api.get_balance()
        checks["edm_api"] = "ok"
        checks["balance"] = balance
    except Exception as e:
        checks["edm_api"] = f"error: {e}"

    # SureNotify API connectivity
    try:
        webhooks = surenotify_api.get_webhooks()
        checks["surenotify_api"] = "ok"
    except Exception as e:
        checks["surenotify_api"] = f"error: {e}"

    return checks
```
