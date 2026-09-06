# V3 产品缺陷

状态：当前缺陷索引  
日期：2026-09-06

本目录记录产品开发与实验中已经取得现场证据的通用缺陷。每份缺陷摘要只保存产品责任、复现证据、影响范围、目标行为和关闭条件。处理器候选的设计错误、实验组内部实现细节和未经核验的猜测不进入本目录。

## 缺陷记录

1. [PA3-DEFECT-001：Windows Chisel 仿真入口未建立完整工具链环境](PA3-DEFECT-001-WINDOWS_CHISEL_SIM_ENV.md)，已修复并通过现场仿真验证。
2. [PA3-DEFECT-002：Windows PowerShell 默认解码破坏中文权威文档](PA3-DEFECT-002-WINDOWS-UTF8-DOC-READ.md)，产品修复已实现，待全新 Agent 会话现场验收。
3. [PA3-DEFECT-003：隔离 Codex home 的空 Memory 启动未完成上下文重建](PA3-DEFECT-003-ISOLATED-MEMORY-BOOTSTRAP.md)，已修复，run-003 已验证摘要生成、独立会话读取和两组同源隔离。
4. [PA3-DEFECT-004：Windows CMD 包装器破坏多词参数并返回伪成功](PA3-DEFECT-004-WINDOWS-CMD-ARGUMENT-FORWARDING.md)，产品与隔离实验基线均已修复，完整 acceptance 连续 10 次通过。
5. [PA3-DEFECT-005：Codex 上游 404 缺少实验运行恢复机制](PA3-DEFECT-005-UPSTREAM-404-RUN-RECOVERY.md)，现场运行已恢复，自动恢复与回归测试待实现。
6. [PA3-DEFECT-007：PowerShell 原生命令管道产生错误退出码](PA3-DEFECT-007-POWERSHELL-NATIVE-PIPELINE-EXITCODE.md)，已修复，100 次 validator 回归与 10 次完整 acceptance 均通过。
7. [PA3-DEFECT-008：候选执行环境缺少验收工具替换门禁](PA3-DEFECT-008-VALIDATOR-TOOL-SHADOWING-GUARD.md)，已修复，run-003 独立验收通过。
8. [PA3-DEFECT-009：独立组织者无法编译 Chisel verification layers](PA3-DEFECT-009-ORGANIZER-VERILATOR-INCLUDE-PATHS.md)，已修复，run-003 portable RTL snapshot 编译与仿真通过。
9. [PA3-DEFECT-010：独立组织者未固定模拟器运行时 DLL 路径](PA3-DEFECT-010-ORGANIZER-SIMULATOR-RUNTIME-PATH.md)，已修复，run-003 独立模拟器与两个 CoreMark workload 通过。
10. [PA3-DEFECT-011：organizer 冻结了易变且不可接受的原始 PATH](PA3-DEFECT-011-ORGANIZER-PATH-FREEZE-VOLATILITY.md)，run-003 与 run-004 均以隔离修订完成验收，通用冻结器待收敛。
11. [PA3-DEFECT-012：并发 Agent 争用全局 sbt boot lock](PA3-DEFECT-012-CONCURRENT-SBT-BOOT-LOCK.md)，run-003 已在 Skill 与 Control 两组复现，通用构建协调待实现。
12. [PA3-DEFECT-013：文档任务未触发文档组织 Skill](PA3-DEFECT-013-DOCUMENTATION-SKILL-SELECTION-GAP.md)，run-003 已确认未读取文档组织 Skill 或运行其检查器，Skill 选择与门禁闭环待实现。
13. [PA3-DEFECT-014：Codex 运行时状态触发 home inventory 误报](PA3-DEFECT-014-CODEX-HOME-RUNTIME-INVENTORY.md)，run-004 post 审计再次复现动态 plugin cache 误报，通用审计器待收敛。
14. [PA3-DEFECT-015：异步 Memory 写回被错误绑定到实验完成](PA3-DEFECT-015-MEMORY-POST-WRITE-CLOSURE-COUPLING.md)，已修复并通过完整回归，run-003 已按 `session_read` 门禁封存。
15. [PA3-DEFECT-016：已恢复的重连事件被误判为会话失败](PA3-DEFECT-016-RECOVERED-RECONNECT-MARKED-FATAL.md)，run-003 Control main 已复现，证据解析修复待实现。
16. [PA3-DEFECT-017：零 idle Memory 初始化把摘要归因固定在错误会话](PA3-DEFECT-017-ZERO-IDLE-MEMORY-PROBE-RACE.md)，run-004 已使用隔离兼容封存继续运行，通用修复待实现。
17. [PA3-DEFECT-018：中文交付包路径导致 Chisel 适配器编译失败](PA3-DEFECT-018-NON-ASCII-PACKAGE-RUNTIME-PATH.md)，按用户决定接受为已知限制，交付文档已声明完整 ASCII 包路径要求，不实施中文包路径适配。
