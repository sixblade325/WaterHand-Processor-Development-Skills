# Contributing

[中文](CONTRIBUTING.md) | English

This repository maintains six processor development Skills, supporting scripts, and user documentation. Before making changes, read [AGENTS.md](../AGENTS.md) (Chinese) and the affected Skill and its references.

## Issues and pull requests

In [Issues](https://github.com/sixblade325/WaterHand-Processor-Development-Skills/issues), provide the version, Skill name, task input, expected result, and actual result. For script failures, include the command, Python version, and error output. When using an example from a user project, provide enough context to explain the issue and remove private information.

For a Skill change, describe the input under which the current rule causes a problem and the scope of the proposed revision. Preserve fact ownership, designer authorization, and evidence requirements. Each Skill owns its methods; check existing responsibilities before adding rules.

A pull request should explain the problem, final changes, and validation. Script changes need tests for affected inputs, outputs, or failure paths. Documentation changes need link, image, and consistency checks against the Skill text.

## Local checks

Use Git and Python 3.10 or later. These checks use only the Python standard library. Run them from the repository root:

```sh
python maintenance/check_release.py
python -m unittest discover -s maintenance -p 'test_*.py'
python -m unittest discover -s skills/organize-processor-docs/scripts -p 'test_*.py'
python -m unittest discover -s skills/trace-vivado-timing-to-rtl/scripts -p 'test_*.py'
```

The [public-file checker](../maintenance/check_release.py) verifies plugin metadata, the six Skills, resources, and document links. [GitHub Actions](../.github/workflows/ci.yml) runs checks and tests on Linux, macOS, and Windows. They verify files, scripts, and distribution requirements. Processor functionality, physical timing, and model behavior require separate evaluation.

`Logs/`, `PRODUCT_PLAN/`, `.runtime/`, and historical Skill archives remain local to maintainers. They are excluded from these checks and release packages. `report/` publicly contains three historical delivery PDFs; source documents and layout assets remain local.

## Documentation, media, and licensing

Maintain the Chinese and English README, user guide, contribution guide, and changelog together. Keep language links working in both directions. The English guide uses the original images with English captions. The six Skill directories are shared by both editions; document translation does not require changes to their methods or language defaults.

The user guides reference media under `docs/assets/user-guide/`. The [media notes](assets/user-guide/README.en.md) record historical examples, source files, and scope. Preserve actual text when updating screenshots and explain whether an image shows input, an artifact, execution evidence, or a result summary.

New files follow the repository's [MulanPSL-2.0 license](../LICENSE). Preserve attribution and licensing when adding third-party material. Facts and source code specific to a user project stay in that project.

## Build and release

The [release builder](../maintenance/build_release.py) reads files from a specified Git commit, selects public files, produces a ZIP, `SHA256SUMS`, and `release-manifest.json`, then extracts and checks the archive. The same commit and inputs produce identical package contents. Uncommitted working-tree changes are excluded.

```sh
python maintenance/build_release.py --ref HEAD --version 3.1.2 --output .runtime/release
```

For a new release:

1. Update the version in `.codex-plugin/plugin.json`, `skills/MANIFEST.md`, and both changelogs. Update pinned-version commands in both user guides and the build examples in both contribution guides.
2. Run all checks and tests. Verify the public directory, historical report, and media scope.
3. Commit and push the changes. Confirm that CI passes for that commit, then build the release from it.
4. Create a `v<version>` tag at the same commit and attach the ZIP, checksums, and build manifest to a GitHub Release.
5. Download the public attachments and verify SHA-256 values, the source commit, extracted files, and script tests.

Release notes describe the changes, installation entrypoint, and actual validation scope. Published tags and attachments remain stable; later fixes use a new version.
