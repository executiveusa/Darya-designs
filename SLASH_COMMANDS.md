# Jarvis Slash Commands & Workflows

## Overview
Slash commands are powerful shortcuts that trigger complex workflows. They can be executed via:
- Text input: `/command-name`
- Voice: "Run command name" or "Execute command name"
- Buttons in UI
- Keyboard shortcuts (customizable)

## Core Commands

### 📋 Audit & Analysis Commands

#### `/audit [repo-pattern]`
**Description**: Comprehensive audit of repositories
**Usage**: `/audit` or `/audit backend-*` or `/audit all`
**Activates Skills**:
1. `code-review/multi-agent-review`
2. `analysis/complexity-analyzer`
3. `security/vulnerability-scanner`
4. `analytics/codebase-health-report`
5. `analytics/technical-debt-calculator`

**Parameters**:
- `--depth quick|standard|thorough` (default: standard)
- `--focus security|quality|performance|all` (default: all)
- `--report-format summary|detailed|pdf` (default: summary)

**Voice Alternative**: "Audit all my repos" or "Give me a health report"

**Example Output**:
```
Audit Report: Dashboard
Status: ✅ Complete (12/12 repos)
Time: 18 minutes

Summary:
- Code Quality: 82/100 (good)
- Security: 95/100 (excellent)
- Performance: 78/100 (good)
- Test Coverage: 84% average
- Technical Debt: 12% of codebase

Critical Issues: 2
- auth-service: SQL injection vulnerability
- api-gateway: Unhandled exception in route

High Issues: 8
[List of 8 items]

Recommended Actions:
1. Fix SQL injection in auth-service (30 min)
2. Add error handling in api-gateway (1 hour)
3. Increase test coverage in 3 repos (4 hours)
```

---

#### `/status`
**Description**: Quick health check of all projects
**Voice Alternative**: "What's the status of my projects?" or "Give me a summary"

**Output**:
```
Project Status Report
====================

🟢 Healthy (8 repos)
  - production-api
  - web-frontend
  - mobile-app
  - [5 others]

🟡 Needs Attention (2 repos)
  - analytics-service (test coverage: 60%)
  - reporting-service (2 security warnings)

🔴 Critical (0 repos)

Next Recommended Actions:
1. Increase test coverage in analytics-service
2. Fix security warnings in reporting-service
```

---

### 🚀 Automation Commands

#### `/update-dependencies [repo-pattern]`
**Description**: Safely update all dependencies across repos
**Usage**: `/update-dependencies` or `/update-dependencies backend-*`
**Activates Skills**:
1. `automation/dependency-updater`
2. `security/dependency-auditor`
3. `testing/coverage-analyzer`
4. `automation/approval-workflow`

**Parameters**:
- `--security-only` (only update security patches)
- `--major` (include major version updates)
- `--auto-approve` (skip approval if tests pass)
- `--parallel N` (number of repos to update in parallel, default: 2)

**Voice Alternative**: "Update all dependencies" or "Check for dependency updates"

**Workflow**:
1. Scan all repos for outdated dependencies
2. Check for security vulnerabilities
3. Run dependency audit
4. Create PRs for updates
5. Run tests automatically
6. Auto-merge if tests pass (if `--auto-approve`)

---

#### `/security-scan [repo-pattern]`
**Description**: Comprehensive security scan across repositories
**Activates Skills**:
1. `security/vulnerability-scanner`
2. `security/secrets-detector`
3. `security/sast-analyzer`
4. `security/dependency-auditor`
5. `security/auth-review`

**Parameters**:
- `--depth quick|full` (default: full)
- `--create-issues` (create GitHub issues for findings)
- `--auto-fix` (auto-fix fixable issues)

**Voice Alternative**: "Scan for security issues" or "Check security"

---

#### `/create-prs [template-name] [repo-pattern]`
**Description**: Create pull requests across multiple repos
**Examples**:
```
/create-prs refactor-logging backend-*
/create-prs add-tests all
/create-prs upgrade-react frontend-*
```

**Available Templates**:
- `add-tests` - Add missing test files
- `refactor-logging` - Standardize logging
- `add-ts-strict` - Enable TypeScript strict mode
- `upgrade-react` - Upgrade React to latest
- `fix-a11y` - Fix accessibility issues
- `add-error-boundaries` - Add React error boundaries

**Activates Skills**:
1. `code-generation/generate-production-code`
2. `automation/batch-pr-generator`
3. `testing/test-case-generator`
4. `automation/approval-workflow`

**Parameters**:
- `--auto-merge` (merge when tests pass)
- `--sequential` (create one PR at a time)
- `--with-review` (require review before merge)

---

### 📚 Documentation Commands

#### `/sync-docs [repo-pattern]`
**Description**: Sync and update documentation across repos
**Activates Skills**:
1. `documentation/readme-generator`
2. `documentation/api-docs-generator`
3. `documentation/architecture-docs`
4. `collaboration/documentation-sync`

**Parameters**:
- `--auto-approve` (auto-merge doc updates)
- `--include api|architecture|readme|all` (default: all)

**Voice Alternative**: "Update all documentation" or "Sync docs"

---

#### `/generate-changelog`
**Description**: Generate CHANGELOG from recent commits
**Activates Skills**:
1. `documentation/changelog-generator`
2. `automation/approval-workflow`

**Parameters**:
- `--since last-release` (default)
- `--since-date YYYY-MM-DD`
- `--format markdown|html` (default: markdown)

---

### 🧪 Testing Commands

#### `/add-tests [repo-pattern]`
**Description**: Generate and add missing tests
**Activates Skills**:
1. `testing/test-case-generator`
2. `testing/coverage-analyzer`
3. `code-generation/generate-production-code`
4. `automation/batch-pr-generator`

**Parameters**:
- `--coverage-target 80|85|90` (default: 85)
- `--test-type unit|integration|e2e|all` (default: all)
- `--auto-merge` (merge when coverage target met)

**Voice Alternative**: "Add tests to everything" or "Improve test coverage"

---

#### `/coverage-report`
**Description**: Generate test coverage report
**Activates Skills**:
1. `testing/coverage-analyzer`
2. `analytics/codebase-health-report`

**Output**: Summary of coverage by repo, highlighting areas below threshold

---

### ⚡ Performance Commands

#### `/optimize-performance [repo-pattern]`
**Description**: Analyze and optimize performance
**Activates Skills**:
1. `performance/bundle-analyzer`
2. `performance/rendering-optimizer`
3. `performance/database-optimizer`
4. `performance/caching-strategist`
5. `optimization/build-time-reducer`

**Parameters**:
- `--focus web|mobile|backend|all` (default: all)
- `--target-metric time|size|memory` (default: all)

**Voice Alternative**: "Make everything faster" or "Optimize performance"

---

### 🎨 UI/UX Commands

#### `/check-branding`
**Description**: Check brand compliance across all repos
**Activates Skills**:
1. `branding/style-guide-enforcer`
2. `branding/color-consistency-checker`
3. `ui-ux/component-analyzer`
4. `ui-ux/design-token-generator`

**Parameters**:
- `--fix-automatically` (create PRs to fix issues)
- `--ignore-warnings` (only report errors)

**Voice Alternative**: "Check brand consistency" or "Audit branding"

---

#### `/a11y-audit`
**Description**: Accessibility audit
**Activates Skills**:
1. `ui-ux/accessibility-auditor`
2. `code-review/accessibility-review`

**Parameters**:
- `--wcag-level A|AA|AAA` (default: AA)
- `--create-issues` (create issues for violations)

---

### 🔄 Deployment Commands

#### `/deploy-safe [service] [environment]`
**Description**: Safe deployment with validation
**Usage**: `/deploy-safe api-service staging`
**Activates Skills**:
1. `devops/deployment-validator`
2. `devops/deployment-health-checker`

**Parameters**:
- `--with-tests` (run tests first)
- `--canary 5|10|20` (% of traffic for canary)
- `--rollback-on-error` (auto-rollback if issues)

**Voice Alternative**: "Deploy to staging" or "Deploy api service"

---

#### `/scale-infra [service] [target-percentage]`
**Description**: Scale infrastructure based on metrics
**Usage**: `/scale-infra api-service 150` (scale to 150% capacity)
**Activates Skills**:
1. `devops/scaling-advisor`
2. `monitoring/health-checker`

---

### 🎯 Decision Commands

#### `/recommend [task-type]`
**Description**: Get AI recommendation for next step
**Usage**: `/recommend refactoring` or `/recommend testing`
**Voice Alternative**: "What should I do next?" or "What do you recommend?"

**Output**: Prioritized list of recommended actions with effort/impact estimates

---

#### `/approve [change-type] [criteria]`
**Description**: Set auto-approval criteria
**Usage**: `/approve PRs if coverage>85% and no-security-issues`
**Voice Alternative**: "Auto-approve PRs with high test coverage"

---

### 📊 Analytics Commands

#### `/team-insights`
**Description**: Generate team performance insights
**Activates Skills**:
1. `collaboration/team-insight-generator`
2. `analytics/code-velocity-tracker`
3. `analytics/codebase-health-report`

**Output**:
```
Team Insights Report
====================

Velocity:
- PRs/week: 12 (📈 up 20% from last month)
- Avg review time: 2.1 hours (📉 down from 3.2)
- Deployment frequency: 8/week

Code Quality:
- Avg coverage: 84%
- Test passing rate: 98.5%
- Regression rate: 2/50 deployments

Learning Opportunities:
- Consider React patterns workshop (5 repos using inconsistent hooks)
- Improve error handling in backend (8 instances of unhandled exceptions)
- Establish async/await standards (7 promise anti-patterns found)
```

---

#### `/technical-debt`
**Description**: Quantify technical debt
**Activates Skills**:
1. `analytics/technical-debt-calculator`
2. `analysis/complexity-analyzer`
3. `analysis/dead-code-detector`
4. `analysis/code-duplication-detector`

---

### 🧠 Learning Commands

#### `/learn-best-practices`
**Description**: Extract and document best practices from codebase
**Activates Skills**:
1. `learning/pattern-extractor`
2. `learning/best-practices-guide`

**Output**: Guide showing patterns used, best practices, recommendations

---

#### `/tech-recommendations`
**Description**: Get recommendations for tech stack improvements
**Activates Skills**:
1. `learning/technology-recommender`
2. `analysis/dependency-analyzer`

---

### 🔧 Configuration Commands

#### `/config [setting] [value]`
**Description**: Configure Jarvis behavior
**Examples**:
```
/config approval-mode supervised
/config auto-approve-threshold 0.95
/config voice-language spanish
/config response-style professional
/config parallel-pr-limit 5
```

**Available Settings**:
- `approval-mode`: manual | supervised | auto
- `auto-approve-threshold`: 0.5-0.99
- `voice-language`: en | es | fr | de | zh | ja | ...
- `response-style`: professional | friendly | technical | minimal
- `parallel-pr-limit`: 1-20
- `log-level`: silent | errors | warnings | info | debug

---

#### `/show-config`
**Description**: Display current configuration
**Voice Alternative**: "Show my settings" or "What's my configuration?"

---

#### `/help [command]`
**Description**: Get help on commands
**Usage**: `/help audit` or `/help` (show all)
**Voice Alternative**: "What can you do?" or "How do I update dependencies?"

---

#### `/skills`
**Description**: List all available skills
**Parameters**:
- `--by-category` (group by category)
- `--search [keyword]` (search skills)

---

### 🛡️ Safety Commands

#### `/rollback [repo] [version]`
**Description**: Rollback a specific repo to previous version
**Voice Alternative**: "Rollback the api service"

---

#### `/pause-all`
**Description**: Pause all agent operations immediately
**Voice Alternative**: "Stop everything" or "Pause"

---

#### `/audit-trail [start-date] [end-date]`
**Description**: View all decisions made by Jarvis
**Parameters**:
- `--since YYYY-MM-DD`
- `--action-type` (filter by type)
- `--export` (export to CSV/JSON)

---

## Command Patterns

### Basic Pattern
```
/command-name [required-param] [optional-params] --flags
```

### Multi-Repo Pattern
```
/command-name repo-pattern --flags
# Examples:
/audit backend-*              # all repos starting with "backend-"
/audit *-service              # all repos ending with "-service"
/audit frontend-*,backend-*   # multiple patterns
/audit all                     # all repos
```

### Chaining Commands
```
/audit && /create-prs add-tests if-coverage-below-80 --auto-merge
```

This means: "Run audit, and if coverage is below 80%, create PRs to add tests and auto-merge"

---

## Auto-Complete & Suggestions

As user types:
```
User types: /aud
Suggestions:
  ├─ /audit [repo-pattern] - Comprehensive repo audit
  └─ /audit-trail - View decision history

User types: /audit back
Suggestions:
  ├─ /audit backend-api
  ├─ /audit backend-*
  └─ /audit all
```

---

## Keyboard Shortcuts

Customizable shortcuts:
```
Ctrl+Shift+A  → /audit
Ctrl+Shift+S  → /status
Ctrl+Shift+D  → /deploy-safe
Ctrl+Shift+T  → /add-tests
Ctrl+Shift+H  → /help
```

---

## Integration with Voice

Voice commands can include slash command logic:
```
Voice: "Audit everything and create PRs for low coverage"
Equivalent: /audit all && /create-prs add-tests if-coverage-below-80

Voice: "Auto-approve dependency updates if tests pass"
Equivalent: /approve PRs if coverage>85% and tests-pass
```

---

## Command Aliases

Shorter versions of common commands:
```
/audit → /a
/status → /s
/deploy-safe → /deploy
/add-tests → /test
/update-dependencies → /deps
/security-scan → /sec
/sync-docs → /docs
```

---

## Future Slash Commands (v2.0)

Coming soon:
- `/integrate-service` - Add external service integrations
- `/train-agent` - Train agents on specific patterns
- `/split-monorepo` - Break monorepo into separate repos
- `/merge-repos` - Combine multiple repos
- `/cost-analyze` - Analyze infrastructure costs
- `/compliance-check` - Check regulatory compliance

---

*Last Updated: 2026-01-22*
*Part of OpenHands Jarvis v1.0*
