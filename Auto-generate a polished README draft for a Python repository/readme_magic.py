#!/usr/bin/env python3
"""
readme_magic.py

Auto-generate a polished README draft for a Python repository.

Save in repo root and run:
    python readme_magic.py --path . --owner myuser --repo myrepo

Outputs README_generated.md (or overwrites README.md with --inplace).

MIT License (you can change it for your submission).
"""
from __future__ import annotations
import argparse
import os
import re
import ast
import textwrap
from pathlib import Path
from typing import List, Optional, Tuple

# ---------- Helpers to read common metadata ----------
def read_file(p: Path) -> Optional[str]:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return None

def detect_license(path: Path) -> Optional[str]:
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt"):
        p = path / name
        if p.exists():
            txt = read_file(p)
            if txt:
                # Pull first line as title if possible
                first = txt.strip().splitlines()[0]
                return first[:200]
    return None

def parse_requirements(path: Path) -> List[str]:
    p = path / "requirements.txt"
    if not p.exists():
        return []
    lines = []
    for raw in (p.read_text().splitlines()):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines

def parse_pyproject(path: Path) -> Tuple[Optional[str], Optional[str]]:
    p = path / "pyproject.toml"
    if not p.exists():
        return None, None
    txt = p.read_text(encoding="utf-8")
    # naive parsing for name and description (works for many projects)
    name = re.search(r'name\s*=\s*["\']([^"\']+)["\']', txt)
    desc = re.search(r'description\s*=\s*["\']([^"\']+)["\']', txt)
    return (name.group(1) if name else None, desc.group(1) if desc else None)

def parse_setup_py(path: Path) -> Tuple[Optional[str], Optional[str]]:
    p = path / "setup.py"
    if not p.exists():
        return None, None
    txt = p.read_text(encoding="utf-8")
    name = re.search(r"name\s*=\s*['\"]([^'\"]+)['\"]", txt)
    desc = re.search(r"description\s*=\s*['\"]([^'\"]+)['\"]", txt)
    return (name.group(1) if name else None, desc.group(1) if desc else None)

# ---------- Code scanning for usage snippets ----------
def find_python_files(path: Path) -> List[Path]:
    pyfiles = [p for p in path.rglob("*.py") if p.is_file() and "venv" not in p.parts and ".venv" not in p.parts]
    return pyfiles

def extract_main_examples(py: Path) -> List[str]:
    txt = read_file(py)
    if not txt:
        return []
    examples = []
    # simple search for if __name__ == "__main__"
    if "__main__" in txt:
        # Extract block after the if line (naive)
        parts = txt.splitlines()
        for i, line in enumerate(parts):
            if re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', line):
                # capture next up to 20 lines indented or not
                snippet = []
                for j in range(i+1, min(i+40, len(parts))):
                    snippet.append(parts[j])
                    # stop if we hit another top-level def/class or blank line + not indented
                    if parts[j].strip().startswith("def ") or parts[j].strip().startswith("class "):
                        break
                examples.append("\n".join(snippet).rstrip())
    return examples

def extract_top_level_functions(py: Path, limit: int = 6) -> List[Tuple[str, str]]:
    txt = read_file(py)
    if not txt:
        return []
    try:
        tree = ast.parse(txt)
    except SyntaxError:
        return []
    results = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            name = node.name
            # build tiny signature from args
            args = []
            for a in node.args.args:
                args.append(a.arg)
            sig = f"{name}({', '.join(args)})"
            # docstring
            doc = ast.get_docstring(node) or ""
            doc = doc.strip().splitlines()[0] if doc else ""
            results.append((sig, doc))
            if len(results) >= limit:
                break
    return results

# ---------- README generation ----------
BADGE_TPL = {
    "license": "https://img.shields.io/badge/license-{license}-brightgreen",
    "python": "https://img.shields.io/badge/python-3.x-blue",
    "pypi": "https://img.shields.io/pypi/v/{pkg}.svg",
    "github_workflow": "https://img.shields.io/github/actions/workflow/status/{owner}/{repo}/ci.yml",
    "stars": "https://img.shields.io/github/stars/{owner}/{repo}.svg?style=social",
}

def make_badges(owner: Optional[str], repo: Optional[str], license_name: Optional[str], pkg_name: Optional[str]) -> str:
    badges = []
    if license_name:
        label = re.sub(r"\s+", "_", license_name.split()[0])
        badges.append(f"![license]({BADGE_TPL['license'].format(license=label)})")
    badges.append(f"![python]({BADGE_TPL['python']})")
    if owner and repo:
        badges.append(f"![workflow]({BADGE_TPL['github_workflow'].format(owner=owner, repo=repo)})")
        badges.append(f"![stars]({BADGE_TPL['stars'].format(owner=owner, repo=repo)})")
    if pkg_name:
        badges.append(f"![pypi]({BADGE_TPL['pypi'].format(pkg=pkg_name)})")
    return " ".join(badges)

def short_intro(name: str, desc: Optional[str]) -> str:
    d = desc or "A useful Python project."
    return f"# {name}\n\n{d}\n"

def dependencies_section(reqs: List[str]) -> str:
    if not reqs:
        return "No pinned dependencies found. Typical install via `pip install -r requirements.txt` if provided.\n"
    lines = "\n".join(f"- `{r}`" for r in reqs[:50])
    return f"**Dependencies**\n\n{lines}\n"

def usage_block(examples: List[str], functions: List[Tuple[str,str]]) -> str:
    parts = []
    if examples:
        parts.append("## Example (from repository)\n\n```bash\n# example extracted from repo\n")
        # take first example and show trimmed version
