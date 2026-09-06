# processor_agent 协作规则

## 0. 最高优先级

1. 用户对当前任务的明确指令决定任务目标、授权范围和交付形式。
2. 用户明确作出的决定与当前 Git 权威材料共同构成正式依据。用户后续的一般表述视为修改意图。只有用户明确声明替换既有事实时，才更新正式事实。
3. 回答问题、Review、诊断或修改前，先读取直接相关的计划、文档、源码、测试和本地协作约束。
4. 未完成相关材料读取和证据核对时，不输出确定性技术结论。无法核验时，直接说明缺少的文件、代码路径、工具输出或输入条件。
5. 明确区分当前已实现行为、当前正式计划、实验结果、历史材料和新建议。
6. 回答和人类可读文档默认使用中文。模块名、信号名、字段名、文件名、命令和代码保持英文。
7. Windows PowerShell 读取 UTF-8 文档时必须使用 `Get-Content -Raw -Encoding utf8 -LiteralPath <path>` 或 `scripts\read-text.cmd <path>`，不得依赖默认编码。
8. 永远不要使用先否定 A 再转折替换为 B 的中文对照句式。不要出现破折号。
9. 不使用先模糊认可再转折纠错的套话。发现错误时直接说明位置、证据和影响。
10. 回答保持客观、直接，零吹捧，零情绪。
11. 除非用户明确要求状态，否则不发送中途状态回报，不描述正在执行或将要执行的动作。完成后直接交付结果。
12. Agent 的建议、草案、默认项和推断均不等于用户决定，不得标记为已确认或已批准。
13. 回答、解释、Review 和诊断任务默认只读。用户明确要求修改、实现、运行或发布时，才执行对应写入或外部操作。
14. 不扩大用户授权范围。写权限、外部副作用、破坏性操作或架构取舍不明确时，先取得用户授权。
15. 现有工作树修改属于用户资产。保留无关修改，不使用破坏性 Git 命令清除或覆盖它们。

## 1. 仓库职责

1. 本仓库维护 WaterHand Processor Development Skills、Codex plugin manifest、环境与工具链契约、确定性脚本、工具级测试、发布材料和产品计划。
2. 产品依赖 Codex 提供会话、上下文、文件编辑、工具调用和 Agent 执行能力。
3. 当前产品不维护独立 Harness、Stage、Task、Run、Approval、Agent Executor 或第二份处理器模型。
4. 具体处理器的 Architecture、Design、Source、Verification 和工程结论进入对应用户项目。
5. 龙芯杯、WaterHand、LoongArch、Zircon 和其他项目材料只作为来源或案例。通用产品中不复制其源码、设计正文和项目专属事实。
6. A/B 对照、最小处理器示例和行为 eval 属于实验资产，不构成可运行产品的必需部分。

## 2. 权威文档与事实归属

1. `PRODUCT_PLAN/V3/PRODUCT_PLAN.md` 是当前产品总纲，维护产品定位、职责边界、Skill 体系和验收标准。
2. `PRODUCT_PLAN/V3/RUNNABLE_PRODUCT_AND_EXPERIMENT_BOUNDARY.md` 定义可运行产品、Execution Support Kit 和实验资产的边界。
3. `PRODUCT_PLAN/V3/SKILL_PACKAGE_COMPARATIVE_EVALUATION.md` 定义当前 A/B 对照评测协议。具体运行状态由对应 readiness、precheck 和证据文件表达。
4. `README.md` 是产品入口，`USER_GUIDE.md` 是用户操作入口。安装、命令或 Skill 使用方式变化时同步更新相应入口。
5. `skills/<name>/SKILL.md` 定义对应正式 Skill 的方法、输入、输出、权限边界和门禁。`skills/MANIFEST.md` 维护正式 Skill 清单。
6. `environment/README.md` 与 `environment/toolchains.json` 定义当前环境和工具链契约。
7. `PRODUCT_PLAN/V2/`、`PRODUCT_PLAN/V1/`、`Logs/` 和其他历史材料保留设计过程，不指导当前实现，除非 V3 权威文档明确引用其结论。
8. `PRODUCT_PLAN/V3/缺陷/` 记录已确认的产品或实验基础设施缺陷。缺陷状态以索引和具体缺陷文档的当前内容为准。
9. 同一规范性事实只在一个权威文档中完整定义，其他位置使用摘要和链接。
10. 新建议必须标明提议状态。实验观察必须绑定运行、时间、输入基线和证据路径。

## 3. 用户项目边界

1. 框架读取用户项目时，先读取该项目的 `AGENTS.md`。
2. 项目内 Architecture 和 Design 决定实现约束，框架默认值不能覆盖项目事实。
3. 框架只通过明确接口读写用户项目，不依赖本机绝对路径。
4. 通用逻辑不得硬编码 `dual_issue_demo` 或龙芯杯项目的模块名、信号名和流水级。
5. 用户项目的人类可读文档默认使用中文，模块名、信号名、字段名、文件名、命令和代码保持英文。
6. 新项目缺少 `AGENTS.md` 时，可以依据 `bootstrap-processor-project` 基线生成严格协作约束。已有 `AGENTS.md` 默认保留，增量修改需要用户确认。
7. 用户项目的 Architecture、Design、Source 和 Verification 始终由该项目及其 Git 历史维护。Skill Package 不生成可覆盖它们的平行权威表示。

## 4. Skill 与安装包规则

1. 每个正式 Skill 使用独立目录，并以 `SKILL.md` 为入口。一个正式 Skill 只保留一份。
2. Skill 描述可复用方法、输入、输出、权限边界、门禁、检查项和必要参考材料。
3. 项目专属事实、源码摘录、临时搜索结果和运行日志不得进入 Skill。
4. 从遗产提炼 Skill 时，先区分通用规则与具体项目规则，并保留来源和验证依据。
5. 修改 Skill 后运行 `scripts\run.cmd validate-skills`，执行受影响的测试，并记录受影响的工作流。
6. Skill 的公开调用方式或职责边界变化时同步更新 `README.md`、`USER_GUIDE.md` 和 `skills/MANIFEST.md` 中的相关内容。
7. 安装包只包含运行所需的 plugin、Skill、工具、环境契约、脚本和用户文档。产品计划、日志、测试、缓存和实验运行结果不得进入正式安装包。
8. `bootstrap-processor-project` 只创建或提议更新用户项目根目录 `AGENTS.md`。环境和工具链工作由确定性脚本承担。
9. `organize-processor-docs` 负责信息架构和写作约束。周期精确语义由 `design-chisel-processor` 负责。
10. `implement-chisel-processor` 要求同步维护源码旁 `_codex.md`。双 subagent 核验默认关闭，只在用户明确要求时开启。
11. 本仓库许可证以根目录 `LICENSE` 为准，统一标识为 `MulanPSL-2.0`。插件、Skill、安装包元数据和发布文档保持一致；保留第三方材料、外部工具及用户项目各自的许可证归属。

## 5. 环境与确定性脚本

1. 当前产品运行环境固定为纯 Windows x86-64。MSYS2 UCRT64 只作为 Windows 内部工具链。
2. 用户初始化的统一入口是 `scripts\initialize.cmd`。环境诊断使用 `scripts\doctor.cmd`，Chisel 命令使用 `scripts\chisel-run.cmd`。
3. 脚本负责工具探测、参数转发、进程级环境、结构化结果、退出码和运行产物位置。Agent 负责选择操作并解释证据。
4. 环境变量或工具没有进入 `PATH` 时，使用已声明的 `PROCESSOR_SKILLS_*` 配置接口。通用逻辑不写入用户名、本机工具绝对路径或临时盘符。
5. 未经用户明确授权，不修改全局 `PATH`、系统包、WSL、Vivado 许可证或仓库外工具安装。
6. 脚本修改必须有对应测试。命令转发、编码、路径、退出码或工具探测变化需要覆盖 Windows 边界条件。
7. 原始日志、缓存、生成文件、临时工作树和一次性产物进入仓库或用户项目指定的 `.runtime/`。

## 6. 实验资产与隔离

1. 实验资产验证产品效果，不得把一次实验的处理器事实或临时绕行写入通用 Skill 和产品主线。
2. 正式 A/B 运行使用冻结的 baseline、prompt、`RUN_CONFIG`、Skill Package、Memory 起点、工具链和验收器。
3. Skill 与 Control 使用独立 repository、Codex home、Memory、日志和结果目录。两组不得读取彼此的会话、工作树、决定和结果。
4. 正式实验线程只在用户明确要求后启动。Skill 组结果完成封存并取得用户确认后，才允许启动 Control 组。
5. 人类干预进入对应正式 thread，并按连续语义主题归档。基础设施恢复与技术设计干预分开记录，技术干预对对照有效性的影响必须在结果中披露。
6. 运行中发现产品缺陷时，将通用问题记录到 `PRODUCT_PLAN/V3/缺陷/`。实验专属修复留在隔离实验目录，避免扩大产品主线。
7. 未经用户确认，不清理、覆盖或复用既有实验运行证据。

## 7. 变更与交付要求

1. 修改范围保持在当前功能涉及的模块内。发现相邻问题时记录为未解决问题。
2. 新增目录、Schema、状态或抽象前，说明其长期职责、所有者、生命周期和退出条件。
3. 代码变更需要相应测试，工作流变更需要最小端到端样例，文档变更需要链接、格式和事实一致性检查。
4. 不创建 `v1`、`v2`、`final` 或备份目录保存当前内容。Git 管理历史版本。
5. 未经用户确认，不删除遗产项目、缓存、生成物、实验证据或用户维护的正式材料。
6. 交付时报告修改文件、对应权威材料、验证命令、验证结果、风险和未解决问题。
