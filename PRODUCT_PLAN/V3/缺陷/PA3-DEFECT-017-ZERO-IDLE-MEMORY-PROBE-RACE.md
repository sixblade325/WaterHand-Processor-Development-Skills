# PA3-DEFECT-017：零 idle Memory 初始化把摘要归因固定在错误会话

状态：run-004 已使用隔离兼容封存继续运行，通用修复待实现

发现日期：2026-09-05

来源：`dual_issue_demo_V2` run-004 启动初始化

## 产品责任

Memory 初始化器需要从真实 Codex 会话取得共同摘要，并将逐字节相同的起点部署给 Skill 与 Control。`min_rollout_idle_hours = 0` 时，摘要可能在 seed 会话退出前后生成。初始化器必须接受整个双会话初始化窗口内可归因的真实摘要。

## 现场证据

1. seed 会话 `01a06d60-2c17-7de3-9d32-509c0ac7c2dc` 正常退出，并在其 after inventory 中记录真实生成的 `memory_summary.md`。
2. trigger 会话 `01a06d63-025d-7a60-bae7-be9f1dd27625` 从 seed after inventory 启动，其 before 与 after inventory 相同。
3. `run-memory-initialization-probe.ps1` 继续等待 trigger 后新增 durable delta，无法及时返回。
4. `bootstrap-experiment-memory.ps1` 只接受归因于 trigger 的 summary 时间戳和内容 delta，因此拒绝已经由 seed 生成的真实摘要。
5. seed 最终消息包含 `MEMORY_PROBE_COMPLETE.`。检查器要求无尾随标点的精确结尾，进一步造成证据误拒绝。

原始证据位于：

```text
E:\107\.runtime\dual_issue_demo_V2\run-004\evidence\probe-seed.exit.json
E:\107\.runtime\dual_issue_demo_V2\run-004\evidence\probe-trigger.exit.json
E:\107\.runtime\dual_issue_demo_V2\run-004\homes\probe\memories\memory_summary.md
```

## 影响

1. 零 idle 配置会使已成功生成 Memory 摘要的初始化流程等待到超时。
2. 实验启动时间被无意义的 post-exit 观察占用。
3. 初始化状态机把摘要生成会话选择写成固定事实，无法覆盖 Codex 的合法异步调度。

## run-004 隔离处理

1. 停止只等待新增 delta 的外层观察进程，保留两份真实 session 和全部原始证据。
2. 兼容封存器接受 seed 开始至 trigger 结束之间生成的摘要。
3. 兼容封存器仍要求两个不同的持久 session、空 `MEMORY.md`、合法 rollout、干净 stderr、绑定的 Codex executable、相同起止 inventory 链和稳定摘要 hash。
4. Skill 与 Control 正式 home 获得逐字节相同的空 `MEMORY.md` 和 `memory_summary.md`。
5. 该兼容逻辑只位于 `processor_agent/.runtime/`，未写入产品脚本或用户处理器项目。

## 目标行为

1. 初始化摘要可以归因于 seed、trigger 或两者之间的异步 Memory worker。
2. 已存在稳定有效摘要时，trigger 不要求制造第二次内容变化。
3. completion marker 应按独立标记行解析，并容忍普通句末标点。
4. 正式完成门禁继续使用 `session_read`。

## 关闭条件

1. 双 session 初始化状态机显式建模 summary owner 和生成时间窗口。
2. 回归覆盖摘要由 seed 生成、由 trigger 生成和 trigger 后异步生成三种时序。
3. 零 idle 初始化不再等待无必要的 900 秒超时。
4. 两组 pre audit 均达到 `initialized`，主 session post audit 能达到 `session_read`。
