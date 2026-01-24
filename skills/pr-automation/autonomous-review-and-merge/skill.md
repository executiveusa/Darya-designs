# Autonomous PR Review & Merge Skill

## Overview

The Autonomous PR Review & Merge skill implements Deep Agent QA philosophy for continuous code validation. Instead of passive test execution, this system actively probes assumptions, shifts perspectives, and makes trust-based merge decisions at scale.

**Core Philosophy**: Empathy + Paranoia
- **Empathy**: Understand real code impact, user experience, security implications
- **Paranoia**: Probe for how things break, stress edge cases, validate assumptions continuously

## Architecture

### Multi-Perspective Review System

```
PullRequestOrchestrator (Main Agent - CodeActAgent)
│
├─ 1. GitHub Context Agent
│   └─ Fetches PR details, diff, CI status, existing reviews
│
├─ 2. Security Review Agent (Paranoid Mode)
│   ├─ Dependency vulnerability scanning
│   ├─ Credential/secret detection
│   ├─ OWASP top-10 pattern detection
│   ├─ Permission/access control validation
│   └─ Supply chain risk assessment
│
├─ 3. Code Quality Agent (Empathy Mode)
│   ├─ Architecture alignment validation
│   ├─ Code pattern consistency
│   ├─ Duplication detection
│   ├─ Maintainability scoring
│   └─ Documentation quality assessment
│
├─ 4. Testing & Coverage Agent (Rigor Mode)
│   ├─ Test execution (npm test, pytest, etc.)
│   ├─ Coverage metrics extraction
│   ├─ Critical path testing
│   ├─ Regression risk assessment
│   └─ E2E scenario validation
│
├─ 5. Performance & Scalability Agent
│   ├─ Bundle size analysis
│   ├─ Runtime performance profiling
│   ├─ Database query optimization
│   ├─ Memory leak detection
│   └─ Concurrent load testing
│
├─ 6. UX & Integration Agent
│   ├─ Cross-browser compatibility
│   ├─ Accessibility compliance (WCAG)
│   ├─ Responsive design validation
│   ├─ Integration point validation
│   └─ Customer impact assessment
│
└─ 7. Merge Decision Agent
    ├─ Aggregates all review perspectives
    ├─ Calculates confidence score
    ├─ Evaluates merge criteria
    ├─ Handles merge conflicts
    ├─ Executes merge strategy
    └─ Posts review summary comment
```

## Autonomous Decision Making

### Confidence Scoring Model

```
Final Confidence = (
  Security_Score × 0.30 +        # Non-negotiable
  Code_Quality_Score × 0.20 +    # Important
  Test_Coverage_Score × 0.25 +   # Critical path dependent
  Performance_Score × 0.15 +     # Application dependent
  UX_Integration_Score × 0.10    # User-facing dependent
)

Action Thresholds:
- Confidence ≥ 0.92 → Auto-merge (squash)
- Confidence ≥ 0.85 → Approve + Request Review (1 human)
- Confidence ≥ 0.75 → Request Changes (with specific feedback)
- Confidence < 0.75 → Reject (with detailed reasoning)
```

### Risk Assessment Matrix

```
Risk Level  | Security Impact | Scope | Change Type   | Auto-Merge? | Action
-----------|--------------------|-------|---------------|-------------|--------
CRITICAL   | HIGH           | >50%  | Breaking API  | NO          | Reject + Alert
HIGH       | MEDIUM         | >30%  | Core logic    | NO          | Request review
MEDIUM     | LOW            | <30%  | Feature add   | YES*        | Merge + Monitor
LOW        | NONE           | <10%  | Docs/Config   | YES         | Auto-merge
*with confidence > 0.92
```

## Agent Implementations

### 1. GitHub Context Agent

**Responsibility**: Fetch and normalize PR metadata

```python
class GitHubContextAgent(CodeActAgent):
    """
    Fetches all PR context needed for review decision.
    Uses GitHub API via MCP tool.
    """

    async def execute(self, pr_number: int, repo: str) -> PullRequestContext:
        # Fetch PR details, diff, files, CI status, reviews
        # Extract change metrics: files changed, lines added/removed, complexity
        # Analyze branch history
        # Check for conflicts
        # Get author history and risk profile
        return PullRequestContext(...)
```

**Outputs**:
- PR metadata (title, description, author)
- Diff analysis (files, hunks, complexity)
- CI status and logs
- Dependency changes
- Branch conflict status

### 2. Security Review Agent (Paranoid Mode)

**Responsibility**: Find how code breaks security assumptions

```python
class SecurityReviewAgent(CodeActAgent):
    """
    Operates in paranoia mode: assumes everything is a security risk
    until proven otherwise.
    """

    async def execute(self, context: PullRequestContext) -> SecurityReviewResult:
        checks = [
            # Dynamic checks
            check_dependency_vulnerabilities(),      # npm audit, pip check
            check_secrets_and_credentials(),          # detect hardcoded secrets
            check_injection_vulnerabilities(),        # SQL, XSS, command injection

            # Static analysis
            check_permission_escalation(),            # auth/role changes
            check_api_security_practices(),           # OAuth, JWT, CORS
            check_cryptographic_implementation(),     # proper algorithms/key mgmt

            # Architecture analysis
            check_data_exposure_risks(),              # PII, sensitive data handling
            check_supply_chain_risks(),               # new dependencies, manifest changes
            check_privilege_boundaries(),             # admin/user/public separation

            # Pattern detection
            detect_dangerous_patterns(),              # suspicious code patterns
            validate_security_headers(),              # HTTP security
            verify_encryption_usage(),                # proper encryption
        ]

        return aggregate_security_findings(checks)
```

**Scoring**:
- 0 critical findings → 1.0 score
- 1-2 critical → 0.7 score (request changes)
- 3+ critical → 0.0 score (reject)
- Medium findings reduce score by 0.05-0.1 each

### 3. Code Quality Agent (Empathy Mode)

**Responsibility**: Understand code health and maintainability

```python
class CodeQualityAgent(CodeActAgent):
    """
    Evaluates code from maintainers' and future developers' perspective.
    """

    async def execute(self, context: PullRequestContext) -> CodeQualityResult:
        # Architecture validation
        validate_architecture_patterns()

        # Code consistency
        check_code_style_consistency()
        check_naming_conventions()
        check_function_complexity()

        # Duplication
        detect_code_duplication()
        identify_similar_patterns()

        # Documentation
        assess_comment_quality()
        check_readme_updates()
        validate_type_annotations()

        # Maintainability
        calculate_cyclomatic_complexity()
        measure_cognitive_complexity()
        assess_testability_score()

        return CodeQualityResult(...)
```

**Scoring**:
- Low complexity + good docs + DRY → 1.0
- Medium complexity + some docs → 0.75
- High complexity + no docs → 0.4
- Copy-paste code → 0.2

### 4. Testing & Coverage Agent (Rigor Mode)

**Responsibility**: Execute and verify test reliability

```python
class TestingCoverageAgent(CodeActAgent):
    """
    Runs full test suite, analyzes coverage, probes for untested paths.
    """

    async def execute(self, context: PullRequestContext) -> TestingResult:
        # Execute tests
        npm_test_result = run_command("npm run test")
        pytest_result = run_command("poetry run pytest tests/")

        # Parse coverage
        coverage_data = extract_coverage_metrics()

        # Analyze critical paths
        critical_paths = identify_critical_code_paths(context.diff)
        coverage_for_critical = check_coverage(critical_paths)

        # Risk assessment
        untested_risk = assess_untested_code_risk()
        regression_risk = assess_regression_risk()

        # Edge case probing
        edge_cases = generate_edge_cases(context.changes)
        test_edge_case_handling(edge_cases)

        return TestingResult(
            test_pass=npm_test_result.success,
            coverage_percent=coverage_data.percent,
            critical_path_coverage=coverage_for_critical,
            untested_risk_score=untested_risk,
            regression_risk=regression_risk,
            edge_case_findings=edge_cases,
        )
```

**Scoring**:
- All tests pass + >80% coverage + critical paths covered → 1.0
- Tests pass + >60% coverage → 0.8
- Tests pass + <60% coverage → 0.5
- Test failures → 0.0

### 5. Performance & Scalability Agent

**Responsibility**: Measure real-world performance impact

```python
class PerformanceAgent(CodeActAgent):
    """
    Profiles performance impact, identifies bottlenecks.
    """

    async def execute(self, context: PullRequestContext) -> PerformanceResult:
        # Build and measure
        build_result = run_build()
        bundle_size_delta = measure_bundle_size_change()

        # Runtime profiling
        memory_profile = run_memory_profiling()
        cpu_profile = run_cpu_profiling()

        # Database/query analysis
        new_queries = analyze_database_queries()
        n_plus_one_detection = detect_n_plus_one_problems()

        # Scalability testing
        concurrent_users = simulate_concurrent_load(100, 1000)
        memory_leak = detect_memory_leaks()

        return PerformanceResult(...)
```

**Scoring**:
- No performance regression + improved metrics → 1.0
- <5% bundle increase, <10% memory increase → 0.9
- <10% bundle increase, <20% memory increase → 0.7
- >20% regression in any metric → 0.4

### 6. UX & Integration Agent

**Responsibility**: Validate user experience and system integration

```python
class UXIntegrationAgent(CodeActAgent):
    """
    Tests real user scenarios, accessibility, integration points.
    """

    async def execute(self, context: PullRequestContext) -> UXResult:
        # Cross-browser testing
        test_browsers = ["Chrome", "Firefox", "Safari", "Edge"]
        browser_results = test_all_browsers(test_browsers)

        # Accessibility compliance
        a11y_audit = run_axe_audit()
        wcag_compliance = check_wcag_2_1_aa()

        # Responsive design
        responsive_test = test_viewports([
            "mobile", "tablet", "desktop", "ultra-wide"
        ])

        # Integration testing
        api_integration = test_api_endpoints()
        external_service_integration = test_external_services()

        # User flow scenarios
        critical_flows = [
            "user_signup",
            "user_login",
            "payment_flow",
            "data_export",
        ]
        flow_results = test_user_flows(critical_flows)

        return UXResult(...)
```

**Scoring**:
- All browsers pass + WCAG AA + responsive pass → 1.0
- 1 browser failure or 1 a11y issue → 0.85
- 2+ browser failures or multiple a11y issues → 0.6
- Critical flow broken → 0.0

### 7. Merge Decision Agent

**Responsibility**: Synthesize all reviews, make autonomous decision

```python
class MergeDecisionAgent(CodeActAgent):
    """
    Aggregates all review perspectives, calculates confidence,
    makes merge/reject decision with full transparency.
    """

    async def execute(self,
                     reviews: List[ReviewResult]) -> MergeDecision:

        # Aggregate scores
        confidence = calculate_confidence_score(reviews)
        risk_level = assess_overall_risk(reviews)

        # Decision logic
        if confidence >= 0.92 and risk_level <= "MEDIUM":
            decision = "AUTO_MERGE"
            merge_strategy = "squash"
        elif confidence >= 0.85:
            decision = "APPROVE_REQUEST_REVIEW"
        elif confidence >= 0.75:
            decision = "REQUEST_CHANGES"
        else:
            decision = "REJECT"

        # Post comprehensive summary
        summary = build_review_summary(reviews, confidence, decision)
        post_pr_comment(summary)

        # Execute merge if approved
        if decision == "AUTO_MERGE":
            merge_pr(merge_strategy, auto_delete_branch=True)

        return MergeDecision(
            decision=decision,
            confidence=confidence,
            risk_level=risk_level,
            reasoning=summary,
        )
```

**Summary Format**:
```
## Autonomous PR Review Summary

**Overall Confidence**: 92% ✅

| Perspective | Score | Status |
|-----------|-------|--------|
| Security | 98% | ✅ All checks passed |
| Code Quality | 88% | ⚠️ 2 style issues noted |
| Testing | 95% | ✅ 642/650 tests passed |
| Performance | 92% | ✅ Bundle -2% |
| UX/Integration | 90% | ✅ WCAG AA compliant |

**Decision**: AUTO-MERGED (squash strategy)
**Risk Level**: LOW

**Key Findings**:
- 3 new dependencies added (all verified safe)
- Performance improved by 2% on bundle size
- Critical path coverage: 94%
- 2 minor accessibility improvements needed for future

**Next Steps**:
- Monitoring for 6 hours post-deployment
- Metric collection enabled
```

## Configuration

### Environment Setup

```bash
# Required environment variables
export GITHUB_TOKEN="github_pat_..."
export GH_REPO="executiveusa/Darya-designs"
export PR_REVIEW_MODE="autonomous"  # or "approval_required", "info_only"
export CONFIDENCE_THRESHOLD="0.85"
export AUTO_MERGE_ENABLED="true"
```

### Agent Configuration

```python
# openhands/config/pr_automation_config.py

PR_AUTOMATION_CONFIG = {
    "enabled": True,
    "mode": "autonomous",  # autonomous, approval_required, info_only

    "agents": {
        "security": {
            "enabled": True,
            "severity_threshold": "MEDIUM",
            "scan_dependencies": True,
            "scan_secrets": True,
        },
        "code_quality": {
            "enabled": True,
            "complexity_threshold": "medium",
            "documentation_required": True,
        },
        "testing": {
            "enabled": True,
            "require_tests": True,
            "min_coverage": 0.75,
            "critical_path_required": True,
        },
        "performance": {
            "enabled": True,
            "bundle_size_delta": 0.10,  # 10% max increase
            "memory_delta": 0.15,        # 15% max increase
        },
        "ux": {
            "enabled": True,
            "browsers": ["Chrome", "Firefox", "Safari"],
            "accessibility_level": "WCAG_AA",
        },
    },

    "merge_strategy": {
        "auto_merge_threshold": 0.92,
        "approve_threshold": 0.85,
        "request_changes_threshold": 0.75,
        "strategy": "squash",
        "auto_delete_branch": True,
    },

    "notifications": {
        "post_summary_comment": True,
        "notify_on_rejection": True,
        "alert_on_critical_issues": True,
    },

    "monitoring": {
        "track_metrics_hours": 6,
        "rollback_on_error": True,
        "alert_threshold": 0.95,
    },
}
```

### Webhook Integration

```json
{
  "name": "pr-review-automation",
  "events": [
    "pull_request.opened",
    "pull_request.reopened",
    "pull_request.synchronize"
  ],
  "url": "https://your-domain/webhooks/pr-automation",
  "active": true,
  "content_type": "json"
}
```

## Integration Points

### 1. With Existing CodeActAgent

```python
# Skill extends existing CodeActAgent capabilities
# Uses all available tools: bash, file operations, LLM reasoning

from openhands.agenthub.codeact_agent import CodeActAgent

class PRReviewAgent(CodeActAgent):
    # Inherits all CodeActAgent tools automatically
    pass
```

### 2. With MCP (Model Context Protocol)

```python
# Custom GitHub MCP tool
mcp_tool = ChatCompletionToolParam(
    type='function',
    function=ChatCompletionToolParamFunctionChunk(
        name='github_api',
        description='GitHub API operations for PR management',
        parameters={
            'type': 'object',
            'properties': {
                'operation': {'type': 'string'},  # list_prs, merge_pr, etc.
                'arguments': {'type': 'object'},
            },
        },
    ),
)

agent.set_mcp_tools([mcp_tool])
```

### 3. With Existing Skills System

```python
# Skill can invoke other skills for specialized checks
from skills.code_review.multi_agent_review import MultiAgentReviewSkill

class PRAutomationSkill(Skill):
    def __init__(self):
        self.code_review = MultiAgentReviewSkill()

    async def execute(self, pr_context):
        # Leverage existing multi-agent code review
        review_result = await self.code_review.execute(pr_context.diff)
        # Combine with other agents' results
```

### 4. With Existing Runtime

```python
# Uses existing openhands runtime for command execution
from openhands.runtime import Runtime

runtime = Runtime()
result = runtime.run_bash("npm run test")
```

## Execution Flow

### Trigger Points

1. **Webhook Event**: PR opened/updated
   ```
   GitHub Event → Webhook Handler → PR Automation Agent
   ```

2. **Scheduled (Batch Mode)**:
   ```
   Cron (e.g., every 4 hours) → List Open PRs → Review Each
   ```

3. **Manual Invocation**:
   ```
   User Command → Orchestrator Agent → Review → Decision
   ```

### Execution Timeline

```
T+0s:     PR opened/updated → Webhook triggers
T+1s:     Fetch PR context
T+5s:     Parallel execution of all review agents:
          - Security Agent (3-5s)
          - Code Quality Agent (2-3s)
          - Testing Agent (15-30s depending on test suite)
          - Performance Agent (10-20s)
          - UX Agent (5-10s)
T+30s:    All results aggregated
T+32s:    Merge Decision Agent makes decision
T+33s:    Post summary comment to PR
T+35s:    If auto-merge: execute merge, monitor for 6h
```

## Safety & Rollback

### Safeguards

```python
class SafeguardFramework:
    """
    Prevents autonomous merge disasters
    """

    # Confidence check - requires minimum threshold
    MIN_CONFIDENCE = 0.92

    # Risk gate - blocks critical/high risk PRs
    BLOCK_CRITICAL = True

    # Dependency gate - requires security approval for new deps
    NEW_DEPENDENCY_REQUIRES_APPROVAL = True

    # Breaking change detection - blocks major version changes
    BLOCK_BREAKING_CHANGES = True

    # Rate limiting - prevent merge floods
    MAX_MERGES_PER_HOUR = 5

    # Timeout - abort if any check hangs
    AGENT_TIMEOUT_SECONDS = 120
```

### Rollback Strategy

```python
if post_merge_monitoring_detects_issue():
    if issue_severity == "CRITICAL":
        # Immediate rollback
        revert_merge_commit()
        post_alert("Critical issue detected, reverted merge")
    elif issue_severity == "HIGH":
        # Notify + manual intervention
        notify_team("High severity issue, manual review needed")
```

## Metrics & Observability

### Key Metrics to Track

```
pr_review_duration_seconds
pr_review_confidence_score
pr_auto_merge_success_rate
pr_review_accuracy_vs_human
security_findings_per_pr
code_quality_trend
test_coverage_trend
merged_pr_production_failure_rate
deployment_frequency
lead_time_for_changes
time_to_recovery_on_failure
```

### Logging

```python
# Structure logs for easy analysis
log_entry = {
    "timestamp": datetime.now(),
    "pr_number": 123,
    "event": "pr_review_started",
    "confidence_score": 0.92,
    "decision": "AUTO_MERGE",
    "agents_involved": ["security", "testing", "code_quality"],
    "duration_seconds": 35,
    "merge_succeeded": True,
}
```

## Limitations & Future Enhancements

### Current Limitations

1. **Test Suite Dependent**: Accuracy depends on existing test quality
2. **Context Dependent**: Works best with well-structured repos
3. **Documentation Dependent**: Can't assess undocumented critical features
4. **No Domain Knowledge**: Doesn't understand business logic deeply
5. **Generic Security Checks**: Not customized to specific architecture

### Future Enhancements

1. **Custom Rule Engine**: Define org-specific approval rules
2. **Feedback Loop**: Learn from human overrides
3. **Risk Profiling**: Adapt thresholds based on code area risk
4. **Team-Specific Models**: Fine-tune for specific teams
5. **Incident Correlation**: Link merge decisions to production incidents
6. **Trend Analysis**: Identify improving/degrading code metrics
7. **Rollback Automation**: Auto-revert on detected production issues

## Getting Started

### Installation

```bash
# 1. Copy skill to skills directory
cp -r autonomous-review-and-merge skills/pr-automation/

# 2. Install dependencies
poetry install

# 3. Configure environment
cp .env.example .env
# Edit .env with your GitHub token and settings

# 4. Register MCP tool
# Add to openhands/mcp/__init__.py

# 5. Start agent
python -m openhands.cli \
  --skill "skills/pr-automation/autonomous-review-and-merge" \
  --mode "autonomous"
```

### First Run

```bash
# Test with a single PR
python -m openhands \
  --task "Review PR #123" \
  --repo "executiveusa/Darya-designs"
```

## References

- Deep Agent QA Philosophy: Speed + Safety at scale
- Multi-perspective review: Security, Quality, Testing, Performance, UX
- Autonomous decision-making: Confidence-based, transparent reasoning
- Integration: With existing CodeActAgent, MCP tools, runtime
