# Autonomous PR Review & Merge Skill - Integration Guide

This guide shows how to integrate the PR automation skill into your OpenHands ecosystem.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Integration with CodeActAgent](#integration-with-codeactagent)
3. [GitHub Webhook Setup](#github-webhook-setup)
4. [Configuration](#configuration)
5. [Monitoring & Observability](#monitoring--observability)
6. [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Environment Setup

```bash
# Set required environment variables
export GITHUB_TOKEN="ghp_your_github_token_here"
export GH_REPO="executiveusa/Darya-designs"
export PR_REVIEW_MODE="autonomous"  # or "approval_required", "info_only"

# Verify configuration
echo $GITHUB_TOKEN
echo $GH_REPO
```

### 2. Install Dependencies

```bash
# Install the skill (already in your skills directory)
cd /home/user/Darya-designs

# No additional dependencies needed - uses existing openhands infrastructure
poetry install
```

### 3. Test with a Single PR

```bash
# Run a single PR review
python -c "
import asyncio
from skills.pr_automation.autonomous_review_and_merge import review_and_merge_pr

async def test():
    result = await review_and_merge_pr(
        repo='executiveusa/Darya-designs',
        pr_number=123,
        auto_merge_enabled=False,  # Test without merging
        post_comment=True,
    )
    print(result)

asyncio.run(test())
"
```

## Integration with CodeActAgent

### Option 1: Agent-Based Trigger

Add the skill as an agent that extends CodeActAgent:

```python
# openhands/agenthub/pr_review_agent/pr_review_agent.py

from openhands.agenthub.codeact_agent import CodeActAgent
from openhands.events.action import AgentFinishAction, MessageAction
from skills.pr_automation.autonomous_review_and_merge import review_and_merge_pr

class PRReviewAgent(CodeActAgent):
    """
    Agent for autonomous PR review and merge.
    Uses Deep Agent QA philosophy for comprehensive validation.
    """

    async def step(self, state):
        # Extract PR number from user message
        pr_number = self._extract_pr_number(state.history)

        if not pr_number:
            return MessageAction("Please specify a PR number")

        # Run review
        result = await review_and_merge_pr(
            repo="executiveusa/Darya-designs",
            pr_number=pr_number,
            auto_merge_enabled=True,
            post_comment=True,
        )

        # Return result
        return AgentFinishAction(
            output=f"PR #{pr_number} reviewed. Decision: {result['decision']}"
        )

    @staticmethod
    def _extract_pr_number(history):
        """Extract PR number from conversation history"""
        for event in reversed(history):
            if hasattr(event, 'message'):
                import re
                match = re.search(r'#(\d+)', event.message)
                if match:
                    return int(match.group(1))
        return None
```

### Option 2: Skill-Based Integration

Add as a skill that agents can invoke:

```python
# skills/pr_automation/__init__.py

from openhands.skills.base import BaseSkill

class PRAutomationSkill(BaseSkill):
    """
    Skill for autonomous PR review and merge automation.
    """

    name = "pr_automation"
    description = "Review and merge PRs autonomously"

    async def execute(self, pr_number: int, **kwargs):
        from .autonomous_review_and_merge import review_and_merge_pr

        return await review_and_merge_pr(
            repo=kwargs.get("repo", "executiveusa/Darya-designs"),
            pr_number=pr_number,
            auto_merge_enabled=kwargs.get("auto_merge_enabled", True),
            post_comment=kwargs.get("post_comment", True),
        )
```

### Option 3: Tool-Based Integration (MCP)

Register as an MCP tool for use by any agent:

```python
# openhands/mcp/github_pr_tool.py

from litellm import ChatCompletionToolParam
from skills.pr_automation.autonomous_review_and_merge import create_github_tool_definition

# Register tool
GITHUB_PR_TOOL = create_github_tool_definition("executiveusa/Darya-designs")

# Add to agent's tools
agent.set_mcp_tools([GITHUB_PR_TOOL])
```

## GitHub Webhook Setup

### 1. Create Webhook in GitHub

Go to: `https://github.com/executiveusa/Darya-designs/settings/hooks`

**Create new webhook:**

```
Payload URL: https://your-domain/webhooks/pr-review
Content type: application/json
Events: Let me select individual events
  ✓ Pull requests (all events)
Secret: (generate a random secret)
Active: ✓
```

### 2. Create Webhook Handler

```python
# openhands/server/webhook_handlers.py

from fastapi import FastAPI, Request, verify_signature
from skills.pr_automation.autonomous_review_and_merge import review_and_merge_pr
import asyncio

app = FastAPI()

@app.post("/webhooks/pr-review")
async def handle_pr_webhook(request: Request):
    # Verify GitHub signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_signature(await request.body(), signature, GITHUB_SECRET):
        return {"error": "Invalid signature"}

    payload = await request.json()

    # Only process PR opened/reopened/synchronized events
    if payload["action"] not in ["opened", "reopened", "synchronize"]:
        return {"skipped": "event not processed"}

    # Queue review task
    pr_number = payload["pull_request"]["number"]
    repo = payload["repository"]["full_name"]

    asyncio.create_task(
        review_and_merge_pr(
            repo=repo,
            pr_number=pr_number,
            auto_merge_enabled=True,
            post_comment=True,
        )
    )

    return {"queued": pr_number}
```

### 3. Deploy Webhook Handler

```bash
# The webhook handler needs to be running on a publicly accessible server
# Examples: AWS Lambda, Heroku, Google Cloud Run, DigitalOcean, etc.

# For local testing, use ngrok:
ngrok http 8000

# Update webhook URL in GitHub to ngrok URL
```

## Configuration

### Basic Configuration

```python
# openhands/config/pr_automation_config.py

from skills.pr_automation.autonomous_review_and_merge.config import (
    load_config,
    PRAutomationConfig,
    create_moderate_config,
)

# Load preset configuration
config = load_config("moderate")  # strict, moderate, permissive, info_only

# Or create custom config
config = PRAutomationConfig(
    repo="executiveusa/Darya-designs",
    mode="autonomous",
    merge_config__auto_merge_confidence_threshold=0.90,
)
```

### Environment-Based Configuration

```bash
# .env file

# Repository
GH_REPO=executiveusa/Darya-designs
GITHUB_TOKEN=ghp_xxxx...

# Mode: autonomous, approval_required, info_only
PR_REVIEW_MODE=autonomous

# Confidence thresholds (0.0-1.0)
AUTO_MERGE_THRESHOLD=0.92
APPROVE_THRESHOLD=0.85

# Feature flags
ENABLE_AUTO_MERGE=true
ENABLE_MONITORING=true
POST_SUMMARY_COMMENTS=true

# Rate limiting
MAX_MERGES_PER_HOUR=5

# Safeguards
BLOCK_CRITICAL_SECURITY=true
REQUIRE_TESTS=true
MIN_COVERAGE_PCT=0.75
```

### Loading Configuration

```python
from dotenv import load_dotenv
from skills.pr_automation.autonomous_review_and_merge.config import load_config
import os

load_dotenv()

# Load configuration by environment
mode = os.getenv("PR_REVIEW_MODE", "moderate")
config = load_config(mode)

# Override specific values
config.repo = os.getenv("GH_REPO")
config.github_token = os.getenv("GITHUB_TOKEN")
```

## Monitoring & Observability

### Metrics to Track

```python
# openhands/integrations/monitoring/pr_metrics.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class PRReviewMetrics:
    """Metrics for PR review system"""
    review_duration_seconds: float
    confidence_score: float
    decision: str  # auto_merge, approve, request_changes, reject
    security_score: float
    code_quality_score: float
    test_coverage_score: float
    performance_score: float
    ux_score: float
    merged: bool
    merge_strategy: str
    author: str
    files_changed: int
    additions: int
    deletions: int
    timestamp: datetime

    @property
    def decision_made_in_seconds(self) -> float:
        return self.review_duration_seconds

    def to_prometheus_metrics(self) -> str:
        """Format as Prometheus metrics"""
        return f"""
pr_review_duration_seconds{{decision="{self.decision}"}} {self.review_duration_seconds}
pr_review_confidence{{decision="{self.decision}"}} {self.confidence_score}
pr_auto_merge_success{{decision="{self.decision}"}} {"1" if self.merged else "0"}
pr_security_score {self.security_score}
pr_code_quality_score {self.code_quality_score}
pr_test_coverage {self.test_coverage_score}
"""
```

### Logging

```python
import logging

logger = logging.getLogger("pr_automation")
logger.setLevel(logging.INFO)

# Structured logging
logger.info("pr_review_started", extra={
    "pr_number": 123,
    "repo": "executiveusa/Darya-designs",
    "timestamp": datetime.now().isoformat(),
})

logger.info("pr_review_completed", extra={
    "pr_number": 123,
    "decision": "auto_merge",
    "confidence": 0.92,
    "duration_seconds": 45,
})

logger.warning("high_risk_pr_detected", extra={
    "pr_number": 123,
    "risk_level": "high",
    "security_score": 0.70,
})

logger.error("pr_review_failed", extra={
    "pr_number": 123,
    "error": str(e),
    "traceback": traceback.format_exc(),
})
```

### Observability Stack

```yaml
# docker-compose.observability.yml

version: '3'
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  loki:
    image: grafana/loki
    ports:
      - "3100:3100"
```

## Troubleshooting

### Issue: "GitHub token not found"

**Solution:**
```bash
export GITHUB_TOKEN="your_token_here"
# or set in .env file
```

### Issue: "PR merging fails with 403"

**Possible causes:**
1. GitHub token doesn't have `repo` and `admin:repo_hook` scopes
2. Branch protection rules require reviews

**Solution:**
```bash
# Check token scopes
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Verify branch protection in GitHub Settings
# Disable "Require pull request reviews" if testing
```

### Issue: Webhook not triggering

**Debugging steps:**
```bash
# Check webhook delivery in GitHub
# Settings → Webhooks → (webhook) → Recent Deliveries

# Verify webhook is receiving events
# Check logs on webhook handler server

# Test webhook locally with ngrok
ngrok http 8000
# Update GitHub webhook URL to ngrok URL
```

### Issue: Test suite failing in PR review

**Solution:**
```python
# Ensure test suite runs in PR environment
# openhands/skills/pr_automation/autonomous_review_and_merge/pr_review_agents.py

# Check if test command is configured correctly
# Default: npm run test && poetry run pytest

# Override test command in config
config.testing_config.test_command = "npm run test:ci"
```

### Issue: Confidence score too low

**Debug steps:**
```python
# Print detailed review breakdown
result = await review_and_merge_pr(...)

# Check individual agent scores
for agent_name, score in result['scores'].items():
    print(f"{agent_name}: {score:.0%}")

# Check which agent is failing
# Lower thresholds if being too strict
config.merge_config.auto_merge_confidence_threshold = 0.85
```

## Next Steps

1. **Monitor Performance**: Track PR review accuracy vs. human reviews
2. **Adjust Thresholds**: Fine-tune confidence thresholds based on production incidents
3. **Extend Agents**: Add domain-specific review agents for your codebase
4. **Integrate Feedback**: Use human overrides to improve agent decision-making
5. **Scale Out**: Run multiple concurrent PR reviews

## Support & Contributing

For issues, questions, or contributions:
- Open an issue in the repository
- Check existing integration examples
- Review skill documentation at `./skill.md`
