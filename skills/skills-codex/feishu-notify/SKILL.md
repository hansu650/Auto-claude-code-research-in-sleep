---
name: "feishu-notify"
description: "Send a Feishu/Lark notification explicitly requested or already authorized by the user. May serve as a utility for authorized workflow notifications. Use for 发飞书 or notify Feishu; an existing configuration or another skill requesting status updates does not itself authorize a message."
---

# Feishu/Lark Notification

Send a notification: **$ARGUMENTS**

## Overview

This skill provides Feishu/Lark integration for ARIS. It is designed as an **internal utility** — other skills call it at key events (experiment done, review scored, checkpoint waiting). It can also be invoked manually.

**Zero-impact guarantee**: If no `feishu.json` config exists, this skill does nothing and returns silently. All existing workflows are completely unaffected.

## Configuration

The skill reads `~/.codex/feishu.json`. If this file does not exist, **all Feishu functionality is disabled** — skills behave exactly as before.

### Config Format

```json
{
  "mode": "push",
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID",
  "interactive": {
    "bridge_url": "http://localhost:5000",
    "timeout_seconds": 300
  }
}
```

### Modes

| Mode | `"mode"` value | What it does | Requires |
|------|----------------|--------------|----------|
| **Off** | `"off"` or file absent | Nothing. Pure CLI as-is | Nothing |
| **Push only** | `"push"` | Send webhook notifications at key events. Mobile push, no reply | Feishu bot webhook URL |
| **Interactive** | `"interactive"` | Full bidirectional. Approve/reject from Feishu, reply to checkpoints | [feishu-claude-code](https://github.com/joewongjc/feishu-claude-code) running |

## Authorization

Send only messages covered by an explicit user request or an existing session authorization, with the authorized destination and content scope. A calling skill, available webhook or configured mode is not authorization. Skip optional notifications without interrupting the main task when they were not authorized.

## Workflow

### Step 1: Read Config

Read only the mode and required configuration fields through a local parser. Keep webhook URLs and bridge credentials inside the sending process; do not print the raw configuration or secrets into tool output.

- **File not found** → return silently, do nothing
- **`"mode": "off"`** → return silently, do nothing
- **`"mode": "push"`** → proceed to Step 2 (push)
- **`"mode": "interactive"`** → proceed to Step 3 (interactive)

### Step 2: Push Notification (webhook)

Send a rich card to the Feishu webhook:

```bash
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {"tag": "plain_text", "content": "TITLE"},
        "template": "COLOR"
      },
      "elements": [
        {"tag": "markdown", "content": "BODY"}
      ]
    }
  }'
```

**Card templates by event type:**

| Event | Title | Color | Body |
|-------|-------|-------|------|
| `experiment_done` | Experiment Complete | `green` | Results table, delta vs baseline |
| `review_scored` | Review Round N: X/10 | `blue` (≥6) / `orange` (<6) | Score, verdict, top 3 weaknesses |
| `checkpoint` | Checkpoint: Waiting for Input | `yellow` | Question, options, context |
| `error` | Error: [type] | `red` | Error message, what failed |
| `pipeline_done` | Pipeline Complete | `purple` | Final summary, deliverables |
| `custom` | Custom | `blue` | Free-form message from $ARGUMENTS |

**Return immediately after curl** — push mode never waits for a response.

### Step 3: Interactive Notification (bidirectional)

Interactive mode uses [feishu-claude-code](https://github.com/joewongjc/feishu-claude-code) as a bridge:

1. **Send message** to the bridge:
   ```bash
   curl -s -X POST "$BRIDGE_URL/send" \
     -H "Content-Type: application/json" \
     -d '{"type": "EVENT_TYPE", "title": "TITLE", "body": "BODY", "options": ["approve", "reject", "custom"]}'
   ```

2. **Wait for reply** (with timeout):
   ```bash
   curl -s "$BRIDGE_URL/poll?timeout=$TIMEOUT_SECONDS"
   ```
   Returns: `{"reply": "approve"}` or `{"reply": "reject"}` or `{"reply": "user typed message"}` or `{"timeout": true}`

3. **On timeout**: Return the timeout to the caller. Continue only work already authorized that does not depend on the missing answer; required approval remains pending.

4. **Return the user's reply** to the calling skill so it can act on it.

### Step 4: Verify Delivery

- **Push mode**: Check curl exit code. If non-zero, log warning but do NOT block the workflow.
- **Interactive mode**: If bridge is unreachable, fall back to push mode (if webhook configured) or skip silently.

## Helper Function (for other skills)

Other skills should use this pattern to send notifications:

```markdown
### Feishu Notification (if configured)

First verify explicit user authorization for this notification. Then check if `~/.codex/feishu.json` exists and mode is not "off":
- If **push** mode: send webhook notification with event summary
- If **interactive** mode: send notification and wait for user reply
- If **off** or file absent: skip entirely (no-op)
```

**This check is always guarded.** If the config file doesn't exist, the skill skips the notification block entirely — zero overhead, zero side effects.

## Event Catalog

Skills send these events at these moments:

| Skill | Event | When |
|-------|-------|------|
| `/auto-review-loop` | `review_scored` | After each round's review score |
| `/auto-review-loop` | `pipeline_done` | Loop complete (positive or max rounds) |
| `/auto-paper-improvement-loop` | `review_scored` | After each round's review score |
| `/auto-paper-improvement-loop` | `pipeline_done` | All rounds complete |
| `/run-experiment` | `experiment_done` | Screen session finishes |
| `/idea-discovery` | `checkpoint` | Between phases (if interactive) |
| `/idea-discovery` | `pipeline_done` | Final report ready |
| `/monitor-experiment` | `experiment_done` | Results collected |
| `/research-pipeline` | `checkpoint` | Between workflow stages |
| `/research-pipeline` | `pipeline_done` | Full pipeline complete |

## Key Rules

- **NEVER block a workflow** because Feishu is unreachable. Always fail open.
- **NEVER require Feishu config** — all skills must work without it.
- **Config file absent = mode off.** No error, no warning, no log.
- **Push mode is fire-and-forget.** Send curl, check exit code, move on.
- **Interactive timeout is not approval.** Return control to the caller and preserve any pending required decision.
- **Respect existing authorization**: `AUTO_PROCEED` may continue already authorized work, never approve a new action or resolve a required missing answer.
- **No secrets in notifications.** Never include API keys, tokens, or passwords in Feishu messages.

