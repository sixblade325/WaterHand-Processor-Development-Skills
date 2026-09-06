# WaterHand Processor Development Skills 交付包

<p align="center">
  <img src="logo.png" alt="WaterHand Processor Development Skills" width="320">
</p>

当前版本：v3.0.3。

这是面向 Codex 的处理器开发插件，包含六项 Skill 和配套的 Windows 工具脚本。安装后，可在自己的处理器项目中使用 Codex 开展文档组织、微架构设计、Chisel 实现与验证、Vivado 时序分析和优化。

本说明对应已经构建好的 ZIP。包版本、源码来源和文件校验值记录在 `PACKAGE_MANIFEST.json` 中。

## 1. 准备运行环境

| 使用范围 | 需要准备 |
|---|---|
| 安装和调用插件 | Windows x86-64、可用的 Codex 环境、支持 `codex plugin` 命令组的 Codex CLI |
| 运行包内脚本 | Python 3.10 以上、Git 2.30 以上；按操作补齐环境诊断列出的工具 |
| 执行 Chisel 编译与仿真 | Java、sbt、Verilator、C++ 编译器、Make 及完整的 MSYS2 UCRT64 工具链依赖 |
| 获取 Vivado 实现结果 | Vivado、相应器件支持及许可证 |

模型访问、账户和外部工具由使用者准备。包内不附带模型、API 凭据或 Vivado 等外部工具。详细版本与路径配置见 [环境契约](environment/README.md)和[用户指南](USER_GUIDE.md)。

先在 PowerShell 确认 CLI 可用：

```powershell
codex plugin --help
```

若提示命令不存在，先修复 Codex CLI 安装或命令路径。仅进行文档与设计审查时，可以先完成插件安装，后续执行仿真或实现时再准备对应工具链。

## 2. 解压并安装

**包的完整解压路径及所有父目录必须使用 ASCII 字符。** 推荐使用 `E:\tools\waterhand` 这类英文路径。当前版本不支持在含中文或其他非 ASCII 字符的包路径下运行 Chisel 工具；这类路径会导致原生适配器编译失败，即使插件安装和 `doctor` 已经通过。

包路径含英文空格已实测通过。该限制针对包及其工具脚本所在目录；处理器项目目录包含中文、空格或较长路径的测试已通过。

将 ZIP 完整解压到符合上述要求的固定目录，在包含本文件的目录中打开 PowerShell。应能找到 `.codex-plugin/plugin.json`、`.agents/plugins/marketplace.json` 和 `skills/`。

依次执行，前一步成功后再执行下一步：

```powershell
codex plugin marketplace add . --json
```

```powershell
codex plugin add processor-development-skills@processor-development-skills-local --json
```

第一步将解压目录登记为本地插件源，第二步安装插件。配置写入当前 Codex 环境；本机使用了多个 Codex 环境时，应在日常使用的同一个环境中完成安装和调用。

这条安装路径直接使用包内文件，不需要源码仓库、源码测试或重新构建。包内 `scripts/initialize.cmd` 和 `scripts/build.cmd` 属于源码构建流程，使用条件见 [用户指南](USER_GUIDE.md#1-安装与初始化)。

安装后保留解压目录，后续工具调用和本地插件源更新会使用它。

## 3. 确认安装并开始使用

检查安装状态：

```powershell
codex plugin list --json
```

应在 `installed` 中看到 `processor-development-skills`，所属 marketplace 为 `processor-development-skills-local`，并且 `enabled` 为 `true`。

随后在目标处理器项目中打开新的 Codex 会话，显式指定 Skill 和任务范围。已有项目可以先进行一次只读审查：

```text
使用 $design-chisel-processor 只读审查当前项目的取指与重定向设计。
先读取项目 AGENTS.md、相关 Architecture、Design 和源码。
追踪重定向请求的产生、寄存器边界、消费位置和失效行为。
列出设计缺口、证据路径和需要补充的定向测试，区分文档约定与已验证行为。
本次只输出审查结果。
```

首次验收时，确认插件已启用、会话能够找到该 Skill，并且审查结果引用目标项目中的实际材料。缺少相关设计或源码的项目，需要先补充任务输入。

| 需要完成的工作 | 调用的 Skill |
|---|---|
| 建立精简的项目根目录协作规则 | `$bootstrap-processor-project` |
| 组织和维护工程文档 | `$organize-processor-docs` |
| 闭合微架构设计和周期语义 | `$design-chisel-processor` |
| 实现 Chisel RTL 并验证 | `$implement-chisel-processor` |
| 将 Vivado 时序路径映射回源码 | `$trace-vivado-timing-to-rtl` |
| 修改并验证 FPGA 时序优化方案 | `$optimize-chisel-fpga-timing` |

各项 Skill 的输入、权限边界和完整提示词见 [用户指南](USER_GUIDE.md#9-skill-使用方式)。处理器项目的功能和时序验收由该项目的测试与实现结果确定。

新项目先用 bootstrap 建立项目 `AGENTS.md`，再用文档组织 Skill 按需建立文档。两者采用一致的 `doc/` 默认布局；已有项目保留其明确映射。`AGENTS.md` 保存项目约束和入口，技术细则由对应 Skill 按任务加载，详见[初始化规则](USER_GUIDE.md#92-bootstrap-processor-project)。

## 4. 使用配套工具

以下命令从解压目录运行。先检查需要的工具环境：

```powershell
.\scripts\doctor.cmd --profile package
.\scripts\doctor.cmd --profile chisel
.\scripts\doctor.cmd --profile vivado
```

按任务选择对应 profile。随后可检查项目文档或执行 Chisel 测试，请替换示例路径：

```powershell
.\scripts\run.cmd check-docs E:\projects\my-cpu --json
.\scripts\chisel-run.cmd E:\projects\my-cpu -- sbt -batch test
```

`doctor` 输出缺失工具、解析路径和恢复提示。工具脚本通过当前进程的 `PROCESSOR_SKILLS_*` 变量读取显式配置，详见 [用户指南](USER_GUIDE.md#4-明确工具路径)。

## 5. 常见问题与卸载

| 现象 | 处理方式 |
|---|---|
| 找不到 marketplace 清单 | 确认 ZIP 已完整解压，并在包含本 README 的目录执行安装命令 |
| 同名 marketplace 指向旧目录 | 用 `codex plugin marketplace list --json` 核对路径；需要迁移时，先从旧包执行卸载，再从新目录安装 |
| 插件已安装，会话未找到 Skill | 检查插件的 `enabled` 状态，然后在目标项目打开新会话 |
| `doctor` 返回工具缺失或版本不足 | 按诊断结果安装或配置相应工具，再运行该 profile |
| `chisel-run` 报 `cannot build native Chisel adapter`，路径包含中文 | 将包重新解压到完整路径均为 ASCII 的目录，按第 2 节安装；核对本地 marketplace 路径，避免继续使用旧包目录 |
| 提示缺少 `tests` 目录 | 核对是否调用了源码构建入口；交付包按第 2 节直接安装 |

卸载时，在包根目录执行：

```powershell
.\scripts\uninstall.cmd
```

该命令移除 `processor-development-skills` 插件和 `processor-development-skills-local` marketplace。解压目录和用户项目文件继续保留。

## 包内文件与来源

`skills/` 保存六项 Skill；`tools/`、`scripts/` 和 `environment/` 提供执行支撑；[USER_GUIDE.md](USER_GUIDE.md)提供详细操作说明。`PACKAGE_MANIFEST.json` 记录版本、源码 commit、`sourceDirty` 和逐文件 SHA-256。

收到同名 `.zip.sha256` 文件时，可在解压前运行 `Get-FileHash -Algorithm SHA256 <ZIP路径>`，将结果与该文件比较。`sourceDirty: true` 表示构建时包含未提交的源码工作树状态。

源码、测试和产品计划见 [项目仓库](https://github.com/sixblade325/processor_agent)。实验数据和用户处理器工程按各自的交付材料提供。

## 许可证

本产品的代码、Skill、模板和文档采用木兰宽松许可证，第 2 版，SPDX 标识为 `MulanPSL-2.0`，完整条款见 [LICENSE](LICENSE)。另有标注的第三方材料、外部工具和用户处理器项目遵循各自许可证。再分发时应附带许可证并保留相关声明。
