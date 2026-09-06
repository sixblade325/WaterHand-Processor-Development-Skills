# PA3-DEFECT-014：Codex 运行时状态触发 home inventory 误报

状态：run-004 post 审计再次复现，`session_read` 可独立验证，通用审计器待收敛  
发现日期：2026-09-04  
来源：`dual_issue_demo_V2` run-003 Control 组 post-run Memory trigger

## 产品责任

A/B 实验基础设施需要区分冻结输入与 Codex 在正常会话中生成的运行时状态。工程 main session 结束后，Memory trigger 应继续核验配置、Skill 隔离和不可变输入，同时允许并记录由同一冻结 Codex 版本生成的合法动态状态。

## 现场证据

Control main session 于 `2026-09-04T14:01:13.5393834Z` 正常退出并提交候选。随后使用冻结入口启动 `control/trigger`，launcher 在创建 trigger 进程前失败：

```text
Current common Codex home content differs from the finalized shared inventory.
```

冻结 common inventory 为 2 个文件，SHA256 为：

```text
024506a6857a074cccb79b1740ae656e4a776d12b28d59df9d275e8c03ce7f0e
```

main session 退出后的 Control home inventory 为 209 个文件，SHA256 为：

```text
c13a020369ea06aa21f326791d92109d1d7ff56726ab432f4914b784147403ed
```

新增内容包含 Codex 正常生成或安装的状态：

```text
.sandbox/
.sandbox-bin/
cache/
goals_1.sqlite*
logs_2.sqlite
memories_1.sqlite
models_cache.json
plugins/cache/
skills/.system/
thread_history_1.sqlite
thread-writer-locks/
```

Codex 还在各组 `config.toml` 中自动加入本组仓库专属的 trusted project 段。例如 Control home 新增：

```toml
[projects.'e:\107\.runtime\dual_issue_demo_v2\run-003\repositories\control']
trust_level = "trusted"
```

Memory、模型、subagent 和 sandbox 配置值未发生变化。当前 inventory 将运行时物化文件与配置中的合法本组路径差异一起视为冻结输入变化，因此拒绝了合法的第二个 session。

对应现场：

```text
E:\107\.runtime\dual_issue_demo_V2\run-003\homes\control
E:\107\.runtime\dual_issue_demo_V2\run-003\evidence\control-main.exit.json
E:\107\.runtime\dual_issue_demo_V2\run-003\inputs\RUN_CONFIG.json
```

失败发生在 trigger 进程创建前，没有改变处理器候选、Control main session 或 CoreMark 结果。

## 影响

1. 使用干净 Codex home 启动 main 后，后续 trigger 会被确定性拒绝。
2. `post_write` 无法验证，正常 Memory 行为会被误判为实验失败。
3. 直接放宽整个 home hash 会削弱 Skill 泄漏、配置漂移和跨组污染检测。
4. Codex 版本升级后新增状态文件可能再次触发同类失败。

## 当前边界

1. 该缺陷属于隔离实验与 Memory 证据基础设施，不属于处理器候选实现错误。
2. run-003 Control main 结果及提交保持有效，post-run Memory 证据需要按已记录的协议修订单独处理。
3. 修复不得删除或覆盖现有 Codex home、session、Memory 和运行证据。
4. 修复不得把整个动态 home 排除后停止审计。动态状态仍需记录完整 inventory，denylist、配置语义和本组路径绑定仍需独立核验。

## 通用关闭条件

1. 冻结输入 inventory 与 Codex 动态状态 inventory 分开记录和校验。
2. `config.toml` 采用规范化语义校验，允许且只允许绑定当前组仓库的 trusted project 段。
3. `.sandbox`、SQLite、cache、系统 Skill 和 plugin cache 等运行时生成内容具有明确分类与证据清单。
4. Control post 审计继续证明本产品 Skill denylist 未进入有效上下文。
5. 两个从同一空起点创建的 home 连续运行 main 与可选 trigger 时，合法动态状态不触发冻结输入误报；显式 `post_write` 诊断仍独立校验写回证据。
6. 回归覆盖未知顶层文件、错误 project path、denylist Skill 注入和静态配置修改，以上情况仍必须失败。

## 修复结果

1. common home inventory 排除项按文件与目录分别处理，Codex 运行时状态不再混入冻结输入 hash。
2. `config.toml` 使用规范化语义比较，允许当前组 repository 对应的 trusted project 段。
3. Memory 隔离回归覆盖未知文件、错误 project path、denylist 注入、静态配置变化和连续 session。
4. `Experiment\tests\run.cmd` 于 2026-09-04 完整通过。
5. run-003 已按 `session_read` 完成门禁封存，未修改既有 home、session 或原始证据。

## run-004 复现

run-004 Skill 主会话使用全新隔离 home 启动。pre 审计记录的 common non-product Skill inventory SHA-256 为：

```text
3d2412db5bc7142784dc154f3dea904afd5c60d3ea23fae9ad8ebc6faa27758a
```

主会话正常退出后，Codex 已在本组 home 中物化系统 Skill 和 plugin cache。post 审计重新扫描可发现 Skill，得到 SHA-256：

```text
354e89f943579a41dd4e9f5347d6d99b0f4ba7a204ccdffd8c81e1677b04f641
```

post 报告的 Memory 生命周期为 `session_read`，`sessionRead.ok` 与 `sessionRead.observed` 均为 `true`，产品 Skill allowlist、启动目录和会话绑定也全部通过。报告整体结果仅因 `nonProductSkillInventoryOk=false` 返回失败。

本次没有运行 Memory trigger，也没有等待异步 post_write。Skill 候选实现与独立 organizer 验收不受该误报影响。现场证据位于：

```text
E:\107\.runtime\dual_issue_demo_V2\run-004\evidence\skill-post-context.json
E:\107\.runtime\dual_issue_demo_V2\run-004\evidence\skill-session-read-evidence.json
E:\107\.runtime\dual_issue_demo_V2\run-004\evidence\skill-result-seal.json
```

当前修复覆盖了 common home 文件 inventory，尚未处理 Codex 会话期间物化的可发现非产品 Skill。审计器需要分别冻结稳定的外部 Skill 来源与 Codex 自带动态 plugin cache，并继续检查两组是否获得同一版本和同一集合。
