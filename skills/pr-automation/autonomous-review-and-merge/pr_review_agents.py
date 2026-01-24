"""
Multi-Perspective PR Review Agents

Implements Deep Agent QA Philosophy:
- Security Agent (Paranoid Mode): Find how things break
- Code Quality Agent (Empathy Mode): Understand code health
- Testing Agent (Rigor Mode): Validate reliability
- Performance Agent: Measure impact
- UX Agent: Validate user experience
"""

import asyncio
import json
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from github_mcp_tool import PullRequestContext, ReviewResult


# ============================================================================
# Base Review Agent
# ============================================================================

@dataclass
class ReviewFinding:
    """Individual finding from a review"""
    severity: str  # critical, high, medium, low, info
    category: str
    message: str
    location: Optional[str] = None  # file:line
    suggestion: Optional[str] = None
    confidence: float = 1.0


@dataclass
class AgentReviewResult(ReviewResult):
    """Extended review result with structured findings"""
    agent_name: str
    findings: List[ReviewFinding] = field(default_factory=list)
    confidence_factors: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    def __post_init__(self):
        super().__init__(
            score=self.score,
            passed=self.passed,
            findings=[f.message for f in self.findings],
            timestamp=datetime.now().isoformat(),
            duration_seconds=self.duration_seconds,
        )


class BaseReviewAgent(ABC):
    """Base class for all PR review agents"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.start_time = None

    async def execute(self, context: PullRequestContext) -> AgentReviewResult:
        """Execute review, measuring time"""
        self.start_time = datetime.now()
        try:
            result = await self._review(context)
            duration = (datetime.now() - self.start_time).total_seconds()
            result.duration_seconds = duration
            return result
        except Exception as e:
            return AgentReviewResult(
                agent_name=self.agent_name,
                score=0.5,
                passed=False,
                findings=[ReviewFinding(
                    severity="high",
                    category="agent_error",
                    message=f"Review agent error: {str(e)}",
                )],
                confidence_factors={},
                timestamp=datetime.now().isoformat(),
                duration_seconds=(datetime.now() - self.start_time).total_seconds(),
            )

    @abstractmethod
    async def _review(self, context: PullRequestContext) -> AgentReviewResult:
        """Implement review logic in subclass"""
        pass

    def _run_command(self, cmd: str) -> str:
        """Execute shell command and return output"""
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
        )
        return result.stdout + result.stderr

    def _score_from_findings(
        self,
        critical_count: int = 0,
        high_count: int = 0,
        medium_count: int = 0,
        low_count: int = 0,
    ) -> float:
        """Calculate score based on finding severity"""
        penalties = {
            "critical": 0.30,
            "high": 0.10,
            "medium": 0.05,
            "low": 0.02,
        }

        deductions = (
            critical_count * penalties["critical"] +
            high_count * penalties["high"] +
            medium_count * penalties["medium"] +
            low_count * penalties["low"]
        )

        return max(0.0, min(1.0, 1.0 - deductions))


# ============================================================================
# Security Review Agent (Paranoid Mode)
# ============================================================================

class SecurityReviewAgent(BaseReviewAgent):
    """
    Operates in paranoia mode: assumes everything is a security risk
    until proven otherwise. Probes for how code breaks security assumptions.
    """

    def __init__(self):
        super().__init__("SecurityReview")
        self.critical_patterns = {
            # SQL injection patterns
            r"SELECT.*\+|INSERT.*\+|UPDATE.*\+|DELETE.*\+": "SQL injection risk",
            # XSS patterns
            r"innerHTML\s*=|eval\(|dangerouslySetInnerHTML": "XSS vulnerability",
            # Command injection
            r"exec\(|system\(|shell\(|\$\(.*\)": "Command injection risk",
            # Hardcoded credentials
            r"password\s*=\s*['\"]|api[_-]?key\s*=\s*['\"]|token\s*=\s*['\"]": "Hardcoded credential",
            # Missing HTTPS
            r"http://.*api|http://.*oauth": "Unencrypted communication",
        }

    async def _review(self, context: PullRequestContext) -> AgentReviewResult:
        """Execute security review across multiple dimensions"""
        findings: List[ReviewFinding] = []

        # 1. Dependency vulnerability check
        findings.extend(await self._check_dependency_vulnerabilities(context))

        # 2. Code pattern security check
        findings.extend(self._check_security_patterns(context.diff))

        # 3. Credential detection
        findings.extend(self._detect_credentials(context.diff))

        # 4. Permission escalation checks
        findings.extend(self._check_permission_escalation(context))

        # 5. Supply chain risk assessment
        if context.dependency_files_changed:
            findings.extend(
                await self._assess_supply_chain_risk(context)
            )

        # Calculate score
        critical = len([f for f in findings if f.severity == "critical"])
        high = len([f for f in findings if f.severity == "high"])
        medium = len([f for f in findings if f.severity == "medium"])
        low = len([f for f in findings if f.severity == "low"])

        score = self._score_from_findings(critical, high, medium, low)

        return AgentReviewResult(
            agent_name=self.agent_name,
            score=score,
            passed=score >= 0.85,
            findings=findings,
            confidence_factors={
                "dependency_check": 0.95,
                "pattern_detection": 0.90,
                "credential_detection": 0.98,
            },
            recommendations=self._build_recommendations(findings),
            timestamp=datetime.now().isoformat(),
            duration_seconds=0,
        )

    async def _check_dependency_vulnerabilities(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Check for known vulnerabilities in dependencies"""
        findings = []

        if not context.dependency_files_changed:
            return findings

        # Run npm audit for JavaScript
        npm_result = self._run_command("npm audit --json 2>/dev/null || echo '{}'")
        try:
            npm_data = json.loads(npm_result)
            vulns = npm_data.get("vulnerabilities", {})
            for pkg, info in vulns.items():
                severity = info.get("severity", "unknown").lower()
                findings.append(ReviewFinding(
                    severity=severity if severity in ["critical", "high"] else "medium",
                    category="dependency_vulnerability",
                    message=f"Vulnerable dependency: {pkg}",
                    suggestion=f"Update {pkg} to a patched version",
                ))
        except json.JSONDecodeError:
            pass

        # Run pip check for Python
        pip_result = self._run_command("pip check 2>/dev/null || echo 'ok'")
        if "has requirement" in pip_result:
            findings.append(ReviewFinding(
                severity="high",
                category="dependency_conflict",
                message="Python dependency conflict detected",
                suggestion="Resolve dependency conflicts in requirements",
            ))

        return findings

    def _check_security_patterns(self, diff: str) -> List[ReviewFinding]:
        """Check for dangerous code patterns"""
        findings = []
        import re

        for pattern, description in self.critical_patterns.items():
            if re.search(pattern, diff, re.IGNORECASE):
                severity = "critical" if pattern in [
                    r"SELECT.*\+|INSERT.*\+",  # SQL injection
                    r"eval\(|dangerouslySetInnerHTML",  # XSS
                ] else "high"

                findings.append(ReviewFinding(
                    severity=severity,
                    category="security_pattern",
                    message=f"Detected: {description}",
                    suggestion="Review and replace with parameterized queries or safe alternatives",
                    confidence=0.85,
                ))

        return findings

    def _detect_credentials(self, diff: str) -> List[ReviewFinding]:
        """Detect hardcoded credentials"""
        findings = []
        import re

        # Patterns for detecting secrets
        secret_patterns = {
            r"password\s*[:=]\s*['\"][^'\"]*['\"]": "Hardcoded password",
            r"(api[_-]?key|apikey)\s*[:=]\s*['\"][^'\"]*['\"]": "Hardcoded API key",
            r"(token|access[_-]token)\s*[:=]\s*['\"][^'\"]*['\"]": "Hardcoded token",
            r"aws[_-]?secret[_-]?access[_-]?key": "AWS secret key",
            r"private[_-]?key": "Private key",
        }

        for pattern, desc in secret_patterns.items():
            matches = re.finditer(pattern, diff, re.IGNORECASE)
            for match in matches:
                findings.append(ReviewFinding(
                    severity="critical",
                    category="hardcoded_secret",
                    message=f"Potential {desc} detected",
                    suggestion="Move to environment variables or secrets manager",
                    confidence=0.90,
                ))

        return findings

    def _check_permission_escalation(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Check for permission/access control changes"""
        findings = []
        import re

        # Look for auth-related changes
        auth_patterns = {
            r"isAdmin|isRoot|isSuperUser": "Admin flag change",
            r"role\s*=\s*['\"]admin": "Role escalation",
            r"permissions?\s*[:=]": "Permission modification",
        }

        for pattern, desc in auth_patterns.items():
            if re.search(pattern, context.diff, re.IGNORECASE):
                findings.append(ReviewFinding(
                    severity="high",
                    category="permission_change",
                    message=f"Detected: {desc}",
                    suggestion="Verify this is intentional and properly tested",
                ))

        return findings

    async def _assess_supply_chain_risk(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Assess risk from new dependencies"""
        findings = []

        # Check for suspicious dependencies (heuristic)
        suspicious_keywords = {
            "crypto": "cryptographic library addition",
            "shell": "shell execution library",
            "eval": "code evaluation library",
            "exec": "execution library",
        }

        for keyword, desc in suspicious_keywords.items():
            if any(keyword.lower() in f for f in context.files_changed):
                findings.append(ReviewFinding(
                    severity="medium",
                    category="supply_chain_risk",
                    message=f"New dependency with {desc} keyword",
                    suggestion="Verify this dependency is from trusted source",
                ))

        return findings

    def _build_recommendations(
        self,
        findings: List[ReviewFinding],
    ) -> List[str]:
        """Build actionable recommendations from findings"""
        recs = []

        critical_findings = [f for f in findings if f.severity == "critical"]
        if critical_findings:
            recs.append(
                "CRITICAL: Address all critical security findings before merge"
            )

        return recs


# ============================================================================
# Code Quality Agent (Empathy Mode)
# ============================================================================

class CodeQualityAgent(BaseReviewAgent):
    """
    Evaluates code from maintainers' and future developers' perspective.
    Emphasizes readability, maintainability, and consistency.
    """

    def __init__(self):
        super().__init__("CodeQuality")

    async def _review(self, context: PullRequestContext) -> AgentReviewResult:
        """Execute code quality review"""
        findings: List[ReviewFinding] = []

        # 1. Complexity analysis
        findings.extend(self._analyze_complexity(context))

        # 2. Naming and style consistency
        findings.extend(self._check_naming_conventions(context))

        # 3. Duplication detection
        findings.extend(self._detect_duplication(context))

        # 4. Documentation quality
        findings.extend(self._assess_documentation(context))

        # Calculate score
        critical = len([f for f in findings if f.severity == "critical"])
        high = len([f for f in findings if f.severity == "high"])
        medium = len([f for f in findings if f.severity == "medium"])
        low = len([f for f in findings if f.severity == "low"])

        score = self._score_from_findings(critical, high, medium, low)

        return AgentReviewResult(
            agent_name=self.agent_name,
            score=score,
            passed=score >= 0.75,
            findings=findings,
            confidence_factors={
                "complexity_analysis": 0.85,
                "style_check": 0.80,
                "documentation": 0.75,
            },
            recommendations=[
                "Focus on reducing function complexity",
                "Add JSDoc/docstring comments for public APIs",
            ] if findings else [],
            timestamp=datetime.now().isoformat(),
            duration_seconds=0,
        )

    def _analyze_complexity(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Analyze cyclomatic/cognitive complexity"""
        findings = []
        import re

        # Simple heuristic: look for deeply nested structures
        max_indent_level = 0
        for line in context.diff.split("\n"):
            if line.startswith("+"):
                indent = len(line) - len(line.lstrip())
                max_indent_level = max(max_indent_level, indent)

        # Warn if nesting gets too deep
        if max_indent_level > 32:  # More than 8 levels of indentation
            findings.append(ReviewFinding(
                severity="medium",
                category="high_complexity",
                message="Deep nesting detected (8+ levels)",
                suggestion="Consider refactoring into smaller functions",
            ))

        return findings

    def _check_naming_conventions(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Check naming consistency"""
        findings = []
        import re

        # Look for inconsistent naming patterns
        # e.g., mixing camelCase with snake_case
        camel_case = len(re.findall(r"[a-z][a-z0-9]*[A-Z]", context.diff))
        snake_case = len(re.findall(r"[a-z0-9]*_[a-z0-9]*", context.diff))

        if camel_case > 0 and snake_case > 0 and max(camel_case, snake_case) > 5:
            findings.append(ReviewFinding(
                severity="low",
                category="naming_inconsistency",
                message="Mixed naming conventions (camelCase and snake_case)",
                suggestion="Use consistent naming convention across the codebase",
            ))

        return findings

    def _detect_duplication(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Detect code duplication"""
        findings = []

        # Simple heuristic: look for repeated lines
        lines = [l.strip() for l in context.diff.split("\n") if l.startswith("+")]
        line_counts = {}
        for line in lines:
            line_counts[line] = line_counts.get(line, 0) + 1

        # Flag lines that appear multiple times
        duplicates = {line: count for line, count in line_counts.items()
                     if count > 2 and len(line) > 20}

        if duplicates:
            findings.append(ReviewFinding(
                severity="medium",
                category="code_duplication",
                message=f"Potential code duplication detected ({len(duplicates)} patterns)",
                suggestion="Consider extracting duplicated code into reusable functions",
            ))

        return findings

    def _assess_documentation(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Assess code documentation quality"""
        findings = []

        # Check if PR description is substantive
        if len(context.description) < 50:
            findings.append(ReviewFinding(
                severity="low",
                category="documentation",
                message="PR description is brief (less than 50 characters)",
                suggestion="Provide more detail about the changes and motivation",
            ))

        # Check for comments in code
        comment_ratio = context.diff.count("//") + context.diff.count("#")
        if context.additions > 50 and comment_ratio < 2:
            findings.append(ReviewFinding(
                severity="low",
                category="inline_documentation",
                message=f"Large change ({context.additions} lines) with few comments",
                suggestion="Add comments explaining non-obvious logic",
            ))

        return findings


# ============================================================================
# Testing & Coverage Agent (Rigor Mode)
# ============================================================================

class TestingCoverageAgent(BaseReviewAgent):
    """
    Executes test suite, analyzes coverage, probes for untested paths.
    """

    def __init__(self):
        super().__init__("TestingCoverage")

    async def _review(self, context: PullRequestContext) -> AgentReviewResult:
        """Execute testing and coverage review"""
        findings: List[ReviewFinding] = []

        # 1. Run tests
        test_results = await self._run_tests()
        findings.extend(test_results["findings"])

        # 2. Check coverage
        if test_results["success"]:
            coverage = await self._check_coverage()
            findings.extend(coverage["findings"])

        # 3. Assess critical path coverage
        findings.extend(await self._assess_critical_paths(context))

        # Calculate score
        critical = len([f for f in findings if f.severity == "critical"])
        high = len([f for f in findings if f.severity == "high"])
        medium = len([f for f in findings if f.severity == "medium"])
        low = len([f for f in findings if f.severity == "low"])

        score = self._score_from_findings(critical, high, medium, low)

        return AgentReviewResult(
            agent_name=self.agent_name,
            score=score,
            passed=test_results["success"] and score >= 0.75,
            findings=findings,
            confidence_factors={
                "test_execution": 0.98,
                "coverage_analysis": 0.85,
            },
            recommendations=[
                "Increase test coverage for critical code paths",
                "Add edge case tests for error handling",
            ] if findings else ["All tests passing with good coverage"],
            timestamp=datetime.now().isoformat(),
            duration_seconds=0,
        )

    async def _run_tests(self) -> Dict[str, Any]:
        """Run test suite and capture results"""
        findings = []

        # Try npm test
        npm_result = subprocess.run(
            "npm run test -- --reporter=json 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if npm_result.returncode == 0:
            return {"success": True, "findings": []}
        else:
            # Parse test failures
            output = npm_result.stdout + npm_result.stderr
            findings.append(ReviewFinding(
                severity="high",
                category="test_failure",
                message="Test suite failed",
                suggestion="Fix failing tests before merge",
            ))

        # Try pytest
        pytest_result = subprocess.run(
            "poetry run pytest --tb=short 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if pytest_result.returncode != 0:
            findings.append(ReviewFinding(
                severity="high",
                category="test_failure",
                message="Python tests failed",
                suggestion="Fix failing tests",
            ))

        return {
            "success": len(findings) == 0,
            "findings": findings,
        }

    async def _check_coverage(self) -> Dict[str, Any]:
        """Check code coverage metrics"""
        findings = []

        # Try getting coverage from npm
        coverage_result = subprocess.run(
            "npm run test:coverage -- --reporter=json 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if coverage_result.returncode == 0:
            try:
                data = json.loads(coverage_result.stdout)
                coverage_pct = data.get("total", {}).get("lines", {}).get("pct", 0)

                if coverage_pct < 60:
                    findings.append(ReviewFinding(
                        severity="high",
                        category="low_coverage",
                        message=f"Code coverage low: {coverage_pct}%",
                        suggestion="Target 75%+ coverage for critical paths",
                    ))
                elif coverage_pct < 75:
                    findings.append(ReviewFinding(
                        severity="medium",
                        category="coverage",
                        message=f"Code coverage: {coverage_pct}% (target: 75%)",
                        suggestion="Add tests for uncovered code paths",
                    ))
            except json.JSONDecodeError:
                pass

        return {"findings": findings}

    async def _assess_critical_paths(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Assess testing of critical code paths"""
        findings = []

        # Look for changes to core files
        critical_paths = [
            "auth", "payment", "security", "core", "lib",
            "api", "routes", "middleware",
        ]

        changed_critical = [
            f for f in context.files_changed
            if any(cp in f.lower() for cp in critical_paths)
        ]

        if changed_critical and context.additions > 20:
            findings.append(ReviewFinding(
                severity="medium",
                category="critical_path_testing",
                message=f"Changes to critical files: {len(changed_critical)}",
                suggestion="Ensure comprehensive test coverage for critical paths",
            ))

        return findings


# ============================================================================
# Performance & Scalability Agent
# ============================================================================

class PerformanceAgent(BaseReviewAgent):
    """Measures real-world performance impact"""

    def __init__(self):
        super().__init__("Performance")

    async def _review(self, context: PullRequestContext) -> AgentReviewResult:
        """Execute performance review"""
        findings: List[ReviewFinding] = []

        # 1. Bundle size analysis
        findings.extend(await self._analyze_bundle_size(context))

        # 2. Build time impact
        findings.extend(await self._check_build_time())

        # 3. Runtime performance estimation
        findings.extend(self._estimate_runtime_impact(context))

        # Calculate score
        score = self._score_from_findings(
            len([f for f in findings if f.severity == "critical"]),
            len([f for f in findings if f.severity == "high"]),
            len([f for f in findings if f.severity == "medium"]),
            len([f for f in findings if f.severity == "low"]),
        )

        return AgentReviewResult(
            agent_name=self.agent_name,
            score=score,
            passed=score >= 0.80,
            findings=findings,
            confidence_factors={"bundle_analysis": 0.80, "build_impact": 0.70},
            timestamp=datetime.now().isoformat(),
            duration_seconds=0,
        )

    async def _analyze_bundle_size(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Analyze bundle size changes"""
        findings = []

        # Check for large file additions
        large_files = [f for f in context.files_changed
                      if f.endswith((".js", ".css", ".ts", ".tsx"))]

        for file in large_files:
            if context.additions > 1000:
                findings.append(ReviewFinding(
                    severity="medium",
                    category="bundle_size",
                    message=f"Large file changes: {context.additions} lines added",
                    suggestion="Consider code splitting or lazy loading",
                ))
                break

        return findings

    async def _check_build_time(self) -> List[ReviewFinding]:
        """Check if build time is impacted"""
        findings = []
        # Would measure actual build time in production
        return findings

    def _estimate_runtime_impact(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Estimate runtime performance impact"""
        findings = []

        # Check for common performance anti-patterns
        perf_antipatterns = {
            r"for.*for.*for": "Triple nested loop",
            r"while.*true": "Infinite loop risk",
            r"\.*\.\*\..*": "Long method chain",
        }

        for pattern, desc in perf_antipatterns.items():
            import re
            if re.search(pattern, context.diff):
                findings.append(ReviewFinding(
                    severity="medium",
                    category="performance_antipattern",
                    message=f"Detected: {desc}",
                    suggestion="Review for performance implications",
                ))

        return findings


# ============================================================================
# UX & Integration Agent
# ============================================================================

class UXIntegrationAgent(BaseReviewAgent):
    """Tests UX and system integration"""

    def __init__(self):
        super().__init__("UXIntegration")

    async def _review(self, context: PullRequestContext) -> AgentReviewResult:
        """Execute UX/integration review"""
        findings: List[ReviewFinding] = []

        # 1. Check for breaking UI changes
        findings.extend(self._analyze_ui_changes(context))

        # 2. Accessibility assessment
        findings.extend(self._assess_accessibility(context))

        # 3. Integration point validation
        findings.extend(self._validate_integrations(context))

        # Calculate score
        score = self._score_from_findings(
            len([f for f in findings if f.severity == "critical"]),
            len([f for f in findings if f.severity == "high"]),
            len([f for f in findings if f.severity == "medium"]),
            len([f for f in findings if f.severity == "low"]),
        )

        return AgentReviewResult(
            agent_name=self.agent_name,
            score=score,
            passed=score >= 0.80,
            findings=findings,
            confidence_factors={"ui_analysis": 0.70, "accessibility": 0.75},
            timestamp=datetime.now().isoformat(),
            duration_seconds=0,
        )

    def _analyze_ui_changes(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Analyze UI/UX changes"""
        findings = []

        # Check for CSS changes
        css_files = [f for f in context.files_changed if f.endswith((".css", ".scss"))]
        if css_files and context.additions > 100:
            findings.append(ReviewFinding(
                severity="low",
                category="ui_change",
                message="Significant CSS changes detected",
                suggestion="Verify visual consistency across browsers",
            ))

        return findings

    def _assess_accessibility(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Assess WCAG accessibility compliance"""
        findings = []

        # Check for common accessibility issues
        a11y_issues = {
            r"<img[^>]*>(?!.*alt=)": "Missing image alt text",
            r"<button[^>]*>.*onclick": "Keyboard navigation issue",
            r"color:\s*#": "Hardcoded color (contrast issue)",
        }

        import re
        for pattern, desc in a11y_issues.items():
            if re.search(pattern, context.diff, re.IGNORECASE):
                findings.append(ReviewFinding(
                    severity="low",
                    category="accessibility",
                    message=f"Potential a11y issue: {desc}",
                    suggestion="Review WCAG 2.1 AA guidelines",
                ))

        return findings

    def _validate_integrations(
        self,
        context: PullRequestContext,
    ) -> List[ReviewFinding]:
        """Validate API/external integrations"""
        findings = []

        # Check for API calls
        api_patterns = [
            "fetch(", "axios.", "http.get", "http.post",
        ]

        for pattern in api_patterns:
            if pattern in context.diff:
                findings.append(ReviewFinding(
                    severity="low",
                    category="integration",
                    message="External API call detected",
                    suggestion="Verify API error handling and timeout logic",
                ))
                break

        return findings


# ============================================================================
# Orchestration
# ============================================================================

class MultiPerspectiveReviewer:
    """
    Orchestrates all review agents and synthesizes results.
    Implements Deep Agent QA philosophy.
    """

    def __init__(self):
        self.agents: List[BaseReviewAgent] = [
            SecurityReviewAgent(),
            CodeQualityAgent(),
            TestingCoverageAgent(),
            PerformanceAgent(),
            UXIntegrationAgent(),
        ]

    async def review_pr(
        self,
        context: PullRequestContext,
    ) -> Dict[str, AgentReviewResult]:
        """Execute all review agents in parallel"""
        # Run all agents concurrently
        results = await asyncio.gather(*[
            agent.execute(context) for agent in self.agents
        ])

        return {agent.agent_name: result
               for agent, result in zip(self.agents, results)}
