#!/usr/bin/env python3
"""Validate the maintained Skill release without installing tools or using a network."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


SKILLS = (
    "bootstrap-processor-project",
    "design-chisel-processor",
    "implement-chisel-processor",
    "optimize-chisel-fpga-timing",
    "organize-processor-docs",
    "trace-vivado-timing-to-rtl",
)
PLUGIN_NAME = "processor-development-skills"
REPOSITORY = "https://github.com/sixblade325/WaterHand-Processor-Development-Skills"
LICENSE_ID = "MulanPSL-2.0"
ROOT_FILES = frozenset({
    "README.md", "USER_GUIDE.md", "LICENSE", "logo.png", "CHANGELOG.md",
    "CONTRIBUTING.md", "AGENTS.md", ".gitignore",
})
REPORT_FILES = frozenset({
    "report/作品简介.pdf", "report/设计文档.pdf", "report/实验补充说明.pdf",
})
PREFIXES = (".codex-plugin/", ".agents/plugins/", "assets/user-guide/", "maintenance/", ".github/")
EXCLUDED_ROOTS = {"Logs", "PRODUCT_PLAN", ".runtime"}
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
VERSION_RE = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\Z")
LINK_RE = re.compile(r'!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[\"\'][^\n]*?[\"\'])?\s*\)')
REF_DEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)", re.MULTILINE)


class ReleaseError(ValueError):
    """An input cannot form this project's release."""


def safe_path(value: str) -> PurePosixPath:
    if not value or "\\" in value or ":" in value or any(ord(c) < 32 for c in value):
        raise ReleaseError(f"unsafe release path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or re.match(r"^[A-Za-z]:", value) or any(
        part in {"", ".", ".."} or part.endswith((".", " ")) for part in value.split("/")
    ):
        raise ReleaseError(f"unsafe release path: {value!r}")
    return path


def included_path(value: str) -> bool:
    path = safe_path(value)
    if path.parts[0] in EXCLUDED_ROOTS or value == "skills/ChiselDevelopSkillPack.zip":
        return False
    allowed = (
        value in ROOT_FILES or value in REPORT_FILES or value == "skills/MANIFEST.md"
        or value.startswith(PREFIXES)
        or any(value.startswith(f"skills/{name}/") for name in SKILLS)
    )
    if not allowed:
        raise ReleaseError(f"unrecognized release input: {value}")
    if any(part in CACHE_PARTS for part in path.parts) or path.suffix in {".pyc", ".pyo"}:
        return False
    if path.suffix.lower() == ".zip":
        raise ReleaseError(f"nested archive is not a release input: {value}")
    return True


def validate_version(value: object) -> str:
    if not isinstance(value, str) or not VERSION_RE.fullmatch(value):
        raise ReleaseError(f"version must be numeric MAJOR.MINOR.PATCH without leading zeros: {value!r}")
    return value


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ReleaseError(f"cannot read UTF-8 text {path}: {error}") from error


def read_object(path: Path) -> dict:
    try:
        result = json.loads(read_text(path))
    except json.JSONDecodeError as error:
        raise ReleaseError(f"invalid JSON {path}: {error}") from error
    if not isinstance(result, dict):
        raise ReleaseError(f"JSON object required: {path}")
    return result


def yaml_scalar(value: str, location: str) -> str:
    """Accept the single-line scalar forms used by the maintained Skill files."""
    if not value or value[0] in "|>{[&*!" or " #" in value:
        raise ReleaseError(f"unsupported YAML scalar at {location}; use a single-line string")
    if value.startswith('"'):
        try:
            result = json.loads(value)
        except json.JSONDecodeError as error:
            raise ReleaseError(f"invalid quoted YAML scalar at {location}") from error
        if not isinstance(result, str):
            raise ReleaseError(f"string required at {location}")
        return result
    if value.startswith("'"):
        if not value.endswith("'"):
            raise ReleaseError(f"unterminated YAML scalar at {location}")
        return value[1:-1].replace("''", "'")
    if re.search(r":\s", value) or value in {"null", "true", "false", "~"}:
        raise ReleaseError(f"unsupported YAML scalar at {location}; quote this string")
    return value


def frontmatter(text: str, location: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        raise ReleaseError(f"missing frontmatter: {location}")
    result = {}
    metadata = False
    for line in lines[1:lines[1:].index("---") + 1]:
        if not line:
            continue
        if line == "metadata:" and "metadata" not in result:
            result["metadata"] = ""
            metadata = True
            continue
        match = re.fullmatch(r"(  )?([a-z][a-z-]*): (.+)", line)
        if not match:
            raise ReleaseError(f"unsupported YAML frontmatter at {location}: {line!r}")
        indent, key, value = match.groups()
        if indent:
            if not metadata or key != "short-description":
                raise ReleaseError(f"unsupported YAML metadata at {location}: {line!r}")
            key = "metadata." + key
        else:
            metadata = False
            if key not in {"name", "description", "license"}:
                raise ReleaseError(f"unsupported YAML key at {location}: {key}")
        if key in result:
            raise ReleaseError(f"duplicate YAML key at {location}: {key}")
        result[key] = yaml_scalar(value, location)
    return result


def ui_metadata(text: str, location: str) -> dict[str, str]:
    lines = [line for line in text.splitlines() if line]
    if not lines or lines[0] != "interface:":
        raise ReleaseError(f"unsupported YAML UI metadata at {location}; expected interface mapping")
    result = {}
    keys = {"display_name", "short_description", "default_prompt"}
    for line in lines[1:]:
        match = re.fullmatch(r"  ([a-z_]+): (.+)", line)
        if not match or match[1] not in keys or match[1] in result:
            raise ReleaseError(f"unsupported or duplicate YAML UI field at {location}: {line!r}")
        result[match[1]] = yaml_scalar(match[2], location)
    if set(result) != keys or any(not value.strip() for value in result.values()):
        raise ReleaseError(f"missing or empty YAML UI field at {location}")
    return result


def without_code(text: str) -> str:
    lines = []
    fence = ""
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = ""
            lines.append("")
        elif marker:
            fence = marker[1]
            lines.append("")
        elif line.startswith("    ") or line.startswith("\t"):
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    content = without_code(text)
    found = set(re.findall(r'<(?:a|span)\b[^>]*\b(?:id|name)=["\']([^"\']+)', content))
    counts: dict[str, int] = {}
    for title in re.findall(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", content, re.MULTILINE):
        title = html.unescape(re.sub(r"<[^>]*>", "", title)).lower()
        slug = "".join(c for c in title if c in " -_" or unicodedata.category(c)[0] in "LNM")
        slug = slug.replace(" ", "-")
        count = counts.get(slug, 0)
        found.add(f"{slug}-{count}" if count else slug)
        counts[slug] = count + 1
    return found


def link_targets(text: str) -> list[str]:
    content = without_code(text)
    content = re.sub(r"(`+).*?\1", "", content)
    targets = [match[1] for match in LINK_RE.finditer(content)]
    definitions = {match[1].casefold(): match[2] for match in REF_DEF_RE.finditer(content)}
    targets.extend(definitions.values())
    for label, reference in re.findall(r"!?\[([^\]]*)\]\[([^\]]*)\]", content):
        name = (reference or label).casefold()
        if name not in definitions:
            raise ReleaseError(f"undefined Markdown reference: {name}")
    targets.extend(re.findall(r'<(?:img|a)\b[^>]*\b(?:src|href)=["\']([^"\']+)', content))
    return [html.unescape(target.strip("<>")) for target in targets]


def check_links(root: Path, files: list[Path]) -> None:
    for file in files:
        if file.suffix.lower() != ".md":
            continue
        for target in link_targets(read_text(file)):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                if parts.scheme.lower() in {"file"} or re.match(r"^[A-Za-z]:", target):
                    raise ReleaseError(f"local absolute link in {file.relative_to(root)}: {target}")
                continue
            relative = unquote(parts.path)
            if "\\" in relative or relative.startswith("/"):
                raise ReleaseError(f"invalid relative link in {file.relative_to(root)}: {target}")
            destination = (file.parent / relative).resolve() if relative else file
            if not destination.is_relative_to(root):
                raise ReleaseError(f"link escapes release in {file.relative_to(root)}: {target}")
            if not destination.exists():
                raise ReleaseError(f"missing link in {file.relative_to(root)}: {target}")
            if parts.fragment and destination.suffix.lower() == ".md":
                if unquote(parts.fragment) not in anchors(read_text(destination)):
                    raise ReleaseError(f"missing anchor in {file.relative_to(root)}: {target}")


def check_release(root: Path, expected_version: str | None = None) -> dict:
    root = root.resolve()
    required = ROOT_FILES | REPORT_FILES | {
        ".codex-plugin/plugin.json", ".agents/plugins/marketplace.json", "skills/MANIFEST.md",
        "skills/bootstrap-processor-project/assets/AGENTS.md",
        "maintenance/check_release.py", "maintenance/build_release.py",
    }
    required |= {f"skills/{name}/{leaf}" for name in SKILLS for leaf in ("SKILL.md", "agents/openai.yaml")}
    missing = sorted(name for name in required if not (root / name).is_file())
    if missing:
        raise ReleaseError("missing required release files: " + ", ".join(missing))
    skill_dirs = {path.name for path in (root / "skills").iterdir() if path.is_dir() and path.name not in CACHE_PARTS}
    if skill_dirs != set(SKILLS):
        raise ReleaseError(f"Skill directories must be exactly {', '.join(SKILLS)}; found {sorted(skill_dirs)}")
    files = []
    for name in sorted(ROOT_FILES | REPORT_FILES | {"skills/MANIFEST.md"}):
        files.append(root / name)
    for prefix in (*PREFIXES, *(f"skills/{name}/" for name in SKILLS)):
        directory = root / prefix
        if directory.is_symlink():
            raise ReleaseError(f"symlink in release: {prefix}")
        if directory.is_dir():
            for path in sorted(directory.rglob("*")):
                if path.is_symlink():
                    raise ReleaseError(f"symlink in release: {path.relative_to(root)}")
                if path.is_file() and included_path(path.relative_to(root).as_posix()):
                    files.append(path)
    for path in files:
        relative = path.relative_to(root)
        has_link = any((root.joinpath(*relative.parts[:index])).is_symlink() for index in range(1, len(relative.parts) + 1))
        if has_link or not path.resolve().is_relative_to(root):
            raise ReleaseError(f"symlink or escaping release file: {path}")
    plugin = read_object(root / ".codex-plugin/plugin.json")
    version = validate_version(plugin.get("version"))
    if expected_version is not None and validate_version(expected_version) != version:
        raise ReleaseError(f"version mismatch: expected {expected_version}, plugin has {version}")
    for key, value in {"name": PLUGIN_NAME, "repository": REPOSITORY, "license": LICENSE_ID, "skills": "./skills/"}.items():
        if plugin.get(key) != value:
            raise ReleaseError(f"plugin.{key} must equal {value!r}")
    marketplace = read_object(root / ".agents/plugins/marketplace.json")
    if not isinstance(marketplace.get("name"), str) or not marketplace["name"].strip():
        raise ReleaseError("marketplace.name must be a nonempty string")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        raise ReleaseError("marketplace must contain exactly one plugin")
    if entries[0].get("name") != PLUGIN_NAME or entries[0].get("source") != {"source": "local", "path": "./"}:
        raise ReleaseError("marketplace plugin name/source must identify the root plugin at ./")
    for name in SKILLS:
        path = root / "skills" / name / "SKILL.md"
        fields = frontmatter(read_text(path), str(path.relative_to(root)))
        if fields.get("name") != name or fields.get("license") != LICENSE_ID:
            raise ReleaseError(f"Skill name/license mismatch: {name}")
        description = fields.get("description", "")
        if not description.strip() or len(description) > 1024:
            raise ReleaseError(f"Skill description must contain 1..1024 characters: {name}")
        if "[TODO:" in read_text(path):
            raise ReleaseError(f"unresolved Skill placeholder: {name}")
        ui_path = path.parent / "agents/openai.yaml"
        ui = ui_metadata(read_text(ui_path), str(ui_path.relative_to(root)))
        if f"${name}" not in ui["default_prompt"]:
            raise ReleaseError(f"Skill UI prompt must reference ${name}")
    baseline = root / "skills/bootstrap-processor-project/assets/AGENTS.md"
    if baseline.stat().st_size > 4096:
        raise ReleaseError("bootstrap AGENTS.md exceeds 4096 UTF-8 bytes")
    if "Mulan" not in read_text(root / "LICENSE") or "木兰宽松许可证" not in read_text(root / "LICENSE"):
        raise ReleaseError("LICENSE must retain the Mulan PSL v2 text")
    check_links(root, files)
    return {"version": version, "skills": len(SKILLS), "files": len(files)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--version", help="require this MAJOR.MINOR.PATCH version")
    args = parser.parse_args()
    try:
        print(json.dumps(check_release(args.root, args.version), ensure_ascii=False, sort_keys=True))
    except (ReleaseError, OSError) as error:
        print(f"release check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
