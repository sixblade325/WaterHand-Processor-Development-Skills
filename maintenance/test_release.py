from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from build_release import build_release
from check_release import (
    LICENSE_ID, PLUGIN_NAME, REPOSITORY, REPORT_FILES, ROOT_FILES, SKILLS,
    ReleaseError, check_release, included_path, safe_path,
)


class ReleaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        for name in ROOT_FILES | REPORT_FILES:
            self.write(name, "# Entry\n")
        self.write("LICENSE", "木兰宽松许可证，第2版\nMulan Permissive Software License, Version 2\n")
        self.write("README.md", "# Example\n\n[Guide](USER_GUIDE.md#使用)\n<img src=\"logo.png\">\n")
        self.write("USER_GUIDE.md", "# 使用\n\n[License](LICENSE)\n")
        self.write("skills/MANIFEST.md", "# Skills\n\n[License](../LICENSE)\n")
        for name in SKILLS:
            self.write(f"skills/{name}/SKILL.md", (
                f"---\nname: {name}\nlicense: {LICENSE_ID}\n"
                "description: A maintained engineering method.\n"
                "metadata:\n  short-description: A short summary\n---\n\n"
                "# Skill\n\n[Reference](references/example.md#detail)\n"
            ))
            self.write(f"skills/{name}/references/example.md", "# Detail\n")
            self.write(f"skills/{name}/agents/openai.yaml", (
                'interface:\n  display_name: "Example"\n'
                '  short_description: "A concise engineering description"\n'
                f'  default_prompt: "Use ${name} to complete the task."\n'
            ))
        self.write("skills/bootstrap-processor-project/assets/AGENTS.md", "# Rules\n")
        self.write("maintenance/check_release.py", "# checker fixture\n")
        self.write("maintenance/build_release.py", "# builder fixture\n")
        self.write(".github/workflows/check.yml", "name: Check\n")
        self.plugin = {
            "name": PLUGIN_NAME, "version": "3.1.0", "license": LICENSE_ID,
            "repository": REPOSITORY, "skills": "./skills/",
        }
        self.write_json(".codex-plugin/plugin.json", self.plugin)
        self.marketplace = {
            "name": "waterhand-skills", "plugins": [{
                "name": PLUGIN_NAME, "source": {"source": "local", "path": "./"},
            }],
        }
        self.write_json(".agents/plugins/marketplace.json", self.marketplace)

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def write_json(self, name: str, value: dict) -> None:
        self.write(name, json.dumps(value))

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args], check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return result.stdout.strip()

    def commit_fixture(self) -> str:
        self.git("init", "--quiet")
        self.git("config", "core.autocrlf", "false")
        self.git("add", ".")
        self.git("-c", "user.name=Release Test", "-c", "user.email=release-test@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "fixture")
        return self.git("rev-parse", "HEAD")

    def test_complete_release_and_optional_version(self) -> None:
        self.assertEqual(check_release(self.root)["version"], "3.1.0")
        self.assertEqual(check_release(self.root, "3.1.0")["skills"], 6)

    def test_missing_skill_and_extra_skill_are_rejected(self) -> None:
        path = self.root / "skills" / SKILLS[0]
        path.rename(path.with_name("unexpected"))
        with self.assertRaisesRegex(ReleaseError, "missing required"):
            check_release(self.root)
        path.with_name("unexpected").rename(path)
        (self.root / "skills/unexpected").mkdir()
        with self.assertRaisesRegex(ReleaseError, "exactly"):
            check_release(self.root)

    def test_missing_linked_resource_is_rejected(self) -> None:
        (self.root / "skills" / SKILLS[0] / "references/example.md").unlink()
        with self.assertRaisesRegex(ReleaseError, "missing link"):
            check_release(self.root)

    def test_frontmatter_rejects_unsupported_yaml_and_wrong_license(self) -> None:
        path = self.root / "skills" / SKILLS[0] / "SKILL.md"
        original = path.read_text()
        for changed, diagnostic in (
            (original.replace("description: A maintained engineering method.", "description: >\n  folded text"), "YAML"),
            (original.replace(LICENSE_ID, "MIT"), "name/license"),
            (original.replace(f"name: {SKILLS[0]}", "name: another-skill"), "name/license"),
            (original.replace("description: A maintained engineering method.", "description: \"\""), "description"),
        ):
            with self.subTest(diagnostic=diagnostic):
                path.write_text(changed)
                with self.assertRaisesRegex(ReleaseError, diagnostic):
                    check_release(self.root)
        path.write_text(original)

    def test_invalid_version_and_mismatch_are_rejected(self) -> None:
        for version in ("v3.1.0", "3.1", "03.1.0", "../3.1.0", 310):
            with self.subTest(version=version):
                self.write_json(".codex-plugin/plugin.json", {**self.plugin, "version": version})
                with self.assertRaisesRegex(ReleaseError, "version"):
                    check_release(self.root)
        self.write_json(".codex-plugin/plugin.json", self.plugin)
        with self.assertRaisesRegex(ReleaseError, "mismatch"):
            check_release(self.root, "3.2.0")

    def test_plugin_repository_and_marketplace_root_are_checked(self) -> None:
        self.write_json(".codex-plugin/plugin.json", {**self.plugin, "repository": "https://example.invalid/repo"})
        with self.assertRaisesRegex(ReleaseError, "repository"):
            check_release(self.root)
        self.write_json(".codex-plugin/plugin.json", self.plugin)
        self.marketplace["plugins"][0]["source"]["path"] = "../"
        self.write_json(".agents/plugins/marketplace.json", self.marketplace)
        with self.assertRaisesRegex(ReleaseError, "marketplace"):
            check_release(self.root)

    def test_unknown_ui_yaml_shape_is_diagnosed(self) -> None:
        self.write(f"skills/{SKILLS[0]}/agents/openai.yaml", "interface: {default_prompt: invalid}\n")
        with self.assertRaisesRegex(ReleaseError, "YAML UI"):
            check_release(self.root)

    def test_link_anchors_and_code_examples(self) -> None:
        self.write("README.md", (
            "# Example\n[Guide](USER_GUIDE.md#使用)\n"
            "```markdown\n[Example](missing.md#missing)\n```\n"
            "~~~text\n[Example](missing.md)\n~~~\n"
            "`[Inline example](missing.md)`\n"
            "    [Indented example](missing.md)\n"
        ))
        check_release(self.root)
        self.write("README.md", "[Guide](USER_GUIDE.md#missing)\n")
        with self.assertRaisesRegex(ReleaseError, "missing anchor"):
            check_release(self.root)

    def test_duplicate_heading_anchor_and_reference_link(self) -> None:
        self.write("USER_GUIDE.md", "# 使用\n\n# 使用\n")
        self.write("README.md", "[Guide][guide]\n\n[guide]: USER_GUIDE.md#使用-1\n")
        check_release(self.root)
        self.write("README.md", "[Guide][undefined]\n")
        with self.assertRaisesRegex(ReleaseError, "undefined"):
            check_release(self.root)

    def test_escaping_link_is_rejected(self) -> None:
        self.write("README.md", "[Outside](../outside.md)\n")
        with self.assertRaisesRegex(ReleaseError, "escapes"):
            check_release(self.root)

    def test_bootstrap_budget_counts_utf8_bytes(self) -> None:
        self.write("skills/bootstrap-processor-project/assets/AGENTS.md", "中" * 1366)
        with self.assertRaisesRegex(ReleaseError, "4096"):
            check_release(self.root)

    def test_archive_paths_and_input_allowlist(self) -> None:
        for value in ("../a", "/a", "a/../b", "a//b", "a/./b", "C:/a", "a\\b", "a\nname", "a/.. /b", "a/file:stream"):
            with self.subTest(value=value), self.assertRaises(ReleaseError):
                safe_path(value)
        for value in ("unknown/file.txt", "unknown/__pycache__/file.pyc", "report/private.txt", "skills/unknown/SKILL.md", "maintenance/old.zip"):
            with self.subTest(value=value), self.assertRaises(ReleaseError):
                included_path(value)
        for value in ("Logs/history.md", "PRODUCT_PLAN/V3/PRODUCT_PLAN.md", ".runtime/output.txt", "skills/ChiselDevelopSkillPack.zip"):
            self.assertFalse(included_path(value))

    @unittest.skipUnless(shutil.which("git"), "Git is required for snapshot build tests")
    def test_build_is_reproducible_and_reads_committed_blobs(self) -> None:
        commit = self.commit_fixture()
        self.write("README.md", "dirty tree must never enter the archive\n")
        self.write("assets/user-guide/untracked.txt", "untracked file\n")
        first = build_release(self.root, commit, Path(self.temporary.name) / "one")
        second = build_release(self.root, "HEAD", Path(self.temporary.name) / "two", "3.1.0")
        for key in ("archive", "manifest", "checksums"):
            self.assertEqual(Path(first[key]).read_bytes(), Path(second[key]).read_bytes())
        prefix = f"{PLUGIN_NAME}-3.1.0/"
        with zipfile.ZipFile(first["archive"]) as archive:
            self.assertIsNone(archive.testzip())
            self.assertTrue(all(name.startswith(prefix) for name in archive.namelist()))
            self.assertNotIn(b"dirty tree", archive.read(prefix + "README.md"))
            self.assertNotIn(prefix + "assets/user-guide/untracked.txt", archive.namelist())
        manifest = json.loads(Path(first["manifest"]).read_text())
        self.assertEqual(manifest["sourceCommit"], commit)
        self.assertEqual(manifest["archive"], f"{PLUGIN_NAME}-3.1.0.zip")
        self.assertEqual(first["sourceCommit"], commit)
        for line in Path(first["checksums"]).read_text().splitlines():
            digest, name = line.split("  ", 1)
            self.assertEqual(digest, hashlib.sha256((Path(first["archive"]).parent / name).read_bytes()).hexdigest())
        with zipfile.ZipFile(first["archive"]) as archive:
            for item in manifest["files"]:
                data = archive.read(prefix + item["path"])
                self.assertEqual(len(data), item["size"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])

    @unittest.skipUnless(shutil.which("git"), "Git is required for snapshot build tests")
    def test_build_rechecks_extracted_archive(self) -> None:
        commit = self.commit_fixture()
        with patch("build_release.check_release", wraps=check_release) as checker:
            build_release(self.root, commit, Path(self.temporary.name) / "out")
        self.assertEqual(checker.call_count, 2)
        self.assertIn("extracted", str(checker.call_args_list[1].args[0]))

    @unittest.skipUnless(shutil.which("git"), "Git is required for snapshot build tests")
    def test_build_rejects_unknown_tracked_files_and_report_extras(self) -> None:
        for name in ("unknown.txt", "report/private.txt"):
            with self.subTest(name=name):
                self.write(name, "not a release input\n")
                commit = self.commit_fixture()
                with self.assertRaisesRegex(ReleaseError, "unrecognized"):
                    build_release(self.root, commit, Path(self.temporary.name) / "out")
                self.git("rm", name)

    @unittest.skipUnless(shutil.which("git"), "Git is required for snapshot build tests")
    def test_build_excludes_historical_assets(self) -> None:
        for name in ("Logs/old.md", "PRODUCT_PLAN/old.md", ".runtime/output.txt", "skills/ChiselDevelopSkillPack.zip"):
            self.write(name, "historical material\n")
        commit = self.commit_fixture()
        result = build_release(self.root, commit, Path(self.temporary.name) / "out")
        with zipfile.ZipFile(result["archive"]) as archive:
            self.assertFalse(any("historical" in name or "ChiselDevelopSkillPack" in name or "/.runtime/" in name or "/Logs/" in name or "/PRODUCT_PLAN/" in name for name in archive.namelist()))

    @unittest.skipUnless(shutil.which("git"), "Git is required for snapshot build tests")
    def test_build_rejects_version_mismatch_without_publishing_files(self) -> None:
        commit = self.commit_fixture()
        output = Path(self.temporary.name) / "out"
        with self.assertRaisesRegex(ReleaseError, "version mismatch"):
            build_release(self.root, commit, output, "3.2.0")
        self.assertEqual(list(output.iterdir()), [])

    @unittest.skipUnless(shutil.which("git"), "Git is required for snapshot build tests")
    def test_build_rejects_gitlink_even_in_excluded_directory(self) -> None:
        commit = self.commit_fixture()
        self.git("update-index", "--add", "--cacheinfo", f"160000,{commit},.runtime/research/example")
        self.git("-c", "user.name=Release Test", "-c", "user.email=release-test@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "gitlink")
        with self.assertRaisesRegex(ReleaseError, "160000"):
            build_release(self.root, "HEAD", Path(self.temporary.name) / "out")

    @unittest.skipUnless(shutil.which("git") and os.name != "nt", "POSIX symlink fixture")
    def test_symlink_is_rejected_by_checker_and_builder(self) -> None:
        link = self.root / "assets/user-guide/linked.md"
        link.parent.mkdir(parents=True)
        link.symlink_to("../../README.md")
        with self.assertRaisesRegex(ReleaseError, "symlink"):
            check_release(self.root)
        commit = self.commit_fixture()
        with self.assertRaisesRegex(ReleaseError, "120000"):
            build_release(self.root, commit, Path(self.temporary.name) / "out")


if __name__ == "__main__":
    unittest.main()
