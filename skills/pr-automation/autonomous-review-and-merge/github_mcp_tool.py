"""
GitHub MCP Tool - Model Context Protocol integration for PR operations

This tool provides agents with access to GitHub operations for PR review
and merge automation. Implements Safe Mode with confidence-based safeguards.
"""

import json
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime


class GitHubOperation(Enum):
    """Available GitHub operations"""
    LIST_PRS = "list_prs"
    GET_PR = "get_pr"
    GET_PR_DIFF = "get_pr_diff"
    GET_PR_FILES = "get_pr_files"
    GET_PR_REVIEWS = "get_pr_reviews"
    GET_PR_CHECKS = "get_pr_checks"
    POST_COMMENT = "post_comment"
    REQUEST_CHANGES = "request_changes"
    APPROVE = "approve"
    MERGE = "merge"
    CLOSE = "close"
    CHECK_CONFLICTS = "check_conflicts"
    GET_PR_AUTHOR_HISTORY = "get_pr_author_history"


@dataclass
class PullRequestContext:
    """Complete PR context for review"""
    number: int
    title: str
    description: str
    author: str
    created_at: str
    updated_at: str
    branch: str
    base: str
    diff: str
    files_changed: List[str]
    files_modified: List[Dict[str, Any]]
    additions: int
    deletions: int
    changed_files_count: int
    ci_status: str  # passing, failing, pending
    ci_check_runs: List[Dict[str, Any]]
    has_conflicts: bool
    mergeable: bool
    existing_reviews: List[Dict[str, Any]]
    review_comments: List[Dict[str, Any]]
    dependency_files_changed: bool
    breaking_changes_detected: bool


@dataclass
class ReviewResult:
    """Base class for all review results"""
    score: float  # 0.0 to 1.0
    passed: bool
    findings: List[str]
    timestamp: str
    duration_seconds: float


class GitHubMCPTool:
    """
    GitHub API wrapper for PR automation.
    Uses 'gh' CLI for reliability and GitHub MCP for advanced operations.
    """

    def __init__(self, repo: str, github_token: Optional[str] = None):
        self.repo = repo
        self.github_token = github_token or self._get_token_from_env()
        self.session = None

    @staticmethod
    def _get_token_from_env() -> str:
        """Get GitHub token from environment"""
        import os
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError(
                "GITHUB_TOKEN environment variable not set. "
                "Required for GitHub PR operations."
            )
        return token

    def _run_gh_command(self, command: str) -> Dict[str, Any]:
        """Execute gh CLI command and return JSON response"""
        try:
            result = subprocess.run(
                f"gh {command}",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
            )
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"output": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            return {
                "error": e.stderr,
                "exit_code": e.returncode,
            }

    async def list_prs(
        self,
        state: str = "open",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        List pull requests.

        Args:
            state: 'open', 'closed', or 'all'
            limit: Maximum PRs to return

        Returns:
            List of PR metadata
        """
        cmd = (
            f"pr list -R {self.repo} "
            f"--state {state} "
            f"--limit {limit} "
            f"--json number,title,author,createdAt,state"
        )
        result = self._run_gh_command(cmd)
        return result if isinstance(result, list) else [result]

    async def get_pr(self, pr_number: int) -> PullRequestContext:
        """
        Fetch complete PR context for review.
        Aggregates PR metadata, diff, files, checks, and reviews.
        """
        # Basic PR info
        pr_cmd = f"pr view {pr_number} -R {self.repo} --json number,title,body,author,createdAt,updatedAt,headRefName,baseRefName,additions,deletions,files,state"
        pr_data = self._run_gh_command(pr_cmd)

        # Get diff
        diff_cmd = f"pr diff {pr_number} -R {self.repo}"
        diff_result = subprocess.run(
            f"gh {diff_cmd}",
            shell=True,
            capture_output=True,
            text=True,
        )
        diff = diff_result.stdout

        # Check for conflicts
        conflict_cmd = f"pr view {pr_number} -R {self.repo} --json mergeable"
        conflict_data = self._run_gh_command(conflict_cmd)
        has_conflicts = not conflict_data.get("mergeable", True)

        # Get CI status
        checks_cmd = f"pr checks {pr_number} -R {self.repo}"
        checks_result = subprocess.run(
            f"gh {checks_cmd}",
            shell=True,
            capture_output=True,
            text=True,
        )
        check_runs = [
            line for line in checks_result.stdout.split("\n") if line.strip()
        ]

        # Get existing reviews
        reviews_cmd = f"pr review-list {pr_number} -R {self.repo} --json author,state,submittedAt,body"
        reviews_data = self._run_gh_command(reviews_cmd)

        # Detect dependency changes
        files_changed = [f.get("name", "") for f in pr_data.get("files", [])]
        dependency_files = {
            "package.json", "package-lock.json", "requirements.txt",
            "Pipfile", "Pipfile.lock", "pyproject.toml", "poetry.lock",
            "Gemfile", "Gemfile.lock", "go.mod", "go.sum",
        }
        dependency_files_changed = any(
            f in dependency_files for f in files_changed
        )

        # Detect breaking changes (heuristic)
        breaking_changes = any(
            pattern in diff.lower()
            for pattern in [
                "breaking change", "@deprecated", "removed:",
                "backwards incompatible", "api change",
            ]
        )

        return PullRequestContext(
            number=pr_number,
            title=pr_data.get("title", ""),
            description=pr_data.get("body", ""),
            author=pr_data.get("author", {}).get("login", ""),
            created_at=pr_data.get("createdAt", ""),
            updated_at=pr_data.get("updatedAt", ""),
            branch=pr_data.get("headRefName", ""),
            base=pr_data.get("baseRefName", ""),
            diff=diff,
            files_changed=files_changed,
            files_modified=pr_data.get("files", []),
            additions=pr_data.get("additions", 0),
            deletions=pr_data.get("deletions", 0),
            changed_files_count=len(files_changed),
            ci_status=self._parse_ci_status(check_runs),
            ci_check_runs=check_runs,
            has_conflicts=has_conflicts,
            mergeable=not has_conflicts,
            existing_reviews=reviews_data if isinstance(reviews_data, list) else [],
            review_comments=[],  # Would populate from review comments endpoint
            dependency_files_changed=dependency_files_changed,
            breaking_changes_detected=breaking_changes,
        )

    @staticmethod
    def _parse_ci_status(check_runs: List[str]) -> str:
        """Parse CI check output to determine overall status"""
        if not check_runs:
            return "pending"

        output = "\n".join(check_runs)
        if "✓" in output and "✗" not in output:
            return "passing"
        elif "✗" in output:
            return "failing"
        else:
            return "pending"

    async def post_comment(
        self,
        pr_number: int,
        body: str,
    ) -> bool:
        """Post review comment to PR"""
        # Escape special characters
        body_escaped = body.replace('"', '\\"').replace('$', '\\$')
        cmd = f"pr comment {pr_number} -R {self.repo} -b \"{body_escaped}\""
        result = self._run_gh_command(cmd)
        return "error" not in result

    async def approve_pr(
        self,
        pr_number: int,
        review_body: str = "",
    ) -> bool:
        """Approve PR with optional review body"""
        cmd = f"pr review {pr_number} -R {self.repo} --approve"
        if review_body:
            body_escaped = review_body.replace('"', '\\"')
            cmd += f" -b \"{body_escaped}\""
        result = self._run_gh_command(cmd)
        return "error" not in result

    async def request_changes(
        self,
        pr_number: int,
        review_body: str,
    ) -> bool:
        """Request changes on PR"""
        body_escaped = review_body.replace('"', '\\"')
        cmd = f"pr review {pr_number} -R {self.repo} --request-changes -b \"{body_escaped}\""
        result = self._run_gh_command(cmd)
        return "error" not in result

    async def merge_pr(
        self,
        pr_number: int,
        strategy: str = "squash",
        auto_delete: bool = True,
    ) -> bool:
        """
        Merge PR with specified strategy.

        Args:
            pr_number: PR number to merge
            strategy: 'squash', 'rebase', or 'merge'
            auto_delete: Delete branch after merge

        Returns:
            Success status
        """
        cmd = f"pr merge {pr_number} -R {self.repo} --{strategy}"
        if auto_delete:
            cmd += " --delete-branch"

        result = self._run_gh_command(cmd)
        return "error" not in result

    async def close_pr(
        self,
        pr_number: int,
        reason: str = "",
    ) -> bool:
        """Close PR without merging"""
        cmd = f"pr close {pr_number} -R {self.repo}"
        result = self._run_gh_command(cmd)

        if result.get("error"):
            return False

        # Post closing reason if provided
        if reason:
            await self.post_comment(pr_number, f"PR closed: {reason}")

        return True

    async def check_branch_conflicts(
        self,
        pr_number: int,
    ) -> Dict[str, Any]:
        """Check if PR has merge conflicts"""
        cmd = f"pr view {pr_number} -R {self.repo} --json mergeable,mergeStateStatus"
        result = self._run_gh_command(cmd)
        return {
            "has_conflicts": not result.get("mergeable", True),
            "merge_state": result.get("mergeStateStatus", "unknown"),
        }

    async def get_pr_author_risk_profile(
        self,
        author: str,
    ) -> Dict[str, Any]:
        """
        Get risk profile of PR author.
        Returns: merged PRs, merged success rate, reverted PRs count.
        """
        # Query: How many PRs from this author were merged?
        cmd = f"search prs -R {self.repo} --author {author} --state merged"
        merged = self._run_gh_command(cmd)

        # Query: How many PRs reverted?
        revert_cmd = f"search commits -R {self.repo} --author {author} -q 'Revert'"
        reverted = self._run_gh_command(revert_cmd)

        return {
            "author": author,
            "merged_prs": len(merged) if isinstance(merged, list) else 0,
            "reverted_commits": len(reverted) if isinstance(reverted, list) else 0,
            "risk_level": self._calculate_author_risk(merged, reverted),
        }

    @staticmethod
    def _calculate_author_risk(merged: List, reverted: List) -> str:
        """Determine author risk level based on history"""
        merged_count = len(merged) if isinstance(merged, list) else 0
        reverted_count = len(reverted) if isinstance(reverted, list) else 0

        if merged_count == 0:
            return "unknown"  # New contributor

        revert_rate = reverted_count / max(merged_count, 1)

        if revert_rate > 0.2:
            return "high"
        elif revert_rate > 0.1:
            return "medium"
        else:
            return "low"


# Tool interface for LiteLLM integration
def create_github_tool_definition(repo: str) -> Dict[str, Any]:
    """
    Create LiteLLM ChatCompletionToolParam for GitHub operations.

    This tool can be added to agents via:
    agent.set_mcp_tools([create_github_tool_definition(repo)])
    """
    return {
        "type": "function",
        "function": {
            "name": "github_operations",
            "description": (
                "Perform GitHub PR operations: list, view, comment, approve, "
                "request changes, merge, or close PRs. Uses GitHub API and gh CLI."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [op.value for op in GitHubOperation],
                        "description": "GitHub operation to perform",
                    },
                    "pr_number": {
                        "type": "integer",
                        "description": "PR number (required for most operations)",
                    },
                    "body": {
                        "type": "string",
                        "description": "Comment/review body (for comments, reviews)",
                    },
                    "strategy": {
                        "type": "string",
                        "enum": ["squash", "rebase", "merge"],
                        "description": "Merge strategy (for merge operation)",
                    },
                    "state": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "description": "PR state filter (for list_prs)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Result limit (for list operations)",
                    },
                },
                "required": ["operation"],
            },
        },
    }
