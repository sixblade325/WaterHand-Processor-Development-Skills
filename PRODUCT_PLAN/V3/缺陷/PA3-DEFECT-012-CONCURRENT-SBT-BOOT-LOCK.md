# PA3-DEFECT-012：并发 Agent 争用全局 sbt boot lock

状态：已取得 run-003 现场证据，通用修复待实现，本轮墙钟比较已归一化  
发现日期：2026-09-04  
来源：`dual_issue_demo_V2` run-003 Skill 组并发实现与编译

## 产品责任

产品允许主线程并发调度多个实现 Agent，固定 Chisel 命令入口需要保证同一 Windows 用户下的并发构建具有确定行为。构建进程应等待可用构建槽位，或使用经过验证的隔离缓存和 boot 目录，不能让用户级 sbt 锁争用直接形成随机编译失败。

## 现场证据

Skill 组多个 Agent 从同一候选工作树并发执行 `scripts\compile.cmd`，三个独立会话均在 sbt launcher 阶段失败：

```text
java.io.FileNotFoundException:
C:\Users\13926\.sbt\boot\sbt.boot.lock (拒绝访问。)
```

具体记录：

1. `frontend_impl` 于 `2026-09-04T11:15:22.112Z` 失败，session JSONL 第 144 行。
2. `decode_queue_impl` 于 `2026-09-04T11:17:22.051Z` 失败，session JSONL 第 188 行。
3. 主线程于 `2026-09-04T11:21:27.953Z` 失败，session JSONL 第 571 行。
4. 全部直接 subagent 已完成后，主线程于 `2026-09-04T11:53:01.374Z` 再次因同一锁失败，证明用户级全局锁还会受到同机其他 sbt 进程影响。
5. Control 组主线程于 `2026-09-04T12:59:42.773Z` 执行 `scripts\compile.cmd` 时再次命中同一 `C:\Users\13926\.sbt\boot\sbt.boot.lock` 拒绝访问，session JSONL 第 391 行。随后 `verification_strategy` 报告 `scripts\test.cmd` 也因并发 sbt lock 未能启动。该缺陷已在 A/B 两组独立复现。

对应证据文件位于：

```text
E:\107\.runtime\dual_issue_demo_V2\run-003\homes\skill\sessions\2026\09\04\
```

锁争用结束后，相同工作树中的后续 `scripts\compile.cmd` 返回 0。现场环境、Java 与 sbt 安装均保持不变，因此该现象属于并发启动冲突，不属于工具缺失。

## 影响

1. 主线程和 subagent 会把可恢复的并发冲突判定为源码或环境失败。
2. 重试会额外消耗时间、token 和构建资源。
3. A/B 结果会受到 Agent 调度时序影响，降低资源指标与首次通过时间的可比性。
4. 并发越高，首次编译阶段越容易出现非确定失败。

## run-003 比较口径

run-003 保留两组原始 rollout、时间戳和墙钟时间，并新增 `evidence/sbt-lock-delay-normalization.json`。该证据按结构化 `CommandExecution` 事件识别 `sbt.boot.lock` 拒绝访问：

1. 同一 session 未执行其他命令便重试构建时，扣除失败命令开始至下一次构建开始的区间。
2. 同一 session 先继续其他工作时，只扣除失败命令自身耗时。
3. 同组并行区间取并集，避免重复计时。

Skill 组扣除 67.862 秒，Control 组扣除 155.572 秒。锁归一化墙钟时间分别为 4,180.653 秒和 4,281.746 秒。Token 与命令计数仍采用原始值。

## 当前边界

1. run-003 Skill 组早期失败已通过后续重试恢复。Control 组也已复现，线程仍在按原流程推进编译与验证。
2. 本记录不要求关闭 subagent 并发。代码阅读、文档和互不冲突的实现工作仍可并发。
3. 修复应位于通用 Windows Chisel 执行支持或项目构建入口，不进入处理器 Design 与 RTL。

## 通用关闭条件

1. 同一工作树并发启动至少三个 `compile.cmd` 时，不再出现 `sbt.boot.lock` 拒绝访问。
2. 每个调用明确等待、执行并返回自身真实退出码，不产生伪成功。
3. 编译、测试、RTL 生成和 CoreMark 共用一致的构建协调机制。
4. 缓存或 boot 目录隔离不会重复下载依赖，也不会修改用户级或系统级永久环境。
5. Windows 回归覆盖冷启动、热缓存、一个进程异常退出和后续调用恢复。
6. A/B 两组使用逐字节相同的协调实现与配置。
