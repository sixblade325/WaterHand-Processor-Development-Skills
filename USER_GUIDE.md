# WaterHand Processor Development Skills 用户指南

适用版本：v3.0.3。

本产品采用木兰宽松许可证，第 2 版（`MulanPSL-2.0`），适用范围与再分发说明见 [README 的许可证章节](README.md#许可证)，完整条款见 [LICENSE](LICENSE)。Vivado 等外部工具及用户处理器项目遵循各自的许可证。

## 1. 加载 Skill

本仓库将处理器工程经验和能力整理为六项可复用 Skill，清单见 [skills/MANIFEST.md](skills/MANIFEST.md)。每个 Skill 目录以 `SKILL.md` 为入口，参考材料、模板和辅助脚本随对应目录维护。

按当前宿主支持的方式加载所需的完整 Skill 目录，保留其中引用的全部内容。Codex 的加载、发现和调用方式见 [OpenAI 官方 Skill 文档](https://developers.openai.com/codex/skills/)。在目标处理器项目中确认所需 Skill 已可用，再开始具体任务。

## 2. 准备项目输入

进入目标处理器项目的 Git 仓库根目录，先明确项目 `AGENTS.md`、Architecture、Design、源码和验证材料的实际位置。已有项目采用自己的路径映射和协作规则；新项目可以使用 `$bootstrap-processor-project` 建立根目录 `AGENTS.md`。

环境构建和工具配置由用户项目承担。编译、仿真、综合及实现任务使用该项目已核验的命令、工具版本和产物目录。Agent 先读取项目说明，核对命令入口与当前任务授权，再执行对应操作。

请求中应给出任务范围、权威文档、固定基线、验收标准和已有证据路径。原始日志、生成 RTL、波形和临时报告进入用户项目指定的运行产物目录。

## 3. Skill 使用方式

### 3.1 通用调用方式

在请求中显式写出 `$<skill-name>`，同时给出任务边界：

```text
使用 $<skill-name> 完成 <任务>。
权威材料：<AGENTS.md、Architecture、Design 或其他文档路径>。
修改范围：<允许修改的目录和文件>。
固定基线：<commit、DCP、报告或配置>。
验收标准：<测试、时序、文档或审查要求>。
```

Agent 会先读取目标项目中适用的 `AGENTS.md`。Skill 提供工作方法，项目文档、源码、测试和工具输出提供具体工程事实。

常见组合如下：

| 目标 | 推荐顺序 |
|---|---|
| 新项目建立协作规则和文档框架 | `$bootstrap-processor-project`，随后 `$organize-processor-docs` |
| 从架构目标形成 RTL | `$design-chisel-processor`，随后 `$implement-chisel-processor` |
| 定位并修复 FPGA 时序问题 | `$trace-vivado-timing-to-rtl`，随后 `$optimize-chisel-fpga-timing` |

### 3.2 `$bootstrap-processor-project`

用于创建精简的项目根目录 `AGENTS.md`，或将已有 `AGENTS.md` 与包内基线按职责进行比较。基线保留事实权威、授权、目录映射、已核验的工具入口和任务 Skill 索引。设计门禁、硬件规则、源码摘要和验证细则由对应 Skill 维护；通用基线不复制个人化输出风格。

新项目的默认映射见[包内基线](skills/bootstrap-processor-project/assets/AGENTS.md)：Architecture、Design、Verification 分别位于 `doc/Architecture/`、`doc/Design/`、`doc/Verification/`，文档总入口为 `doc/README.md`，源码为 `src/`，运行产物为 `.runtime/`。bootstrap 只登记这些路径，后续文档组织 Skill 在有实际内容时创建相应文档。

已有项目保留可核验的实际映射和局部约束。变更映射时须经授权，并同步项目 `AGENTS.md`、实际文档和链接。更新 Skill 后，已经写入项目的 `AGENTS.md` 继续由项目自身维护。

缺少 `AGENTS.md` 时，可以直接要求初始化：

```text
使用 $bootstrap-processor-project 初始化 <project-root> 的项目级 AGENTS.md。
保留仓库中可验证的映射和命令；缺少既有映射时采用包内默认值。
只允许修改根目录 AGENTS.md。
```

已有 `AGENTS.md` 时，先请求增量建议：

```text
使用 $bootstrap-processor-project 比较当前 AGENTS.md 与包内基线。
保留现有项目规则，先报告建议新增项、冲突和过时规则，经我确认后再修改。
```

该 Skill 的写入范围只有目标项目根目录 `AGENTS.md`。环境检查、工具安装、文档脚手架、源码和测试均不在其职责内。

### 3.3 `$organize-processor-docs`

用于渐进建立、撰写、重构或审查人类可读文档网络。新项目默认使用项目根目录 `doc/`，已有项目按其明确映射解释 Skill 中的默认路径。它提供三种模式：

| 模式 | 使用时机 | 主要结果 |
|---|---|---|
| `Bootstrap` | 项目缺少清晰文档框架，或现有材料需要归位 | 权威映射、阅读路径和必要目录 |
| `Author` | 新建或修订 Architecture、Design、Protocol、Lifecycle、ADR、Verification、Research 或 Review | 符合对应内容契约的文档 |
| `Maintain` | 拆分、合并、迁移、裁剪或审计现有文档 | 保持单一事实来源的精简文档网络 |

调用示例：

```text
使用 $organize-processor-docs 的 Bootstrap 模式整理当前项目文档。
按 AGENTS.md 中的项目映射组织文档；没有既有映射时采用 doc/ 默认布局。
建立 README 阅读入口；Design/Module 按稳定物理模块拓扑组织，并链接 Protocol、Lifecycle、ADR 和 Verification。
先列出权威归属、目标路径和需要用户决定的冲突，再实施已确定的部分。
```

涉及接口时，文档按 `Scala declaration -> semantics` 顺序解释。涉及周期精确的状态、握手、冲突优先级、flush、replay 或生命周期语义时，同时调用 `$design-chisel-processor`。修改完成后，按[文档检查](#4-文档检查)运行 Skill 自带检查器，并核对文档语义。

### 3.4 `$design-chisel-processor`

用于实现前的 Chisel 处理器微架构设计、设计审查和设计文档闭合。

```text
使用 $design-chisel-processor 设计当前 IssueQueue 的双路选择机制。
保持 Architecture 定义的对外行为和已确认模块边界。
明确每个字段的 producer、consumer、置位与清除条件、有效期、同周期优先级、寄存器边界、flush 与安全复用规则。
给出状态转换表、失败反例、断言和定向测试要求，并同步维护相关 Design 文档。
```

有效输入包括 Architecture、当前 Design、相关 RTL、参考实现、接口约束和验收目标。交付结果应区分现有实现、当前设计、参考实现和新建议，并标记缺少验证证据的判断。

### 3.5 `$implement-chisel-processor`

用于依据已经闭合的 Architecture 和 Design 实现、审查并验证 Chisel 处理器 RTL。请求中应给出真实 elaboration top、允许修改的源码范围、相关测试入口和验收标准。

```text
使用 $implement-chisel-processor 按 doc/Architecture 和 doc/Design 实现 IssueQueue。
修改范围限于指定 Scala 源码、对应测试和同目录 _codex.md。
追踪 Bundle 的定义、构造、存储、producer、consumer、宽度和端口顺序。
使用项目已核验的入口运行聚焦 Verilator 测试，报告命令、seed、周期数、结果和日志路径。
```

每个由项目维护且在任务中新增或修改的 `.scala` 文件，都必须在同目录创建或更新 `<SourceBase>_codex.md`。双 subagent 核验默认关闭。需要独立静态审查和独立测试时，在当前请求中显式加入：

```text
本任务显式开启 dual-subagent verification。
一个 subagent 只读审查源码和文档，另一个 subagent 独立运行已批准测试并保存原始证据。
```

### 3.6 `$trace-vivado-timing-to-rtl`

用于只读分析 Vivado synthesis 或 routed timing 证据，并将物理路径映射回生成 RTL、Chisel 源码和流水级语义。根据结论范围选择模式：

| 模式 | 使用时机 |
|---|---|
| `Targeted Path Trace` | 分析一个命名路径、端点、模块边界或信号族 |
| `Whole-design Timing Audit` | 判断全局收敛、限制路径族、覆盖率或优化优先级 |
| `Cross-run Comparison` | 比较两个配置可比的实现运行 |

```text
使用 $trace-vivado-timing-to-rtl 的 Targeted Path Trace 模式分析该 setup path。
DCP：<routed DCP path>；时序报告：<report path>；源码基线：<commit>。
记录 source/destination pin、clock、slack、logic/route delay、primitive、net fanout 和 hierarchy crossing。
将每段结论标记为 measured、mapped、inferred 或 unknown，保持 Design 和 RTL 只读，输出按证据排序的修改方向。
```

全局结论需要 `Whole-design Timing Audit` 的 endpoint universe 和明确的查询上限。跨运行结论需要先核对 top、part、clock、constraints、strategy、parameters、seed 和源码身份。

### 3.7 `$optimize-chisel-fpga-timing`

用于在保持周期语义的前提下修改 Chisel RTL，并通过 emitted RTL、Verilator 和 routed implementation A/B 证据验证时序效果。适用于 ready 或 admission 长路径、priority encoder、one-hot arbitration、宽 mux、高扇出控制、跨模块 predicate 和寄存器边界调整。

```text
使用 $optimize-chisel-fpga-timing 优化已定位的关键路径。
基线证据：<commit、DCP、timing report、clock constraint、strategy 和 seed>。
先冻结受影响信号的 producer、consumer、组合表达式、寄存器边界、fire、backpressure、flush、reset 和同周期更新契约。
实施最小拓扑修改，增加必要断言，检查 emitted RTL，运行聚焦 Verilator 测试，再以相同配置执行 routed A/B 比较。
```

增加流水级延迟、表项字段、接口或保守保护条件需要用户明确授权。交付结果应分别报告 D input、Q output、feedback、control 和 hold 路径，以及资源代价、剩余瓶颈和未验证判断。

## 4. 文档检查

`organize-processor-docs` 自带的[文档检查器](skills/organize-processor-docs/scripts/check_docs.py)可以独立调用。使用项目中可用的兼容 Python 解释器，以下示例以 `python` 表示；将 `<skills-root>` 和 `<project-root>` 替换为实际路径：

```text
python "<skills-root>/organize-processor-docs/scripts/check_docs.py" "<project-root>" --json
```

检查器默认发现 `doc/` 下的文档域。已有项目采用其他明确映射时，按映射重复传入自定义文档根：

```text
python "<skills-root>/organize-processor-docs/scripts/check_docs.py" "<project-root>" --root Architecture --root Microarchitecture --json
```

检查器覆盖文档链接、阅读深度、冲突标记、编码和长度预算。项目 `AGENTS.md`、文档总入口及其链接另行核对；周期语义与实现一致性继续按对应 Skill 审查。
