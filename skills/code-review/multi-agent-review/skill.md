# Skill: Multi-Agent Code Review

## Purpose
Coordinate multiple specialized agents to provide comprehensive code review from different angles: security, performance, maintainability, and accessibility.

## When to Use
- Pull request submission
- Major refactors
- New feature implementation
- Dependency updates
- Cross-repository changes

## Review Agents Activated

### Security Agent
Checks:
- Input validation
- Injection vulnerabilities (SQL, XSS, etc.)
- Authentication/Authorization
- Secrets exposure
- Crypto usage
- Data sanitization

### Performance Agent
Checks:
- Algorithm efficiency (Big O)
- Database query optimization
- Memory leaks
- Render performance (React)
- Bundle size impact
- Caching opportunities

### Maintainability Agent
Checks:
- Code complexity
- Naming conventions
- Function/method length
- Module dependencies
- Dead code
- Commented code

### Testing Agent
Checks:
- Test coverage
- Test quality
- Edge cases covered
- Mock data appropriate
- Integration test needed
- Performance tests included

### Accessibility Agent
Checks:
- WCAG compliance
- Semantic HTML
- ARIA labels
- Color contrast
- Keyboard navigation
- Screen reader compatibility

## Execution Process

### Phase 1: Parallel Analysis (All agents run simultaneously)
```
Security → Scan for vulnerabilities
Performance → Analyze efficiency
Maintainability → Check code quality
Testing → Verify coverage
Accessibility → Check a11y compliance
```

### Phase 2: Findings Aggregation
```
Compile results from all agents:
- Critical issues (block merge)
- Major issues (must fix)
- Minor issues (nice to have)
- Suggestions (for discussion)
```

### Phase 3: Report Generation
```
Create review report with:
- Summary of findings
- Severity breakdown
- Specific line references
- Suggested fixes
- Estimated effort
- Approval recommendation
```

## Output Format
```
Code Review Report
=================

Overall Score: X/10
Recommendation: [Approve | Request Changes | Reject]

Security Review:
  - Issues: N
  - Severity: [Critical/High/Medium/Low]
  - Files Affected: [list]

Performance Review:
  - Issues: N
  - Potential Impact: [High/Medium/Low]
  - Files Affected: [list]

Maintainability Review:
  - Issues: N
  - Complexity Score: X
  - Files Affected: [list]

Testing Review:
  - Coverage: X%
  - Missing Coverage: [areas]
  - Files Affected: [list]

Accessibility Review:
  - Issues: N
  - WCAG Level: [A/AA/AAA]
  - Files Affected: [list]

Detailed Findings:
[Grouped by severity and file]

Recommended Actions:
1. [Action with line reference]
2. [Action with line reference]
```

## Approval Logic

### Auto-Approve If:
- All agents: No critical/major issues
- Security: Zero security findings
- Testing: Coverage >80% for new code
- Performance: No regressions
- Accessibility: WCAG AA compliant

### Request Changes If:
- Minor issues found
- Suggestions for improvement
- Coverage 70-80%
- Performance warnings (not failures)

### Block Merge If:
- Security: Any critical vulnerability
- Testing: Coverage <70% for new code
- Accessibility: WCAG A violations
- Performance: Major regression detected

## Configuration Options

### Review Depth
- **Quick**: Security + Testing only (5 min)
- **Standard**: All agents (10 min) - DEFAULT
- **Thorough**: All agents + detailed analysis (20 min)

### Issue Severity Mapping
- Critical: Blocks deployment
- High: Should be fixed before merge
- Medium: Should fix before merge
- Low: Consider fixing in future

## Parameters
- `depth`: quick | standard | thorough
- `auto_approve`: true | false
- `block_on`: critical | high | all
- `coverage_threshold`: 50-100 (default: 80)

## Success Criteria
- [ ] All agents completed
- [ ] Report generated with clear recommendations
- [ ] Line references accurate
- [ ] Severity levels appropriate
- [ ] Actionable suggestions provided

## Integration Points
- GitHub PR checks
- Pre-merge hooks
- CI/CD pipeline
- Slack/email notifications
- Agent learning system

## Related Skills
- `security/vulnerability-scanner` - Detailed security
- `testing/coverage-analyzer` - Detailed coverage
- `performance/bundle-analyzer` - Detailed performance
- `ui-ux/accessibility-auditor` - Detailed a11y
