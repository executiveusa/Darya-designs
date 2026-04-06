"""
PR Review Orchestrator - Main agent for autonomous PR review and merge

Synthesizes multi-perspective reviews, calculates confidence score,
and makes autonomous merge decisions based on Deep Agent QA philosophy.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from enum import Enum

from github_mcp_tool import GitHubMCPTool, PullRequestContext
from pr_review_agents import (
    MultiPerspectiveReviewer,
    AgentReviewResult,
    ReviewFinding,
)


class MergeDecision(Enum):
    """PR merge decision"""
    AUTO_MERGE = "auto_merge"
    APPROVE_REQUEST_REVIEW = "approve_request_review"
    REQUEST_CHANGES = "request_changes"
    REJECT = "reject"


class RiskLevel(Enum):
    """Risk assessment level"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class MergeRecommendation:
    """Complete merge recommendation"""
    decision: MergeDecision
    confidence: float  # 0.0 to 1.0
    risk_level: RiskLevel
    score_breakdown: Dict[str, float]
    summary: str
    detailed_findings: List[str]
    recommendations: List[str]
    warnings: List[str]
    next_steps: List[str]
    merge_strategy: str  # squash, rebase, merge
    estimated_merge_safety: float  # Post-merge safety estimate


class MergeDecisionEngine:
    """
    Makes autonomous merge decisions based on aggregate review results.

    Implements confidence-based thresholds:
    - Confidence ≥ 0.92 → Auto-merge (low risk)
    - Confidence ≥ 0.85 → Approve (request human review for safety)
    - Confidence ≥ 0.75 → Request Changes
    - Confidence < 0.75 → Reject
    """

    # Configuration thresholds
    AUTO_MERGE_CONFIDENCE = 0.92
    APPROVE_CONFIDENCE = 0.85
    REQUEST_CHANGES_CONFIDENCE = 0.75

    # Scoring weights (must sum to 1.0)
    SCORE_WEIGHTS = {
        "security": 0.30,          # Non-negotiable
        "testing": 0.25,            # Critical path dependent
        "code_quality": 0.20,       # Important for maintainability
        "performance": 0.15,        # Application dependent
        "ux_integration": 0.10,     # User-facing dependent
    }

    # Risk gate configuration
    CRITICAL_RISK_BLOCKS_MERGE = True
    HIGH_RISK_REQUIRES_REVIEW = True
    BREAKING_CHANGES_BLOCK_MERGE = True
    NEW_DEPENDENCIES_REQUIRE_APPROVAL = True

    # Rate limiting
    MAX_MERGES_PER_HOUR = 5

    def __init__(self, repo: str):
        self.repo = repo
        self.github = GitHubMCPTool(repo)
        self.reviewer = MultiPerspectiveReviewer()
        self.merges_this_hour: List[datetime] = []

    async def evaluate_pr(
        self,
        pr_number: int,
    ) -> MergeRecommendation:
        """
        Comprehensive PR evaluation with autonomous decision.

        Flow:
        1. Fetch PR context
        2. Run all review agents (parallel)
        3. Assess risk factors
        4. Calculate confidence score
        5. Make merge decision
        6. Post summary comment
        """

        # 1. Fetch PR context
        context = await self.github.get_pr(pr_number)

        # 2. Run reviews
        review_results = await self.reviewer.review_pr(context)

        # 3. Assess risks
        risk_factors = await self._assess_risk_factors(context, review_results)

        # 4. Calculate confidence
        confidence = self._calculate_confidence(review_results)

        # 5. Make decision
        decision = self._make_decision(confidence, risk_factors, context)

        # 6. Build recommendation
        recommendation = self._build_recommendation(
            decision=decision,
            confidence=confidence,
            risk_factors=risk_factors,
            review_results=review_results,
            context=context,
        )

        return recommendation

    async def _assess_risk_factors(
        self,
        context: PullRequestContext,
        review_results: Dict[str, AgentReviewResult],
    ) -> Dict[str, Any]:
        """Assess multiple risk dimensions"""
        return {
            "merge_conflicts": context.has_conflicts,
            "breaking_changes": context.breaking_changes_detected,
            "new_dependencies": context.dependency_files_changed,
            "author_risk": await self.github.get_pr_author_risk_profile(
                context.author
            ),
            "scope_risk": self._assess_scope_risk(context),
            "test_risk": self._assess_test_risk(review_results),
            "security_risk": self._assess_security_risk(review_results),
            "overall_risk": "unknown",
        }

    def _assess_scope_risk(self, context: PullRequestContext) -> str:
        """Assess risk based on change scope"""
        if context.changed_files_count > 50:
            return "high"
        elif context.changed_files_count > 20:
            return "medium"
        elif context.additions > 1000:
            return "medium"
        else:
            return "low"

    def _assess_test_risk(
        self,
        review_results: Dict[str, AgentReviewResult],
    ) -> str:
        """Assess risk based on test coverage"""
        testing_result = review_results.get("TestingCoverage")
        if testing_result:
            if testing_result.score >= 0.90:
                return "low"
            elif testing_result.score >= 0.75:
                return "medium"
            else:
                return "high"
        return "unknown"

    def _assess_security_risk(
        self,
        review_results: Dict[str, AgentReviewResult],
    ) -> str:
        """Assess risk based on security findings"""
        security_result = review_results.get("SecurityReview")
        if security_result:
            # Check for critical findings
            critical = any(
                f.severity == "critical" for f in security_result.findings
            )
            if critical:
                return "critical"
            elif security_result.score < 0.85:
                return "high"
            elif security_result.score < 0.95:
                return "medium"
            else:
                return "low"
        return "unknown"

    def _calculate_confidence(
        self,
        review_results: Dict[str, AgentReviewResult],
    ) -> float:
        """
        Calculate overall confidence score from reviews.

        Weighted average of all review scores with penalties for critical issues.
        """
        scores = {
            "security": review_results.get("SecurityReview", object()).score or 0.5,
            "code_quality": review_results.get("CodeQuality", object()).score or 0.5,
            "testing": review_results.get("TestingCoverage", object()).score or 0.5,
            "performance": review_results.get("Performance", object()).score or 0.5,
            "ux_integration": review_results.get("UXIntegration", object()).score or 0.5,
        }

        # Calculate weighted score
        weighted_score = sum(
            scores[key] * self.SCORE_WEIGHTS[key]
            for key in self.SCORE_WEIGHTS
        )

        # Apply penalties for critical findings
        for result in review_results.values():
            critical_count = len([
                f for f in result.findings
                if f.severity == "critical"
            ])
            if critical_count > 0:
                weighted_score *= (0.95 ** critical_count)  # Each critical: -5%

        return max(0.0, min(1.0, weighted_score))

    def _make_decision(
        self,
        confidence: float,
        risk_factors: Dict[str, Any],
        context: PullRequestContext,
    ) -> MergeDecision:
        """
        Make merge decision based on confidence and risk gates.

        Decision tree:
        1. Check critical risk gates (block auto-merge)
        2. Check high risk gates (require human review)
        3. Apply confidence thresholds
        """

        # Gate 1: Critical risk blocks merge
        if self.CRITICAL_RISK_BLOCKS_MERGE:
            if risk_factors["security_risk"] == "critical":
                return MergeDecision.REJECT

        # Gate 2: Breaking changes require caution
        if self.BREAKING_CHANGES_BLOCK_MERGE and context.breaking_changes_detected:
            if confidence < self.APPROVE_CONFIDENCE:
                return MergeDecision.REJECT

        # Gate 3: Merge conflicts block merge
        if context.has_conflicts:
            return MergeDecision.REQUEST_CHANGES

        # Gate 4: New dependencies with high risk
        if self.NEW_DEPENDENCIES_REQUIRE_APPROVAL and context.dependency_files_changed:
            if risk_factors["security_risk"] in ["high", "critical"]:
                return MergeDecision.APPROVE_REQUEST_REVIEW

        # Apply confidence thresholds
        if confidence >= self.AUTO_MERGE_CONFIDENCE:
            return MergeDecision.AUTO_MERGE
        elif confidence >= self.APPROVE_CONFIDENCE:
            return MergeDecision.APPROVE_REQUEST_REVIEW
        elif confidence >= self.REQUEST_CHANGES_CONFIDENCE:
            return MergeDecision.REQUEST_CHANGES
        else:
            return MergeDecision.REJECT

    def _build_recommendation(
        self,
        decision: MergeDecision,
        confidence: float,
        risk_factors: Dict[str, Any],
        review_results: Dict[str, AgentReviewResult],
        context: PullRequestContext,
    ) -> MergeRecommendation:
        """Build comprehensive recommendation with reasoning"""

        # Determine risk level
        risk_level = self._determine_risk_level(risk_factors, review_results)

        # Calculate post-merge safety estimate
        merge_safety = self._estimate_merge_safety(confidence, risk_level)

        # Build detailed summary
        summary = self._build_summary(
            decision=decision,
            confidence=confidence,
            risk_level=risk_level,
            review_results=review_results,
            context=context,
        )

        # Extract findings
        all_findings = []
        for result in review_results.values():
            all_findings.extend([f.message for f in result.findings])

        # Build recommendations
        recommendations = self._build_recommendations(
            decision=decision,
            review_results=review_results,
            context=context,
        )

        # Build warnings
        warnings = self._build_warnings(risk_factors, decision)

        # Determine merge strategy
        merge_strategy = self._select_merge_strategy(context)

        # Build next steps
        next_steps = self._build_next_steps(decision, context)

        return MergeRecommendation(
            decision=decision,
            confidence=confidence,
            risk_level=risk_level,
            score_breakdown={
                name: result.score
                for name, result in review_results.items()
            },
            summary=summary,
            detailed_findings=all_findings,
            recommendations=recommendations,
            warnings=warnings,
            next_steps=next_steps,
            merge_strategy=merge_strategy,
            estimated_merge_safety=merge_safety,
        )

    def _determine_risk_level(
        self,
        risk_factors: Dict[str, Any],
        review_results: Dict[str, AgentReviewResult],
    ) -> RiskLevel:
        """Determine overall risk level"""
        if (risk_factors["security_risk"] == "critical" or
            any(risk_factors.get(k) == "critical" for k in risk_factors)):
            return RiskLevel.CRITICAL

        security_result = review_results.get("SecurityReview")
        if security_result and security_result.score < 0.8:
            return RiskLevel.HIGH

        if (risk_factors.get("scope_risk") == "high" or
            risk_factors.get("test_risk") == "high"):
            return RiskLevel.HIGH

        if (risk_factors.get("scope_risk") == "medium" or
            risk_factors.get("test_risk") == "medium"):
            return RiskLevel.MEDIUM

        return RiskLevel.LOW

    def _estimate_merge_safety(
        self,
        confidence: float,
        risk_level: RiskLevel,
    ) -> float:
        """Estimate post-merge safety based on confidence and risk"""
        base_safety = confidence

        # Adjust for risk level
        risk_adjustments = {
            RiskLevel.CRITICAL: 0.60,
            RiskLevel.HIGH: 0.75,
            RiskLevel.MEDIUM: 0.85,
            RiskLevel.LOW: 0.95,
        }

        return base_safety * risk_adjustments.get(risk_level, 0.70)

    def _build_summary(
        self,
        decision: MergeDecision,
        confidence: float,
        risk_level: RiskLevel,
        review_results: Dict[str, AgentReviewResult],
        context: PullRequestContext,
    ) -> str:
        """Build human-readable summary"""
        status_emoji = {
            MergeDecision.AUTO_MERGE: "✅",
            MergeDecision.APPROVE_REQUEST_REVIEW: "👀",
            MergeDecision.REQUEST_CHANGES: "⚠️",
            MergeDecision.REJECT: "❌",
        }

        decision_text = {
            MergeDecision.AUTO_MERGE: "AUTO-MERGED",
            MergeDecision.APPROVE_REQUEST_REVIEW: "APPROVED (Review Required)",
            MergeDecision.REQUEST_CHANGES: "CHANGES REQUESTED",
            MergeDecision.REJECT: "REJECTED",
        }

        return f"""## Autonomous PR Review Summary

**Decision**: {status_emoji.get(decision, '')} {decision_text.get(decision, '')}
**Confidence**: {confidence:.1%}
**Risk Level**: {risk_level.value.upper()}
**Files Changed**: {context.changed_files_count} | **+{context.additions}/-{context.deletions}**

### Review Breakdown

| Perspective | Score | Status |
|------------|-------|--------|
{self._build_review_table(review_results)}
"""

    def _build_review_table(
        self,
        review_results: Dict[str, AgentReviewResult],
    ) -> str:
        """Build review table for summary"""
        rows = []
        for name, result in review_results.items():
            status = "✅" if result.score >= 0.85 else "⚠️" if result.score >= 0.75 else "❌"
            clean_name = name.replace("Review", "").replace("Agent", "").strip()
            rows.append(f"| {clean_name} | {result.score:.0%} | {status} |")
        return "\n".join(rows)

    def _build_recommendations(
        self,
        decision: MergeDecision,
        review_results: Dict[str, AgentReviewResult],
        context: PullRequestContext,
    ) -> List[str]:
        """Build actionable recommendations"""
        recs = []

        # Add recommendations from review agents
        for result in review_results.values():
            recs.extend(result.recommendations)

        # Add decision-specific recommendations
        if decision == MergeDecision.REJECT:
            recs.insert(0, "Address all critical findings before attempting merge")

        elif decision == MergeDecision.REQUEST_CHANGES:
            recs.insert(0, "Implement requested changes and address review findings")

        elif decision == MergeDecision.APPROVE_REQUEST_REVIEW:
            recs.insert(0, "Awaiting human review before merge")

        # Add context-specific recommendations
        if context.breaking_changes_detected:
            recs.append("Breaking changes detected - consider major version bump")

        if context.dependency_files_changed:
            recs.append("Verify all new/updated dependencies are from trusted sources")

        return recs[:5]  # Top 5 recommendations

    def _build_warnings(
        self,
        risk_factors: Dict[str, Any],
        decision: MergeDecision,
    ) -> List[str]:
        """Build warning messages"""
        warnings = []

        if risk_factors.get("merge_conflicts"):
            warnings.append("⚠️ Merge conflicts detected - must be resolved")

        if risk_factors.get("breaking_changes"):
            warnings.append("⚠️ Breaking changes detected")

        if risk_factors.get("security_risk") in ["high", "critical"]:
            warnings.append("🔒 Security concerns identified")

        if decision == MergeDecision.AUTO_MERGE:
            warnings.append("✅ Auto-merge enabled (requires high confidence)")

        return warnings

    def _select_merge_strategy(
        self,
        context: PullRequestContext,
    ) -> str:
        """Select appropriate merge strategy"""
        # Use squash for feature branches (fewer commits = cleaner history)
        if "feature" in context.branch or "feat" in context.branch:
            return "squash"

        # Use rebase for bugfix branches
        if "bugfix" in context.branch or "fix" in context.branch:
            return "rebase"

        # Default to squash for cleaner history
        return "squash"

    def _build_next_steps(
        self,
        decision: MergeDecision,
        context: PullRequestContext,
    ) -> List[str]:
        """Build next steps for PR"""
        if decision == MergeDecision.AUTO_MERGE:
            return [
                "PR will be merged in 2 minutes",
                "Branch will be automatically deleted",
                "Deployment pipeline will be triggered",
                "Monitoring will be active for 6 hours",
            ]

        elif decision == MergeDecision.APPROVE_REQUEST_REVIEW:
            return [
                "Awaiting human review and approval",
                "Request will ping code owners",
                "Merge will proceed once approved",
            ]

        elif decision == MergeDecision.REQUEST_CHANGES:
            return [
                "Address the requested changes",
                "Re-submit for automated review",
                "Manual approval may be required",
            ]

        else:  # REJECT
            return [
                "Resolve critical issues and re-open PR",
                "Contact team lead if changes require architecture discussion",
                "Security team should review any security-related issues",
            ]

    async def execute_merge(
        self,
        recommendation: MergeRecommendation,
        pr_number: int,
    ) -> bool:
        """Execute merge if decision is AUTO_MERGE"""
        if recommendation.decision != MergeDecision.AUTO_MERGE:
            return False

        # Rate limiting check
        self._enforce_rate_limit()

        # Execute merge
        success = await self.github.merge_pr(
            pr_number=pr_number,
            strategy=recommendation.merge_strategy,
            auto_delete=True,
        )

        if success:
            self.merges_this_hour.append(datetime.now())

        return success

    def _enforce_rate_limit(self):
        """Enforce merge rate limiting"""
        # Remove old entries (older than 1 hour)
        cutoff = datetime.now() - timedelta(hours=1)
        self.merges_this_hour = [
            t for t in self.merges_this_hour if t > cutoff
        ]

        # Check limit
        if len(self.merges_this_hour) >= self.MAX_MERGES_PER_HOUR:
            raise RuntimeError(
                f"Rate limit exceeded: max {self.MAX_MERGES_PER_HOUR} "
                "merges per hour"
            )


# ============================================================================
# Main Entry Point
# ============================================================================

async def review_and_merge_pr(
    repo: str,
    pr_number: int,
    auto_merge_enabled: bool = True,
    post_comment: bool = True,
) -> Dict[str, Any]:
    """
    Main function to review and merge a PR autonomously.

    Args:
        repo: GitHub repository (e.g., "owner/repo")
        pr_number: PR number to review
        auto_merge_enabled: Allow automatic merge execution
        post_comment: Post summary comment to PR

    Returns:
        Decision and results
    """
    engine = MergeDecisionEngine(repo)

    # Evaluate PR
    recommendation = await engine.evaluate_pr(pr_number)

    # Post comment if enabled
    if post_comment:
        github = GitHubMCPTool(repo)
        await github.post_comment(
            pr_number=pr_number,
            body=recommendation.summary,
        )

    # Execute merge if enabled and approved
    merged = False
    if auto_merge_enabled:
        merged = await engine.execute_merge(recommendation, pr_number)

    return {
        "pr_number": pr_number,
        "decision": recommendation.decision.value,
        "confidence": recommendation.confidence,
        "risk_level": recommendation.risk_level.value,
        "merged": merged,
        "scores": recommendation.score_breakdown,
        "next_steps": recommendation.next_steps,
    }
