# Processor Agent Skills

适用版本：v3.0.3。

Generated: 2026-09-03

## Available Skills

Each directory contains a `SKILL.md` entrypoint.

本清单中的全部 Skill 采用木兰宽松许可证，第 2 版（`MulanPSL-2.0`）。许可证全文见仓库根目录 [LICENSE](../LICENSE)；每个 Skill 的 frontmatter 同步声明该标识。

- `bootstrap-processor-project`
- `design-chisel-processor`
- `implement-chisel-processor`
- `organize-processor-docs`
- `optimize-chisel-fpga-timing`
- `trace-vivado-timing-to-rtl`

## Notes

- The initial processor implementation and timing Skills were extracted from the LoongArch Cup legacy bundle on 2026-08-29.
- `bootstrap-processor-project` creates or safely compares one user-owned project-root `AGENTS.md`, limited to authority, authorization, path mapping, verified tool entrypoints, and task-Skill routing. Technical methods remain in their owning Skills; the user project maintains its environment, toolchain, and verified tool entrypoints.
- `organize-processor-docs` is a stateless Skill for a human-first processor documentation network, evidence, and review. Its new-project `doc/` default matches the bootstrap baseline; existing approved project mappings take precedence in both Skills.
- Its Bootstrap, Author, and Maintain workflows use a Design directory axis aligned with physical Chisel or RTL module topology, target-budget warnings, configurable provisional hard thresholds, two-link Architecture and Design navigation checks, encoding diagnostics, and separate handling for explanatory diagrams and evidence captures.
- Project-specific facts remain in the legacy project and user projects.
- Generated caches are excluded.
- Agent sessions, task execution, and tool calls remain Agent Runtime responsibilities. Skills do not maintain Harness workflow state.
