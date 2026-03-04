#!/usr/bin/env python3
"""Interactive git diff annotation tool.

Generates a cleaned diff, opens it in an editor, and returns user annotations
as a git diff from a temporary review repository.

Usage:
    git-review.py
    git-review.py <base_ref>
    git-review.py --clean
    git-review.py --test
"""

from __future__ import annotations

import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

OVERLAY_TIMEOUT_SECONDS = int(os.environ.get("REVIEW_TIMEOUT_SECONDS", "1800"))


def git(*args: str, cwd: str | None = None) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)
    return result.stdout.strip()


def git_ok(*args: str, cwd: str | None = None) -> bool:
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)
    return result.returncode == 0


def detect_default_branch() -> str:
    ref = git("symbolic-ref", "refs/remotes/origin/HEAD")
    if ref:
        return ref.replace("refs/remotes/origin/", "")

    for branch in ("master", "main", "trunk"):
        if git_ok("rev-parse", "--verify", f"origin/{branch}"):
            return branch
    for branch in ("master", "main", "trunk"):
        if git_ok("rev-parse", "--verify", branch):
            return branch
    return "master"


def has_uncommitted_changes() -> bool:
    return bool(
        git("diff", "--name-only")
        or git("diff", "--cached", "--name-only")
        or git("ls-files", "--others", "--exclude-standard")
    )


def get_project_name() -> str:
    remote = git("remote", "get-url", "origin")
    if remote:
        name = remote.rstrip("/").rsplit("/", 1)[-1]
        return name.removesuffix(".git")
    return Path.cwd().name


def get_current_branch() -> str:
    return git("rev-parse", "--abbrev-ref", "HEAD")


def get_file_status(diff_args: list[str]) -> dict[str, str]:
    output = git("diff", "--name-status", *diff_args)
    statuses: dict[str, str] = {}
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        code, name = parts
        if code.startswith(("R", "C")):
            multi = line.split("\t")
            if len(multi) >= 3:
                name = multi[2]
                statuses[name] = "renamed" if code.startswith("R") else "copied"
                continue
        statuses[name] = {"A": "new", "M": "modified", "D": "deleted"}.get(code[0], "changed")
    return statuses


def get_untracked_files() -> list[str]:
    output = git("ls-files", "--others", "--exclude-standard")
    return output.splitlines() if output else []


def generate_untracked_diff(files: list[str]) -> str:
    sections: list[str] = []
    for fpath in files:
        try:
            content = Path(fpath).read_text()
        except (OSError, UnicodeDecodeError):
            continue
        prefixed = "\n".join(f"+{line}" for line in content.splitlines())
        sections.append(f"=== {fpath} (untracked) ===\n\n{prefixed}")
    return "\n\n".join(sections) + "\n" if sections else ""


def generate_clean_diff(diff_args: list[str]) -> str:
    raw = git("diff", *diff_args)
    if not raw:
        return ""

    statuses = get_file_status(diff_args)
    lines = raw.splitlines()
    out: list[str] = []
    skip_header = True

    for line in lines:
        if line.startswith("diff --git "):
            match = re.search(r" b/(.+)$", line)
            if match:
                file_name = match.group(1)
                status = statuses.get(file_name, "changed")
                if out:
                    out.append("")
                out.append(f"=== {file_name} ({status}) ===")
                out.append("")
            skip_header = True
            continue

        if skip_header and line.startswith(
            (
                "index ",
                "--- ",
                "+++ ",
                "old mode",
                "new mode",
                "new file mode",
                "deleted file mode",
                "similarity index",
                "rename from",
                "rename to",
                "copy from",
                "copy to",
            )
        ):
            continue

        if line.startswith("@@"):
            skip_header = False
            context = re.search(r"@@ .+? @@\s*(.+)", line)
            out.append(f"··· {context.group(1)}" if context else "···")
            continue

        skip_header = False
        out.append(line)

    return "\n".join(out) + "\n"


def make_header(diff_args: list[str], mode: str) -> str:
    branch = get_current_branch()
    parts = [f"Branch: {branch}"]
    if mode == "uncommitted":
        staged = len(git("diff", "--cached", "--name-only").splitlines()) if git("diff", "--cached", "--name-only") else 0
        unstaged = len(git("diff", "--name-only").splitlines()) if git("diff", "--name-only") else 0
        untracked = len(get_untracked_files())
        parts.extend([f"Staged: {staged}", f"Unstaged: {unstaged}"])
        if untracked:
            parts.append(f"Untracked: {untracked}")
    else:
        base = diff_args[0].split("...")[0] if diff_args else "?"
        commits = git("rev-list", "--count", f"{base}..HEAD") if diff_args and "..." in diff_args[0] else "?"
        files = len(git("diff", "--name-only", *diff_args).splitlines())
        parts.extend([f"Base: {base}", f"Commits: {commits}", f"Files: {files}"])
    return " | ".join(parts)


def get_review_dir() -> Path:
    safe = re.sub(r"[^a-zA-Z0-9_.-]", "-", f"{get_project_name()}-{get_current_branch()}")
    return Path(tempfile.gettempdir()) / f"git-review-{safe}"


def setup_review_repo(review_dir: Path, content: str) -> None:
    review_file = review_dir / "review.diff"
    if not (review_dir / ".git").exists():
        review_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=review_dir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "review@local"], cwd=review_dir, capture_output=True)
        subprocess.run(["git", "config", "user.name", "review"], cwd=review_dir, capture_output=True)

    review_file.write_text(content)
    subprocess.run(["git", "add", "review.diff"], cwd=review_dir, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", "update review", "--allow-empty"], cwd=review_dir, capture_output=True)


def wait_for_sentinel(sentinel: Path, timeout_seconds: int) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if sentinel.exists():
            return True
        time.sleep(0.25)
    return False


def open_overlay(editor: str, path: Path) -> int:
    if os.environ.get("TMUX") and shutil.which("tmux"):
        result = subprocess.run(
            [
                "tmux",
                "display-popup",
                "-E",
                "-w",
                "90%",
                "-h",
                "90%",
                "-T",
                "Git Review",
                "--",
                editor,
                str(path),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode

    kitty_socket = os.environ.get("KITTY_LISTEN_ON")
    if kitty_socket and shutil.which("kitty"):
        fd, sentinel_raw = tempfile.mkstemp(prefix="git-review-")
        os.close(fd)
        os.unlink(sentinel_raw)
        sentinel = Path(sentinel_raw)
        wrapper = f"{shlex.quote(editor)} {shlex.quote(str(path))}; touch {shlex.quote(str(sentinel))}"
        cmd = [
            "kitty",
            "@",
            "--to",
            kitty_socket,
            "launch",
            "--type=overlay",
            f"--title=Git Review: {path.name}",
        ]
        wid = os.environ.get("KITTY_WINDOW_ID")
        if wid:
            cmd.extend(["--match", f"id:{wid}"])
        cmd.extend(["sh", "-c", wrapper])

        launch = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if launch.returncode != 0:
            sentinel.unlink(missing_ok=True)
            return 1
        ok = wait_for_sentinel(sentinel, OVERLAY_TIMEOUT_SECONDS)
        sentinel.unlink(missing_ok=True)
        return 0 if ok else 1

    pane = os.environ.get("WEZTERM_PANE")
    if pane and shutil.which("wezterm"):
        fd, sentinel_raw = tempfile.mkstemp(prefix="git-review-")
        os.close(fd)
        os.unlink(sentinel_raw)
        sentinel = Path(sentinel_raw)
        wrapper = f"{shlex.quote(editor)} {shlex.quote(str(path))}; touch {shlex.quote(str(sentinel))}"
        launch = subprocess.run(
            [
                "wezterm",
                "cli",
                "split-pane",
                "--bottom",
                "--percent",
                "80",
                "--pane-id",
                pane,
                "--",
                "sh",
                "-c",
                wrapper,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if launch.returncode != 0:
            sentinel.unlink(missing_ok=True)
            return 1
        ok = wait_for_sentinel(sentinel, OVERLAY_TIMEOUT_SECONDS)
        sentinel.unlink(missing_ok=True)
        return 0 if ok else 1

    return 1


def open_editor(path: Path) -> int:
    editor = os.environ.get("EDITOR", "vi")
    if open_overlay(editor, path) == 0:
        return 0
    return subprocess.run([editor, str(path)]).returncode


def get_annotations(review_dir: Path) -> str:
    return git("diff", cwd=str(review_dir))


def run_review(base_ref: str | None = None) -> int:
    if not git_ok("rev-parse", "--is-inside-work-tree"):
        print("error: not inside a git repository", file=sys.stderr)
        return 1

    if base_ref:
        diff_args = [base_ref if ("..." in base_ref or ".." in base_ref) else f"{base_ref}...HEAD"]
        mode = "branch"
    elif has_uncommitted_changes():
        diff_args = ["HEAD"]
        mode = "uncommitted"
    else:
        diff_args = [f"{detect_default_branch()}...HEAD"]
        mode = "branch"

    clean_diff = generate_clean_diff(diff_args)
    untracked_diff = generate_untracked_diff(get_untracked_files()) if mode == "uncommitted" else ""

    if not clean_diff and not untracked_diff:
        print("no changes to review", file=sys.stderr)
        return 0

    content_parts = [f"# {make_header(diff_args, mode)}"]
    if clean_diff:
        content_parts.append(clean_diff)
    if untracked_diff:
        content_parts.append(untracked_diff)
    content = "\n\n".join(content_parts) + "\n"

    review_dir = get_review_dir()
    setup_review_repo(review_dir, content)

    review_file = review_dir / "review.diff"
    if open_editor(review_file) != 0:
        print("error: editor launch failed", file=sys.stderr)
        return 1

    annotations = get_annotations(review_dir)
    if annotations:
        print(annotations)
    return 0


def run_tests() -> int:
    import unittest

    class TestCore(unittest.TestCase):
        def test_branch_detection(self) -> None:
            self.assertIsInstance(detect_default_branch(), str)

        def test_project_name(self) -> None:
            self.assertTrue(get_project_name())

        def test_review_dir(self) -> None:
            review_dir = get_review_dir()
            self.assertTrue(str(review_dir).startswith(tempfile.gettempdir()))

        def test_untracked_diff_empty(self) -> None:
            self.assertEqual(generate_untracked_diff([]), "")

        def test_sentinel_timeout(self) -> None:
            missing = Path(tempfile.gettempdir()) / "missing-git-review-sentinel"
            self.assertFalse(wait_for_sentinel(missing, 1))

    class TestRepoSetup(unittest.TestCase):
        def test_setup_repo(self) -> None:
            temp_dir = Path(tempfile.mkdtemp(prefix="git-review-test-"))
            try:
                setup_review_repo(temp_dir, "hello\n")
                self.assertTrue((temp_dir / ".git").exists())
                self.assertEqual((temp_dir / "review.diff").read_text(), "hello\n")
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for tc in (TestCore, TestRepoSetup):
        suite.addTests(loader.loadTestsFromTestCase(tc))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="interactive git diff annotation tool")
    parser.add_argument("--test", action="store_true", help="run tests")
    parser.add_argument("--clean", action="store_true", help="remove temporary review repository")
    parser.add_argument("base_ref", nargs="?", help="base ref for diff")
    args = parser.parse_args()

    if args.test:
        return run_tests()

    if args.clean:
        review_dir = get_review_dir()
        if review_dir.exists():
            shutil.rmtree(review_dir)
            print(f"removed {review_dir}", file=sys.stderr)
        else:
            print("no review repository found", file=sys.stderr)
        return 0

    return run_review(args.base_ref)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\r\033[K", end="")
        raise SystemExit(130)
