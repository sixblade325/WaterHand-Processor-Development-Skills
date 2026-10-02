# 正式 Skill 清单

适用版本：v3.1.0。六项 Skill 均以各自目录中的 `SKILL.md` 为入口，必要的参考材料、模板、脚本和测试随目录提供。

| Skill | 职责 |
|---|---|
| [bootstrap-processor-project](bootstrap-processor-project/SKILL.md) | 初始化或比较用户项目根目录的协作规则 |
| [organize-processor-docs](organize-processor-docs/SKILL.md) | 建立、撰写和维护处理器文档及阅读路径 |
| [design-chisel-processor](design-chisel-processor/SKILL.md) | 设计与审查周期精确的微架构机制 |
| [implement-chisel-processor](implement-chisel-processor/SKILL.md) | 根据已确认设计实现 Chisel RTL、源码说明和测试 |
| [trace-vivado-timing-to-rtl](trace-vivado-timing-to-rtl/SKILL.md) | 将物理时序证据映射到 RTL 和周期含义 |
| [optimize-chisel-fpga-timing](optimize-chisel-fpga-timing/SKILL.md) | 实施受周期契约约束的时序优化并比较结果 |

初始设计、实现和时序方法于 2026-08-29 从龙芯杯处理器开发经验中提炼，后续加入项目协作和文档组织方法。具体项目的模块、信号、源码和工程结论继续留在原项目。

新项目默认使用 `doc/` 文档布局，已有项目按自己的明确映射工作。工程环境和运行命令由用户项目维护，会话与工具调用由宿主提供。六项 Skill 的详细用法见[用户指南](../USER_GUIDE.md)。

全部正式 Skill 采用 `MulanPSL-2.0`，完整条款见 [LICENSE](../LICENSE)。
