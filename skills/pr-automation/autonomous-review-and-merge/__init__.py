"""
Autonomous PR Review & Merge Skill

Implements Deep Agent QA philosophy for continuous code validation.
Multi-perspective review from security, quality, testing, performance, and UX angles.

Usage:
    from skills.pr_automation.autonomous_review_and_merge import review_and_merge_pr

    result = await review_and_merge_pr(
        repo="executiveusa/Darya-designs",
        pr_number=123,
        auto_merge_enabled=True,
    )
"""

from .pr_orchestrator import (
    review_and_merge_pr,
    MergeDecisionEngine,
    MergeDecision,
    RiskLevel,
    MergeRecommendation,
)

from .pr_review_agents import (
    MultiPerspectiveReviewer,
    SecurityReviewAgent,
    CodeQualityAgent,
    TestingCoverageAgent,
    PerformanceAgent,
    UXIntegrationAgent,
    AgentReviewResult,
    ReviewFinding,
)

from .github_mcp_tool import (
    GitHubMCPTool,
    PullRequestContext,
    create_github_tool_definition,
)

__all__ = [
    # Main entry point
    "review_and_merge_pr",

    # Decision engine
    "MergeDecisionEngine",
    "MergeDecision",
    "RiskLevel",
    "MergeRecommendation",

    # Review agents
    "MultiPerspectiveReviewer",
    "SecurityReviewAgent",
    "CodeQualityAgent",
    "TestingCoverageAgent",
    "PerformanceAgent",
    "UXIntegrationAgent",
    "AgentReviewResult",
    "ReviewFinding",

    # GitHub integration
    "GitHubMCPTool",
    "PullRequestContext",
    "create_github_tool_definition",
]

__version__ = "1.0.0"
__author__ = "Darya OpenHands Team"
__description__ = "Autonomous PR review and merge automation using Deep Agent QA philosophy"
