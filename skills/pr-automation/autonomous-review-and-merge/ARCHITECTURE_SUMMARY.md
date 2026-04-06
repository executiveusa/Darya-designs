# Autonomous PR Review & Merge Skill - Architecture Summary

## What Was Built

A production-ready, autonomous PR review and merge system integrated into the OpenHands ecosystem. This implements the Deep Agent QA philosophy: **Speed + Safety** through intelligent, multi-perspective code validation.

## Core Philosophy

**Empathy + Paranoia**
- **Empathy**: Understand code impact across security, quality, performance, UX
- **Paranoia**: Find how things break, stress test assumptions, validate rigorously

Instead of passive testing (checking if code works), this system actively probes (finding how code breaks).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Event (PR opened)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            PR Orchestrator (Main Agent)                          │
│  - Coordinates all review agents                                │
│  - Aggregates results                                           │
│  - Makes merge decision                                         │
│  - Executes merge (if approved)                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
  ┌────────────┐  ┌────────────┐  ┌────────────┐
  │  Fetch PR  │  │  Calculate │  │   Risk     │
  │  Context   │  │ Confidence │  │ Assessment │
  │            │  │   Score    │  │            │
  └────────────┘  └────────────┘  └────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────┐
        │ Multi-Perspective Review Agents         │
        │ (Run in parallel: 15-30 seconds)       │
        ├────────────────────────────────────────┤
        │                                        │
        │  ┌──────────────────────────────────┐ │
        │  │ Security Agent (Paranoid Mode)   │ │
        │  │ - Dependency vulnerabilities     │ │
        │  │ - Hardcoded credentials          │ │
        │  │ - OWASP patterns                 │ │
        │  │ - Permission escalation          │ │
        │  │ - Supply chain risks             │ │
        │  │ Score: 30% weight (critical)     │ │
        │  └──────────────────────────────────┘ │
        │                                        │
        │  ┌──────────────────────────────────┐ │
        │  │ Code Quality Agent (Empathy)     │ │
        │  │ - Complexity analysis            │ │
        │  │ - Naming conventions             │ │
        │  │ - Duplication detection          │ │
        │  │ - Documentation quality          │ │
        │  │ Score: 20% weight                │ │
        │  └──────────────────────────────────┘ │
        │                                        │
        │  ┌──────────────────────────────────┐ │
        │  │ Testing Agent (Rigor Mode)       │ │
        │  │ - Test suite execution           │ │
        │  │ - Coverage metrics               │ │
        │  │ - Critical path coverage         │ │
        │  │ - Regression risk                │ │
        │  │ Score: 25% weight                │ │
        │  └──────────────────────────────────┘ │
        │                                        │
        │  ┌──────────────────────────────────┐ │
        │  │ Performance Agent                │ │
        │  │ - Bundle size analysis           │ │
        │  │ - Build time impact              │ │
        │  │ - Runtime performance            │ │
        │  │ - Scalability                    │ │
        │  │ Score: 15% weight                │ │
        │  └──────────────────────────────────┘ │
        │                                        │
        │  ┌──────────────────────────────────┐ │
        │  │ UX/Integration Agent             │ │
        │  │ - Browser compatibility          │ │
        │  │ - Accessibility (WCAG)           │ │
        │  │ - Responsive design              │ │
        │  │ - Integration points             │ │
        │  │ Score: 10% weight                │ │
        │  └──────────────────────────────────┘ │
        │                                        │
        └────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    ┌────────────┐              ┌────────────────┐
    │  Aggregate │              │ Apply Risk     │
    │  Scores    │              │ Gates          │
    │            │              │                │
    │ Security   │              │ Critical       │
    │ Quality    │              │ Security → No  │
    │ Testing    │              │                │
    │ Performance│              │ Merge Conflict │
    │ UX         │              │ → No           │
    │            │              │                │
    │ = Combined │              │ Breaking Change│
    │ Confidence │              │ → Caution      │
    │ Score      │              │                │
    └────────────┘              └────────────────┘
         │                               │
         └───────────────┬───────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   Decision Tree                    │
        │                                    │
        │ If Confidence ≥ 0.92              │
        │   → AUTO_MERGE ✅                 │
        │                                    │
        │ Else if Confidence ≥ 0.85         │
        │   → APPROVE_REQUEST_REVIEW 👀     │
        │                                    │
        │ Else if Confidence ≥ 0.75         │
        │   → REQUEST_CHANGES ⚠️            │
        │                                    │
        │ Else                              │
        │   → REJECT ❌                     │
        │                                    │
        └────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │ Post Summary Comment to PR         │
        │ (with scores, findings, next steps)│
        └────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │ If AUTO_MERGE              │
         │                               │
         ▼                               ▼
    ┌────────────┐              ┌────────────────┐
    │  Execute   │              │  Enable 6-Hour │
    │  Merge     │              │  Monitoring    │
    │  (squash)  │              │                │
    │            │              │  - Error rates │
    │ Delete     │              │  - Performance │
    │ branch     │              │  - Rollback    │
    │            │              │                │
    └────────────┘              └────────────────┘
```

## File Structure

```
skills/pr-automation/autonomous-review-and-merge/
│
├── __init__.py
│   └─ Package exports for main functions
│
├── README.md (THIS FILE)
│   └─ Quick start guide and feature overview
│
├── skill.md
│   └─ Comprehensive 1000+ line skill documentation
│   └─ Agent implementations, configuration, integration points
│
├── ARCHITECTURE_SUMMARY.md (THIS FILE)
│   └─ High-level architecture overview
│
├── INTEGRATION_GUIDE.md
│   └─ Step-by-step integration with OpenHands
│   └─ Webhook setup, configuration, troubleshooting
│
├── config.py (600 lines)
│   └─ Configuration system
│   ├─ Dataclasses for all config aspects
│   ├─ Predefined profiles: strict, moderate, permissive, info_only
│   └─ Environment-based loading
│
├── github_mcp_tool.py (400 lines)
│   └─ GitHub API wrapper (MCP-compatible)
│   ├─ PullRequestContext dataclass
│   ├─ GitHubMCPTool class for GitHub operations
│   ├─ list_prs, get_pr, post_comment, merge_pr, etc.
│   └─ LiteLLM tool definition for agent use
│
├── pr_review_agents.py (800 lines)
│   └─ Multi-perspective review agents
│   ├─ BaseReviewAgent abstract class
│   ├─ SecurityReviewAgent (paranoid mode)
│   ├─ CodeQualityAgent (empathy mode)
│   ├─ TestingCoverageAgent (rigor mode)
│   ├─ PerformanceAgent
│   ├─ UXIntegrationAgent
│   └─ MultiPerspectiveReviewer orchestrator
│
└── pr_orchestrator.py (1000 lines)
    └─ Main decision engine & execution
    ├─ MergeDecisionEngine class
    ├─ MergeRecommendation dataclass
    ├─ Confidence calculation
    ├─ Risk assessment
    ├─ Decision tree logic
    ├─ Rate limiting
    ├─ Safeguards
    └─ review_and_merge_pr() main entry point
```

## Key Components

### 1. GitHub MCP Tool (`github_mcp_tool.py`)
- **Purpose**: Unified interface to GitHub API
- **Uses**: `gh` CLI + GitHub API
- **Operations**: List PRs, get PR context, post comments, approve, merge
- **Integration**: Can be used as MCP tool by any agent

### 2. Review Agents (`pr_review_agents.py`)
Five specialized agents running in parallel:

| Agent | Mode | Focus | Weight |
|-------|------|-------|--------|
| Security | Paranoid | Find vulnerabilities | 30% |
| Code Quality | Empathy | Code health | 20% |
| Testing | Rigor | Test coverage & reliability | 25% |
| Performance | Measurement | Speed & scalability | 15% |
| UX/Integration | User-focused | Experience & system integration | 10% |

**Parallelization**: All 5 agents run concurrently (15-30 seconds total)

### 3. Merge Decision Engine (`pr_orchestrator.py`)
- **Aggregates** all review results
- **Calculates** confidence score (weighted average)
- **Applies** risk gates and safety constraints
- **Makes** autonomous decision
- **Executes** merge or requests changes
- **Monitors** for 6 hours post-merge

### 4. Configuration System (`config.py`)
- **Presets**: strict, moderate, permissive, info_only
- **Customizable**: Every decision threshold can be tuned
- **Environment-based**: Loads from `.env` or environment variables
- **Type-safe**: Uses dataclasses for validation

## Decision Logic

### Confidence Score Calculation

```python
confidence = (
    security_score × 0.30 +
    code_quality_score × 0.20 +
    testing_score × 0.25 +
    performance_score × 0.15 +
    ux_score × 0.10
)

# Apply penalties for critical findings
for each critical finding:
    confidence -= 0.05
```

### Decision Tree

```
if critical_security_risk:
    → REJECT

if breaking_changes and confidence < 0.85:
    → REJECT

if merge_conflicts:
    → REQUEST_CHANGES

if confidence >= 0.92:
    → AUTO_MERGE ✅

elif confidence >= 0.85:
    → APPROVE_REQUEST_REVIEW 👀

elif confidence >= 0.75:
    → REQUEST_CHANGES ⚠️

else:
    → REJECT ❌
```

## Integration Points

### 1. With CodeActAgent
```python
class PRReviewAgent(CodeActAgent):
    async def step(self, state):
        result = await review_and_merge_pr(...)
```

### 2. With GitHub Webhooks
```
GitHub Event → Webhook Handler → Async Task Queue
            → review_and_merge_pr() → Post Comment
            → Merge (if approved) → Monitor
```

### 3. With Existing Agents
```python
agent.set_mcp_tools([create_github_tool_definition(repo)])
```

### 4. As Skill
```python
class PRAutomationSkill(BaseSkill):
    async def execute(self, pr_number):
        return await review_and_merge_pr(...)
```

## Safety Mechanisms

### 1. Confidence Thresholds
- 0.92+: Auto-merge (low risk)
- 0.85-0.92: Approve (request human review)
- 0.75-0.85: Request changes
- <0.75: Reject

### 2. Risk Gates
- ✅ Critical security findings block merge
- ✅ Breaking changes flagged
- ✅ Merge conflicts detected
- ✅ New dependencies reviewed
- ✅ Author risk profiling
- ✅ Rate limiting (5/hour)
- ✅ Timeout enforcement

### 3. Post-Merge Monitoring
- 6-hour observation window
- Error rate detection
- Performance degradation alerts
- Automatic rollback on critical issues

## Performance Metrics

### Execution Timeline
```
T+0s:  PR webhook received
T+1s:  Fetch PR context
T+5s:  Start parallel agent execution
       - Security Agent: 3-5s
       - Code Quality: 2-3s
       - Testing: 15-30s (test suite dependent)
       - Performance: 10-20s
       - UX: 5-10s
T+30s: All results aggregated
T+32s: Decision made, summary posted
T+35s: Merge executed (if auto-merge)
```

### Review Overhead
- Skill initialization: <1s
- PR context fetch: 1-2s
- Agent execution: 15-30s (mostly test suite)
- Decision & merge: 1-2s
- **Total**: 20-40 seconds per PR

## Extensibility

### Add New Review Agent
```python
class CustomAgent(BaseReviewAgent):
    async def _review(self, context):
        # Implement custom logic
        return AgentReviewResult(...)

# Register in MultiPerspectiveReviewer
self.agents.append(CustomAgent())
```

### Customize Scoring
```python
# In config.py
SCORE_WEIGHTS = {
    "security": 0.40,  # Increase security weight
    "testing": 0.30,
    "code_quality": 0.15,
    "performance": 0.10,
    "ux": 0.05,
}
```

### Add Custom Risk Gates
```python
# In pr_orchestrator.py MergeDecisionEngine._make_decision()
if custom_risk_condition:
    return MergeDecision.REJECT
```

## Observability

### Metrics Emitted
```
pr_review_duration_seconds
pr_review_confidence_score
pr_auto_merge_success_rate
pr_security_findings
pr_code_quality_score
pr_test_coverage
pr_performance_impact
```

### Structured Logging
```python
logger.info("pr_review_completed", extra={
    "pr_number": 123,
    "decision": "auto_merge",
    "confidence": 0.92,
    "duration_seconds": 32,
})
```

### Integration with Monitoring
- Prometheus metrics
- Grafana dashboards
- Loki logs
- Custom alerts

## Known Limitations

1. **Test Suite Dependent**: Accuracy depends on existing test quality
2. **Pattern-Based Security**: Not comprehensive vulnerability detection
3. **No Deep Context**: Can't understand business logic
4. **Configuration Dependent**: Thresholds need tuning per org
5. **Heuristic Performance**: Estimation, not actual profiling

## Future Enhancements

- Custom rule engine (org-specific policies)
- ML-based scoring (learn from human overrides)
- Risk profiling per code area
- Incident correlation
- Enhanced rollback automation
- Team-specific fine-tuning
- Issue tracker integration

## Development Notes

### Testing
```bash
# Test with single PR (no merge)
python -c "
import asyncio
from skills.pr_automation.autonomous_review_and_merge import review_and_merge_pr

async def test():
    result = await review_and_merge_pr(
        repo='executiveusa/Darya-designs',
        pr_number=123,
        auto_merge_enabled=False,
        post_comment=True,
    )

asyncio.run(test())
"
```

### Configuration
```bash
# Load environment
source .env

# Test configuration
python -c "
from config import load_config
config = load_config('moderate')
print(config.to_dict())
"
```

## Related Documentation

- [README.md](./README.md) - Quick start
- [skill.md](./skill.md) - Comprehensive design doc
- [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) - Integration instructions
- [config.py](./config.py) - Configuration reference

---

**Summary**: A production-ready PR review system implementing Deep Agent QA philosophy. 5 specialized agents, confidence-based decisions, safety gates, and full OpenHands integration. ~3000 lines of well-structured Python code.
