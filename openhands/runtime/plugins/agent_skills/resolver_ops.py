from __future__ import annotations

import subprocess
from pathlib import Path

DEFAULT_RESOLVER_REPO = "https://github.com/All-Hands-AI/openhands-resolver.git"

__all__ = [
    "clone_openhands_resolver_repo",
    "update_openhands_resolver_repo",
    "run_openhands_resolver_command",
]


def clone_openhands_resolver_repo(
    destination: str = "openhands-resolver", branch: str = "main"
) -> str:
    """Clone the OpenHands resolver repository.

    Returns the absolute path to the cloned repository.
    """
    dest_path = Path(destination).expanduser().resolve()
    if dest_path.exists() and (dest_path / ".git").exists():
        return str(dest_path)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            branch,
            DEFAULT_RESOLVER_REPO,
            str(dest_path),
        ],
        check=True,
    )
    return str(dest_path)


def update_openhands_resolver_repo(destination: str = "openhands-resolver") -> str:
    """Update the OpenHands resolver repository with the latest changes.

    Returns the absolute path to the repository.
    """
    dest_path = Path(destination).expanduser().resolve()
    if not (dest_path / ".git").exists():
        return clone_openhands_resolver_repo(destination)

    subprocess.run(["git", "-C", str(dest_path), "fetch", "--all"], check=True)
    subprocess.run(["git", "-C", str(dest_path), "pull", "--ff-only"], check=True)
    return str(dest_path)


def run_openhands_resolver_command(
    command: list[str], destination: str = "openhands-resolver"
) -> str:
    """Run a command inside the OpenHands resolver repository.

    Returns stdout as a string.
    """
    dest_path = Path(destination).expanduser().resolve()
    if not dest_path.exists():
        dest_path = Path(clone_openhands_resolver_repo(destination))

    completed = subprocess.run(
        command,
        cwd=str(dest_path),
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()
