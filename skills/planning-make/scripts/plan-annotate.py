#!/usr/bin/env python3
"""Interactive plan annotation tool.

Opens a temporary copy of a plan file in the editor, waits for edits,
and prints a unified diff to stdout when changes are made.

Usage:
    plan-annotate.py <plan-file>
    plan-annotate.py --test
"""

from __future__ import annotations

import difflib
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SENTINEL_TIMEOUT_SECONDS = int(os.environ.get("ANNOTATE_TIMEOUT_SECONDS", "1800"))


def get_diff(original: str, edited: str) -> str:
    """Return unified diff between original and edited text."""
    original_lines = original.splitlines(keepends=True)
    edited_lines = edited.splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            original_lines,
            edited_lines,
            fromfile="original",
            tofile="annotated",
            n=2,
        )
    )


def wait_for_sentinel(sentinel: Path, timeout_seconds: int) -> bool:
    """Wait until sentinel appears or timeout expires."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if sentinel.exists():
            return True
        time.sleep(0.25)
    return False


def open_in_overlay(editor: str, path: Path) -> int:
    """Try tmux/kitty/wezterm overlay editors. Return 0 on success."""
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
                "Plan Review",
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
        fd, sentinel_raw = tempfile.mkstemp(prefix="plan-annotate-")
        os.close(fd)
        os.unlink(sentinel_raw)
        sentinel = Path(sentinel_raw)
        wrapper = (
            f"{shlex.quote(editor)} {shlex.quote(str(path))}; "
            f"touch {shlex.quote(str(sentinel))}"
        )
        cmd = [
            "kitty",
            "@",
            "--to",
            kitty_socket,
            "launch",
            "--type=overlay",
            f"--title=Plan Review: {path.name}",
        ]
        kitty_wid = os.environ.get("KITTY_WINDOW_ID")
        if kitty_wid:
            cmd.extend(["--match", f"id:{kitty_wid}"])
        cmd.extend(["sh", "-c", wrapper])

        launch = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if launch.returncode != 0:
            sentinel.unlink(missing_ok=True)
            return 1
        ok = wait_for_sentinel(sentinel, SENTINEL_TIMEOUT_SECONDS)
        sentinel.unlink(missing_ok=True)
        return 0 if ok else 1

    wezterm_pane = os.environ.get("WEZTERM_PANE")
    if wezterm_pane and shutil.which("wezterm"):
        fd, sentinel_raw = tempfile.mkstemp(prefix="plan-annotate-")
        os.close(fd)
        os.unlink(sentinel_raw)
        sentinel = Path(sentinel_raw)
        wrapper = (
            f"{shlex.quote(editor)} {shlex.quote(str(path))}; "
            f"touch {shlex.quote(str(sentinel))}"
        )
        launch = subprocess.run(
            [
                "wezterm",
                "cli",
                "split-pane",
                "--bottom",
                "--percent",
                "80",
                "--pane-id",
                wezterm_pane,
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
        ok = wait_for_sentinel(sentinel, SENTINEL_TIMEOUT_SECONDS)
        sentinel.unlink(missing_ok=True)
        return 0 if ok else 1

    return 1


def open_editor(path: Path) -> int:
    """Open editor with overlay first, then plain editor fallback."""
    editor = os.environ.get("EDITOR", "vi")

    if open_in_overlay(editor, path) == 0:
        return 0

    return subprocess.run([editor, str(path)]).returncode


def run_file_mode(plan_file: Path) -> int:
    """Open a temp plan copy and print unified diff if edited."""
    if not plan_file.exists():
        print(f"error: file not found: {plan_file}", file=sys.stderr)
        return 1

    original = plan_file.read_text()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", prefix="plan-review-", delete=False) as tmp:
        tmp.write(original)
        tmp_path = Path(tmp.name)

    try:
        if open_editor(tmp_path) != 0:
            print("error: editor launch failed", file=sys.stderr)
            return 1
        edited = tmp_path.read_text()
        diff = get_diff(original, edited)
        if diff:
            print(diff)
        return 0
    finally:
        tmp_path.unlink(missing_ok=True)


def run_tests() -> int:
    """Run embedded tests."""
    import unittest

    class TestDiff(unittest.TestCase):
        def test_no_changes(self) -> None:
            text = "# A\n- x\n"
            self.assertEqual(get_diff(text, text), "")

        def test_addition(self) -> None:
            diff = get_diff("a\n", "a\nb\n")
            self.assertIn("+b", diff)

        def test_modification(self) -> None:
            diff = get_diff("- a\n", "- b\n")
            self.assertIn("- a", diff)
            self.assertIn("+- b", diff)

    class TestSentinel(unittest.TestCase):
        def test_times_out(self) -> None:
            missing = Path(tempfile.gettempdir()) / "does-not-exist-sentinel"
            self.assertFalse(wait_for_sentinel(missing, 1))

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for tc in (TestDiff, TestSentinel):
        suite.addTests(loader.loadTestsFromTestCase(tc))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="plan annotation tool")
    parser.add_argument("--test", action="store_true", help="run tests")
    parser.add_argument("plan_file", nargs="?", help="path to plan file")
    args = parser.parse_args()

    if args.test:
        return run_tests()
    if not args.plan_file:
        parser.error("plan_file is required unless --test is used")
    return run_file_mode(Path(args.plan_file))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\r\033[K", end="")
        raise SystemExit(130)
