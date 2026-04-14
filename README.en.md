# Newsleopard API — AI Agent Skill

English | [繁體中文](README.md)

**Enable AI coding assistants to generate integration code for Newsleopard's newsletter and SMS APIs, covering EDM marketing campaigns and SureNotify transactional notifications.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill Format](https://img.shields.io/badge/Format-Agent%20Skill-blue.svg)](https://agentskills.io)

---

## About Newsleopard

[Newsleopard](https://newsleopard.com) is the leading email marketing platform in Taiwan, trusted by over 15,000 businesses. The platform offers Email EDM marketing and SMS messaging services, featuring intelligent subscriber list management, automated behavioral analytics, and a high-performance cloud delivery infrastructure — capable of sending 10,000 emails per minute with a 99% delivery rate.

Newsleopard also provides **SureNotify**, a transactional notification service designed for real-time scenarios such as order confirmations, password resets, and verification codes, ensuring critical messages are delivered on time.

---

## Features

- **EDM API Integration** (20 endpoints) — Contact management, campaign creation/scheduling/A-B testing, performance report export, templates, automation scripts, account balance queries
- **SureNotify API Integration** (11 endpoints) — Transactional email delivery, SMS messaging, webhook management, event tracking, sender domain verification
- **Debugging Workflows** — Common error code reference, step-by-step troubleshooting guides (no opens, undelivered emails, undelivered SMS, webhook not triggered)
- **QA Checklists** — Comprehensive verification items for both EDM API and SureNotify API

---

## What is an Agent Skill?

An Agent Skill is a knowledge package following the [agentskills.io open standard](https://agentskills.io) that allows AI coding assistants to automatically load domain-specific API specs, best practices, and debugging knowledge when needed.

A single Skill works across tools, supporting these major AI coding assistants:

| AI Tool | Support |
|---------|---------|
| Claude Code | ✅ |
| GitHub Copilot (VS Code) | ✅ |
| Cursor | ✅ |
| Windsurf | ✅ |
| OpenAI Codex | ✅ |
| OpenClaw | ✅ |

---

## Installation

### Prerequisites

| Method | Requirements |
|--------|-------------|
| Quick install (`npx skills add`) | [Node.js](https://nodejs.org/) 18+ (includes `npx`) |
| Manual install (`git clone`) | [Git](https://git-scm.com/) |

#### Quick Install (Recommended)

One-command install using `npx skills add`:

```bash
# Install to current project (default, all supported AI assistants)
npx skills add https://github.com/Newsleopard/nlm-open-skills --all

# Global install (available to all projects)
npx skills add https://github.com/Newsleopard/nlm-open-skills --all -g

# Install for a specific AI assistant only (e.g., Claude Code)
npx skills add https://github.com/Newsleopard/nlm-open-skills -a claude-code -y
```

> **Common flags:** `--all` installs for all agents and skips prompts; `-a <agent>` targets a specific agent (e.g., `claude-code`, `cursor`, `copilot`); `-y` skips confirmation; `-g` installs globally.

#### Manual Install

Clone this repository into the corresponding Skills directory for your AI tool.

### Claude Code

**Project install** (single project only):

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.claude/skills/newsleopard-api
```

**Global install** (available to all projects):

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.claude/skills/newsleopard-api
```

### GitHub Copilot (VS Code)

**Project install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.github/skills/newsleopard-api
```

**Global install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.copilot/skills/newsleopard-api
```

> Also supports the `.agents/skills/` directory.

### Cursor

**Project install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.cursor/skills/newsleopard-api
```

**Global install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.cursor/skills/newsleopard-api
```

> Also supports the `.agents/skills/` directory and GitHub Remote Rule imports.

### Windsurf

**Project install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.windsurf/skills/newsleopard-api
```

**Global install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.codeium/windsurf/skills/newsleopard-api
```

### OpenAI Codex

**Project install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <your-project>/.agents/skills/newsleopard-api
```

**Global install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.agents/skills/newsleopard-api
```

**System-level install:**

```bash
sudo git clone https://github.com/Newsleopard/nlm-open-skills.git /etc/codex/skills/newsleopard-api
```

> Supports symlinks, allowing you to point to a shared location.

### OpenClaw

**Project install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git <workspace>/skills/newsleopard-api
```

**Global install:**

```bash
git clone https://github.com/Newsleopard/nlm-open-skills.git ~/.openclaw/skills/newsleopard-api
```

> Load priority: workspace > `~/.openclaw/skills` > bundled.
> You can configure additional search paths via `skills.load.extraDirs`.
> If published to ClawHub in the future, install with `clawhub install <skill-slug>`.

---

## Skill Content Structure

```
newsleopard-api/
├── SKILL.md                        # Skill entry point: API overview, quick reference, integration patterns
└── references/
    ├── edm-api.md                  # EDM API reference: endpoints, parameters, request/response examples
    ├── surenotify-api.md           # SureNotify API reference: Email, SMS, Webhook, domain verification
    └── debugging-qa.md             # Debugging guide and QA checklists
```

| File | Description |
|------|-------------|
| `SKILL.md` | Skill entry point with quick reference tables for both APIs, authentication, rate limits, and common integration flows |
| `references/edm-api.md` | Full EDM API endpoint specs including contacts, campaigns, A/B testing, reports, templates, and automation |
| `references/surenotify-api.md` | Full SureNotify API endpoint specs including email, SMS, webhook signature verification, and domain authentication |
| `references/debugging-qa.md` | Troubleshooting workflows, error code reference, and separate QA acceptance checklists for EDM and SureNotify |

---

## API Coverage

### EDM API (Marketing Campaigns)

| Category | Endpoints |
|----------|-----------|
| Contact Management | Create groups, list groups, import contacts (file/text), check import status, remove contacts |
| Campaign Management | Submit campaign, single-upload campaign, A/B test campaign, delete campaign, pause campaign, check campaign status |
| Reports | Get campaign codes, campaign performance, export reports, get download links |
| Templates | List templates, get template content |
| Automation | Trigger/stop automation scripts |
| Account | Check balance |

### SureNotify API (Transactional Notifications)

| Category | Endpoints |
|----------|-----------|
| Email | Send email |
| SMS | Send SMS |
| Email Webhook | Create/update, query, delete |
| SMS Webhook | Create/update, query, delete |
| Event Queries | Email events, SMS events |
| Domain Verification | Create verification record, verify DNS, remove domain |

---

## Using with MCP Server

In addition to the Agent Skill, Newsleopard also provides an **MCP Server** that allows AI assistants to directly operate platform features without writing code.

### Skill vs MCP Server

| | Agent Skill | MCP Server |
|---|---|---|
| **Purpose** | API knowledge base for AI coding assistants | Let AI directly operate platform features |
| **Use Case** | Developers writing code, with AI referencing API specs to generate integration code | Marketers or anyone managing newsletters through AI conversation |
| **Code Required?** | Yes, AI helps you write API integration code | No, AI executes operations directly |
| **Supported Tools** | Claude Code, Copilot, Cursor, Windsurf, Codex, OpenClaw | Claude Desktop, ChatGPT, Cursor, Lovable, GitHub Copilot, OpenAI Codex |

### MCP Server Configuration

For the full installation and setup walkthrough, see the official guide: [Newsleopard AI Agent Setup](https://newsleopard.com/ai-lab/ai-agent/).

**Connection details:**

- MCP endpoint: `https://mcp.newsleopard.com/mcp`
- Authentication: **OAuth 2.1** (guided login and authorization on first connection)

**Supported AI clients:** Claude (Desktop, requires Claude Pro/Team/Enterprise), ChatGPT, Cursor, Lovable, GitHub Copilot, OpenAI Codex.

**Quick setup (Claude Desktop example):**

1. Open Settings → Connectors → click "Add custom connector"
2. Name it `Newsleopard`, URL: `https://mcp.newsleopard.com/mcp`
3. Click "Connect", sign in with your Newsleopard account, and authorize
4. Start with natural language commands such as "Analyze this month's open rates"

The MCP Server provides a full tool set covering campaign management, report analysis, list management, template operations, automation control, and more.

---

## Usage Examples

After installing the Skill, you can give natural language instructions to your AI assistant, such as:

**EDM Marketing Campaigns:**

- "Create a marketing campaign using the Newsleopard API to send a promotional email to the VIP group"
- "Query the open rates and click rates for all campaigns from last week"
- "Import this CSV of contacts into the specified group"
- "Create an A/B test campaign to test two different subject lines"
- "Check the remaining sending quota for my account"
- "Export a detailed report for last month's campaigns"

**SureNotify Transactional Notifications:**

- "Send an order confirmation email to the customer using SureNotify"
- "Set up a webhook to receive email delivery and open events"
- "How do I write code to verify webhook signatures?"
- "Help me complete the SPF/DKIM verification process for my sender domain"
- "Send an SMS verification code using SureNotify"

**Debugging & Troubleshooting:**

- "Campaign was sent but there are no open records — how do I troubleshoot?"
- "SureNotify returns 'sender domain unverified' — how do I fix this?"
- "What does API error code 40012 mean?"

---

## Debugging & QA

This Skill includes comprehensive debugging guides and QA checklists (see [`references/debugging-qa.md`](newsleopard-api/references/debugging-qa.md)):

**Debugging Workflows:**

- Campaign sent but no opens/clicks
- SureNotify email not delivered
- SMS not delivered
- Webhook not receiving events

**QA Acceptance Checklists:**

- EDM API — Authentication, contacts, campaigns, A/B testing, reports, templates (30+ test items)
- SureNotify API — Email, SMS, webhooks, domain verification (25+ test items)

---

## Related Links

- [Newsleopard EDM API Documentation](https://newsleopard.com/api/v1/)
- [SureNotify API Documentation](https://newsleopard.com/surenotify/api/v1/)
- [Newsleopard MCP Server Setup Guide](https://newsleopard.com/ai-lab/ai-agent/) — MCP Server connection and authorization walkthrough
- [Agent Skills Open Standard](https://agentskills.io)
- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
- [GitHub Copilot Skills Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-extensions-to-integrate-external-tools-with-copilot-chat)
- [Cursor Skills Documentation](https://docs.cursor.com/context/skills)
- [Windsurf Skills Documentation](https://docs.codeium.com/windsurf/skills)
- [OpenAI Codex Skills Documentation](https://developers.openai.com/codex/skills/)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Made with ❤️ by the Newsleopard Team
