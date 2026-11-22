"""Every text read, write and subprocess pipe in the repo's Python names its encoding.

Without `encoding=` Python decodes with the locale (cp1250 on Polish Windows), so UTF-8
from node or from files turns Polish letters into garbage and tests fail only on Windows.
Same check as ruff PLW1514 (unspecified-encoding); the repo has no ruff, so it lives here.

Features: design-system#126
Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKIP = {".git", "node_modules", ".venv"}
SUBPROCESS = {"run", "check_output", "Popen", "call", "check_call"}


def _kw(call: ast.Call, name: str) -> ast.expr | None:
    return next((k.value for k in call.keywords if k.arg == name), None)


def _true(node: ast.expr | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def _binary(mode: ast.expr | None) -> bool:
    return isinstance(mode, ast.Constant) and isinstance(mode.value, str) and "b" in mode.value


def problems(source: str) -> list[str]:
    """Returns `line: call` for every text-mode call without `encoding=`."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call) or _kw(node, "encoding") is not None:
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name in SUBPROCESS and isinstance(func, ast.Attribute):
            text = _true(_kw(node, "text")) or _true(_kw(node, "universal_newlines"))
        elif name == "open":
            mode = _kw(node, "mode") or (node.args[1] if len(node.args) > 1 else None)
            # Path.open's mode is the first argument, builtin open's the second.
            if isinstance(func, ast.Attribute) and node.args:
                mode = node.args[0]
            text = not _binary(mode)
        elif name in {"read_text", "write_text"} and isinstance(func, ast.Attribute):
            text = len(node.args) < (2 if name == "write_text" else 1)
        else:
            continue
        if text:
            found.append(f"{node.lineno}: {name}")
    return found


class TextEncoding(unittest.TestCase):
    def test_flags_text_calls_without_encoding(self) -> None:
        source = (
            "subprocess.run(['node'], text=True)\n"
            "open('a')\n"
            "Path('a').read_text()\n"
            "Path('a').write_text('x')\n"
        )
        self.assertEqual(problems(source), ["1: run", "2: open", "3: read_text", "4: write_text"])

    def test_accepts_explicit_encoding_and_binary_mode(self) -> None:
        source = (
            "subprocess.run(['node'], text=True, encoding='utf-8')\n"
            "subprocess.run(['node'], capture_output=True)\n"
            "open('a', 'rb')\n"
            "Path('a').open('wb')\n"
            "Path('a').read_text(encoding='utf-8')\n"
            "Path('a').read_bytes()\n"
        )
        self.assertEqual(problems(source), [])

    def test_repo_python_names_every_encoding(self) -> None:
        bad = []
        for path in sorted(ROOT.rglob("*.py")):
            if SKIP.intersection(path.relative_to(ROOT).parts):
                continue
            bad += [f"{path.relative_to(ROOT).as_posix()}:{p}" for p in problems(path.read_text(encoding="utf-8"))]
        self.assertEqual(bad, [], "add encoding='utf-8' to these calls")
