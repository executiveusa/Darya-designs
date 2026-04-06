# OpenHands Jarvis Agent Skills Manifest

## Overview
This document catalogs all available Agent Skills for the OpenHands platform, organized by category. Each skill represents a repeatable workflow or capability that agents can discover and use to perform tasks more accurately and efficiently.

**Platform**: OpenHands v0.59.0 with Jarvis Voice Agent Framework
**Skills Standard**: Anthropic Agent Skills Format
**Total Skills**: 50+ across 20 categories

---

## 🎯 TOP 20 PRIORITY SKILLS (For Your Use Case)

### Tier 1: Critical Core Skills (Must Have)
1. **Code Generation & Architecture** - Generate production-ready code with proper patterns
2. **Repository Auditing** - Comprehensive analysis of GitHub repos
3. **Code Review & Quality** - Automated multi-agent code review across repositories
4. **Dependency Analysis** - Security and version vulnerability scanning
5. **Test Generation & Execution** - Auto-create and run test suites
6. **Documentation Generation** - API docs, README, inline documentation
7. **Git Workflow Automation** - Commit, PR, merge with best practices
8. **Performance Profiling** - Identify bottlenecks and optimization opportunities
9. **Security Scanning** - SAST, dependency checks, secrets detection
10. **Multi-Repo Orchestration** - Coordinate changes across repositories

### Tier 2: Advanced Capabilities (High Value)
11. **Voice Command Processing** - Convert natural language to agent actions
12. **Auto Decision Making** - Autonomous decision making with human checkpoints
13. **Batch Repository Updates** - Apply changes across multiple repos simultaneously
14. **CI/CD Pipeline Management** - Create, update, and monitor workflows
15. **Monitoring & Alerting** - Real-time issue detection and reporting
16. **UI/UX Pattern Analysis** - Consistency checking across frontend code
17. **Branding Compliance** - Ensure brand standards across repos
18. **API Integration** - Connect external services and data sources
19. **Cost & Resource Optimization** - Analyze and reduce infrastructure costs
20. **Agent Learning & Adaptation** - Self-improving agent capabilities

---

## 📁 SKILLS BY CATEGORY

### 1. Code Generation (8 skills)
- `code-generation/generate-production-code` - Generate industry-standard code
- `code-generation/architecture-design` - Design system architecture
- `code-generation/boilerplate-generator` - Create project templates
- `code-generation/refactor-legacy-code` - Modernize legacy codebases
- `code-generation/code-to-mermaid` - Generate diagrams from code
- `code-generation/pattern-implementation` - Implement design patterns
- `code-generation/type-generation` - Generate TypeScript/Python types
- `code-generation/api-client-generator` - Create API client code

### 2. Code Review (6 skills)
- `code-review/multi-agent-review` - Coordinate multiple agents for comprehensive review
- `code-review/quality-gates` - Enforce quality standards
- `code-review/security-review` - Security-focused code analysis
- `code-review/performance-review` - Performance impact analysis
- `code-review/accessibility-review` - WCAG compliance checking
- `code-review/cross-repo-consistency` - Ensure consistency across repos

### 3. Debugging (7 skills)
- `debugging/root-cause-analysis` - Find bug origins systematically
- `debugging/stack-trace-analyzer` - Interpret error logs and traces
- `debugging/regression-detector` - Identify breaking changes
- `debugging/memory-leak-detector` - Find memory leaks in code
- `debugging/performance-degradation` - Track performance regressions
- `debugging/flaky-test-analyzer` - Identify and fix flaky tests
- `debugging/debug-statement-generator` - Create targeted debugging code

### 4. DevOps & Infrastructure (6 skills)
- `devops/docker-optimizer` - Optimize Docker configurations
- `devops/kubernetes-deployer` - Deploy to Kubernetes clusters
- `devops/ci-cd-generator` - Generate GitHub Actions/GitLab CI workflows
- `devops/infrastructure-as-code` - Create Terraform/CloudFormation
- `devops/deployment-validator` - Verify deployments are safe
- `devops/scaling-advisor` - Recommend scaling strategies

### 5. Security (8 skills)
- `security/vulnerability-scanner` - Scan for known vulnerabilities
- `security/secrets-detector` - Find exposed secrets and credentials
- `security/dependency-auditor` - Audit third-party dependencies
- `security/sast-analyzer` - Static application security testing
- `security/auth-review` - Review authentication implementations
- `security/encryption-validator` - Verify encryption practices
- `security/compliance-checker` - Check against security standards (SOC2, ISO)
- `security/penetration-test-prep` - Prepare code for security audits

### 6. Documentation (5 skills)
- `documentation/api-docs-generator` - Generate OpenAPI/GraphQL documentation
- `documentation/readme-generator` - Create comprehensive READMEs
- `documentation/changelog-generator` - Generate CHANGELOG from commits
- `documentation/architecture-docs` - Document system architecture
- `documentation/inline-docs-generator` - Add JSDoc/docstrings

### 7. Testing (7 skills)
- `testing/test-case-generator` - Generate comprehensive test cases
- `testing/coverage-analyzer` - Analyze and improve coverage
- `testing/mutation-tester` - Run mutation testing
- `testing/e2e-test-generator` - Generate end-to-end tests
- `testing/integration-test-creator` - Create integration test suites
- `testing/mock-data-generator` - Generate realistic test data
- `testing/performance-test-builder` - Create load and performance tests

### 8. Performance Optimization (6 skills)
- `performance/bundle-analyzer` - Analyze build bundles
- `performance/rendering-optimizer` - Optimize React/Vue rendering
- `performance/database-optimizer` - Optimize database queries
- `performance/caching-strategist` - Design caching strategies
- `performance/cdn-config-optimizer` - Optimize CDN configuration
- `performance/memory-profiler` - Profile and optimize memory usage

### 9. Automation (6 skills)
- `automation/batch-pr-generator` - Create PRs across multiple repos
- `automation/changelog-automation` - Auto-generate release notes
- `automation/dependency-updater` - Auto-update dependencies safely
- `automation/migration-automator` - Automate code migrations
- `automation/workflow-scheduler` - Schedule recurring agent tasks
- `automation/approval-workflow` - Smart approval routing

### 10. UI/UX Development (6 skills)
- `ui-ux/component-analyzer` - Analyze component consistency
- `ui-ux/accessibility-auditor` - WCAG accessibility review
- `ui-ux/responsive-tester` - Test responsive design
- `ui-ux/design-token-generator` - Generate design tokens
- `ui-ux/interaction-validator` - Validate user interactions
- `ui-ux/theme-generator` - Create color/theme systems

### 11. Branding & Consistency (4 skills)
- `branding/style-guide-enforcer` - Enforce brand guidelines
- `branding/color-consistency-checker` - Check color usage consistency
- `branding/logo-placement-validator` - Validate logo/asset usage
- `branding/typography-auditor` - Ensure font consistency

### 12. Analytics & Metrics (5 skills)
- `analytics/code-metrics-analyzer` - Calculate complexity, LOC, etc.
- `analytics/dependency-graph-generator` - Create dependency visualizations
- `analytics/code-velocity-tracker` - Track development velocity
- `analytics/technical-debt-calculator` - Quantify technical debt
- `analytics/codebase-health-report` - Generate health reports

### 13. API Integration (5 skills)
- `integration/api-connector` - Create API integrations
- `integration/webhook-manager` - Manage webhook implementations
- `integration/data-transformer` - Transform between data formats
- `integration/auth-integrator` - Handle authentication flows
- `integration/rate-limiting-manager` - Implement rate limiting

### 14. Collaboration (4 skills)
- `collaboration/pr-context-generator` - Auto-generate PR descriptions
- `collaboration/issue-analyzer` - Analyze and categorize issues
- `collaboration/team-insight-generator` - Generate team insights
- `collaboration/documentation-sync` - Sync docs across repos

### 15. Learning & Knowledge (4 skills)
- `learning/codebase-learner` - Learn codebase structure
- `learning/pattern-extractor` - Extract common patterns
- `learning/best-practices-guide` - Generate best practices docs
- `learning/technology-recommender` - Recommend tech stack improvements

### 16. Optimization Strategy (4 skills)
- `optimization/algorithm-improver` - Optimize algorithms
- `optimization/query-optimizer` - Optimize database queries
- `optimization/asset-optimizer` - Compress/optimize assets
- `optimization/build-time-reducer` - Reduce build times

### 17. Code Analysis (5 skills)
- `analysis/complexity-analyzer` - Calculate cyclomatic complexity
- `analysis/dead-code-detector` - Find unused code
- `analysis/dependency-analyzer` - Analyze dependencies
- `analysis/code-duplication-detector` - Find code duplication
- `analysis/anti-pattern-detector` - Find anti-patterns

### 18. Workflow Automation (5 skills)
- `workflow/voice-command-parser` - Convert voice to actions
- `workflow/decision-engine` - Auto-make decisions with parameters
- `workflow/task-orchestrator` - Coordinate multi-step workflows
- `workflow/approval-chain` - Manage approval workflows
- `workflow/notification-manager` - Handle notifications

### 19. Infrastructure Monitoring (4 skills)
- `monitoring/health-checker` - Check system health
- `monitoring/log-analyzer` - Parse and analyze logs
- `monitoring/alert-manager` - Manage alerts
- `monitoring/metrics-collector` - Collect and report metrics

### 20. Agent Intelligence (6 skills)
- `agent/self-learner` - Learn from past decisions
- `agent/context-manager` - Manage agent context and memory
- `agent/decision-maker` - Make autonomous decisions
- `agent/error-handler` - Handle and learn from errors
- `agent/capability-discoverer` - Discover available skills
- `agent/performance-optimizer` - Optimize agent performance

---

## 🎯 SKILL USAGE GUIDE FOR AGENTS

### How Agents Discover Skills
1. Read this manifest at startup
2. Query llm.txt for relevant skills for their role
3. Load skill instructions from appropriate category folder
4. Execute with full context of user's codebase

### Skill Execution Pattern
```
Agent Role → Required Task → llm.txt (Find Relevant Skills) → Load Skill File → Execute → Report Results
```

### Skill Categories at a Glance

| Category | Count | Primary Use | Key Skills |
|----------|-------|-------------|-----------|
| Code Generation | 8 | Creating new code | Production code, Architecture |
| Code Review | 6 | Quality assurance | Multi-agent review, Security |
| Debugging | 7 | Problem solving | Root cause analysis, Trace analysis |
| DevOps | 6 | Infrastructure | Docker, Kubernetes, CI/CD |
| Security | 8 | Risk mitigation | Vulnerability scan, Secrets detect |
| Documentation | 5 | Knowledge sharing | API docs, README, Architecture |
| Testing | 7 | Quality verification | Test generation, Coverage analysis |
| Performance | 6 | Optimization | Bundle analysis, Memory profiling |
| Automation | 6 | Repetitive tasks | Batch PR, Dependency update |
| UI/UX | 6 | User experience | Component analysis, Accessibility |
| Branding | 4 | Consistency | Style guide, Color consistency |
| Analytics | 5 | Insights | Metrics, Technical debt, Health |
| Integration | 5 | External systems | API connectors, Webhooks |
| Collaboration | 4 | Team coordination | PR context, Issues, Insights |
| Learning | 4 | Knowledge building | Pattern extraction, Best practices |
| Optimization | 4 | Performance | Algorithms, Queries, Assets |
| Analysis | 5 | Code insights | Complexity, Dead code, Duplication |
| Workflow | 5 | Automation | Voice parsing, Decision engine |
| Monitoring | 4 | Observability | Health, Logs, Alerts, Metrics |
| Agent Intelligence | 6 | Self-improvement | Learning, Context, Decisions |

---

## 🔄 Integration with OpenHands

All skills integrate seamlessly with:
- **Agent Controller**: Skills are available to all agents
- **EventStream**: Skills emit structured events
- **LLM Context**: Skills provide context windows
- **Voice Agent**: Skills respond to voice commands
- **Auto Decision Mode**: Skills support autonomous execution

---

## 📝 Adding New Skills

To add a new skill:
1. Create folder in appropriate category
2. Create `skill.md` with instructions
3. Create `examples.md` with examples
4. Update this manifest
5. Register in voice-agent config

---

## 🚀 Next Steps

1. Implement voice agent framework (see voice-agent.md)
2. Configure slash commands (see slash-commands.md)
3. Set up auto-decision making (see auto-decisions.md)
4. Integrate Microsoft Agent Lightning (see agent-lightning.md)

---

*Last Updated: 2026-01-22*
*Platform: OpenHands Jarvis Edition v1.0*
