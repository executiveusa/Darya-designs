"""
Configuration for Autonomous PR Review & Merge Skill

Define all customizable parameters for the skill:
- Decision thresholds
- Risk gates
- Agent settings
- Notification preferences
- Monitoring configuration
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AgentConfig:
    """Configuration for individual review agents"""
    enabled: bool = True
    timeout_seconds: int = 120
    retry_on_failure: bool = True
    max_retries: int = 2


@dataclass
class SecurityAgentConfig(AgentConfig):
    """Security review agent specific config"""
    scan_dependencies: bool = True
    scan_secrets: bool = True
    scan_injection_vulnerabilities: bool = True
    severity_threshold: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    block_on_critical: bool = True


@dataclass
class CodeQualityAgentConfig(AgentConfig):
    """Code quality agent specific config"""
    max_complexity: int = 10
    documentation_required: bool = True
    enforce_naming_conventions: bool = True
    max_duplication_percent: float = 0.05


@dataclass
class TestingAgentConfig(AgentConfig):
    """Testing & coverage agent specific config"""
    require_tests: bool = True
    min_coverage_percent: float = 0.75
    critical_path_coverage_percent: float = 0.90
    min_passing_tests_ratio: float = 0.98  # 2% tolerance for flaky tests


@dataclass
class PerformanceAgentConfig(AgentConfig):
    """Performance agent specific config"""
    max_bundle_size_delta: float = 0.10  # 10% increase max
    max_memory_delta: float = 0.15  # 15% increase max
    max_build_time_delta: float = 0.20  # 20% build time increase max
    profile_on_change: bool = True


@dataclass
class UXAgentConfig(AgentConfig):
    """UX & integration agent specific config"""
    test_browsers: List[str] = None
    accessibility_level: str = "WCAG_AA"  # WCAG_A, WCAG_AA, WCAG_AAA
    responsive_test_viewports: List[str] = None

    def __post_init__(self):
        if self.test_browsers is None:
            self.test_browsers = ["Chrome", "Firefox", "Safari"]
        if self.responsive_test_viewports is None:
            self.responsive_test_viewports = ["mobile", "tablet", "desktop"]


@dataclass
class MergeStrategyConfig:
    """Merge execution configuration"""
    auto_merge_enabled: bool = True
    auto_merge_confidence_threshold: float = 0.92
    approve_confidence_threshold: float = 0.85
    request_changes_threshold: float = 0.75
    default_merge_strategy: str = "squash"  # squash, rebase, merge
    auto_delete_branch_after_merge: bool = True
    require_status_checks_to_pass: bool = True
    require_branch_up_to_date: bool = False
    max_merges_per_hour: int = 5
    merge_delay_seconds: int = 120  # Delay before executing merge


@dataclass
class SafeguardConfig:
    """Safety constraints to prevent merge disasters"""
    # Block critical risk PRs
    block_critical_security_risk: bool = True

    # Block breaking changes
    block_breaking_changes: bool = False  # Set to True to be conservative
    require_breaking_change_approval: bool = True

    # Block merge conflicts
    block_merge_conflicts: bool = True

    # Gate new dependencies
    require_approval_for_new_dependencies: bool = True
    require_approval_for_major_updates: bool = True

    # Author-based gates
    require_approval_for_new_contributors: bool = True
    contributor_history_threshold_merged_prs: int = 5

    # Timeout enforcement
    agent_execution_timeout_seconds: int = 120
    total_review_timeout_seconds: int = 600  # 10 minutes

    # Post-merge rollback
    enable_post_merge_monitoring: bool = True
    monitoring_duration_hours: int = 6
    rollback_on_critical_alert: bool = True


@dataclass
class NotificationConfig:
    """Notification and communication settings"""
    # PR comments
    post_summary_comment: bool = True
    post_detailed_findings: bool = False
    post_as_bot: bool = True
    bot_name: str = "deepagent[bot]"

    # Alerts and escalation
    notify_on_rejection: bool = True
    notify_on_critical_security_finding: bool = True
    notify_author_on_changes_requested: bool = True
    alert_on_high_risk: bool = True

    # Team notifications
    notify_team_slack: bool = False
    slack_webhook_url: Optional[str] = None
    slack_channel: str = "#dev-alerts"

    # Email notifications
    send_email_on_merge: bool = False
    email_recipients: List[str] = None

    def __post_init__(self):
        if self.email_recipients is None:
            self.email_recipients = []


@dataclass
class MonitoringConfig:
    """Post-merge monitoring and observability"""
    enabled: bool = True
    duration_hours: int = 6
    error_rate_threshold: float = 0.01  # 1% error rate
    performance_degradation_threshold: float = 0.15  # 15% slower
    check_interval_seconds: int = 30

    # Metrics to track
    track_error_rate: bool = True
    track_response_time: bool = True
    track_failed_deployments: bool = True
    track_customer_support_tickets: bool = False

    # Rollback triggers
    auto_rollback_on_critical_errors: bool = True
    auto_rollback_on_deployment_failure: bool = True
    manual_rollback_threshold: float = 0.05  # 5% error rate


@dataclass
class PRAutomationConfig:
    """Main configuration class for PR automation"""
    # Repository
    repo: str = os.getenv("GH_REPO", "executiveusa/Darya-designs")
    github_token: str = os.getenv("GITHUB_TOKEN", "")

    # Mode of operation
    mode: str = "autonomous"  # autonomous, approval_required, info_only

    # Agent configurations
    security_config: SecurityAgentConfig = None
    code_quality_config: CodeQualityAgentConfig = None
    testing_config: TestingAgentConfig = None
    performance_config: PerformanceAgentConfig = None
    ux_config: UXAgentConfig = None

    # Merge strategy
    merge_config: MergeStrategyConfig = None

    # Safety constraints
    safeguard_config: SafeguardConfig = None

    # Notifications
    notification_config: NotificationConfig = None

    # Monitoring
    monitoring_config: MonitoringConfig = None

    def __post_init__(self):
        """Initialize defaults"""
        if self.security_config is None:
            self.security_config = SecurityAgentConfig()
        if self.code_quality_config is None:
            self.code_quality_config = CodeQualityAgentConfig()
        if self.testing_config is None:
            self.testing_config = TestingAgentConfig()
        if self.performance_config is None:
            self.performance_config = PerformanceAgentConfig()
        if self.ux_config is None:
            self.ux_config = UXAgentConfig()
        if self.merge_config is None:
            self.merge_config = MergeStrategyConfig()
        if self.safeguard_config is None:
            self.safeguard_config = SafeguardConfig()
        if self.notification_config is None:
            self.notification_config = NotificationConfig()
        if self.monitoring_config is None:
            self.monitoring_config = MonitoringConfig()

    def to_dict(self) -> Dict:
        """Convert config to dictionary"""
        return {
            "repo": self.repo,
            "mode": self.mode,
            "security": self.security_config.__dict__,
            "code_quality": self.code_quality_config.__dict__,
            "testing": self.testing_config.__dict__,
            "performance": self.performance_config.__dict__,
            "ux": self.ux_config.__dict__,
            "merge": self.merge_config.__dict__,
            "safeguards": self.safeguard_config.__dict__,
            "notifications": self.notification_config.__dict__,
            "monitoring": self.monitoring_config.__dict__,
        }


# ============================================================================
# Predefined Configuration Profiles
# ============================================================================

def create_strict_config() -> PRAutomationConfig:
    """
    Strict mode: Require high confidence, extensive checks.
    Suitable for critical systems (payment, security).
    """
    return PRAutomationConfig(
        mode="approval_required",
        merge_config=MergeStrategyConfig(
            auto_merge_enabled=False,
            auto_merge_confidence_threshold=0.98,
        ),
        safeguard_config=SafeguardConfig(
            block_critical_security_risk=True,
            block_breaking_changes=True,
            require_approval_for_new_dependencies=True,
        ),
        testing_config=TestingAgentConfig(
            require_tests=True,
            min_coverage_percent=0.90,
            critical_path_coverage_percent=0.95,
        ),
    )


def create_moderate_config() -> PRAutomationConfig:
    """
    Moderate mode: Balance speed and safety.
    Suitable for most projects.
    """
    return PRAutomationConfig(
        mode="autonomous",
        merge_config=MergeStrategyConfig(
            auto_merge_enabled=True,
            auto_merge_confidence_threshold=0.92,
        ),
    )


def create_permissive_config() -> PRAutomationConfig:
    """
    Permissive mode: Prioritize speed.
    Suitable for internal tools, documentation.
    """
    return PRAutomationConfig(
        mode="autonomous",
        merge_config=MergeStrategyConfig(
            auto_merge_enabled=True,
            auto_merge_confidence_threshold=0.80,
        ),
        safeguard_config=SafeguardConfig(
            block_breaking_changes=False,
            require_approval_for_new_dependencies=False,
        ),
        testing_config=TestingAgentConfig(
            require_tests=False,
            min_coverage_percent=0.50,
        ),
    )


def create_info_only_config() -> PRAutomationConfig:
    """
    Info-only mode: Post summary but don't merge.
    Suitable for testing or observation.
    """
    return PRAutomationConfig(
        mode="info_only",
        merge_config=MergeStrategyConfig(
            auto_merge_enabled=False,
        ),
        notification_config=NotificationConfig(
            post_summary_comment=True,
            post_detailed_findings=True,
        ),
    )


# ============================================================================
# Configuration Loading
# ============================================================================

def load_config(profile: str = "moderate") -> PRAutomationConfig:
    """
    Load configuration by profile name.

    Args:
        profile: "strict", "moderate", "permissive", or "info_only"

    Returns:
        PRAutomationConfig instance
    """
    profiles = {
        "strict": create_strict_config,
        "moderate": create_moderate_config,
        "permissive": create_permissive_config,
        "info_only": create_info_only_config,
    }

    if profile not in profiles:
        raise ValueError(f"Unknown profile: {profile}. "
                        f"Choose from: {list(profiles.keys())}")

    return profiles[profile]()


# Default configuration (loaded from environment or defaults)
DEFAULT_CONFIG = PRAutomationConfig(
    repo=os.getenv("GH_REPO", "executiveusa/Darya-designs"),
    github_token=os.getenv("GITHUB_TOKEN", ""),
    mode=os.getenv("PR_REVIEW_MODE", "autonomous"),
)
