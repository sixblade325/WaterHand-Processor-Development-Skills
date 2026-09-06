# PA3-DEFECT-013：文档任务未触发文档组织 Skill

状态：已取得 run-003 现场证据，Skill 选择与验收闭环待修复，不阻塞本轮实验  
发现日期：2026-09-04  
来源：`dual_issue_demo_V2` run-003 Skill 组 Design 建立过程

## 产品责任

Skill Package 需要让匹配任务稳定进入对应 Skill。建立或重构处理器 Design 时，应组合使用 `organize-processor-docs` 与 `design-chisel-processor`，并留下可检查的调用和门禁证据。仅把 Skill 放入可发现清单无法证明其规则参与了工作。

## 现场证据

对 run-003 Skill 组全部非 guardian session 的 `CommandExecution` 进行检查，结果如下：

1. 主线程读取了 `implement-chisel-processor/SKILL.md` 和 `design-chisel-processor/SKILL.md`。
2. `design_docs` subagent 于 `2026-09-04T11:04:23.350Z` 读取了 `design-chisel-processor/SKILL.md`。
3. 没有会话读取 `organize-processor-docs/SKILL.md` 或其 `references/design.md`。
4. 没有会话运行 `organize-processor-docs/scripts/check_docs.py`。

冻结的 `organize-processor-docs` 明确要求：

1. 以 `doc/Design/` 中的物理模块视图作为主目录轴。
2. 模块视图尽量对齐稳定 Chisel 或 RTL 实例层级与职责边界。
3. 独立拥有职责、状态、接口或维护生命周期的稳定实例模块通常建立独立模块目录和 `README.md`。

当前候选已经形成 `Frontend`、`DecodeStage`、`InstructionQueue`、`RegFile`、`IssueStage`、`ExecuteStage`、`MemoryStage`、`RetireStage`、`Control` 与 `DualIssueCore` 等稳定模块。Design 仍由以下四个平级文件承担：

```text
Design/README.md
Design/PIPELINE.md
Design/PROTOCOLS.md
Design/VERIFICATION.md
```

模块职责集中在总表和跨模块文档中，没有形成 Skill 要求的模块主轴。该结果与源码保持了表格映射，未完成模块级文档 authority 的建立。

## 影响

1. Treatment 组安装了文档 Skill，实际工作没有使用该 Skill，实验无法直接归因其文档效果。
2. Skill 中的物理模块拓扑、目录组织、两跳阅读路径和长度门禁均未进入确定性检查。
3. `design-chisel-processor` 与 `organize-processor-docs` 的触发范围重叠时，Agent 可能只选择周期语义 Skill。
4. 用户需要在结果阶段人工发现文档结构偏差。

## 当前边界

1. 本轮实验继续运行，不向候选线程补发 Skill 指令，不重写其 Design。
2. 该记录评价 Skill 选择和产品门禁，不把候选处理器的具体设计内容写入通用 Skill。
3. 修复不得要求用户逐次点名所有伴随 Skill。

## 通用关闭条件

1. 处理器 Design 建立任务能够稳定触发 `organize-processor-docs` 和必要的 `design-chisel-processor`。
2. 运行证据明确记录实际读取的 Skill 入口、版本与检查器结果。
3. 文档检查器能够报告缺失的物理模块 authority、Design 到 Source 映射和目录根偏差。
4. 回归覆盖已有根级 `Architecture/Design` 项目向 `doc/Architecture` 与 `doc/Design` 迁移或显式兼容的场景。
5. A/B Treatment prompt 不需要硬编码处理器模块名，Control 组仍无法访问产品 Skill。
