# WaterHand Processor Development Skills

<p align="center">
  <img src="logo.png" alt="WaterHand Processor Development Skills" width="320">
</p>

当前版本：v3.0.3。

将处理器工程经验和能力整理为可复用 Skill，扩大个人和小团队设计者的产出带宽，覆盖项目协作、文档组织、微架构设计、Chisel 实现与验证、FPGA 时序分析。当前提供六项 Skill，以及供 Codex 识别的插件元数据。

适用于处理器课程项目、科研原型和已有 Chisel 工程的增量开发。你在自己的处理器项目中提出任务，Codex 根据项目文档和这些 Skill 开展设计、修改与验证，结果保存在该项目中。

## 能完成哪些工作

| 任务 | Skill | 主要交付 |
|---|---|---|
| 建立项目协作约束 | `bootstrap-processor-project` | 精简的项目根目录 `AGENTS.md`，或已有规则的增量建议 |
| 组织与维护工程文档 | `organize-processor-docs` | 文档职责、阅读入口、事实归属和渐进式文档结构 |
| 设计与审查微架构 | `design-chisel-processor` | 周期语义、接口、状态生命周期、优先级和验证要求 |
| 实现并验证 Chisel RTL | `implement-chisel-processor` | 源码、源码旁 `_codex.md`、断言、定向测试及执行证据 |
| 分析 Vivado 时序路径 | `trace-vivado-timing-to-rtl` | 从物理路径到生成 RTL、Chisel 源码及流水级的证据映射 |
| 优化 FPGA 时序 | `optimize-chisel-fpga-timing` | 受周期契约约束的修改候选、功能验证及实现结果比较 |

例如，增加分支预测功能时，可以先整理现有取指与重定向设计，再闭合预测信息的传递、更新和失效规则，随后实现 RTL、补充定向测试并核对文档。任务输入、允许修改范围和验收要求由你提供。

Skill 的完整用法与提示词见 [用户指南](USER_GUIDE.md#3-skill-使用方式)。

## 开始使用

按当前宿主支持的方式加载所需的完整 Skill 目录。每个目录以 `SKILL.md` 为入口，其引用的 `references/`、`assets/`、`scripts/` 等内容应一并保留。Codex 的加载与调用方式见 [OpenAI 官方 Skill 文档](https://developers.openai.com/codex/skills/)。

在目标处理器项目中确认 Skill 已可用，然后提供任务、项目材料和允许修改的范围。模型访问与账户由使用者准备；编译、仿真和综合环境使用用户项目已有的工具与配置。

### 第一次调用

在已有处理器项目中，可以从一次范围明确的只读审查开始：

```text
使用 $design-chisel-processor 只读审查当前项目的取指与重定向设计。
先读取项目 AGENTS.md、相关 Architecture、Design 和源码。
追踪重定向请求的产生、寄存器边界、消费位置和失效行为。
列出设计缺口、证据路径和需要补充的定向测试，区分文档约定与已验证行为。
本次只输出审查结果。
```

新项目的协作规则初始化、文档组织、实现和时序工作流见 [用户指南](USER_GUIDE.md)。

项目级 `AGENTS.md` 保留事实权威、授权、路径和工具入口，技术方法按任务从 Skill 读取。新项目的 bootstrap 与文档组织使用一致的 `doc/` 默认布局；已有项目保留其明确映射，详见[初始化规则](USER_GUIDE.md#32-bootstrap-processor-project)。

## 产品如何与工程配合

Codex 提供会话、模型推理、上下文、文件编辑和工具调用。Skill 提供处理器工程方法、输入输出要求、典型缺陷和检查项。环境构建、工具安装、编译、仿真与综合命令由用户项目维护，Agent 依据项目已核验的入口执行授权任务。

处理器项目自身的 `AGENTS.md`、Architecture、Design、源码和验证结果决定项目事实。项目文件与 Git 历史由该项目维护，设计师负责架构取舍和结果接受。

设计审查结果需要结合项目测试和实现证据判断。处理器的功能、性能和时序由具体项目验收。Skill 自带的文档检查脚本和测试用于支持对应方法，使用方式见 [文档检查](USER_GUIDE.md#4-文档检查)。

## 仓库材料

仓库维护六项正式 Skill、各 Skill 所需的参考材料与辅助脚本、插件元数据和产品文档。修改前先读取 [AGENTS.md](AGENTS.md)，正式 Skill 清单见 [skills/MANIFEST.md](skills/MANIFEST.md)。

[V3 产品总纲](PRODUCT_PLAN/V3/PRODUCT_PLAN.md)与[产品和实验边界](PRODUCT_PLAN/V3/RUNNABLE_PRODUCT_AND_EXPERIMENT_BOUNDARY.md)定义当前产品定位、职责和实验边界。具体处理器的设计报告与工程证据继续由对应用户项目维护。

## 许可证

除另有标注的第三方材料外，本仓库的代码、Skill、模板和文档采用木兰宽松许可证，第 2 版，SPDX 标识为 `MulanPSL-2.0`。完整条款见 [LICENSE](LICENSE)。再分发时应附带许可证并保留相关声明；外部工具和用户处理器项目遵循各自的许可证。
