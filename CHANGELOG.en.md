# Changelog

[中文](CHANGELOG.md) | English

## 3.1.2 · 2026-10-23

- Move both user guides, contribution guides, and supporting media into `docs/`, with Chinese and English documentation indexes.
- Update relative links, repository rules, the release file list, and layout tests. All six Skill directories remain unchanged.

## 3.1.1 · 2026-10-23

- Add English editions of the README, user guide, contribution guide, changelog, and media notes, with links between the language editions.
- Add English examples and image captions while retaining the original Chinese screenshots, animation, and historical PDFs.
- Include English documents in the release file list and test missing translations, broken links, and archive contents.
- Keep all six Skill directories byte-for-byte identical to v3.1.0, including methods, references, templates, scripts, tests, and UI metadata. The bootstrap template's Chinese language default is unchanged.

This release adds bilingual public documentation. It does not introduce a host-interface language switch or establish equivalent model behavior across languages. Historical processor experiments were not rerun.

## 3.1.0 · 2026-10-03

The public package centers on six complete Skills. Their methods retain the state they had at the start of that release preparation.

- Rewrite the project introduction and user guide with project-local installation steps, examples for all six Skills, actual screenshots, and a short animation.
- Remove the Windows Execution Support Kit and its installation, environment adaptation, and execution entrypoints. User projects maintain engineering tools.
- Keep product plans, logs, research copies, and historical archives local. Retain three competition report PDFs publicly.
- Update the plugin version and repository URL. Add a repository marketplace, contribution instructions, and issue templates.
- Add public-file checks, deterministic release builds, SHA-256 checksums, and cross-platform CI.
- Add timing report extractor tests for parsing, filtering, output formats, and failure paths. Fix the summary displaying a blank value for zero logic levels.

Competition reports describe their historical versions. Interpret Windows tools and experimental conditions according to each report's date. Release validation covers Skill resources, Python scripts, and packaging. Historical processor experiments were not rerun during that release.
