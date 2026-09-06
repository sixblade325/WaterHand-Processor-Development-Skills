# PA3-DEFECT-015：异步 Memory 写回被错误绑定到实验完成

状态：已修复并通过完整回归，run-003 已按修订协议封存

发现日期：2026-09-04

来源：`dual_issue_demo_V2` run-003 两组结果收尾

## 产品责任

A/B 实验需要证明两组从相同 Memory 起点启动、主线程实际获得初始化上下文、运行期间保持 home 隔离。工程结果是否可比较不应依赖主线程退出后异步生成的新 Memory 摘要。

## 现场证据

冻结 `RUN_CONFIG` 将 `post_write` 设为 `requiredPostState`，正式 trigger launcher 在 Codex 进程退出后继续轮询 durable Memory inventory，默认超时 900 秒，并要求连续稳定 10 秒。

run-003 中出现以下行为：

1. Skill 与 Control 主线程均已正常退出并提交干净候选。
2. 两组从相同空 `MEMORY.md` 和相同初始化摘要启动，主 rollout 均包含首个 user 之前的结构化 `## Memory` developer block。
3. Skill trigger 正常退出后，异步写回没有立即形成符合旧 `post_write` 定义的新增证据，launcher 继续等待。
4. Control trigger 又受到 Codex home 动态 inventory 误报影响，工程结果收尾被 Memory 证据路径阻塞。
5. 用户先取消一小时 idle，随后明确要求删除退出后的 Memory 等待并尽快完成比较。
6. `scripts/run-experiment-codex-session.ps1` 已移除 post-exit 轮询参数与等待循环。旧 audit、文档和 `test-memory-isolation.ps1` 仍要求 `postExitMemoryObservation`，当前实现与验收表述不一致。

当前运行修订位于：

```text
E:\107\.runtime\dual_issue_demo_V2\run-003\evidence\protocol-amendment-remove-memory-idle-gate.json
```

## 影响

1. 已完成的处理器实现和独立仿真结果无法及时进入报告与封存。
2. 异步 Memory 调度延迟被计入实验组织时间，不能反映工程团队能力。
3. launcher、audit、RUN_CONFIG template、协议文档与回归测试出现语义分裂。
4. 结果封存依赖不可预测的后台写回时机，实验可能在处理器验收通过后继续等待数十分钟。

## 目标行为

1. `pre` 必须证明 `configured` 与 `initialized`。
2. `post` 必须证明主 session 的 `session_read`、候选 commit、退出证据和两组隔离。
3. `post_write` 保留为可选诊断，不作为候选比较和结果封存的前置门禁。
4. formal trigger 在用户显式请求时运行，进程退出后立即返回，不轮询异步 Memory 文件。
5. Memory 读取与生成继续在两组主线程中同时启用。
6. 两组仍从逐字节相同的初始化 Memory 快照启动，仍禁止跨组读取。

## 关闭条件

1. launcher 不再提供或读取 post-exit observation timeout 与 stability 参数。
2. `RUN_CONFIG.template.json` 的必需 post 状态为 `session_read`。
3. audit 能在没有 trigger 的情况下完成普通 post 审计，并可通过显式选项执行严格 `post_write` 诊断。
4. 文档明确区分初始化 probe 的必要写回验证与工程主线程结束后的可选写回观察。
5. 回归覆盖无 trigger 的正常完成、显式严格诊断和两组隔离失败路径。
6. run-003 报告披露本次协议修订，不把未执行的异步写回声明为已验证。

## 修复结果

1. `scripts/run-experiment-codex-session.ps1` 在 main 或可选 trigger 进程退出后立即返回。
2. `scripts/audit-experiment-context.ps1` 以 `session_read` 作为普通 post 门禁，`-RequirePostWrite` 保留严格写回诊断。
3. `RUN_CONFIG.template.json`、实验入口、Memory 隔离说明和对照协议已经同步。
4. Memory 隔离测试覆盖无 trigger 的正常完成、可选 trigger 立即返回和显式 `post_write` 诊断。
5. `Experiment\tests\run.cmd` 于 2026-09-04 完整通过。
6. run-003 修订记录为 `protocol-amendment-session-read-closure.json`，报告不得把可选写回描述为已验证。

## 分支预测实验的快照同步修复

2026-09-06 核验 `branch-prediction-ab-001` 时，确认其历史处理器快照仍携带修复前的 launcher、audit、模板和测试。首次准备仅在运行配置中声明 `no_wait`，处理器的 24/24 验收没有覆盖 Memory 收尾。该配置字段本身不能消除旧代码中的轮询。

用户明确要求修复后，实验公共基线更新为 `697bb292f853ac8450d056b5302bfa06825fd89a`，两组独立副本同步到该 commit。修复同步了退出即返回、普通 `session_read` 门禁及零 idle 配置依赖，并为本次冻结配置提供 `manager/run-arm.ps1` 入口。正常收尾不创建 trigger，不等待 Memory 写回；缺少应有的读取证据时直接报告失败。

Memory 隔离专项回归通过。新增 fixture 在完全不写回 Memory 的条件下，launcher 于 1.025 秒返回，before/after inventory 相同。普通 post 无 trigger、显式严格写回诊断、污染失败路径均由回归覆盖。两组实际配置的 check 通过，两组未授权 run 均在创建会话前被拒绝。

证据位于：

- [修订记录与旧输入内容](E:/107/.runtime/dual_issue_demo_V2/branch-prediction-ab-001/evidence/memory-closure-amendment.json)
- [Memory 专项回归](E:/107/.runtime/dual_issue_demo_V2/branch-prediction-ab-001/evidence/memory-isolation-20260905T232237Z.log)
- [实际启动入口预检](E:/107/.runtime/dual_issue_demo_V2/branch-prediction-ab-001/evidence/launch-entry-precheck.json)

## 保留风险

普通 post 不再证明主线程退出后的异步 Memory 写回。该证据只在显式运行 trigger 并传入 `-RequirePostWrite` 时产生。
