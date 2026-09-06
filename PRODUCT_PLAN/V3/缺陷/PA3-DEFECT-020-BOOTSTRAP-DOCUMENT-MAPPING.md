# PA3-DEFECT-020：bootstrap 与文档组织的默认目录不一致

状态：已修复并通过路径集成回归  
日期：2026-09-06

## 问题与影响

bootstrap 基线将 Architecture、Design、Verification 映射到项目顶层，文档组织 Skill 和默认检查器使用 `doc/` 下的文档域。新项目按用户指南连续调用两个 Skill，会收到两套默认路径。

修复前的确定性复现按基线映射建立三个文档域，再通过正式 CLI 调用文档检查器，返回 `legacy_top_level`，预期的 `doc` 布局断言失败。

## 修复

[bootstrap 基线](../../../skills/bootstrap-processor-project/assets/AGENTS.md) 的文档路径统一为 `doc/Architecture/`、`doc/Design/`、`doc/Verification/`。源码和运行产物路径继续为 `src/`、`.runtime/`。bootstrap 只写根目录 `AGENTS.md`，文档组织按实际内容渐进建立文档。

[文档组织 Skill](../../../skills/organize-processor-docs/SKILL.md) 明确以上路径为新项目默认值。已有项目按其明确映射解释参考材料，避免自动改写项目规则或创建平行 `doc/` 树。获授权迁移时同步规则、文档和链接。检查器不读取项目规则，自定义布局由调用者按映射传入 `--root`，总入口另行核对。

## 验证证据

`tests/test_support_kit.py` 的路径集成测试读取真实基线，建立有实际内容的最小文档网络，经 `check-docs` 返回 `layout=doc`、无问题；文档根与基线一致，`AGENTS.md` 内容保持不变，没有额外建立源码或运行目录。

全量工具测试 37 项、文档 Skill 测试 34 项全部通过，覆盖自定义根、旧布局告警、混合根拒绝、链接和入口检查。此前可选的两项真实工具链测试本次已启用并通过。

原始结果保存在 `.runtime/readme-delivery-smoke/documented-package/`：`bootstrap-fix-red.log`、`bootstrap-fix-build.json`、`bootstrap-fix-doc-tests.log`。v3.0.3 ZIP 与本地 marketplace 已按当前源文件重建；既有报告与冻结实验材料保持不变。
