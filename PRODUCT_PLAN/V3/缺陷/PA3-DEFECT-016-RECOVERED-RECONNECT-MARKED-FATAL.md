# PA3-DEFECT-016：已恢复的重连事件被误判为会话失败

状态：已确认，修复待实现  
发现日期：2026-09-04  
来源：`dual_issue_demo_V2` run-003 Control 组结果封存

## 产品责任

实验会话证据解析器需要区分终止运行的错误与 Codex CLI 已自行恢复的重连事件。唯一 thread ID、最终 `turn.completed`、进程退出码和持久 rollout 可以共同证明会话是否完成。

## 现场证据

Control main stdout 中包含四条 `type=error` 的重连消息：

```text
Reconnecting... 2/5
Reconnecting... 3/5
Reconnecting... 4/5
Reconnecting... 5/5
```

同一 stdout 随后包含 `turn.completed`。进程退出码为 0，候选提交为 `86ffc7c6881c614e6b7e56e8c3b483a8367d5f41`，独立组织者的 15 项仿真全部通过。

`scripts/memory-evidence.ps1` 中的 `Get-PaExecStdoutEvidence` 当前把任意 `type` 匹配 `failed|error` 的 record 设为失败。因此：

1. `control-main.exit.json` 的 `threadId` 为 null。
2. post 审计无法通过标准 exit binding 找到主 rollout。
3. 封存时需要从首条 `thread.started` 和持久 rollout 的 `session_meta` 恢复 thread ID。

原始证据：

```text
E:\107\.runtime\dual_issue_demo_V2\run-003\evidence\control-main.stdout.jsonl
E:\107\.runtime\dual_issue_demo_V2\run-003\evidence\control-main.exit.json
E:\107\.runtime\dual_issue_demo_V2\run-003\homes\control\sessions\2026\09\04\rollout-2026-09-04T20-47-20-01a06c75-96bb-75b1-85da-2b00f23d9ded.jsonl
```

## 影响

1. 已成功完成的工程会话可能无法进入自动封存。
2. retry 期间的可观测错误被保留，这是必要证据；当前判定逻辑丢失了错误是否恢复的语义。
3. 自动生成的 exit evidence 与持久 rollout 对同一 thread 的结论不一致。

## 目标行为

1. 保留所有 error record、重连次数和消息原文 hash。
2. 将可恢复重连与终止性错误分开分类。
3. 存在唯一 `thread.started`、最终 `turn.completed` 且进程退出码为 0 时，重连消息记录为 `recovered_transport_error`。
4. 缺少最终完成事件、出现多个 thread ID 或进程非零退出时继续失败。
5. exit evidence 始终记录可恢复错误数量和最终 thread ID 来源。

## 关闭条件

1. stdout 解析器具有 retryable、recovered 和 terminal 三类结果。
2. 回归覆盖重连后完成、重连后失败、多个 thread ID、无 `turn.completed` 和非零退出。
3. post 审计无需人工恢复即可绑定 run-003 同型证据。
4. 不修改 run-003 既有 stdout、exit evidence 和 rollout。
