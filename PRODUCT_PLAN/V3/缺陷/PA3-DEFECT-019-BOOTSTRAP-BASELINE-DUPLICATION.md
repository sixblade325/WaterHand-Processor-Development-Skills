# PA3-DEFECT-019：项目 AGENTS 基线重复注入技术方法

状态：已修复并通过回归测试  
日期：2026-09-06

## 问题与影响

`bootstrap-processor-project` 的通用 `assets/AGENTS.md` 为 11,982 字节，包含设计门禁、硬件实现、源码摘要、验证检查项和个人化输出风格。技术规则同时由设计和实现 Skill 维护，复制到用户项目后又不会随插件自动升级，增加常驻上下文和规则漂移风险。

其中基线要求所有自主维护的 Scala 文件具备源码摘要，实现 Skill 的要求针对任务中新增或修改的文件，作用范围存在差异。

## 修复

基线缩减至 3,089 字节，只保留事实权威、授权、目录映射、工具入口和任务 Skill 索引。方法继续由其所属 Skill 维护，保留的防止通过扩大 stall、flush、kill 或串行化范围绕过测试的要求归入实现 Skill 的 `hardware-rules.md`。

bootstrap Skill 定义包内基线不超过 4,096 UTF-8 字节。该限制不约束用户项目自行维护的局部规则。已有项目文件保持项目所有权，升级插件不会自动覆盖。

对应权威入口为 [bootstrap Skill](../../../skills/bootstrap-processor-project/SKILL.md) 和[基线](../../../skills/bootstrap-processor-project/assets/AGENTS.md)。产品总纲、协作规则、Skill 清单和用户入口已同步。

## 验证证据

`tests/test_support_kit.py` 新增体积回归，修复前因 11,982 大于 4,096 失败，修复后通过。全量工具测试 37 项通过，文档 Skill 测试 34 项通过，全部正式 Skill 结构校验通过。

原始结果保存在 `.runtime/readme-delivery-smoke/documented-package/`：`bootstrap-fix-red.log`、`bootstrap-fix-build.json`、`bootstrap-fix-doc-tests.log`、`bootstrap-fix-validation.json`。本次保留既有报告和冻结实验材料。
