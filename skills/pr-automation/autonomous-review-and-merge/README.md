# Autonomous PR Review & Merge Skill

> **Speed + Safety**: Intelligent PR review and merge automation using Deep Agent QA philosophy.

A production-ready skill for the OpenHands ecosystem that autonomously reviews and merges pull requests using multi-perspective analysis, risk assessment, and confidence-based decision making.

## 🎯 Core Concept

Instead of just running tests (passive validation), this skill **thinks like QA**: it probes assumptions, shifts perspectives, finds edge cases, and makes trust-based decisions at scale.

**Philosophy**: Empathy + Paranoia
- **Empathy**: Understand real code impact across security, quality, performance, and UX
- **Paranoia**: Find how things break, stress test edge cases, validate continuously

## ✨ Features

### Multi-Perspective Review
- 🔒 **Security Agent** (Paranoid Mode): Vulnerability scanning, credential detection, supply chain analysis
- 📊 **Code Quality Agent** (Empathy Mode): Architecture, consistency, maintainability assessment
- ✅ **Testing Agent** (Rigor Mode): Test execution, coverage analysis, critical path validation
- ⚡ **Performance Agent**: Bundle size, runtime, scalability measurement
- 🎨 **UX Agent**: Accessibility, browser compatibility, integration validation

### Autonomous Decision Making
```
Confidence ≥ 0.92 → Auto-merge (low risk)
Confidence ≥ 0.85 → Approve (request human review)
Confidence ≥ 0.75 → Request changes
Confidence < 0.75 → Reject
```

### Safety Mechanisms
- Critical security findings block merges
- Breaking changes require approval
- Merge conflicts detected and blocked
- Rate limiting (max 5 merges/hour)
- Post-merge monitoring for 6 hours

### Full Integration
- ✅ Extends existing CodeActAgent
- ✅ Uses GitHub MCP Tool
- ✅ Webhook-ready for GitHub automation
- ✅ Configurable decision thresholds
- ✅ Observable with metrics and logging

## 🚀 Quick Start

### 1. Environment Setup

```bash
export GITHUB_TOKEN="ghp_your_token_here"
export GH_REPO="executiveusa/Darya-designs"
export PR_REVIEW_MODE="autonomous"
```

### 2. Review a Single PR

```python
import asyncio
from skills.pr_automation.autonomous_review_and_merge import review_and_merge_pr

async def main():
    result = await review_and_merge_pr(
        repo="executiveusa/Darya-designs",
        pr_number=123,
        auto_merge_enabled=True,
        post_comment=True,
    )
    print(result)

asyncio.run(main())
```

### 3. Output

```json
{
  "pr_number": 123,
  "decision": "auto_merge",
  "confidence": 0.92,
  "risk_level": "low",
  "merged": true,
  "scores": {
    "SecurityReview": 0.98,
    "CodeQuality": 0.88,
    "TestingCoverage": 0.95,
    "Performance": 0.92,
    "UXIntegration": 0.90
  },
  "next_steps": [
    "PR will be merged in 2 minutes",
    "Branch will be automatically deleted",
    "Deployment pipeline will be triggered",
    "Monitoring will be active for 6 hours"
  ]
}
```

## 📊 How It Works

### Review Flow

```
GitHub PR Event
    ↓
Fetch PR Context (diff, files, CI status)
    ↓
┌─────────────────────────────────────────────┐
│ Parallel Agent Execution (15-30 seconds)    │
├─────────────────────────────────────────────┤
│ • SecurityReviewAgent                       │
│ • CodeQualityAgent                          │
│ • TestingCoverageAgent                      │
│ • PerformanceAgent                          │
│ • UXIntegrationAgent                        │
└─────────────────────────────────────────────┘
    ↓
Aggregate Results & Calculate Confidence
    ↓
Apply Risk Gates & Safety Constraints
    ↓
Make Autonomous Decision
    ↓
Post Summary Comment (optional)
    ↓
Execute Merge (if auto-merge approved)
    ↓
Enable Monitoring (6 hours)
```

### Confidence Calculation

```
Confidence = Weighted Average of Agent Scores

Weights:
  Security        30%  (non-negotiable)
  Testing         25%  (critical path dependent)
  Code Quality    20%  (maintainability)
  Performance     15%  (application dependent)
  UX/Integration  10%  (user-facing dependent)

Penalties:
  Each critical finding: -5%
```

## 🔧 Configuration

### Preset Profiles

```python
from config import load_config

# Strict: For critical systems (payment, security)
config = load_config("strict")

# Moderate: Balance speed and safety (default)
config = load_config("moderate")

# Permissive: Prioritize speed
config = load_config("permissive")

# Info-only: Post summary, don't merge
config = load_config("info_only")
```

### Custom Configuration

```python
from config import PRAutomationConfig, MergeStrategyConfig

config = PRAutomationConfig(
    repo="executiveusa/Darya-designs",
    mode="autonomous",
    merge_config=MergeStrategyConfig(
        auto_merge_confidence_threshold=0.90,
        auto_delete_branch_after_merge=True,
    ),
)
```

## 📦 File Structure

```
skills/pr-automation/autonomous-review-and-merge/
├── __init__.py                 # Package exports
├── README.md                   # This file
├── skill.md                    # Comprehensive skill documentation
├── INTEGRATION_GUIDE.md        # Integration with OpenHands
├── config.py                   # Configuration system
├── github_mcp_tool.py          # GitHub API wrapper (MCP tool)
├── pr_review_agents.py         # Multi-perspective review agents
└── pr_orchestrator.py          # Main orchestrator & merge decision engine
```

## 🔌 Integration Options

### Option 1: As an Agent
```python
class PRReviewAgent(CodeActAgent):
    async def step(self, state):
        result = await review_and_merge_pr(...)
        return AgentFinishAction(...)
```

### Option 2: As a Skill
```python
class PRAutomationSkill(BaseSkill):
    async def execute(self, pr_number):
        return await review_and_merge_pr(...)
```

### Option 3: As an MCP Tool
```python
agent.set_mcp_tools([create_github_tool_definition(repo)])
```

See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for detailed examples.

## 🛡️ Safety & Rollback

### Safeguards
- ✅ Confidence-based thresholds
- ✅ Risk assessment gates
- ✅ Critical issue detection
- ✅ Rate limiting
- ✅ Timeout enforcement
- ✅ Merge conflict detection

### Post-Merge Monitoring
- 6-hour monitoring window
- Error rate detection
- Performance degradation alerts
- Automatic rollback on critical issues (configurable)

## 📊 Observability

### Key Metrics
```
pr_review_duration_seconds
pr_review_confidence_score
pr_auto_merge_success_rate
pr_review_accuracy_vs_human
security_findings_per_pr
code_quality_trend
test_coverage_trend
merged_pr_production_failure_rate
```

### Structured Logging
```python
logger.info("pr_review_completed", extra={
    "pr_number": 123,
    "decision": "auto_merge",
    "confidence": 0.92,
    "duration_seconds": 45,
})
```

## ⚙️ Agent Capabilities

### SecurityReviewAgent
- ✅ Dependency vulnerability scanning (npm audit, pip check)
- ✅ Hardcoded credential detection
- ✅ OWASP top-10 pattern detection
- ✅ Permission escalation checks
- ✅ Supply chain risk assessment

### CodeQualityAgent
- ✅ Complexity analysis (cyclomatic, cognitive)
- ✅ Naming convention consistency
- ✅ Code duplication detection
- ✅ Documentation quality assessment
- ✅ Architecture alignment validation

### TestingCoverageAgent
- ✅ Test suite execution (npm test, pytest)
- ✅ Coverage metrics extraction
- ✅ Critical path coverage analysis
- ✅ Regression risk assessment
- ✅ Edge case test generation

### PerformanceAgent
- ✅ Bundle size analysis
- ✅ Build time impact measurement
- ✅ Runtime performance estimation
- ✅ Memory leak detection
- ✅ Scalability assessment

### UXIntegrationAgent
- ✅ Cross-browser compatibility testing
- ✅ WCAG accessibility compliance
- ✅ Responsive design validation
- ✅ API integration testing
- ✅ User flow scenario testing

## 📈 Decision Criteria

### Auto-Merge Eligible (Confidence ≥ 0.92)
✅ All security checks passing
✅ Code quality score ≥ 0.88
✅ Test coverage > 80% on changed code
✅ No merge conflicts
✅ No breaking changes (or documented)
✅ Performance impact < 10%

### Request Changes (Confidence 0.75-0.85)
⚠️ Some code quality issues
⚠️ Test coverage 60-80%
⚠️ Minor security findings
⚠️ Performance regression 10-20%

### Reject (Confidence < 0.75)
❌ Critical security findings
❌ Test suite failing
❌ Merge conflicts present
❌ Major breaking changes
❌ Coverage < 60% on critical code

## 🧪 Testing & Validation

```bash
# Test with a single PR
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
    print(f'Decision: {result[\"decision\"]}')
    print(f'Confidence: {result[\"confidence\"]:.1%}')

asyncio.run(test())
"
```

## 📝 Examples

### Example 1: Review and Auto-Merge

```python
result = await review_and_merge_pr(
    repo="executiveusa/Darya-designs",
    pr_number=42,
    auto_merge_enabled=True,
    post_comment=True,
)

if result["merged"]:
    print(f"✅ PR #{result['pr_number']} merged successfully")
```

### Example 2: Batch Review Mode

```python
from github_mcp_tool import GitHubMCPTool

github = GitHubMCPTool("executiveusa/Darya-designs")
prs = await github.list_prs(state="open", limit=10)

for pr in prs:
    result = await review_and_merge_pr(
        repo="executiveusa/Darya-designs",
        pr_number=pr["number"],
        auto_merge_enabled=True,
    )
```

### Example 3: Custom Configuration

```python
from config import PRAutomationConfig, load_config

config = load_config("strict")
config.merge_config.auto_merge_enabled = False  # Info-only mode
config.notification_config.slack_webhook_url = "https://..."

engine = MergeDecisionEngine("executiveusa/Darya-designs")
recommendation = await engine.evaluate_pr(123)
```

## 🚨 Known Limitations

1. **Test Suite Dependent**: Accuracy depends on existing test quality
2. **Context Limited**: Can't deeply understand business logic
3. **Configuration Dependent**: Thresholds should be tuned per organization
4. **No Human Judgment**: Can't replace human code review for critical decisions
5. **Pattern-Based**: Security scanning is pattern-based, not comprehensive

## 🔮 Future Enhancements

- [ ] Custom rule engine for org-specific policies
- [ ] Feedback loop learning from human overrides
- [ ] Risk profiling per code area/domain
- [ ] Incident correlation and analysis
- [ ] Rollback automation with auto-detection
- [ ] Team-specific model fine-tuning
- [ ] Integration with issue tracking (Jira, Linear)
- [ ] Slack/Teams notifications
- [ ] Custom metrics dashboards

## 📚 Documentation

- [skill.md](./skill.md) - Comprehensive architecture and design
- [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) - Integration instructions
- [config.py](./config.py) - Configuration reference
- [pr_orchestrator.py](./pr_orchestrator.py) - Decision engine implementation

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional security check patterns
- Performance optimization
- New review agent types
- Configuration improvements
- Documentation enhancements

## 📜 License

Same as OpenHands project

## 🙏 Acknowledgments

- Based on Deep Agent QA philosophy (Abacus AI)
- Implements OpenHands agent architecture
- Uses existing CodeActAgent capabilities
- Integrates with GitHub ecosystem

---

**Questions?** See [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for troubleshooting and detailed integration instructions.
