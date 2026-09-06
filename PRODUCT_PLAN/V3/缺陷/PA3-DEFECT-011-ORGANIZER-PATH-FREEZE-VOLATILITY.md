# PA3-DEFECT-011：organizer 冻结了易变且不可接受的原始 PATH

状态：run-003 与 run-004 隔离修复已验证，通用冻结器待收敛
发现日期：2026-09-04  
来源：`dual_issue_demo_V2` run-003 启动前独立组织者验收

## 产品责任

实验组织者需要冻结能够稳定重放的工具解析环境。冻结内容应来自已验证工具目录和必要系统目录，不能吸收一次性启动目录、重复目录或 reparse point。

## 现场证据

run-003 原始 organizer policy 直接保存启动进程的完整 PATH，其中包含：

```text
C:\Users\13926\.codex\tmp\arg0\codex-arg0z1mvsJ
C:\Program Files\Common Files\Oracle\Java\javapath
```

后续调用使用新的 Codex 临时参数目录，launcher 报告：

```text
organizer_input_path_mismatch: index=0
```

按原值恢复 PATH 后，launcher 又检测到 `javapath` 为 reparse point：

```text
organizer_input_path_actual_reparse_point: C:\Program Files\Common Files\Oracle\Java\javapath
```

冻结器和 launcher 对同一份 PATH 给出了互不兼容的要求，导致可用工具链无法重放。

## 影响

1. 每次 Codex CLI 启动产生的新临时目录都会使 organizer 配置失效。
2. 用户 PATH 中的兼容链接会在冻结阶段进入配置，在执行阶段被信任边界拒绝。
3. 独立验收可能在读取候选 RTL 前结束，形成基础设施伪失败。

## run-003 隔离修复

1. 仅在 `run-003/inputs` 中重新冻结稳定 PATH，目录限定为 Windows 系统目录、JDK、Git、sbt、MSYS2 UCRT64 和 MSYS2 user bin。
2. 新 organizer run config SHA-256 为 `78fb31c03058b4f2965b4ce67dd6c9687526edd68e5120eba3bf273de757f629`。
3. 新 frozen policy SHA-256 为 `2552d1353a2de2df580c46c92f7f9238c505edde0a26acb0386ad6a39e302eb0`。
4. 修订只改变 organizer 工具链绑定。Memory 输入、两组 prompt、两组 repository 和 Skill Package 均保持不变。
5. 修订记录位于 `E:\107\.runtime\dual_issue_demo_V2\run-003\evidence\run-config-organizer-path-amendment.json`。
6. 修订后的独立组织者完整验收通过。

## run-004 复现与隔离修复

run-004 于 2026-09-05 再次从调用进程复制完整 PATH，原始配置包含新的 Codex `arg0` 临时目录和 Oracle `javapath` reparse point。原始外层 `RUN_CONFIG` SHA-256 为：

```text
a21d1f31d771ae3db95a9a757860b81370918289a68a1ed796d8c97144a17e64
```

Skill 主会话完成后，实验管理器在 Control 启动前执行与 run-003 相同的隔离修订。修订只更新 organizer 工具链绑定，Memory、两组 prompt、两组 repository 和 Skill Package 均未改变。稳定 PATH 仍限定为 Windows 系统目录、JDK、Git、sbt、MSYS2 UCRT64 和 MSYS2 user bin。

修订后的绑定为：

```text
RUN_CONFIG              2af8ca26e1634fae7bfad63bd53cb69693d4d6878060cdfcb5add4ae11f9d3fc
organizer run config    75ea76ed51abe385c5fdb92dad7e537e0eb1f6683444be149972e86cb1a6597e
frozen tool policy      422cd8281c631a7be50096817d88e41ce0a0431549048f2595e5a03949a29526
```

独立 organizer 随后对 Skill 候选提交 `a5d15e7e4881898b6d8fa752eb0075e1d156efce` 完成 RTL 生成、Verilator 构建、13 个定向用例和两个 CoreMark workload，验收通过。现场证据位于：

```text
E:\107\.runtime\dual_issue_demo_V2\run-004\evidence\run-config-organizer-path-amendment.json
E:\107\.runtime\dual_issue_demo_V2\run-004\outputs\organizer-eval-skill-001\results\organizer-result.json
```

run-004 的再次复现说明通用 `freeze-tools` 尚未满足关闭条件。

## 通用关闭条件

1. `freeze-tools` 从解析成功的受信工具构造最小 PATH，不直接复制调用进程的完整 PATH。
2. 冻结前拒绝易变临时目录、重复目录、缺失目录和 reparse point。
3. 回归覆盖连续两次 Codex CLI 调用产生不同 `arg0` 目录的场景。
4. 回归覆盖 Oracle `javapath` 等目录链接存在于用户 PATH 的场景。
