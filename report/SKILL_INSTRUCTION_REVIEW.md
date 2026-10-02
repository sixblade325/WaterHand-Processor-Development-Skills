# Skill 与 AGENTS.md 指令审查报告

审查日期：2026-09-09。审查对象：WaterHand Processor Development Skills v3.0.3。输入基线：`Gen2` 分支，`3ae9f19e8810e84dcc195ed868059a39f5e46287`。

本轮按用户提供的六类问题审查，只新增本报告。所有建议均保持提议状态，未修改 Skill、AGENTS.md、脚本或历史包。

## 1. 结论与判定边界

当前正式材料中，列出 **5 项需调整的执行措辞或重复操作、53 组应保留的指令**。类别三有 3 项，类别五有 2 项。类别一、二、四、六没有达到本轮判定门槛的当前问题。另列 4 项历史压缩包中的旧写法，以及 1 项六类之外的技术表述准确性问题。

优先处理 F01 的重复检查命令和 F02 的无条件重新生成要求。F03 至 F05 调整固定分析顺序、重复复述和普遍强制 worktree 的执行方式。现有状态生命周期、源码摘要、受影响测试、物理时序证据、用户架构决定和实验隔离要求继续保留。

“旧模型补丁”需要历史来源或行为证据。当前仓库没有提供这些条款针对某代模型而设、且在 GPT-6 Astra 上已经无效的完整对照证据，因此本报告不作这种因果断言。每项“原有目的”明确标注从文字推断的动机。需调整项依据可定位的重复代码路径、无条件措辞或执行范围问题；本轮没有证明任何硬件测试可以随模型升级取消。

用户提供的六类问题作为本轮审查框架。辅助核对的公开资料仅支持一般方法：Skill 使用简明触发信息和渐进加载，模型迁移时按实际任务校准提问与验证强度。这些公开资料不构成本仓库模型效果评测。[OpenAI Skill 文档](https://learn.chatgpt.com/docs/build-skills)，[GPT-6 Astra 指南](https://developers.openai.com/api/docs/guides/latest-model)。

当前事实依据：

- [AGENTS.md](../AGENTS.md)、[V3 产品总纲](../PRODUCT_PLAN/V3/PRODUCT_PLAN.md)和[可运行产品与实验边界](../PRODUCT_PLAN/V3/RUNNABLE_PRODUCT_AND_EXPERIMENT_BOUNDARY.md)。
- [README.md](../README.md)、[USER_GUIDE.md](../USER_GUIDE.md)、[正式 Skill 清单](../skills/MANIFEST.md)及[插件元数据](../.codex-plugin/plugin.json)。
- 六个正式 Skill 的入口、references、agents 元数据、bootstrap 模板，以及有关的四个 Python 文件。
- [ChiselDevelopSkillPack.zip](../skills/ChiselDevelopSkillPack.zip)内的四个历史 Skill。历史内容未被当作当前运行指令。

本报告是静态指令与契约审查。已核对文件内容、引用、脚本分支和历史包差异；未运行处理器仿真、Vivado、正式 A/B 或模型行为实验，未承诺任何 token、时间或缺陷率收益。

## 2. 描述与分层的逐项核对

字符数按 description 原值的 Unicode 字符计，英文词数按空白分词；主文件行数不计末尾空行。长度只作为观测值，不作为缺陷判据。

| Skill | description 字符数 | 英文词数 | SKILL.md 行数 | 判断 |
|---|---:|---:|---:|---|
| `bootstrap-processor-project` | 391 | 53 | 72 | 单文件边界明确，短模板按任务完整读取 |
| `design-chisel-processor` | 531 | 64 | 172 | 设计检查表、文档模板、实现指导已有分层 |
| `implement-chisel-processor` | 383 | 46 | 128 | 硬件规则和验证审查已在两个参考文件 |
| `organize-processor-docs` | 396 | 44 | 94 | Bootstrap/Author/Maintain 路由明确，按文档类型读参考 |
| `optimize-chisel-fpga-timing` | 565 | 69 | 152 | 四类 patterns 与案例已按实测路径选择 |
| `trace-vivado-timing-to-rtl` | 604 | 85 | 202 | 三种证据范围已分流，参考文档有模式章节 |

六份 description 均未超过本地包测试的 1024 字符检查值。design、optimize、trace 的同类名词枚举存在进一步压缩空间；本次没有实际截断或误选技能的证据，不将这些可选精简计为需调整。

本地 1024 字符检查与运行时总元数据预算属于不同约束。OpenAI 的 Skill 文档说明启动时先加载名称、描述等元数据，选中后加载主文件和需要的参考资料；技能很多时仍需检查整体描述预算。单个描述未超本地限制无法证明运行时永不截断。[OpenAI Skill 文档](https://learn.chatgpt.com/docs/build-skills)。

根 AGENTS.md 为 9663 字节，bootstrap 模板为 3089 字节。官方文档描述 AGENTS 指令有默认组合大小限制；本轮没有观察到这两个文件发生截断，也没有用文件大小推断必须删除项目规则。[OpenAI AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

## 3. 当前需调整的指令

### F01 同一检查器连续运行两次

【需调整】所属类别：五、已经过时的测试或验证要求

原文与位置：

[skills/organize-processor-docs/references/maintenance.md](../skills/organize-processor-docs/references/maintenance.md)，第 37 至 42 行：

````text
Run:

```text
python <skill-dir>/scripts/check_docs.py <project-root>
python <skill-dir>/scripts/check_docs.py <project-root> --json
```
````

[skills/organize-processor-docs/scripts/check_docs.py](../skills/organize-processor-docs/scripts/check_docs.py)，第 1012 至 1026 行：

````text
    try:
        report = check_project(
            Path(args.project),
            args.root,
            hard_limit_policy=args.hard_limit_policy,
            budget_overrides=budget_overrides,
        )
    except ValueError as error:
        parser.error(str(error))

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["ok"] and not report["issues"]:
        print(
            f"OK: checked {report['filesChecked']} Markdown files in "
````

原有目的：从措辞推断，原作者希望同时取得便于人阅读和机器处理的检查结果。没有证据表明这来自某一代模型的能力缺陷。

标记理由：两条命令只有 --json 不同。脚本先执行同一个 check_project，再按参数选择输出格式；第二次运行重复读取和检查同一批输入，未增加独立验证。问题由代码路径直接证实，与模型版本无关。

处理建议：把两条命令明确写成任选一种输出格式。需要保存结构化结果时运行 --json 一次；确需两种展示时复用该次结果。保留检查器、检查范围、退出码与项目自定义路径要求。

### F02 使用已绑定基线的 RTL 证据前无条件重新生成

【需调整】所属类别：五、已经过时的测试或验证要求

原文与位置：

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 45 至 47 行：

````text
Regenerate RTL before using it as evidence, and before delivery when generated
RTL is part of acceptance. Record the elaboration top, source set, command, and
output location; stale generated output is not evidence for current source.
````

[skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md)，第 31 至 34 行：

````text
2. Identify source revision, dirty state, parameters, top, device, Vivado version, clocks, constraints, strategies, directives, seed, DCP path, and DCP hash.
3. Treat an implementation run as immutable evidence. Compare source hashes with its manifest before semantic mapping.
4. If source drifted, map through the run snapshot, generated RTL, routed netlist, and DCP. Mark current-source correspondence as unverified.
5. Prefer routed DCP evidence. Use post-place, post-synth, emitted RTL, or source only for questions that evidence level can answer.
````

原有目的：从措辞推断，目的是防止 Agent 把陈旧生成物误当作当前源码的实现证据。无法证明这条证据新鲜度要求已经因模型升级而失效。

标记理由：“before using it as evidence”没有区分本次源码修改后的产物、已验证的相同输入产物和历史运行证据。只读审查已冻结报告时，重新生成不能替代原始运行证据；相同源码、参数、工具版本且已有身份绑定的产物也会被要求再次生成。trace Skill 已明确采用不可变运行与源码哈希核对。

处理建议：改为先核对源码、配置、工具版本、生成命令及产物身份。输入有变、绑定缺失或验收明确要求重新生成时执行；证据与目标基线一致时允许复用。保留“生成 RTL 属于交付验收时必须满足验收”和禁止使用陈旧产物证明当前源码的要求。

### F03 单机制分析强制固定九步顺序

【需调整】所属类别：三、操作步骤过于僵化

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 27 至 39 行：

````text
## Analyze one mechanism

Use this order:

1. Define every field and signal.
2. State producer, consumer, set condition, clear condition, valid interval.
3. State same-cycle priority.
4. Draw combinational work and register boundaries by cycle.
5. Enumerate normal, miss, nack, kill, flush, replay, retry, and late-response paths.
6. Check slot reuse and stale ownership.
7. Give a concrete counterexample cycle for each defect.
8. Derive assertions.
9. Evaluate critical path, fanout, ports, storage mapping, code size, and verification cost.
````

原有目的：从措辞推断，目的是避免分析遗漏字段、生命周期、周期冲突和实现成本。未找到把该固定顺序绑定到旧模型缺陷的历史证据。

标记理由：“Use this order”将分析维度写成唯一顺序。已有明确反例的追问、单个同周期优先级问题或已有完整状态表的设计讨论，仍会被要求从所有字段开始到代码规模和物理成本结束。字段定义先于依赖它的证明具有必要性，其余完整重走和呈现顺序缺少同样的数据依赖。

处理建议：改为按当前问题选用分析维度，复用已核验且未变化的语义；完整机制设计仍需覆盖适用的状态、生命周期、异常路径和成本。保留实际缺陷的具体周期反例，以及状态和身份保护的证明义务。

### F04 每次沟通先复述当前设计

【需调整】所属类别：三、操作步骤过于僵化

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 165 至 172 行：

````text
## Communicate

- Start by restating the current design accurately.
- Report correctness defects before optimizations.
- Give exact cycle examples.
- Mark unverified statements as hypotheses.
- Say explicitly when no new defect was found.
- Avoid replacing the design with a familiar external architecture without authorization.
````

原有目的：从措辞推断，目的是防止 Agent 尚未理解用户方案就提出替代设计。没有证据表明该问题仅存在于旧模型。

标记理由：理解并准确引用现有设计持续必要；把复述规定为所有回答的开头，会在同一方案的连续短问答中重复已经明确的信息。该输出步骤不产生新的设计证据，也未被根 AGENTS.md 规定为团队交付格式。

处理建议：将复述限定为设计存在歧义、初次综合审查、用户要求复述或纠正误解时。其他回答直接给出所问结论和相关依据。保留缺陷优先、具体周期、假设标记和不擅自替换架构的要求。

### F05 所有文档候选修改都使用隔离 worktree

【需调整】所属类别：三、操作步骤过于僵化

原文与位置：

[skills/organize-processor-docs/references/design.md](../skills/organize-processor-docs/references/design.md)，第 96 至 98 行：

````text
## Current Design and rationale

Current Design states how the processor works now. Design ADRs state why a concrete mechanism was chosen. Candidate changes edit the current documents in an isolated worktree; approved content replaces the current version without creating `FinalDesign`, `DesignV2`, or backup trees.
````

原有目的：从措辞推断，目的是隔离候选修改、保护当前正式文档并避免备份目录并存。没有充分材料证明所有普通文档修改都需要这种隔离。

标记理由：句子把 isolated worktree 写成每次候选修改的统一载体。已授权的单文件修订、当前工作树内已隔离的任务与并行方案实验需要的隔离强度不同。V3 的实验隔离约束适用于正式实验；已读当前权威材料未另行要求所有文档候选都新建 worktree。

处理建议：保留在当前权威文档上形成可审查 diff、Git 管理历史及禁止备份树。worktree 作为并行方案、工作树冲突、实验协议或用户明确要求时采用的执行选择。无需为普通已授权编辑增加强制隔离步骤。

## 4. 当前应当保留的指令

以下按相同目的合并为指令组。一个组可以覆盖同一契约在入口、模板和参考文件中的必要重述；文件覆盖表列出每份文件对应条目。“应保留”指所引约束在当前产品中仍有用途，未对所有示例参数或每一种处理器配置作功能验证。

### K01 用户决定、只读范围与现有资产

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 5 至 6 行：

````text
1. 用户对当前任务的明确指令决定任务目标、授权范围和交付形式。
2. 用户明确作出的决定与当前 Git 权威材料共同构成正式依据。用户后续的一般表述视为修改意图。只有用户明确声明替换既有事实时，才更新正式事实。
````

[AGENTS.md](../AGENTS.md)，第 16 至 19 行：

````text
12. Agent 的建议、草案、默认项和推断均不等于用户决定，不得标记为已确认或已批准。
13. 回答、解释、Review 和诊断任务默认只读。用户明确要求修改、实现、运行或发布时，才执行对应写入或外部操作。
14. 不扩大用户授权范围。写权限、外部副作用、破坏性操作或架构取舍不明确时，先取得用户授权。
15. 现有工作树修改属于用户资产。保留无关修改，不使用破坏性 Git 命令清除或覆盖它们。
````

保留理由：这些条款规定事实权威、写入授权和用户资产归属。审查请求授权审查，后续明确要求文档交付才授权新增报告；已明确授权的范围可直接执行。模型能力变化不会消除这些边界。

### K02 按直接相关范围读取上下文

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 7 至 9 行：

````text
3. 回答问题、Review、诊断或修改前，先读取直接相关的计划、文档、源码、测试和本地协作约束。
4. 未完成相关材料读取和证据核对时，不输出确定性技术结论。无法核验时，直接说明缺少的文件、代码路径、工具输出或输入条件。
5. 明确区分当前已实现行为、当前正式计划、实验结果、历史材料和新建议。
````

[skills/bootstrap-processor-project/assets/AGENTS.md](../skills/bootstrap-processor-project/assets/AGENTS.md)，第 9 行：

````text
3. 回答或修改前读取直接相关的项目约束、文档、源码和测试。区分设计意图、已实现行为和验证结论；无法核验时列明证据缺口。
````

保留理由：两处都限定为“直接相关”。没有要求每个微小改动重读整个仓库，也没有要求已经核验且未变化的内容重复读取。应保留项目事实核对，类别四未据此判为问题。

### K03 中文、表达规范和 PowerShell UTF-8

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 10 至 15 行：

````text
6. 回答和人类可读文档默认使用中文。模块名、信号名、字段名、文件名、命令和代码保持英文。
7. Windows PowerShell 读取 UTF-8 文档时必须使用 `Get-Content -Raw -Encoding utf8 -LiteralPath <path>` 或 `scripts\read-text.cmd <path>`，不得依赖默认编码。
8. 永远不要使用先否定 A 再转折替换为 B 的中文对照句式。不要出现破折号。
9. 不使用先模糊认可再转折纠错的套话。发现错误时直接说明位置、证据和影响。
10. 回答保持客观、直接，零吹捧，零情绪。
11. 除非用户明确要求状态，否则不发送中途状态回报，不描述正在执行或将要执行的动作。完成后直接交付结果。
````

保留理由：语言、句式和沟通频率属于明确团队偏好；UTF-8 读取规定对应 Windows PowerShell 的实际编码边界。本轮执行仍受会话中更高优先级指令约束，仓库规则自身无需因模型升级删改。

### K04 V3 产品职责与历史材料地位

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 23 至 28 行：

````text
1. 本仓库维护 WaterHand Processor Development Skills、Codex plugin manifest、环境与工具链契约、确定性脚本、工具级测试、发布材料和产品计划。
2. 产品依赖 Codex 提供会话、上下文、文件编辑、工具调用和 Agent 执行能力。
3. 当前产品不维护独立 Harness、Stage、Task、Run、Approval、Agent Executor 或第二份处理器模型。
4. 具体处理器的 Architecture、Design、Source、Verification 和工程结论进入对应用户项目。
5. 龙芯杯、WaterHand、LoongArch、Zircon 和其他项目材料只作为来源或案例。通用产品中不复制其源码、设计正文和项目专属事实。
6. A/B 对照、最小处理器示例和行为 eval 属于实验资产，不构成可运行产品的必需部分。
````

[AGENTS.md](../AGENTS.md)，第 32 至 38 行：

````text
1. `PRODUCT_PLAN/V3/PRODUCT_PLAN.md` 是当前产品总纲，维护产品定位、职责边界、Skill 体系和验收标准。
2. `PRODUCT_PLAN/V3/RUNNABLE_PRODUCT_AND_EXPERIMENT_BOUNDARY.md` 定义可运行产品、Execution Support Kit 和实验资产的边界。
3. `PRODUCT_PLAN/V3/SKILL_PACKAGE_COMPARATIVE_EVALUATION.md` 定义当前 A/B 对照评测协议。具体运行状态由对应 readiness、precheck 和证据文件表达。
4. `README.md` 是产品入口，`USER_GUIDE.md` 是用户操作入口。安装、命令或 Skill 使用方式变化时同步更新相应入口。
5. `skills/<name>/SKILL.md` 定义对应正式 Skill 的方法、输入、输出、权限边界和门禁。`skills/MANIFEST.md` 维护正式 Skill 清单。
6. `environment/README.md` 与 `environment/toolchains.json` 定义当前环境和工具链契约。
7. `PRODUCT_PLAN/V2/`、`PRODUCT_PLAN/V1/`、`Logs/` 和其他历史材料保留设计过程，不指导当前实现，除非 V3 权威文档明确引用其结论。
````

保留理由：产品维护 Skill、插件、确定性脚本和契约；具体处理器事实进入用户项目。V3 是当前权威，旧计划和实验资产具有明确范围。保留可避免沿用历史 Harness 架构。

### K05 规范性事实归属与用户项目映射

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 40 至 41 行：

````text
9. 同一规范性事实只在一个权威文档中完整定义，其他位置使用摘要和链接。
10. 新建议必须标明提议状态。实验观察必须绑定运行、时间、输入基线和证据路径。
````

[AGENTS.md](../AGENTS.md)，第 45 至 51 行：

````text
1. 框架读取用户项目时，先读取该项目的 `AGENTS.md`。
2. 项目内 Architecture 和 Design 决定实现约束，框架默认值不能覆盖项目事实。
3. 框架只通过明确接口读写用户项目，不依赖本机绝对路径。
4. 通用逻辑不得硬编码 `dual_issue_demo` 或龙芯杯项目的模块名、信号名和流水级。
5. 用户项目的人类可读文档默认使用中文，模块名、信号名、字段名、文件名、命令和代码保持英文。
6. 新项目缺少 `AGENTS.md` 时，可以依据 `bootstrap-processor-project` 基线生成严格协作约束。已有 `AGENTS.md` 默认保留，增量修改需要用户确认。
7. 用户项目的 Architecture、Design、Source 和 Verification 始终由该项目及其 Git 历史维护。Skill Package 不生成可覆盖它们的平行权威表示。
````

保留理由：单一事实权威、项目 AGENTS 优先、禁止硬编码案例项目和保留既有映射是长期产品边界。已有 AGENTS 的增量修改需要授权，已给出的授权可以沿用。

### K06 Skill 验证、发布契约与许可证

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 55 至 65 行：

````text
1. 每个正式 Skill 使用独立目录，并以 `SKILL.md` 为入口。一个正式 Skill 只保留一份。
2. Skill 描述可复用方法、输入、输出、权限边界、门禁、检查项和必要参考材料。
3. 项目专属事实、源码摘录、临时搜索结果和运行日志不得进入 Skill。
4. 从遗产提炼 Skill 时，先区分通用规则与具体项目规则，并保留来源和验证依据。
5. 修改 Skill 后运行 `scripts\run.cmd validate-skills`，执行受影响的测试，并记录受影响的工作流。
6. Skill 的公开调用方式或职责边界变化时同步更新 `README.md`、`USER_GUIDE.md` 和 `skills/MANIFEST.md` 中的相关内容。
7. 安装包只包含运行所需的 plugin、Skill、工具、环境契约、脚本和用户文档。产品计划、日志、测试、缓存和实验运行结果不得进入正式安装包。
8. `bootstrap-processor-project` 只创建或提议更新用户项目根目录 `AGENTS.md`，基线只保留事实权威、授权、目录映射、工具入口和任务 Skill 索引。技术方法由对应 Skill 维护。新项目默认映射与 `organize-processor-docs` 一致，已有项目映射继续有效。环境和工具链工作由确定性脚本承担。
9. `organize-processor-docs` 负责信息架构和写作约束。周期精确语义由 `design-chisel-processor` 负责。
10. `implement-chisel-processor` 要求同步维护源码旁 `_codex.md`。双 subagent 核验默认关闭，只在用户明确要求时开启。
11. 本仓库许可证以根目录 `LICENSE` 为准，统一标识为 `MulanPSL-2.0`。插件、Skill、安装包元数据和发布文档保持一致；保留第三方材料、外部工具及用户项目各自的许可证归属。
````

保留理由：这些要求维护正式 Skill 唯一性、受影响测试、公开入口同步和安装包组成。MulanPSL-2.0 及第三方归属是发布事实。源码摘要和双 subagent 默认关闭在 K25、K28 细查。

### K07 Windows 环境、脚本与全局变更权限

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 69 至 75 行：

````text
1. 当前产品运行环境固定为纯 Windows x86-64。MSYS2 UCRT64 只作为 Windows 内部工具链。
2. 用户初始化的统一入口是 `scripts\initialize.cmd`。环境诊断使用 `scripts\doctor.cmd`，Chisel 命令使用 `scripts\chisel-run.cmd`。
3. 脚本负责工具探测、参数转发、进程级环境、结构化结果、退出码和运行产物位置。Agent 负责选择操作并解释证据。
4. 环境变量或工具没有进入 `PATH` 时，使用已声明的 `PROCESSOR_SKILLS_*` 配置接口。通用逻辑不写入用户名、本机工具绝对路径或临时盘符。
5. 未经用户明确授权，不修改全局 `PATH`、系统包、WSL、Vivado 许可证或仓库外工具安装。
6. 脚本修改必须有对应测试。命令转发、编码、路径、退出码或工具探测变化需要覆盖 Windows 边界条件。
7. 原始日志、缓存、生成文件、临时工作树和一次性产物进入仓库或用户项目指定的 `.runtime/`。
````

保留理由：当前产品限定 Windows x86-64，工具入口和 PROCESSOR_SKILLS_* 是公开契约。命令转发、编码、退出码等边界测试有实际回归价值。全局 PATH、系统工具和许可证变更具有仓库外副作用。

### K08 实验冻结、组间隔离和证据保留

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 79 至 85 行：

````text
1. 实验资产验证产品效果，不得把一次实验的处理器事实或临时绕行写入通用 Skill 和产品主线。
2. 正式 A/B 运行使用冻结的 baseline、prompt、`RUN_CONFIG`、Skill Package、Memory 起点、工具链和验收器。
3. Skill 与 Control 使用独立 repository、Codex home、Memory、日志和结果目录。两组不得读取彼此的会话、工作树、决定和结果。
4. 正式实验线程只在用户明确要求后启动。Skill 组结果完成封存并取得用户确认后，才允许启动 Control 组。
5. 人类干预进入对应正式 thread，并按连续语义主题归档。基础设施恢复与技术设计干预分开记录，技术干预对对照有效性的影响必须在结果中披露。
6. 运行中发现产品缺陷时，将通用问题记录到 `PRODUCT_PLAN/V3/缺陷/`。实验专属修复留在隔离实验目录，避免扩大产品主线。
7. 未经用户确认，不清理、覆盖或复用既有实验运行证据。
````

保留理由：这些规则维护 A/B 对照有效性与运行证据归属。启动正式实验、Control 组门禁和删除证据的权限持续有效，本轮审查没有启动任何实验。

### K09 变更范围、抽象说明与交付证据

【应保留】

原文与位置：

[AGENTS.md](../AGENTS.md)，第 89 至 94 行：

````text
1. 修改范围保持在当前功能涉及的模块内。发现相邻问题时记录为未解决问题。
2. 新增目录、Schema、状态或抽象前，说明其长期职责、所有者、生命周期和退出条件。
3. 代码变更需要相应测试，工作流变更需要最小端到端样例，文档变更需要链接、格式和事实一致性检查。
4. 不创建 `v1`、`v2`、`final` 或备份目录保存当前内容。Git 管理历史版本。
5. 未经用户确认，不删除遗产项目、缓存、生成物、实验证据或用户维护的正式材料。
6. 交付时报告修改文件、对应权威材料、验证命令、验证结果、风险和未解决问题。
````

保留理由：职责、所有者、生命周期和退出条件是新增长期结构的团队标准；代码、工作流与文档检查分别对应真实变更风险。禁止备份树、保护历史材料和提供验证结果均应保留。

### K10 bootstrap 描述范围清楚

【应保留】

原文与位置：

[skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md)，第 4 行：

````text
description: Initialize or safely upgrade a processor project's root AGENTS.md from a maintained baseline. Use when starting a processor project, adding project-level Agent collaboration rules, or comparing an existing AGENTS.md with the package baseline. This skill only handles AGENTS.md; it does not scaffold documentation, inspect or configure environments, install tools, or modify processor source.
````

保留理由：描述同时说明根 AGENTS 初始化、已有文件比较和单文件边界。排除环境、脚手架和源码工作有助于避免错误触发，长度本身不足以判为冗余。

### K11 bootstrap 单文件模板与验收

【应保留】

原文与位置：

[skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md)，第 15 至 17 行：

````text
Read [assets/AGENTS.md](assets/AGENTS.md) completely before drafting or comparing a project file. Treat it as a maintained output template. It becomes project authority only after the user accepts it or it is written into a project that lacks `AGENTS.md` under an explicit bootstrap request.

Keep this maintained baseline within 4096 UTF-8 bytes. It owns only project authority, authorization, path mapping, verified tool entrypoints, and concise routing to task Skills. Detailed design gates, hardware rules, verification checklists, and source-summary requirements belong to the corresponding Skills and their references. Do not copy them or personal conversational style rules into the generic baseline. Project-owned files may grow to record evidenced local constraints; the package budget is not a limit on user projects.
````

[skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md)，第 23 至 29 行：

````text
1. This skill may create or revise only the target project's root `AGENTS.md`.
2. Do not create Architecture, Design, Source, Verification, runtime, configuration, or placeholder files.
3. Do not inspect, install, configure, repair, or validate the development environment. Environment and toolchain responsibilities belong to deterministic scripts outside this skill.
4. Do not run builds, tests, simulators, synthesis tools, package managers, or environment setup commands.
5. Do not modify nested `AGENTS.md` files unless the user explicitly names one as the target.
6. Do not add machine-specific absolute paths, usernames, local tool locations, project-specific processor facts, or inferred architecture decisions.
7. After creation, the user project owns its `AGENTS.md`. Never synchronize or overwrite it from a later package version automatically.
````

[skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md)，第 63 至 70 行：

````text
Before completing, verify:

1. At most one target file changed, `<project-root>/AGENTS.md`.
2. A pre-existing file was not overwritten or reduced without explicit authorization.
3. The file contains no unresolved scaffold markers, guessed commands, or machine-specific paths.
4. The authority rules distinguish explicit user decisions, current Git authorities, implementation evidence, and external references.
5. The file retains authorization, evidence, and no-auto-overwrite constraints. New-project mappings compose with the documentation Skill; existing mappings remain intact unless migration was authorized.
6. No environment command or unrelated project action ran.
````

保留理由：模板本身就是该任务的完整输出契约，通读短模板与任务直接相关。4096 字节约束限制包内模板，用户项目可增长。单文件、无猜测路径和无环境操作的验收适合这一有明确权限边界的工具。

### K12 bootstrap 目标解析、首次创建和已有文件保护

【应保留】

原文与位置：

[skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md)，第 33 至 36 行：

````text
1. Use the project root explicitly named by the user.
2. When no path is named, use the current Git worktree root if it is unambiguous and within the user's stated scope.
3. If multiple repositories or possible roots remain, ask the user to identify the target before writing.
4. Read all applicable existing `AGENTS.md` instructions before examining or changing the target.
````

[skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md)，第 50 至 59 行：

````text
An explicit request to initialize or bootstrap the named project authorizes creating a missing root `AGENTS.md`. It does not authorize any other project or environment change.

## Existing `AGENTS.md`

1. Read the existing file and treat its current project rules as authoritative.
2. Do not replace it with the baseline.
3. Compare by responsibility: project authority, authorization, path mapping, verified tool entrypoints, local constraints, and task-Skill routing. Identify copied methodology as a simplification proposal, keeping the existing project file unchanged until authorized.
4. Preserve every existing rule unless the user explicitly approves its removal or replacement.
5. Report proposed additions, conflicts, and obsolete project-specific rules as an incremental change set.
6. Apply the change set only after the user explicitly authorizes the revision.
````

保留理由：目标不唯一时提问有实际写错仓库风险；明确 bootstrap 请求已经授权创建缺失文件。已有 AGENTS 定义用户项目规则，不能自动覆盖。此处“授权后修改”可以由既有任务授权满足，未发现必须重复询问的要求。

### K13 生成基线的授权继承与任务路由

【应保留】

原文与位置：

[skills/bootstrap-processor-project/assets/AGENTS.md](../skills/bootstrap-processor-project/assets/AGENTS.md)，第 15 至 18 行：

````text
1. 用户当前任务确定目标、范围和交付形式。解释、Review 和诊断默认只读；明确的修改请求授权完成对应工作，已作出的决定无需重复确认。
2. 保留无关工作树修改和用户直接维护的材料。发现相邻问题时记录其影响；清理、删除、迁移或外部状态变更须有明确授权。
3. 影响正确性或项目架构取舍的未决问题，先给出证据和待决事项，取得决定后继续受影响的工作。
4. 已有 `AGENTS.md` 的增量修订须在授权范围内展示差异，不得随包升级自动替换。
````

[skills/bootstrap-processor-project/assets/AGENTS.md](../skills/bootstrap-processor-project/assets/AGENTS.md)，第 22 行：

````text
无既有映射时采用下列默认值；已有项目保留可核验的实际映射。迁移须经授权，并同步本节、实际文档和链接。声明路径不要求创建空目录。
````

[skills/bootstrap-processor-project/assets/AGENTS.md](../skills/bootstrap-processor-project/assets/AGENTS.md)，第 36 至 39 行：

````text
1. 构建、测试、仿真、综合和静态检查使用项目已声明的脚本；初始化时只登记已核验的入口。没有正式入口时先报告缺口，避免猜测命令或本机路径。
2. 环境探测和配置由项目或 Skill Package 的确定性脚本负责。全局 PATH、系统工具、许可证及仓库外配置变更需要明确授权。
3. 按任务读取对应 Skill 及其所需参考资料：文档组织用 `organize-processor-docs`，微架构设计用 `design-chisel-processor`，Chisel 实现与验证用 `implement-chisel-processor`，追踪和优化使用对应 Skill。技术门禁、硬件检查项和源码摘要要求由这些 Skill 维护。
4. 交付说明修改范围、对应项目依据、验证命令与结果、证据位置和未解决事项。
````

保留理由：基线明确写出“已作出的决定无需重复确认”，按任务读对应 Skill，并保留已核验工具入口和现有映射。其内容与根规则分别面向产品仓库和用户项目，具有不同作用域。

### K14 design 描述聚焦微架构设计

【应保留】

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 4 行：

````text
description: Develop, challenge, and document Chisel processor microarchitecture designs before implementation. Use when discussing or writing design documents for processor pipelines, queues, issue logic, rename, ROB, LSU, caches, MSHRs, forwarding, wakeup, replay, flush, privilege, exceptions, or other cycle-accurate hardware mechanisms; when converting design conversations into stable Markdown specifications; or when reviewing a proposed Chisel CPU design for correctness, timing, area, verification cost, and cross-document consistency.
````

保留理由：枚举较多，集中在周期精确的处理器机制、设计文档与方案审查。未触发本地长度上限，也没有错误路由或实际截断证据。可在后续编辑时压缩同类名词，本轮不将可读性偏好判为过时指令。

### K15 design 已有按需参考文件

【应保留】

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 71 行：

````text
Read [references/review-checklist.md](references/review-checklist.md) for the full checklist.
````

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 129 行：

````text
Use [references/design-document-template.md](references/design-document-template.md) when creating or restructuring documents.
````

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 145 行：

````text
Read [references/chisel-guidance.md](references/chisel-guidance.md) before turning the design into RTL.
````

保留理由：完整检查表、文档模板和实现指导分别放在引用文件，后两者有创建文档、转 RTL 的加载条件。主文件约 172 行，保留共同状态语义和简短交接规则具有导航作用，未达到必须继续拆分的证据门槛。

### K16 状态、生命周期和周期反例清单

【应保留】

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 45 至 54 行：

````text
For every stateful structure, prove:

```text
allocation
-> active ownership
-> all possible responses
-> completion or retry
-> release
-> safe reuse
```
````

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 58 至 69 行：

````text
- one-shot events cannot be missed;
- persistent state substitutes for missed events where required;
- flush blocks all forbidden side effects before registers clear;
- external transactions that cannot be canceled retain ownership;
- old responses cannot target a reused slot;
- release and same-cycle reuse rules are explicit;
- multiple writes to one field have a total priority order;
- speculative wakeup has a complete correction path;
- data visibility follows actual RAM read/write semantics.
- committed and speculative entries sharing one structure have separate flush rules.

Derive identity protection from actual lifetime and ownership. Do not add `generation`, epoch, or ROB identity by habit. A bare index can be sufficient when release, reuse, masks, fixed pipeline latency, or retained ownership prove that stale targeting cannot occur.
````

[skills/design-chisel-processor/references/review-checklist.md](../skills/design-chisel-processor/references/review-checklist.md)，第 19 至 25 行：

````text
- Who allocates the slot?
- Which structures retain the index?
- Can completion occur before every reference disappears?
- Can release and allocation target the same slot in one cycle?
- Can a late response hit a reused slot?
- Does a mask bit still identify the original entry after reuse?
- Is extra identity metadata proven necessary by a lifetime counterexample?
````

[skills/design-chisel-processor/references/review-checklist.md](../skills/design-chisel-processor/references/review-checklist.md)，第 88 至 99 行：

````text
Require cycle-specific tests for:

- same-cycle allocate and wake;
- release and attempted reuse;
- response and flush;
- release and flush;
- miss ownership and flush;
- late external response;
- full queue or full MSHR;
- multiple lanes targeting the same structure;
- mask clear and slot reuse;
- Store/Load visibility around RAM writes.
````

保留理由：释放复用、晚响应、同周期冲突、flush 与内存可见性是实际硬件正确性问题。检查项和定向验证具有可检验对象；它们不因模型能够主动推理而失去作用。F03 只调整固定执行顺序。

### K17 完整方案比较与物理证据边界

【应保留】

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 75 至 83 行：

````text
Compare complete implementations under the same capacity, width, stage boundaries, and correctness requirements.

- Include every required set, clear, bypass, retry, release, and ownership mechanism.
- Do not create a counterexample by omitting maintenance already specified for an alternative.
- If a mechanism is unspecified, state the defect conditionally: "If this clear or bypass is absent, the following trace fails."
- Separate unavoidable datapath cost from optional persistent-state maintenance.
- Preserve the selected design unless a concrete invariant fails or measured timing evidence justifies changing it.

For persistent masks, count initial generation, ongoing set and clear networks, same-cycle bypasses, update ports, flush, and slot reuse. For recomputation, count the comparison and selection network on every attempt, including duplicated lanes.
````

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 107 行：

````text
Do not claim placement or routing behavior without synthesis evidence. State likely structures and request timing reports when needed.
````

保留理由：容量、宽度、级边界和维护机制一致是公平比较前提。源代码结构不足以证明布局布线结论。保持已选设计以及条件化缺陷结论可防止把遗漏机制当作方案缺陷。

### K18 设计模板中的字段、优先级和未决项

【应保留】

原文与位置：

[skills/design-chisel-processor/references/design-document-template.md](../skills/design-chisel-processor/references/design-document-template.md)，第 25 至 35 行：

````text
For each field:

```text
semantics:
set:
clear:
valid interval:
consumers:
same-cycle priority:
invariant:
```
````

[skills/design-chisel-processor/references/design-document-template.md](../skills/design-chisel-processor/references/design-document-template.md)，第 55 至 66 行：

````text
Write one total order for each state group.

```text
reset
> flush
> release
> response
> wake or mask update
> allocation
```

Document justified exceptions separately.
````

[skills/design-chisel-processor/references/design-document-template.md](../skills/design-chisel-processor/references/design-document-template.md)，第 104 至 106 行：

````text
## 12. Open decisions

Mark unresolved facts `TODO`. Include alternatives, decision criteria, and affected invariants.
````

保留理由：模板提供可检查的状态语义与信息位置。具体优先级示例仍须服从项目已批准的 Design，并记录例外；模板不赋予默认顺序覆盖项目事实的权限。

### K19 Chisel next-state、身份生命周期与实现证据

【应保留】

原文与位置：

[skills/design-chisel-processor/references/chisel-guidance.md](../skills/design-chisel-processor/references/chisel-guidance.md)，第 33 至 43 行：

````text
Use explicit exceptions for committed state or non-cancelable transactions.

When committed and speculative entries share a structure, compute flush next state per entry:

```scala
when(flush) {
  nextValid(i) := valid(i) && committed(i)
}
```

Do not apply one blanket clear rule to mixed-lifetime entries.
````

[skills/design-chisel-processor/references/chisel-guidance.md](../skills/design-chisel-processor/references/chisel-guidance.md)，第 53 至 59 行：

````text
Define whether clear or set wins for overlapping bits. Assert impossible overlaps when required.

## Responses

For fixed pipelines, carry the minimum identity proven necessary. A bare index is valid when the target cannot be released and reused before the response. Add ROB tag, generation, or epoch only when a concrete lifetime permits stale targeting. Block all forbidden writes on flush before clearing pipeline registers.

For long-latency structures, retain ownership until response:
````

[skills/design-chisel-processor/references/chisel-guidance.md](../skills/design-chisel-processor/references/chisel-guidance.md)，第 100 至 110 行：

````text
RTL cannot guarantee placement. Synthesis may share, duplicate, absorb, or restructure common expressions.

Use timing reports to decide:

- signal replication;
- register insertion;
- memory implementation;
- lane partitioning;
- floorplanning or vendor attributes.

Only register boundaries reliably force a cycle cut.
````

保留理由：混合提交状态、set/clear 冲突、响应身份与不可取消事务需要真实硬件契约。示例用于表达方法，不能直接视为所有模块通用的 reset/flush/release 顺序。布局结论需要工具证据。

### K20 按变更类型验证及重大文档独立审查

【应保留】

原文与位置：

[skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md)，第 149 至 163 行：

````text
For implementation work, provide:

- state transition table;
- Chisel assertions;
- directed ChiselTest scenarios;
- actual test results with failing cycle and signals.

For documentation-only work:

1. search for stale terminology and conflicting rules;
2. check Markdown fences and conflict markers;
3. compare overview, topic, protocol, assertions, and stage plan;
4. independently review substantial changes with a subagent when available.

Subagent review should be read-only. Ask it for findings by severity, file and line, and a concrete counterexample. Reuse a reviewer that already knows the project when repository rules request that behavior.
````

保留理由：实现工作与纯文档工作已经分开。源码需功能证据，文档需术语、链接关系和冲突检查；subagent 审查受 substantial changes 和可用性条件限制。没有材料证明此项重大设计审查门禁已被撤销，保留；本轮审查未执行这些被审规则。

### K21 implement 描述对应实际工作流

【应保留】

原文与位置：

[skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md)，第 4 行：

````text
description: Document-driven workflow for implementing, reviewing, and verifying Chisel processor and memory-subsystem RTL. Use when Codex must work from maintained Architecture and Design, trace a complete integration surface, reason in synthesized-hardware terms, keep source-adjacent _codex.md summaries current, avoid redundant or overprotective logic, or run focused functional verification.
````

保留理由：触发范围是从 Architecture/Design 落实、审查及验证 Chisel RTL。源码旁摘要和聚焦功能验证属于当前正式职责，描述长度与信息量相称。

### K22 实现前的权威链与受影响集成面

【应保留】

原文与位置：

[skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md)，第 11 至 23 行：

````text
Read repository instructions first. Then locate and read, in order:

1. The Architecture documents that define target properties and boundaries.
2. The current Design documents that define the concrete module, protocol, lifecycle, and cycle semantics.
3. Current source, module-local notes, source-adjacent `_codex.md` summaries, tests, generated reports, and relevant reference implementation.
4. The user's explicit task scope and acceptance criteria.

Treat explicit user decisions and the current Git authority as authoritative.
Treat a later ordinary user statement as change intent unless the user clearly
supersedes an existing fact. Architecture defines target properties, Design
defines intended implementation, and Source plus Verification define proven
current behavior. Never silently resolve a conflict. State the target, current
implementation, evidence, and required migration.
````

[skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md)，第 45 至 58 行：

````text
Before editing, identify the real elaboration top, source set, immediate
dependencies, and downstream regression scope. Search for stale paths, duplicate
top-level definitions, and incompatible local copies of shared packages.

For every changed Bundle or protocol, trace definitions, constructors, storage,
all producers, all consumers, partial-write methods, tests, widths, encodings,
and port order. Separate mechanical ABI migration from semantic redesign.
Record which pipeline owns each writable field and which architectural side
effects consume it.

Trace a reference implementation through its complete producer-to-consumer path
before declaring a local fragment incorrect. Classify each mismatch as design,
interface, implementation, documentation, test, or tooling so the correct owner
and migration action are explicit.
````

保留理由：Architecture、Design、源码和结果的层次用于确定目标与已实现事实。Bundle/协议变化要求检查全部真实生产者和消费者，其范围由 changed 和 relevant 限定，属于 ABI 迁移正确性要求。

### K23 只询问影响正确性或接口的未决设计

【应保留】

原文与位置：

[skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md)，第 33 至 41 行：

````text
Use `$design-chisel-processor` when field semantics, ownership lifetime, cycle
boundaries, conflict priority, late-response handling, identity protection, or
acceptance criteria remain unresolved. Begin RTL work only after choices that
affect correctness or interfaces are closed.

Do not repeat questions already answered by the user's latest instruction or
accepted documents. Ask before adding a field, protocol, or identity mechanism
only when its necessity or semantics remain unresolved. Do not invent
unspecified protocols or conservative guards.
````

保留理由：明示不重复用户或正式文档已经回答的问题，仅在新增字段、协议或身份机制的必要性或语义未决时询问。类别六的反复审批问题在当前写法中已被处理。

### K24 硬件结构、更新所有权和参数边界

【应保留】

原文与位置：

[skills/implement-chisel-processor/references/hardware-rules.md](../skills/implement-chisel-processor/references/hardware-rules.md)，第 15 至 19 行：

````text
- Express updates through named events such as `alloc`, `wake`, `issue`, `settle`, `release`, `flush`, and `kill`.
- Centralize conflicts for each register or entry and document priority only when events can overlap.
- Keep orthogonal field updates parallel.
- Use `WireDefault` or explicit next-state wires for composed updates.
- Remember that reading a `Reg` after `:=` in the same elaborated clock cycle observes the old registered value.
````

[skills/implement-chisel-processor/references/hardware-rules.md](../skills/implement-chisel-processor/references/hardware-rules.md)，第 37 至 45 行：

````text
- For every write-port class, list the fields it may update. Zero/default fields
  are safe only when ownership or the partial-write method proves they cannot
  overwrite unrelated state.
- Gate CSR, ROB, LLBit, STQ, predictor, and redirect side effects with their
  documented acceptance event and assert one-shot behavior.
- Add elaboration-time `require` checks for legal widths, divisibility, depths,
  and port counts. Handle `len == 1` and zero-index-width cases statically.
- Build initialized structures from pure Scala literals where required, and
  elaborate representative boundary configurations after parameter changes.
````

[skills/implement-chisel-processor/references/hardware-rules.md](../skills/implement-chisel-processor/references/hardware-rules.md)，第 49 至 54 行：

````text
- Do not broaden stall, flush, kill, or serialization beyond the documented contract to make a test pass.
- Do not duplicate a downstream ready/flush/valid guarantee as runtime logic unless the design requires local enforcement.
- Add an assertion when an upstream module owns the contract.
- Do not add a zero-mask mux around `PriorityEncoderOH`; zero input already produces zero.
- Expect firtool to remove unused internal Bundle fields and logic within an elaborated top. Top-level IO remains externally observable.
- Leave intentional source-level redundancy only when it improves semantic clarity and synthesis can prove equivalence; comment it locally.
````

[skills/implement-chisel-processor/references/hardware-rules.md](../skills/implement-chisel-processor/references/hardware-rules.md)，第 58 至 66 行：

````text
For every remaining chain, report:

1. source location;
2. operands or entry/port count;
3. combinational stages and fanout;
4. critical-path risk;
5. tree, one-hot, banking, clustering, or register-boundary alternative.

Do not rely on Scala hierarchy for FPGA placement. Add a register when a hard timing boundary is required.
````

保留理由：寄存器读取时点、部分写所有权、静态参数合法性和时序链规模具有明确硬件含义。Timing audit 应按当前任务受影响范围理解。协议保持语义另见 T01，本项不为该句的“standard Decoupled”表述背书。

### K25 源码旁 _codex.md 作为明确产品门禁

【应保留】

原文与位置：

[skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md)，第 72 至 89 行：

````text
The Agent maintains source-adjacent summaries. Every project-authored `.scala`
source created or changed by the task must have a same-directory
`<SourceBase>_codex.md` summary. Create a missing summary and update an existing
summary in the same change. Generated, vendored, and third-party Scala sources
are excluded unless the project explicitly owns them.

Each summary records only implementation-facing facts:

- source responsibility and governing Design links;
- public interfaces and field semantics;
- events, same-cycle priority, and state lifecycle;
- producer, register boundary, consumer, and architectural side effects;
- assertions, tests, evidence, timing risks, and unverified behavior.

Keep the summary concise and maintainable. It describes the source and cannot
override Architecture or Design. Before delivery, check every changed
project-authored `.scala` path for its matching summary. The task is incomplete
while any required summary is missing or stale.
````

保留理由：每个受影响的项目自有 Scala 源文件维护摘要，是 AGENTS.md 第 64 行明示的产品要求，已经排除生成、第三方和 vendored 源码。模型上下文更长不能替代团队要求的可维护实现说明。

### K26 适用测试层级与真实物理状态模型

【应保留】

原文与位置：

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 10 至 21 行：

````text
Cover applicable cases:

- normal completion and backpressure;
- empty, full, single-entry, and simultaneous-port states;
- same-cycle event conflicts and documented priority;
- flush, kill, late response, retry, and index reuse;
- one-hot, mask-subset, and mutual-exclusion assertions;
- narrow-address repeated reads and writes;
- same-cache-line ordering and cross-line concurrency;
- hit, miss-owned, miss-nack, forwarding full/partial coverage;
- allocation/merge conflicts, refill/install/writeback interactions;
- reset and long randomized stress with a reference model or scoreboard.
````

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 27 至 41 行：

````text
Select applicable levels from:

1. module unit tests;
2. adjacent queue/pipeline or producer/consumer cascade;
3. subsystem integration;
4. complete Backend or CPU functional/difftest.

Run every affected and available level before delivery. The order may change
when an independently runnable higher-level test provides earlier feedback.
A pass at one level does not close another. ABI or shared-package changes must
use the real dependent source set and rerun affected downstream levels.

The reference model must represent distinct physical states when hardware
separates occupancy, issue existence, pending recycle, committed state, or
uncancelable ownership.
````

保留理由：使用 applicable、affected and available 限定范围，且允许改变层级执行顺序。共享 ABI 的下游回归和 occupancy/issue/recycle 状态分离有实际缺陷检测价值。未证实过时，保留。

### K27 失败复现、证据等级和针对性 probe

【应保留】

原文与位置：

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 49 至 66 行：

````text
Separate these evidence levels:

```text
elaboration
Scala/C++ compilation
directed functional test
random or pressure test
cascade or subsystem integration
Backend or CPU validation
synthesis or timing evidence
```

Report completed cycles and explicit coverage boundaries. An interrupted stress
run remains open. A Verilator or build-tool failure is tooling evidence until
the RTL failure is reproduced.

When DCE, field retention, encoder behavior, or generated topology is disputed,
use an isolated comparison probe and inspect emitted FIRRTL/SystemVerilog.
````

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 87 至 101 行：

````text
Inspect the fixed baseline, Design paths, source paths, tests, and acceptance
criteria. Return findings ordered by severity with file and line references.
Require checks for:

- mismatch between target documents and implementation;
- redundant conditions, overprotection, or invented protocol;
- serial dependency chains, wide muxes, fanout, and ready/valid loops;
- event overlap, missing assertions, late responses, and index reuse;
- weak tests whose observed result cannot distinguish the intended behavior.

## Verification review

Run the approved source and test paths with the exact recorded commands. A short
report contains backend, tool version, seed, cycle count, pass/fail, log path,
and uncovered behavior.
````

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 116 至 120 行：

````text
Follow project `AGENTS.md` for evidence paths and output format. Do not create a
standalone review document unless the project workflow or user requests one.
After fixes, rerun every affected directed test and the relevant stress test.
Preserve failure logs when they explain a resolved bug. Keep generated logs out
of Git when repository policy requires it.
````

保留理由：编译、功能测试、系统验证和时序证据支持不同结论；工具失败不能直接定为 RTL 错误。隔离 probe 由具体生成行为争议触发，修复后仅重跑受影响测试。失败记录的命令、seed、周期和信号便于复现。

### K28 双 subagent 核验默认关闭

【应保留】

原文与位置：

[skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md)，第 100 至 113 行：

````text
Dual-subagent verification is disabled by default. Enable it only when the user
explicitly requests dual-subagent verification for the current task. Preserve
these two independent roles when enabled:

1. A static-review subagent performs a read-only source and document review.
2. A verification subagent independently runs the approved tests and records raw evidence.

Give both roles source paths, authority documents, the fixed baseline, and
acceptance criteria. Do not give them an expected conclusion. If two independent
subagents are unavailable, report that fact and do not claim independent
verification. The active Agent resolves findings, applies authorized fixes,
reruns affected tests, and updates every affected `_codex.md` summary.

When an implementation task follows a failed review, address valid findings and rerun affected tests. Review roles report findings without modifying files. Do not report completion while required tests fail.
````

[skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md)，第 105 至 112 行：

````text
This mode is off unless the user explicitly requests dual-subagent verification
for the current task. When enabled:

1. Give the static-review subagent Design paths, source paths, tests, acceptance criteria, and the fixed baseline. Its role is read-only.
2. Give the verification subagent source paths, test paths, commands, acceptance criteria, and the fixed baseline without the active Agent's expected verdict.
3. Keep both reports independent until the active Agent receives them.
4. Store raw logs under Runtime and place formal review material only where project instructions or the user require it.
5. If both roles cannot run independently, state the limitation and classify the result as active-Agent verification.
````

保留理由：开启条件是用户对当前任务的明确请求。开启后保持角色独立、固定基线和如实报告验证能力有意义。历史包的默认双核验见 H01，不能据历史内容判当前版本仍有该问题。

### K29 organize 描述与语义设计职责分开

【应保留】

原文与位置：

[skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md)，第 4 行：

````text
description: Establish, author, restructure, or audit human-first processor Architecture, Design, Research, Review, and Verification documentation. Use for progressive documentation scaffolding, authority maps, reading paths, document-type content contracts, length-budgeted splitting, or maintainability reviews. Do not use as a substitute for cycle-accurate microarchitecture analysis or RTL implementation.
````

[skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md)，第 27 至 29 行：

````text
When detailed processor semantics are being designed or reviewed, also use `design-chisel-processor`. This skill owns information architecture and writing constraints; `design-chisel-processor` owns cycle-accurate correctness.

All `doc/` paths in this skill and its references describe the default layout. For an established custom layout, resolve them through the project's mapping, including domain entries and the overall reading entry. Preserve that mapping, its authority files, and its local constraints. Do not silently rewrite `AGENTS.md` or create a parallel `doc/` tree. A migration requires authorization and coordinated updates to the mapping, documents, and links.
````

保留理由：描述限定信息架构、阅读路径、内容契约和文档维护。周期精确分析交给设计 Skill，已有项目路径映射优先；边界文字有实际选用价值。

### K30 文档按类型加载与人类可读权威网络

【应保留】

原文与位置：

[skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md)，第 17 至 25 行：

````text
3. For a new project without an established mapping, keep the current document network under one project-root `doc/`, matching `bootstrap-processor-project`. Use one current `doc/Architecture/`, one current `doc/Design/`, and one current `doc/Verification/` when those domains contain real material. Use `doc/Research/` only when project-maintained research exists. An existing project's approved mapping takes precedence. Git keeps history. Research, Review, and Finding remain evidence rather than processor authority.
4. Give each normative fact one owning document. Summaries link to the owner and add no new normative detail.
5. Keep Research, reference implementations, current RTL, current proposed documents, and new recommendations distinct.
6. Do not introduce a document manifest, processor schema, renderer-owned truth, backup tree, or document workflow state.
7. Do not create empty directories, empty topic files, or speculative placeholders.
8. Explain every Chisel-facing interface in `Scala declaration -> semantics` order. Show the minimal Scala structure first, then explain fields in declaration order.
9. Outside interface declarations, use Scala only when prose, a table, or a diagram cannot express the required hardware structure precisely. Keep only the minimal decisive fragment.
10. Keep a same-stem editable source beside every explanatory raster diagram and update both in the same candidate change. Evidence captures such as waveforms and tool screenshots do not require an editable diagram source; bind them to the input commit, run or method, and evidence location.
11. Use the physical module view in `doc/Design/` as the main directory axis. Align this view as closely as possible with stable Chisel or RTL instance hierarchy and responsibility boundaries. Keep Protocols, Lifecycles, ADRs, and Verification as orthogonal views linked to that axis.
````

[skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md)，第 35 至 52 行：

````text
Use when a project lacks a clear document framework or when existing material must be organized. Read [references/bootstrap.md](references/bootstrap.md).

### Author

Use when creating or revising a document within an approved framework.

1. For Architecture goals and processor properties, read [references/architecture.md](references/architecture.md).
2. For Design entry, overview, topology, subsystem, or module documents, read [references/design.md](references/design.md).
3. For cross-module Protocol or Lifecycle documents, read [references/protocol-lifecycle.md](references/protocol-lifecycle.md).
4. For ADR documents, read [references/adr.md](references/adr.md).
5. For Verification documents, read [references/verification.md](references/verification.md).
6. For Research, Review, Finding, or Diagnosis documents, read [references/research-review.md](references/research-review.md).

Read only the references required for the current document types.

### Maintain

Use when auditing, splitting, merging, relocating, or pruning existing documents. Read [references/maintenance.md](references/maintenance.md) plus the references for every affected document type.
````

[skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md)，第 82 至 92 行：

````text
1. A human can understand every document without reading machine state or generated schemas.
2. Every document opens with its responsibility, scope, and owned facts in natural language.
3. `doc/README.md` links directly to every present domain entry.
4. Any Architecture property is reachable from `doc/Architecture/README.md` within two document links.
5. Any module, Protocol, or Lifecycle is reachable from `doc/Design/README.md` within two document links.
6. The Design module view accounts for every stable implemented module responsibility and records justified differences from the Chisel or RTL instance hierarchy.
7. An implemented Design document links its relevant Source and Test locations without copying source bodies.
8. Verification material links to the Architecture property or Design invariant it checks.
9. Every explanatory raster diagram retains a same-stem editable source. Evidence captures identify their input commit, run or method, and evidence location.
10. Removing `.assistant/` leaves the formal documentation complete and readable.
11. Direct user edits remain first-class input and are not overwritten from another representation.
````

保留理由：Bootstrap、Author、Maintain 已分流，明确只读当前文档类型需要的 references。单一权威、模块轴、可编辑图源、两跳阅读路径和直接编辑支持，是人类文档产品的验收要求。

### K31 暂定篇幅预算与可配置门禁

【应保留】

原文与位置：

[skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md)，第 66 至 78 行：

````text
Count `effectiveChars` as non-whitespace Unicode characters and `nonBlankLines` as lines containing non-whitespace content. Count prose, tables, code blocks, links, and embedded examples. Store raw logs, full source listings, and bulk research elsewhere.

| Document kind | Target `effectiveChars` | Target `nonBlankLines` | Provisional hard `effectiveChars` | Provisional hard `nonBlankLines` |
|---|---:|---:|---:|---:|
| Entry `README.md` | 2500 | 60 | 4000 | 100 |
| Architecture topic, Design principles, Design overview | 6000 | 140 | 10000 | 200 |
| Module, Protocol, Lifecycle | 8000 | 180 | 12000 | 250 |
| ADR | 2500 | 60 | 4000 | 100 |
| Research or Review | 6000 | 150 | 10000 | 220 |
| Finding | 2500 | 60 | 4000 | 100 |
| Verification specification | 6000 | 150 | 10000 | 220 |

These budgets are a writing strategy pending validation against real processor projects. Exceeding a target produces a warning and requires a concision review. Provisional hard-limit enforcement is configurable; use blocking enforcement only when the project or evaluation protocol explicitly selects it. Reduce duplication and incidental detail before splitting. Split only at a stable responsibility, ownership, protocol, lifecycle, or independent reading boundary. Never create `Part1`, `Part2`, or size-only fragments. Preserve necessary field tables, pipeline tables, state machines, and assertions when a justified document remains above a provisional threshold.
````

保留理由：预算明确标记 provisional，默认告警，严格阻断须由项目或评测选择；还保留无法合理拆分时的必要字段表、状态机与断言。此处目标是人类阅读和维护，无法由模型容量提升推出预算过时。

### K32 文档框架清点、渐进创建与真实架构审批

【应保留】

原文与位置：

[skills/organize-processor-docs/references/bootstrap.md](../skills/organize-processor-docs/references/bootstrap.md)，第 19 至 27 行：

````text
For every existing document, record:

1. its current path;
2. the reader question it answers;
3. the facts it appears to own;
4. the documents that repeat or contradict those facts;
5. whether it represents current intent, current design, rationale, verification, research, review, finding, or history.

Preserve existing paths until the proposed authority and link migration are understood. An existing project first needs an index and ownership audit; immediate bulk relocation obscures conflicts.
````

[skills/organize-processor-docs/references/bootstrap.md](../skills/organize-processor-docs/references/bootstrap.md)，第 42 至 46 行：

````text
Use the smallest set of documents that supports the actual tasks. Do not create one file per checklist item.

## Canonical directory layout

For a new project without an established mapping, place the maintained processor document network under the project-root `doc/` directory. This matches the `bootstrap-processor-project` baseline. For an existing approved layout, substitute the mapped paths throughout this reference and preserve them unless migration is authorized:
````

[skills/organize-processor-docs/references/bootstrap.md](../skills/organize-processor-docs/references/bootstrap.md)，第 96 至 105 行：

````text
Request explicit confirmation before:

1. introducing a new document domain under `doc/`;
2. choosing or changing Architecture topic boundaries;
3. choosing or changing the Design physical module topology or an exception to its Source correspondence;
4. creating a new cross-module Protocol or Lifecycle authority;
5. relocating normative facts between Architecture, Design, and Verification;
6. retiring a current authority document.

Ordinary link repair, navigation summaries, and terminology alignment can enter the candidate diff without becoming new product concepts.
````

[skills/organize-processor-docs/references/bootstrap.md](../skills/organize-processor-docs/references/bootstrap.md)，第 119 至 127 行：

````text
For an existing project:

1. preserve user-authored content;
2. add or repair entry maps first;
3. resolve conflicting authority before moving files;
4. honor the approved project mapping, including roots outside `doc/`; propose migration only when the task requires reorganizing it, and obtain authorization before relocating authority or revising `AGENTS.md`;
5. relocate one coherent responsibility at a time;
6. update inbound and outbound links in the same candidate change;
7. remove duplicate current copies after their facts have a confirmed owner.
````

保留理由：整套文档框架的整理需要全局清点，任务范围与读取范围相称。域、Architecture 边界、物理模块拓扑和权威迁移涉及用户架构取舍；普通链接修复已有明确例外。结合基线“不重复确认”，不推断这里要求再次审批已批准方案。

### K33 Architecture 维护目标与验收条件

【应保留】

原文与位置：

[skills/organize-processor-docs/references/architecture.md](../skills/organize-processor-docs/references/architecture.md)，第 3 行：

````text
Architecture expresses the current processor properties and design goals chosen by the user. It constrains acceptable Design implementations and remains current throughout active project work.
````

[skills/organize-processor-docs/references/architecture.md](../skills/organize-processor-docs/references/architecture.md)，第 30 行：

````text
A small project can keep this content in one document. Split only when a property area has an independent reader question and change lifecycle.
````

[skills/organize-processor-docs/references/architecture.md](../skills/organize-processor-docs/references/architecture.md)，第 44 至 48 行：

````text
These are candidate concerns, not mandatory files. The user controls the actual property vocabulary and grouping.

## Internal logic of an Architecture topic

Answer only the sections needed for the topic, while covering:
````

[skills/organize-processor-docs/references/architecture.md](../skills/organize-processor-docs/references/architecture.md)，第 62 至 78 行：

````text
Use these ownership rules:

1. A condition used by the user to accept the processor belongs to Architecture.
2. A chosen processor property such as ISA scope, execution width, retirement order, cache requirement, exception scope, or target metric belongs to Architecture.
3. Module boundaries, state fields, signal interfaces, cycle placement, event priority, and implementation state machines belong to Design.
4. Test procedures and observed results belong to Verification.
5. Sources and candidate analyses belong to Research.

Architecture invariants describe acceptable processor behavior. Design invariants prove the concrete mechanism satisfies that behavior.

## Architecture ADRs

Place an ADR under Architecture when the decision changes a processor property, design goal, external contract, acceptance condition, or permitted Design freedom. Keep the current property statement in the Architecture topic and link to the ADR for rationale.

## Version and approval

Keep only current Architecture content in the current tree. Candidate commits carry proposed changes. Git carries history. Approval records bind the exact candidate commit; avoid duplicating approval state or generated decision ledgers inside prose documents.
````

保留理由：属性目标、具体 Design、Verification 与 Research 的内容归属是正式信息架构。小项目可单文档，主题按需要选择；没有强制为每个清单项建文件。

### K34 Design 模块拓扑、源码映射与条件拆分

【应保留】

原文与位置：

[skills/organize-processor-docs/references/design.md](../skills/organize-processor-docs/references/design.md)，第 37 至 47 行：

````text
Each shown child path is conditional. Create it only when it owns current content.

## Physical module topology

Use the stable Chisel or RTL structural hierarchy and responsibility boundaries as the Design directory main axis. Here physical module topology means instantiated structural topology, not post-placement physical layout. Align the Design module view as closely as possible with instantiated hardware modules and their ownership. Source filenames alone do not define this topology. Work Packages, Agent assignments, implementation order, and Harness state never define it.

A stable instantiated module that owns an independent responsibility, state, interface, or maintenance lifecycle normally receives its own module directory and `README.md`. A parent subsystem or module `README.md` explains composition and links to its documented children. An overview that lists several independent state owners cannot replace their module authorities.

Shared Bundles and types, generated code, thin wrappers, adapters, and deliberately co-located mechanisms may justify a different document boundary. Record every material difference with an explicit Design-to-Source mapping, its reason, and its maintenance consequence. A significant divergence requires user approval and a Design ADR. This skill reports an unexplained mismatch and does not authorize source restructuring.

Protocols, Lifecycles, ADRs, and Verification remain orthogonal views. Link them to the module axis and keep their owned facts outside module summaries.
````

[skills/organize-processor-docs/references/design.md](../skills/organize-processor-docs/references/design.md)，第 66 至 76 行：

````text
Open with the reader question, functional boundary, owned state, and exclusions. Cover the relevant items:

1. implemented Architecture properties, functional boundary, internal components, and state owners;
2. external interfaces and backpressure, using the [Scala-first interface exposition](protocol-lifecycle.md#scala-first-interface-exposition) rule;
3. state semantics, transitions, same-cycle priorities, side effects, ownership, and safe reuse required by `design-chisel-processor`;
4. qualified pipeline boundaries and links to applicable Protocol and Lifecycle authorities;
5. correctness invariants, timing or physical risks, and verification obligations;
6. concise links to current Source and Test locations when implementation exists;
7. open decisions that genuinely require user authority.

Do not copy full field tables owned by a Protocol document or full cross-module traces owned by a Lifecycle document.
````

[skills/organize-processor-docs/references/design.md](../skills/organize-processor-docs/references/design.md)，第 86 至 94 行：

````text
Use diagrams when topology, ownership, timing, or state transitions are materially clearer visually. Keep a same-stem `.drawio`, `.svg`, `.mmd`, `.dot`, `.puml`, `.plantuml`, or generating `.py` source beside each explanatory raster image and update both in the same candidate. Waveforms, tool screenshots, and other evidence captures instead identify their input commit, run or method, and evidence location. A diagram supplements the owning prose and cannot become an unreferenced second specification.

## Split and merge

Create an independent module document when the subject has stable responsibility, state ownership, interfaces, or an independent maintenance lifecycle. For implemented designs, apply this rule to stable instantiated Chisel or RTL modules unless a documented exception above applies. Keep small helpers inside the owning mechanism document.

Split a long module document by internal mechanism only when the extracted mechanism has its own state or reader question. Keep a short parent document that explains composition and links.

Merge documents that always change together, cannot be understood separately, and do not own independent state or contracts.
````

保留理由：稳定状态所有者和实例责任边界决定文档主轴，允许有理由的映射差异。Scala-first、源码链接、可编辑图源及按独立责任拆分都是既定写作契约。F05 单独处理强制 worktree。

### K35 Protocol 与 Lifecycle 的内容和呈现约束

【应保留】

原文与位置：

[skills/organize-processor-docs/references/protocol-lifecycle.md](../skills/organize-processor-docs/references/protocol-lifecycle.md)，第 3 至 7 行：

````text
Protocol and Lifecycle are orthogonal views over the Design topology. Create them when a cross-module fact cannot be maintained clearly inside one owning module document.

## Protocol authority

A Protocol document owns a shared interface, Bundle, event family, field vocabulary, or handshake contract consumed by multiple modules.
````

[skills/organize-processor-docs/references/protocol-lifecycle.md](../skills/organize-processor-docs/references/protocol-lifecycle.md)，第 32 至 44 行：

````text
For every Chisel-facing interface, present information in this order:

1. identify whether the declaration is current source, current proposed Design, or a reference implementation;
2. state the module viewpoint from which `Input`, `Output`, and `Flipped` directions are defined;
3. show the minimal relevant Scala `Bundle`, `IO`, `Enum`, request, response, or event declaration;
4. preserve declaration order, exact field names, nesting, types, widths, directions, and encodings;
5. explain each field semantically in the same order as the Scala declaration;
6. explain producer, consumer, valid interval, handshake, register boundary, ownership, backpressure, and side effects after the structural declaration;
7. state cross-field rules, same-cycle priority, kill, flush, retry, stability, and assertions after the field-by-field explanation.

Existing source declarations must link to the exact source path. A Design that precedes implementation can own a proposed Scala interface declaration. If source and Design disagree, label current implementation and target Design separately.

Keep the Scala excerpt limited to the interface surface. Exclude module implementation, helper logic, and unrelated imports. Update the Scala declaration and semantic explanation in the same candidate change. A semantic table cannot precede the Scala declaration for a Chisel-facing interface.
````

[skills/organize-processor-docs/references/protocol-lifecycle.md](../skills/organize-processor-docs/references/protocol-lifecycle.md)，第 57 至 77 行：

````text
Trace:

1. admission or allocation;
2. registered and combinational work by qualified cycle boundary;
3. ownership transfer;
4. all possible responses;
5. success and externally visible side effects;
6. stall, miss, nack, kill, flush, replay, retry, exception, and late response;
7. release and safe reuse;
8. same-cycle interactions with competing events;
9. cross-module invariants and directed scenarios.

A Lifecycle refers to module-owned state and Protocol-owned fields. It does not redefine them.

## Protocol versus Lifecycle

Use Protocol when the reader asks what crosses a boundary and under which handshake or identity rules.

Use Lifecycle when the reader asks how one operation moves from initiation through completion, retry, or cancellation.

One mechanism can need both documents. Cross-link them and keep each normative fact in its owning view.
````

保留理由：接口声明顺序和端到端生命周期分别回答字段契约、交易经过哪些阶段的问题。Scala-first 的规定虽具体，仍是当前明确团队规范。跨模块事实单独维护具有持续价值。

### K36 ADR 保存决策理由

【应保留】

原文与位置：

[skills/organize-processor-docs/references/adr.md](../skills/organize-processor-docs/references/adr.md)，第 3 至 19 行：

````text
An ADR preserves durable rationale for a choice with meaningful alternatives and consequences. Place it under `doc/Architecture/ADR/` or `doc/Design/ADR/` according to the authority affected by the decision.

Use an Architecture ADR for processor properties, goals, external contracts, acceptance conditions, or permitted Design freedom.

Use a Design ADR for topology, state organization, interface shape, timing placement, ownership mechanism, or another concrete implementation choice.

Cover:

1. context and one decision question;
2. fixed constraints;
3. considered alternatives;
4. decision and decisive evidence;
5. relevant correctness, timing, area, complexity, and verification consequences;
6. affected current documents;
7. supersession relationship when a later ADR changes the decision.

The current Architecture or Design document owns current behavior. The ADR owns rationale. Keep activity history, research detail, and current specification text in their respective authorities. Apply the ADR budget in `SKILL.md`.
````

保留理由：ADR 的决策问题、约束、备选方案、证据和后果用于长期理解取舍；当前规范仍归 Architecture/Design。该分工可避免把讨论历史混入实现事实。

### K37 Research、Review、Finding、Diagnosis 的证据边界

【应保留】

原文与位置：

[skills/organize-processor-docs/references/research-review.md](../skills/organize-processor-docs/references/research-review.md)，第 3 行：

````text
These documents provide evidence. They cannot define current Architecture or Design, approve a candidate, or silently select a correction.
````

[skills/organize-processor-docs/references/research-review.md](../skills/organize-processor-docs/references/research-review.md)，第 23 至 30 行：

````text
A Review evaluates one frozen subject. Record:

1. subject commit and reviewed paths;
2. applicable Architecture, Design, Protocol, Lifecycle, ADR, and Verification authorities;
3. review method and excluded scope;
4. findings by severity;
5. areas checked with no finding;
6. evidence references and coverage limits.
````

[skills/organize-processor-docs/references/research-review.md](../skills/organize-processor-docs/references/research-review.md)，第 43 至 56 行：

````text
Each Finding contains:

1. subject commit;
2. file and line or section;
3. precise observation;
4. evidence reference;
5. concrete counterexample, event trace, or failure condition when applicable;
6. affected property, contract, or invariant;
7. correction direction without claiming user approval;
8. unreviewed or unverified scope.

## Diagnosis

A diagnosis report records reproduction, expected and observed behavior, evidence chain, root cause, impact boundary, correction direction, and validation required. Keep current Design, proposed correction, and current implementation explicitly labeled.
````

保留理由：冻结审查对象、列出方法和未覆盖范围、绑定文件行号以及将纠正建议保留为提议，直接支持可复核审查。它们适用于本报告，并不要求 Agent 获得新的审批才能写已获授权的报告。

### K38 Verification 的可复现结果归属

【应保留】

原文与位置：

[skills/organize-processor-docs/references/verification.md](../skills/organize-processor-docs/references/verification.md)，第 3 行：

````text
Formal Verification documents are peers of Architecture and Design. Architecture states acceptance conditions. Design states invariants and verification obligations. Verification states how they are checked and records reproducible results or evidence references.
````

[skills/organize-processor-docs/references/verification.md](../skills/organize-processor-docs/references/verification.md)，第 16 至 33 行：

````text
Cover the applicable items:

1. subject commit or version-binding rule;
2. Architecture property or Design invariant under test;
3. verification level and environment;
4. stimulus and initial conditions;
5. observable signals or outputs;
6. oracle and pass criteria;
7. directed, randomized, assertion, formal, synthesis, timing, or performance scenarios;
8. command ID or reproducible command reference;
9. random seed and workload requirements;
10. expected evidence and result location.

## Results and evidence

Keep human summaries concise and immutable once bound to a commit. Store maintainable result summaries under `doc/Verification/Results/` when useful. Store bulk stdout, stderr, waveforms, reports, and generated artifacts in `.runtime/`, then link them with hashes or stable result references.

A result identifies the input commit, command or method, environment or toolchain, outcome, and evidence location. Waveform images, tool screenshots, and other evidence captures inherit this binding from their result entry or state it beside the capture. They do not require an editable diagram source. A failed result remains evidence and cannot be rewritten into a pass.
````

保留理由：测试对象、oracle、环境、命令、seed 与结果位置是复现所需信息。证据图与解释图的例外合理；失败结果不可改写为通过属于证据完整性。

### K39 文档精简、语义审查与变更报告

【应保留】

原文与位置：

[skills/organize-processor-docs/references/maintenance.md](../skills/organize-processor-docs/references/maintenance.md)，第 7 至 18 行：

````text
When a document exceeds its target budget, apply this order:

1. remove repeated normative facts;
2. remove chat history, task chronology, obsolete states, and implementation diary content;
3. move full research narratives to Research and retain only adopted conclusions with links;
4. move raw commands, logs, waveforms, and generated reports to Verification evidence or runtime storage;
5. replace nondecisive copied source and external specifications with precise references;
6. consolidate repeated prose into a state table, field table, invariant, or diagram;
7. shorten overview detail to a summary and authority link;
8. split only at a stable responsibility, ownership, Protocol, Lifecycle, or independent reader question.

If a provisional hard budget remains exceeded, record why the document cannot be made more concise or split at a stable boundary. Treat it as blocking only when the project or evaluation protocol selected strict hard-limit enforcement.
````

[skills/organize-processor-docs/references/maintenance.md](../skills/organize-processor-docs/references/maintenance.md)，第 22 至 33 行：

````text
Approve a split only when each resulting document can state:

1. an independent reader question;
2. its owned facts;
3. its inbound and outbound links;
4. a stable reason to change independently.

Reject `Part1`, `Part2`, chronological fragments, and arbitrary size slices. Keep a concise parent map when several child documents compose one subsystem or mechanism.

## Merge review

Merge documents when they duplicate facts, always change together, or require each other to answer the same reader question. Choose one authority location, migrate inbound links, and remove the duplicate current text in the same candidate change.
````

[skills/organize-processor-docs/references/maintenance.md](../skills/organize-processor-docs/references/maintenance.md)，第 76 至 96 行：

````text
The Agent must separately check:

1. one authority body per normative fact;
2. Architecture properties separated from Design realization;
3. overview summaries aligned with topic authorities;
4. correspondence between the Design module axis and stable Chisel or RTL instance and responsibility topology;
5. an explicit reason, maintenance consequence, user approval, and Design ADR for every significant topology divergence;
6. independent module authorities for stable instantiated modules that own responsibility, state, interfaces, or an independent maintenance lifecycle;
7. module state and Protocol field ownership;
8. Chisel-facing interfaces presented as minimal Scala declarations followed by field semantics in declaration order;
9. non-interface Scala limited to decisive structure that needs code-level precision;
10. complete Lifecycle terminal paths and safe reuse;
11. implemented Design linked concisely to relevant Source and Test locations;
12. explanatory raster diagrams paired with maintained editable sources, and evidence captures bound to an input commit, run or method, and evidence location;
13. ADR decisions aligned with current documents;
14. Research observations separated from inference and linked to adopted authorities;
15. Review and Finding bound to a frozen subject with evidence and uncovered scope;
16. Verification coverage for Architecture acceptance and Design invariants;
17. stale names, rejected mechanisms, dead links, and orphan concepts;
18. reading paths that stay within two links from the appropriate entry;
19. direct readability without Harness data.
````

[skills/organize-processor-docs/references/maintenance.md](../skills/organize-processor-docs/references/maintenance.md)，第 100 至 108 行：

````text
Report:

1. files created, modified, relocated, merged, or retired;
2. facts whose authority moved;
3. Design-to-Source topology mappings or exceptions changed;
4. reading paths changed;
5. length before and after for affected files;
6. deterministic command and result;
7. semantic findings and remaining user decisions.
````

保留理由：先去重复再按稳定责任拆分、保留解释性理由和人工语义审查具有实际文档质量目标。Maintain 主入口限定受影响类型，根规则限定直接相关范围；没有依据把清单解释为每次改字都重新审查整个处理器。重复命令单列 F01。

### K40 optimize 描述仍限定周期语义下的 FPGA 时序优化

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 4 行：

````text
description: Diagnose and optimize timing-critical Chisel RTL for FPGA implementation while preserving cycle semantics. Use for Vivado timing bottlenecks, long ready or admission paths, queue and issue selection, free-list bank mapping, priority encoders, one-hot arbitration, wide muxes, late-arriving forwarding or override data, high-fanout controls, cross-module predicates, register-boundary changes, emitted-Verilog inspection, or routed-DCP A/B analysis. Also use when a source-level simplification needs proof that it changes timing without changing architectural state.
````

保留理由：较长枚举用于识别常见时序任务，同一项工作均需 RTL/物理证据与周期契约。当前没有超限、误触发或截断实例，保留；后续可压缩关键词而无需改变职责。

### K41 时序模式已经按实测路径选择加载

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 73 至 81 行：

````text
Read only the reference categories matched by the measured path. Read multiple
categories when the path crosses their boundaries.

|Measured topology|Reference|
|---|---|
|Mux width, pure transform, compact comparison, late override, one-hot zero behavior, or DCE|[combinational-data-patterns.md](references/combinational-data-patterns.md)|
|Next-state availability, age priority, registered consumer view, local predicate, or stable update identity|[register-boundary-patterns.md](references/register-boundary-patterns.md)|
|Fixed-width allocation, admission gating, queue handshake, or synchronous RAM control|[protocol-storage-patterns.md](references/protocol-storage-patterns.md)|
|Rare global events, route-dominated registered controls, or physical replication|[physical-control-patterns.md](references/physical-control-patterns.md)|
````

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 135 至 138 行：

````text
Read only the relevant section of
[case-studies.md](references/case-studies.md) when comparing alternatives,
reviewing a failed optimization, or checking a known counterexample. Do not load
it for routine application of a closed pattern.
````

保留理由：四类具体 patterns 按实测路径选取，案例仅在比较、失败优化或反例检查时加载。已达到导航主文件加按需参考的目标，旧 rtl-patterns.md 的情况见 H04。

### K42 优化前冻结契约与寄存器边界验证

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 18 行：

````text
Do not add pipeline latency, table-entry fields, interfaces, or conservative guards without authorization. A timing edit that changes fire timing, ordering, visible latency, or flush behavior is a microarchitecture change and requires explicit approval.
````

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 22 至 43 行：

````text
For every affected signal, state:

```text
producer
consumer
combinational expression
register boundary
valid interval
fire condition
hold requirement under backpressure
flush and reset behavior
same-cycle state updates
```

Classify each condition as one of:

- `state-changing`: directly enables allocation, issue, write, release, or architectural effects;
- `admission-only`: only decides whether work may enter;
- `data-select`: chooses data or an index;
- `assertion-only`: checks an upstream contract.

This classification controls which conditions may be removed, delayed, replicated, or converted into registered hints.
````

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 87 至 97 行：

````text
A useful register cut must satisfy all of these:

1. The registered fact is derivable one cycle early.
2. Data, selector, validity, and identity come from the same logical state version.
3. Backpressure stability remains valid.
4. Flush and reset initialize the new register consistently.
5. The new D-input maintenance cone is acceptable.
6. The new Q-output cone is shorter at the real consumer.
7. Feedback does not recreate the original path through another route.

Registering a final result can overload its D input. Registering smaller intermediate results can balance D-side and Q-side delay. Compare both structures in RTL or isolated synthesis before choosing.
````

[skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md)，第 111 至 133 行：

````text
Inspect emitted SystemVerilog before a full implementation run:

- confirm the targeted LUT, mux, comparator, encoder, or dependency chain changed;
- confirm unused Bundle fields and registers were removed;
- confirm state writes remain gated by the intended fire event;
- search for accidental serial priority chains and duplicated wide compares;
- verify reset, flush, and valid logic survived as intended.

Run focused Verilator tests covering normal traffic, empty/full boundaries, sparse lanes, simultaneous events, backpressure, flush, reset, and assertions. Use symmetric tests that compare the old and new designs when practical.

## Re-run implementation and compare

Use the same configuration and constraints for A/B comparison. Re-query the exact old path and all new boundary paths. Report:

- path delay and slack changes;
- logic and route delay separately;
- level and primitive changes;
- endpoint migration;
- LUT, FF, BRAM, and hierarchy movement;
- functional test evidence;
- any placement, strategy, or seed differences.

Treat fixed-DCP frequency calculations as estimates. A positive WNS under one constraint proves closure at that constraint and does not prove the maximum frequency. A generated bitstream with negative WNS is still a timing failure.
````

保留理由：同周期可见性、fire、backpressure、flush 和 D/Q/反馈路径是优化合法性与收益的真实条件。新增流水周期是架构取舍；功能测试和 routed A/B 各验证不同问题，保留。

### K43 组合变换具有适用条件和收益证据

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/references/combinational-data-patterns.md](../skills/optimize-chisel-fpga-timing/references/combinational-data-patterns.md)，第 3 至 16 行：

````text
Read this reference when the measured path is dominated by selection, wide
transport, comparison, arithmetic, late data, or redundant zero handling.

## Distribute pure work before selection

For a pure transform with no state, side effects, or selector dependence:

```text
f(Mux(sel, a, b)) == Mux(sel, f(a), f(b))
```

Apply `f` to candidates in parallel when the result is narrower or when the
selector is late. For a wide storage line, extract the consumed slice from each
candidate before the final selection:
````

[skills/optimize-chisel-fpga-timing/references/combinational-data-patterns.md](../skills/optimize-chisel-fpga-timing/references/combinational-data-patterns.md)，第 112 至 118 行：

````text
## Required evidence

For every selected pattern:

1. Identify the exact selector, data, and operation stages on the measured path.
2. State which primitive levels are expected to leave or move.
3. Inspect emitted RTL for the intended topology and new duplication.
````

保留理由：按无状态、无副作用等条件选择分配变换，并核对生成拓扑、功能等价及物理代价。代码片段承担精确硬件表达，不属于强迫模型按唯一脚本执行。

### K44 寄存器切分与同一 next-state 版本

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md](../skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md)，第 3 至 4 行：

````text
Read this reference when a consumer path can use a fact derived from the prior
cycle or from the same next-state version as its governing state.
````

[skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md](../skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md)，第 98 至 112 行：

````text
## Register-cut acceptance

Every cut must satisfy:

1. The fact is available early enough.
2. Data, selector, validity, and identity use one state version.
3. Backpressure stability remains valid.
4. Flush and reset initialize all coupled registers consistently.
5. The new D maintenance cone is acceptable.
6. The Q consumer cone is shorter.
7. Feedback does not recreate the old path.

Measure old end-to-end, new D, new Q, feedback, CE, reset, flush, and hold paths.
An improved consumer path with a worse producer D path is bottleneck movement,
not closure.
````

保留理由：新寄存器的选择器、数据、有效性和身份必须对齐，新增 D 侧和反馈路径须检查。消费者路径改善不足以单独证明整体瓶颈改善，这一物理约束持续存在。

### K45 协议和存储优化的语义边界

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/references/protocol-storage-patterns.md](../skills/optimize-chisel-fpga-timing/references/protocol-storage-patterns.md)，第 8 至 20 行：

````text
Before editing, classify the interface as standard `Decoupled`, pulse,
fire-cycle-only data, atomic batch, or another documented protocol. Separate:

```text
admission and ready calculation
accepted fire event
state mutation
visible valid and data holding
flush priority in next-state update
```

A timing edit must not silently change upstream stall, downstream visibility,
or same-cycle ownership.
````

[skills/optimize-chisel-fpga-timing/references/protocol-storage-patterns.md](../skills/optimize-chisel-fpga-timing/references/protocol-storage-patterns.md)，第 89 至 97 行：

````text
## Flush and queue visibility

Giving flush priority in internal next-state updates does not automatically
authorize combinationally gating `ready`, `valid`, or `bits`. Such gating can
change stall timing and prevent another pipeline owner from advancing. Preserve
the documented visible handshake while clearing state at the specified edge.

Test normal traffic, full and empty boundaries, simultaneous enqueue and
dequeue, backpressure, flush overlap, invalid lanes, and reset.
````

保留理由：区分 admission、accepted fire 和 state mutation，保证 flush 可见性及已有接口契约，属于功能正确性边界。持有行为必须来自项目协议，术语准确性见 T01。

### K46 全局事件延迟与物理复制证据

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md](../skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md)，第 8 至 9 行：

````text
Use only with explicit approval for the additional observation cycle. Delay
validity and every coupled payload together:
````

[skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md](../skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md)，第 27 至 42 行：

````text
## Replicate an already registered control

For a shallow, route-dominated registered control, create same-edge replicas
from one pre-register expression and partition consumers by physical region:

```scala
val controlNext = controlEvent
val controlRegs = Seq.fill(regionCount)(RegInit(false.B))
controlRegs.foreach(_ := controlNext)
```

Do not feed replicas from the existing control Q when same-cycle behavior is
required, because that adds a cycle. Prove every replica has the same D
expression, edge, reset, enable, pulse semantics, and cycle-aligned payload.
Consumer groups must remain disjoint and must not reconverge through a new
global mux or OR.
````

[skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md](../skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md)，第 52 至 59 行：

````text
## Required evidence

1. Show the control net on the measured path and report its route delay and fanout.
2. Record source and sink sites and consumer spread.
3. Measure the shared replica D path and every regional Q path.
4. Verify no consumer remains on the original high-fanout net.
5. Report added FF, clock, reset, payload, and congestion cost.
6. Treat missing physical replication or unchanged routing as a rejected hypothesis.
````

保留理由：事件增加观察周期会改变语义，需要已有明确架构授权；同沿复制和 netlist driver/site 检查用于确认物理优化确实发生。别名不提供独立寄存器证据。

### K47 Vivado 路径和 A/B 证据规范

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/references/vivado-evidence.md](../skills/optimize-chisel-fpga-timing/references/vivado-evidence.md)，第 5 行：

````text
Use routed implementation evidence for exact path and frequency claims. Post-synthesis and emitted RTL are useful for topology checks and hypothesis formation.
````

[skills/optimize-chisel-fpga-timing/references/vivado-evidence.md](../skills/optimize-chisel-fpga-timing/references/vivado-evidence.md)，第 64 至 74 行：

````text
For replicated flush, reset-like, recovery, or enable controls, source code is insufficient evidence. Check:

1. The post-synthesis and routed netlists contain the intended number of distinct registers.
2. Each replica Q drives only its assigned consumer region.
3. No original global Q net still drives the full consumer set.
4. Fanout, route delay, and placement distance decrease per replica.
5. The common pre-register D expression and reset network remain within timing.
6. Equivalent-register removal, control-set optimization, or physical optimization did not merge the copies.
7. The replicated payload and valid registers remain cycle-aligned.

Report the old driver, each new driver, load count, sites, consumer hierarchy, longest Q path, and shared D path. A lower source-level fanout count without distinct netlist drivers is not evidence of physical replication.
````

[skills/optimize-chisel-fpga-timing/references/vivado-evidence.md](../skills/optimize-chisel-fpga-timing/references/vivado-evidence.md)，第 106 行：

````text
A positive WNS proves timing closure only at the tested constraint. A successful bitstream generation does not prove timing closure. Hold closure must be reported separately.
````

保留理由：源版本、约束、工具、路径阶段、复制后的驱动与 hold 状态决定结论可比较性。bitstream 生成不能替代时序闭合；模型推理无法提供缺失的 routed 测量。

### K48 通用反例库按假设加载

【应保留】

原文与位置：

[skills/optimize-chisel-fpga-timing/references/case-studies.md](../skills/optimize-chisel-fpga-timing/references/case-studies.md)，第 3 至 4 行：

````text
Load only the section that matches the current hypothesis. These are generic
failure modes. Every project must re-establish its own cycle and timing evidence.
````

[skills/optimize-chisel-fpga-timing/references/case-studies.md](../skills/optimize-chisel-fpga-timing/references/case-studies.md)，第 8 至 10 行：

````text
Registering one final arbitration result can move eligibility, age partition,
and priority encoding onto one D input. Registering smaller intermediate results
from one next-state version may balance D and Q paths. Measure both boundaries.
````

保留理由：当前案例已经抽象为通用失败方式，并要求项目重新建立周期与时序证据。保留反例用于挑战寄存器切分和局部化假设；历史单项目数值不能外推成当前收益。

### K49 trace 描述明确任务规模和只读边界

【应保留】

原文与位置：

[skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md)，第 4 行：

````text
description: Task-sized forensic analysis of Vivado synthesis and routed timing evidence for processor RTL. Use when Codex must trace a named setup or hold path, audit whole-design timing populations, compare implementation runs, map primitive, LUT, CARRY, BRAM, DSP, MUXF, register, and routed-net stages back to Chisel or generated RTL, distinguish logic from routing pressure, identify missing DCP queries, or write an evidence-backed timing report. This skill is read-only by default and stops at ranked modification directions. Use optimize-chisel-fpga-timing for RTL edits and routed A/B implementation closure.
````

保留理由：描述列出定向路径、全设计统计、跨运行比较，并把源码编辑交给优化 Skill。器件名枚举可以压缩，当前长度和作用域没有足够依据判为过时补丁。

### K50 trace 按结论选择证据范围

【应保留】

原文与位置：

[skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md)，第 42 至 66 行：

````text
Choose the smallest mode that supports the requested conclusion.

### Targeted Path Trace

Use for one named path, endpoint, module boundary, signal family, or timing
hypothesis. Query the named path plus its producer, consumer, feedback, and
control boundaries. A full endpoint universe is optional and must not be
generated unless the report makes a global absence, ranking, coverage, or
closure claim.

### Whole-design Timing Audit

Use for global closure, limiting-population, module-coverage, or prioritization
claims. Build the endpoint-worst path universe, distributions, family summaries,
and representative paths. State query caps and truncation.

### Cross-run Comparison

Use for before/after or configuration comparison. First prove top, part, clock,
constraints, strategies, parameters, and source identities are comparable. Use
the same targeted population for a local claim. Use matching endpoint universes
and family classifiers for a global claim.

If the request combines modes, keep each claim bound to the evidence population
that supports it.
````

[skills/trace-vivado-timing-to-rtl/references/evidence-and-queries.md](../skills/trace-vivado-timing-to-rtl/references/evidence-and-queries.md)，第 101 至 105 行：

````text
## 4. Whole-design path universe

This section is required only for Whole-design Timing Audit or a global
Cross-run Comparison.

````

[skills/trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md](../skills/trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md)，第 152 至 161 行：

````text
For **Targeted Path Trace**, add only relevant sections:

```text
target selection and directed-query expansion
producer D, consumer Q, feedback, control, and hold boundaries
logic versus route diagnosis
candidate coverage for the named path or family
```

Do not add a path-universe section unless the report makes a global claim.
````

保留理由：指定路径不强制全局 endpoint universe；全局排序、覆盖和 closure 结论需要全局人口，跨运行比较也按结论选择范围。引用文件已有目录与按模式章节，类别二和四不应重复报旧问题。

### K51 trace 的映射置信度、原始证据与报告

【应保留】

原文与位置：

[skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md)，第 106 至 123 行：

````text
Pair each primitive with its following routed net. Run
[extract_timing_path.py](scripts/extract_timing_path.py) on text reports for an
initial stage table, then verify the selected block and semantic labels against
the raw report.

## Map physical stages to RTL

1. From the startpoint, follow generated net names, cell inputs, and source fanout into the path.
2. From the endpoint, trace the consuming register, memory pin, enable, or reset back to its RTL assignment.
3. Search emitted SystemVerilog, Chisel source, parameters, and Design.
4. Partition the path into regions such as decode, compare, overlay, arbitration, mux, add, correction, ready propagation, state maintenance, and memory control.
5. Label each statement `measured`, `mapped`, `inferred`, or `unknown`.

Never infer an exact LUT function from an optimized name. Query `INIT`, input
pins, driving nets, fanout, and generated-RTL correspondence when exact per-LUT
attribution matters. Read
[rtl-mapping-and-reporting.md](references/rtl-mapping-and-reporting.md) for
confidence rules and mode-sized report structures.
````

[skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md)，第 127 至 132 行：

````text
1. Report logic depth and route share independently.
2. Call a net high-fanout only from measured fanout. Call it causal only when it appears on the path with a material route segment.
3. Record sites for long routes and inspect replication, hierarchy crossings, endpoint spread, congestion, control sets, and `DONT_TOUCH`.
4. Treat parallel cones as parallel unless one ordered primitive chain traverses both.
5. Determine whether a proposed early signal starts the path or joins it mid-cone.
6. Separate BRAM `DOUT`, `ADDR`, `EN`, `WE`, and `DIN` families.
````

[skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md)，第 147 至 169 行：

````text
Count removable logic levels separately from routes. Placement replaces removed
routes with new routes, so old route delay is never a guaranteed gain. If only a
mux selector moves, state whether the data mux remains.

For every proposed register cut, measure the producer-side D cone and request:

```text
old end-to-end path
new register D input
new register Q output
feedback or maintenance path
CE, reset, flush, and hold controls
```

## Compare implementations

In Cross-run Comparison mode:

1. Record every configuration or source difference.
2. For a local claim, compare matching boundaries, physical stages, and path families.
3. For a global claim, also compare WNS, TNS, WHS, path populations, delay bins, route ratios, resources, and qualified power.
4. Track families that entered, left, or changed position in the limiting set.
5. Attribute a change to RTL only when source identity and physical evidence support it. Classify isolated route movement as implementation variance.
````

[skills/trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md](../skills/trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md)，第 205 行：

````text
Do not hand off a guaranteed nanosecond gain. Hand off a structural hypothesis and the evidence needed to accept or reject it.
````

保留理由：文本解析只能形成初始表格，语义标签还需原始报告、连接关系及 RTL 支持。并行锥、route 变动和新寄存器边界不能直接换算为收益；独立证据层级和未测范围须保留。

### K52 六份 agents/openai.yaml 为简短调用提示

【应保留】

原文与位置：

[skills/bootstrap-processor-project/agents/openai.yaml](../skills/bootstrap-processor-project/agents/openai.yaml)，第 3 至 4 行：

````text
  short_description: "安全初始化并维护处理器项目级 Agent 协作规则"
  default_prompt: "Use $bootstrap-processor-project to create or safely compare the root AGENTS.md for this processor project."
````

[skills/design-chisel-processor/agents/openai.yaml](../skills/design-chisel-processor/agents/openai.yaml)，第 3 至 4 行：

````text
  short_description: "构思Chisel处理器微架构并闭合周期语义、正确性与设计文档"
  default_prompt: "Use $design-chisel-processor to develop and document a Chisel processor microarchitecture design."
````

[skills/implement-chisel-processor/agents/openai.yaml](../skills/implement-chisel-processor/agents/openai.yaml)，第 3 至 4 行：

````text
  short_description: "文档驱动的 Chisel 处理器实现、审查与验证流程"
  default_prompt: "Use $implement-chisel-processor to implement this processor module directly from maintained Architecture and Design, update every affected source-adjacent _codex.md summary, and complete focused Verilator validation. Keep dual-subagent verification disabled unless the user explicitly requests it."
````

[skills/organize-processor-docs/agents/openai.yaml](../skills/organize-processor-docs/agents/openai.yaml)，第 3 至 4 行：

````text
  short_description: "渐进建立并维护人类优先的处理器架构、设计、研究、审查与验证文档"
  default_prompt: "Use $organize-processor-docs to establish or maintain a concise, human-first processor documentation framework."
````

[skills/optimize-chisel-fpga-timing/agents/openai.yaml](../skills/optimize-chisel-fpga-timing/agents/openai.yaml)，第 3 至 4 行：

````text
  short_description: "基于周期语义、RTL拓扑与routed DCP证据优化Chisel FPGA时序"
  default_prompt: "Use $optimize-chisel-fpga-timing to diagnose and optimize this Chisel FPGA timing path while preserving cycle semantics and validating the result with emitted RTL and routed implementation evidence."
````

[skills/trace-vivado-timing-to-rtl/agents/openai.yaml](../skills/trace-vivado-timing-to-rtl/agents/openai.yaml)，第 3 至 4 行：

````text
  short_description: "按任务范围追踪Vivado时序路径并映射到处理器RTL"
  default_prompt: "Use $trace-vivado-timing-to-rtl to select a targeted trace, whole-design audit, or cross-run comparison, map the required physical paths to processor RTL, and rank evidence-backed directions without editing the design."
````

保留理由：每份文件只含 UI 名称、短描述和调用提示，未增加另一套操作流程。implement 的默认双核验关闭、trace 的只读与选模式提示和主文件一致。重复少量入口边界有独立触发场景。

### K53 正式清单和插件元数据

【应保留】

原文与位置：

[skills/MANIFEST.md](../skills/MANIFEST.md)，第 11 至 18 行：

````text
本清单中的全部 Skill 采用木兰宽松许可证，第 2 版（`MulanPSL-2.0`）。许可证全文见仓库根目录 [LICENSE](../LICENSE)；每个 Skill 的 frontmatter 同步声明该标识。

- `bootstrap-processor-project`
- `design-chisel-processor`
- `implement-chisel-processor`
- `organize-processor-docs`
- `optimize-chisel-fpga-timing`
- `trace-vivado-timing-to-rtl`
````

[skills/MANIFEST.md](../skills/MANIFEST.md)，第 23 至 28 行：

````text
- `bootstrap-processor-project` creates or safely compares one user-owned project-root `AGENTS.md`, limited to authority, authorization, path mapping, verified tool entrypoints, and task-Skill routing. Technical methods remain in their owning Skills; environment and toolchain work remains in deterministic scripts.
- `organize-processor-docs` is a stateless Skill for a human-first processor documentation network, evidence, and review. Its new-project `doc/` default matches the bootstrap baseline; existing approved project mappings take precedence in both Skills.
- Its Bootstrap, Author, and Maintain workflows use a Design directory axis aligned with physical Chisel or RTL module topology, target-budget warnings, configurable provisional hard thresholds, two-link Architecture and Design navigation checks, encoding diagnostics, and separate handling for explanatory diagrams and evidence captures.
- Project-specific facts remain in the legacy project and user projects.
- Generated caches are excluded.
- Agent sessions, task execution, and tool calls remain Agent Runtime responsibilities. Skills do not maintain Harness workflow state.
````

[.codex-plugin/plugin.json](../.codex-plugin/plugin.json)，第 3 至 4 行：

````text
  "version": "3.0.3",
  "description": "Human-first processor architecture, Chisel implementation, verification, and FPGA timing skills for Codex.",
````

[.codex-plugin/plugin.json](../.codex-plugin/plugin.json)，第 17 至 21 行：

````text
  "skills": "./skills/",
  "interface": {
    "displayName": "WaterHand Processor Development Skills",
    "shortDescription": "Human-first processor design and Chisel engineering workflows.",
    "longDescription": "A composable Skill Package for processor architecture, documentation, cycle-accurate Chisel design, implementation, verification, and Vivado timing analysis.",
````

保留理由：清单登记六项正式 Skill，插件引用当前 skills 目录，版本和许可证一致。产品清单、插件 UI 与 Skill 指令分工清楚；历史 ZIP 不在正式清单中，应按历史内容审查。

## 5. 六类之外的准确性问题

### T01 standard Decoupled 的保持语义表述不准确

本项是接口术语与契约归属问题，缺少将其归因于旧模型能力不足的依据，单独记录，不强行归入六类，也不计入末尾六类占比。

原文与位置：

[skills/implement-chisel-processor/references/hardware-rules.md](../skills/implement-chisel-processor/references/hardware-rules.md)，第 23 至 29 行：

````text
- Classify each interface as standard `Decoupled`, no-stall pulse, atomic batch,
  prefix-valid ports, or fire-cycle-only data.
- Standard `Decoupled` producers hold `valid` and `bits` until `fire`; the Bundle
  does not enforce that behavior automatically.
- Separate admission and `ready` calculation from accepted events. Allocation,
  pointer movement, and architectural updates require the documented `fire` or
  equivalent acceptance event.
````

核对结果：Chisel 官方文档说明，DecoupledIO 本身没有规定 ready/valid 撤销与 bits 保持的保证。因此，“Standard Decoupled producers hold valid and bits until fire”把更强的项目握手契约写成了标准类型的一般要求。后半句指出 Bundle 不自动检查，仍未消除前半句的契约混淆。[Chisel Interfaces and Connections](https://www.chisel-lang.org/docs/explanations/interfaces-and-connections)。

影响：若某用户项目允许未接受请求撤销或 bits 改变，通用 Skill 可能误判合法行为并要求增加 holding register、冻结选择器或其他保护逻辑，从而改变时序和微架构。

建议方向：明确区分 Chisel 接口类型、项目选定的 ready/valid 协议以及该协议要求的保持断言。仅在项目契约要求 stalled request 保持时施加相应规则；任何特定模块的行为继续以该项目 Design 为依据。当前 register-boundary-patterns.md 已有条件化写法，可作为统一术语的参考：

[skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md](../skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md)，第 25 至 27 行：

````text
Prove mapping, payload, and validity refer to the same logical state version.
If `valid && !ready` must hold, freeze the mapping or hold both data and valid.
Keep externally visible flush handshake semantics unchanged.
````

## 6. 历史压缩包审查

ZIP 的 SHA-256：`e0629f9000575b9dd4ec871d0a327768b6c544eeee57fc65e1b0c4a308d3bf37`。

该文件保留历史材料，不在当前六项正式 Skill 清单中。下面的“需调整”表示旧写法若重新进入正式分发时需要调整；当前版本已经作出对应修订。本轮不删除、覆盖或重打包历史证据，同义历史条款不重复计入当前占比。

### H01 历史 implement 默认追加双 subagent 核验

【需调整】所属类别：五、已经过时的测试或验证要求。适用对象：历史压缩包。

原文与位置：[ChiselDevelopSkillPack.zip](../skills/ChiselDevelopSkillPack.zip)：

压缩包内 `implement-chisel-processor/SKILL.md`，第 57 至 64 行：

````text
After primary verification, dispatch two independent subagents when the environment supports them:

1. Static-review subagent: inspect source and documents for correctness, redundancy, overprotection, timing paths, dependency chains, assertion quality, and test gaps.
2. Verification subagent: independently run tests, preserve commands, seeds, logs, failures, and concise conclusions.

Give subagents raw paths and acceptance criteria. Do not leak the expected conclusion. Store their short reports in the module test directory using repository naming conventions. If subagents are unavailable, state that explicitly and perform two clearly separated local passes without claiming independence.

Address valid findings, rerun affected tests, and update reports. Do not mark the task complete while required tests fail or sessions remain active.
````

原有目的：从文字推断，原意是利用独立静态审查和重新运行测试弥补单一 Agent 的遗漏与确认偏误。未核验其最初引入时的模型背景。

标记理由：旧入口在主验证后默认再调两个角色；不可用时要求两次本地过程。当前 AGENTS.md 第 64 行及 implement 主文件第 100 至 113 行已经明确默认关闭，仅按用户请求开启，旧入口也不再与当前产品契约一致。

处理建议：如历史包被重新发布，采用当前显式开启规则。保留用户选择独立验证时的基线、角色独立和证据要求。

### H02 历史 implement 对字段和协议变化统一要求提问

【需调整】所属类别：六、过度谨慎的请示与审批措辞。适用对象：历史压缩包。

原文与位置：[ChiselDevelopSkillPack.zip](../skills/ChiselDevelopSkillPack.zip)：

压缩包内 `implement-chisel-processor/SKILL.md`，第 31 行：

````text
Ask before adding a table-entry field, changing a cross-module protocol, or adding generation/tag protection. Do not invent unspecified protocols or conservative guards.
````

原有目的：从文字推断，原意是限制 Agent 擅自加字段、改协议或添加保守身份保护。未证实该授权风险已经消失。

标记理由：旧句没有区分已决定、已授权的实现与未决架构取舍；当前入口第 38 至 41 行已经增加“不重复已回答问题”和“必要性或语义未决才问”的条件。

处理建议：复用当前写法，沿用用户明确授权；仅让未决且影响正确性或接口的部分等待用户决定。

### H03 历史 trace 不区分定向路径和全设计统计

【需调整】所属类别：三、操作步骤过于僵化。适用对象：历史压缩包。

原文与位置：[ChiselDevelopSkillPack.zip](../skills/ChiselDevelopSkillPack.zip)：

压缩包内 `trace-vivado-timing-to-rtl/SKILL.md`，第 43 至 49 行：

````text
## Build the path universe

1. Record global setup and hold closure separately.
2. Extract paths by slack, endpoint, startpoint, and logical family. Avoid a top-N list filled by bits of one bus.
3. Group paths by physical startpoint class, endpoint class, shared prefix, pipeline boundary, and event type.
4. Count each family and report its longest data delay, worst slack, logic/route split, levels, and representative path.
5. State whether the query was truncated, unconstrained, exception-filtered, or endpoint-worst only.
````

压缩包内 `trace-vivado-timing-to-rtl/SKILL.md`，第 133 至 144 行：

````text
Produce an in-place Markdown report containing:

1. Run identity and evidence boundary.
2. Setup, hold, and path-universe summary.
3. Path-family counts and representative paths.
4. Per-primitive tables with cell, following route, fanout, cumulative delay, and semantic confidence.
5. Shared-prefix and endpoint-tail analysis.
6. Source file and line mapping.
7. Coverage matrix for candidate changes.
8. Ranked modification directions.
9. Exact missing reports or Tcl queries.
10. A handoff checklist for the implementation agent.
````

原有目的：从文字推断，原意是避免只看 top-N 就推断全设计瓶颈，并确保报告足够完整。没有材料证明所有定向问题都需要全设计统计。

标记理由：旧入口对所有任务要求 path universe、family count 和固定完整报告。当前入口第 40 至 66 行以及两个参考文件已经区分定向、全设计与跨运行比较，局部结论明确允许局部人口。

处理建议：历史规则若恢复使用，替换为当前按结论选择证据范围的规则。全局 absence、ranking、coverage 和 closure 主张仍需要全局证据。

### H04 历史 optimize 先读全部模式再选模式

【需调整】所属类别：二、缺少按需加载的分层结构。适用对象：历史压缩包。

原文与位置：[ChiselDevelopSkillPack.zip](../skills/ChiselDevelopSkillPack.zip)：

压缩包内 `optimize-chisel-fpga-timing/SKILL.md`，第 70 至 83 行：

````text
## Select the smallest topology change

Read [rtl-patterns.md](references/rtl-patterns.md), then choose the narrowest applicable pattern:

|Observed topology|Preferred first experiment|
|---|---|
|Current bank state plus phase mux drives `valid` or `ready`|Expose next-state availability and register the next mapped result|
|Priority selection plus age wrap sits on an output path|Register priority results computed from the same next-state version as the entries|
|Wide line or Bundle mux precedes narrow extraction|Extract required slices in parallel, then mux the narrow values|
|A wide mux precedes the same pure transform on either selected value|Apply the transform to each candidate in parallel, then mux the narrower results|
|Global tag or ROB-head compare feeds every issue candidate|Capture a local per-entry predicate one cycle earlier|
|Small fixed dispatch width uses `PopCount`, dynamic shifts, or serial selection|Enumerate fixed count classes and precompute OH rotations|
|An invalid-lane condition only affects admission|Remove it only after proving every state mutation remains fire-gated|
|Zero-mask special case wraps `PriorityEncoderOH`|Use the encoder's natural zero output|
````

原有目的：从文字推断，原意是让 Agent 先了解可选时序变换，避免只想到熟悉模式。未发现必须完整加载所有模式的项目契约。

标记理由：旧 rtl-patterns.md 共 239 行，将寄存器、组合、协议和存储模式放在同一参考文件，入口要求先读取再选择。当前 Skill 第 73 至 81 行已拆为四类按实测路径加载，第 135 至 138 行也限定案例加载条件。

处理建议：保持当前分类导航。未来补充模式时加入对应参考文件，仅在需要比较跨类方案时同时加载多类。

历史包内“保留 backups”和已有证据的要求不等于新建备份树。已有用户资产继续受保留规则保护。旧案例中的项目名、测量值和局部参数按历史证据处理，本轮未复现其收益，也未将其转为当前通用事实。

## 7. 逐文件覆盖清单

### 7.1 当前指令与元数据

当前逐份读取 37 个指令或元数据文件；其中包括 6 个 SKILL.md、6 个 agents/openai.yaml、21 个 references 文档、2 个 AGENTS.md，以及 MANIFEST.md 和 plugin.json。F 为需调整，K 为应保留，T 为六类之外的准确性补充。

| 文件 | 本轮覆盖 |
|---|---|
| [skills/bootstrap-processor-project/SKILL.md](../skills/bootstrap-processor-project/SKILL.md) | K10、K11、K12 |
| [skills/bootstrap-processor-project/agents/openai.yaml](../skills/bootstrap-processor-project/agents/openai.yaml) | K52 |
| [skills/bootstrap-processor-project/assets/AGENTS.md](../skills/bootstrap-processor-project/assets/AGENTS.md) | K02、K13 |
| [skills/design-chisel-processor/SKILL.md](../skills/design-chisel-processor/SKILL.md) | F03、F04、K14、K15、K16、K17、K20 |
| [skills/design-chisel-processor/agents/openai.yaml](../skills/design-chisel-processor/agents/openai.yaml) | K52 |
| [skills/design-chisel-processor/references/chisel-guidance.md](../skills/design-chisel-processor/references/chisel-guidance.md) | K19 |
| [skills/design-chisel-processor/references/design-document-template.md](../skills/design-chisel-processor/references/design-document-template.md) | K18 |
| [skills/design-chisel-processor/references/review-checklist.md](../skills/design-chisel-processor/references/review-checklist.md) | K16 |
| [skills/implement-chisel-processor/SKILL.md](../skills/implement-chisel-processor/SKILL.md) | K21、K22、K23、K25、K28 |
| [skills/implement-chisel-processor/agents/openai.yaml](../skills/implement-chisel-processor/agents/openai.yaml) | K52 |
| [skills/implement-chisel-processor/references/hardware-rules.md](../skills/implement-chisel-processor/references/hardware-rules.md) | K24、T01 |
| [skills/implement-chisel-processor/references/verification-review.md](../skills/implement-chisel-processor/references/verification-review.md) | F02、K26、K27、K28 |
| [skills/organize-processor-docs/SKILL.md](../skills/organize-processor-docs/SKILL.md) | K29、K30、K31 |
| [skills/organize-processor-docs/agents/openai.yaml](../skills/organize-processor-docs/agents/openai.yaml) | K52 |
| [skills/organize-processor-docs/references/adr.md](../skills/organize-processor-docs/references/adr.md) | K36 |
| [skills/organize-processor-docs/references/architecture.md](../skills/organize-processor-docs/references/architecture.md) | K33 |
| [skills/organize-processor-docs/references/bootstrap.md](../skills/organize-processor-docs/references/bootstrap.md) | K32 |
| [skills/organize-processor-docs/references/design.md](../skills/organize-processor-docs/references/design.md) | F05、K34 |
| [skills/organize-processor-docs/references/maintenance.md](../skills/organize-processor-docs/references/maintenance.md) | F01、K39 |
| [skills/organize-processor-docs/references/protocol-lifecycle.md](../skills/organize-processor-docs/references/protocol-lifecycle.md) | K35 |
| [skills/organize-processor-docs/references/research-review.md](../skills/organize-processor-docs/references/research-review.md) | K37 |
| [skills/organize-processor-docs/references/verification.md](../skills/organize-processor-docs/references/verification.md) | K38 |
| [skills/optimize-chisel-fpga-timing/SKILL.md](../skills/optimize-chisel-fpga-timing/SKILL.md) | K40、K41、K42 |
| [skills/optimize-chisel-fpga-timing/agents/openai.yaml](../skills/optimize-chisel-fpga-timing/agents/openai.yaml) | K52 |
| [skills/optimize-chisel-fpga-timing/references/case-studies.md](../skills/optimize-chisel-fpga-timing/references/case-studies.md) | K48 |
| [skills/optimize-chisel-fpga-timing/references/combinational-data-patterns.md](../skills/optimize-chisel-fpga-timing/references/combinational-data-patterns.md) | K43 |
| [skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md](../skills/optimize-chisel-fpga-timing/references/physical-control-patterns.md) | K46 |
| [skills/optimize-chisel-fpga-timing/references/protocol-storage-patterns.md](../skills/optimize-chisel-fpga-timing/references/protocol-storage-patterns.md) | K45 |
| [skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md](../skills/optimize-chisel-fpga-timing/references/register-boundary-patterns.md) | K44 |
| [skills/optimize-chisel-fpga-timing/references/vivado-evidence.md](../skills/optimize-chisel-fpga-timing/references/vivado-evidence.md) | K47 |
| [skills/trace-vivado-timing-to-rtl/SKILL.md](../skills/trace-vivado-timing-to-rtl/SKILL.md) | F02、K49、K50、K51 |
| [skills/trace-vivado-timing-to-rtl/agents/openai.yaml](../skills/trace-vivado-timing-to-rtl/agents/openai.yaml) | K52 |
| [skills/trace-vivado-timing-to-rtl/references/evidence-and-queries.md](../skills/trace-vivado-timing-to-rtl/references/evidence-and-queries.md) | K50 |
| [skills/trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md](../skills/trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md) | K50、K51 |
| [AGENTS.md](../AGENTS.md) | K01、K02、K03、K04、K05、K06、K07、K08、K09 |
| [skills/MANIFEST.md](../skills/MANIFEST.md) | K53 |
| [.codex-plugin/plugin.json](../.codex-plugin/plugin.json) | K53 |

### 7.2 脚本及测试的指令契约

脚本作为执行证据和验证要求的依据读取，其代码语句不作为额外自然语言指令计数。本轮报告没有修改脚本，未为静态审查重新运行处理器测试。

| 文件 | 核对内容与结论 |
|---|---|
| [check_docs.py](../skills/organize-processor-docs/scripts/check_docs.py) | CLI、默认根目录、自定义 --root、编码、预算策略及输出分支；F01 确认 --json 仅改变展示。检查器自身持续有用。 |
| [test_check_docs.py](../skills/organize-processor-docs/scripts/test_check_docs.py) | 目录映射、导航、链接、图源、编码和预算等边界用例，属于确定性工具回归，保留。 |
| [test_skill_package.py](../skills/organize-processor-docs/scripts/test_skill_package.py) | frontmatter、描述上限、引用、UI 元数据、文档契约及参考文件预算；未因部分断言匹配措辞而认定测试过时。后续改写需同步受影响契约。 |
| [extract_timing_path.py](../skills/trace-vivado-timing-to-rtl/scripts/extract_timing_path.py) | 路径过滤、选择、解析、输出和失败出口；脚本只生成初始 stage table，保留原始报告及语义核对要求。 |

### 7.3 历史压缩包逐文件覆盖

历史 ZIP 包含 18 个 Markdown/YAML 指令文件和 1 个 Python 脚本。“相同”指与当前同路径文件 SHA-256 一致；其他条目已读取差异，当前新增的 license 行也会导致哈希不同。

| ZIP 内路径 | 与当前同路径比较 | 覆盖与处理 |
|---|---|---|
| `design-chisel-processor/agents/openai.yaml` | 相同 | K14 至 K20；入口另见 F03、F04 |
| `design-chisel-processor/references/chisel-guidance.md` | 相同 | K14 至 K20；入口另见 F03、F04 |
| `design-chisel-processor/references/design-document-template.md` | 相同 | K14 至 K20；入口另见 F03、F04 |
| `design-chisel-processor/references/review-checklist.md` | 相同 | K14 至 K20；入口另见 F03、F04 |
| `design-chisel-processor/SKILL.md` | 有差异 | K14 至 K20；入口另见 F03、F04 |
| `implement-chisel-processor/agents/openai.yaml` | 有差异 | K21 至 K28；默认核验与提问旧规则见 H01、H02 |
| `implement-chisel-processor/references/hardware-rules.md` | 有差异 | K21 至 K28；默认核验与提问旧规则见 H01、H02 |
| `implement-chisel-processor/references/verification-review.md` | 有差异 | K21 至 K28；默认核验与提问旧规则见 H01、H02 |
| `implement-chisel-processor/SKILL.md` | 有差异 | K21 至 K28；默认核验与提问旧规则见 H01、H02 |
| `optimize-chisel-fpga-timing/agents/openai.yaml` | 相同 | K40 至 K48；入口加载规则见 H04 |
| `optimize-chisel-fpga-timing/references/case-studies.md` | 有差异 | 历史项目案例，保留来源归属，当前通用案例见 K48 |
| `optimize-chisel-fpga-timing/references/rtl-patterns.md` | 当前已拆分为多个参考文件 | H04；具体硬件条件见 K43 至 K46 |
| `optimize-chisel-fpga-timing/references/vivado-evidence.md` | 有差异 | K40 至 K48；入口加载规则见 H04 |
| `optimize-chisel-fpga-timing/SKILL.md` | 有差异 | K40 至 K48；入口加载规则见 H04 |
| `trace-vivado-timing-to-rtl/agents/openai.yaml` | 有差异 | K49 至 K51；任务范围旧规则见 H03 |
| `trace-vivado-timing-to-rtl/references/evidence-and-queries.md` | 有差异 | K49 至 K51；任务范围旧规则见 H03 |
| `trace-vivado-timing-to-rtl/references/rtl-mapping-and-reporting.md` | 有差异 | K49 至 K51；任务范围旧规则见 H03 |
| `trace-vivado-timing-to-rtl/scripts/extract_timing_path.py` | 相同 | 与当前脚本相同，见 7.2 |
| `trace-vivado-timing-to-rtl/SKILL.md` | 有差异 | K49 至 K51；任务范围旧规则见 H03 |

## 8. 交付校验与仍未验证的事项

本次唯一写入是 `report/SKILL_INSTRUCTION_REVIEW.md`。交付检查使用 `git status --short`、`git diff --check`，并将 42 个原有范围文件的 SHA-256 与审查读取时的值逐一对比；同时检查本报告的本地链接、引文行范围、编号和占比。

检查结果：42 个原有文件的 SHA-256 全部一致，Git 状态只列出本报告这一新增文件，HEAD 保持输入基线。186 处本地链接指向的 46 个不同文件全部存在，131 处当前原文引用及历史引用与读取内容一致。F/K/H/T 编号连续，引用代码围栏闭合，无行尾空白，六类与保留项比例合计 100.0%。`git diff --check` 返回 0；新增文件另行通过上述内容检查。

报告级检查与产品测试分开。没有修改 Skill 或脚本，未触发“修改 Skill 后运行 validate-skills”的门禁；本轮不借此宣称产品测试通过。硬件示例未逐一在不同 Chisel/Verilator/Vivado 版本上执行；T01 为已通过官方文档核对的具体术语问题，其他领域规则保留的是当前用途与契约，未形成全面实现认证。

后续若授权调整，F01 可先做最小文档改写；F02 至 F05 应保持原先的正确性与授权条件，并用相应局部任务确认不会强制重复工作。T01 应统一有关 ready/valid 术语并核对项目协议。公开调用方式或职责发生变化时，还需同步 README、USER_GUIDE、MANIFEST，执行 validate-skills 及受影响测试。这些后续修改均未在本轮执行。

## 9. 计数口径与粗略占比

计数单位是本报告中编号的“当前指令组”，共 58 组，即 F01 至 F05 和 K01 至 K53。同一目的的一段步骤或清单合为一组；同义重复引用只算一次。一个文件可以包含多个组，一个组可以跨文件。该占比描述本报告的审查判定分布，不代表逐行字符比例、文件故障率或实际模型失败率。

历史 H01 至 H04 已由当前写法处理，仅单列历史比较，避免再次计入当前缺陷。T01 属于六类之外的技术术语问题，单独披露。按主要问题归类，无跨类重复计数。

| 类别 | 条目数 | 占 58 组比例 |
|---|---:|---:|
| 一、描述过长或宽泛 | 0 | 0.0% |
| 二、缺少按需分层 | 0 | 0.0% |
| 三、步骤过于僵化 | 3 | 5.2% |
| 四、强制完整上下文 | 0 | 0.0% |
| 五、验证要求中的重复执行 | 2 | 3.4% |
| 六、过度请示审批 | 0 | 0.0% |
| 应保留 | 53 | 91.4% |

粗略占比（当前 58 组）：第一类 0.0%，第二类 0.0%，第三类 5.2%，第四类 0.0%，第五类 3.4%，第六类 0.0%，应保留 91.4%。
