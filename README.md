# WaterHand Processor Development Skills

<p align="center">
  <img src="logo.png" alt="WaterHand Processor Development Skills" width="320">
</p>

当前版本：v3.0.3。

面向 Codex 的处理器开发插件，提供项目协作、文档组织、微架构设计、Chisel 实现与验证、FPGA 时序分析的六项 Skill，以及配套的 Windows 工具脚本。

适用于处理器课程项目、科研原型和已有 Chisel 工程的增量开发。你在自己的处理器项目中提出任务，Codex 根据项目文档和这些 Skill 开展设计、修改与验证，结果保存在该项目中。

## 能完成哪些工作

| 任务 | Skill | 主要交付 |
|---|---|---|
| 建立项目协作约束 | `bootstrap-processor-project` | 项目根目录 `AGENTS.md`，或已有规则的增量建议 |
| 组织与维护工程文档 | `organize-processor-docs` | 文档职责、阅读入口、事实归属和渐进式文档结构 |
| 设计与审查微架构 | `design-chisel-processor` | 周期语义、接口、状态生命周期、优先级和验证要求 |
| 实现并验证 Chisel RTL | `implement-chisel-processor` | 源码、源码旁 `_codex.md`、断言、定向测试及执行证据 |
| 分析 Vivado 时序路径 | `trace-vivado-timing-to-rtl` | 从物理路径到生成 RTL、Chisel 源码及流水级的证据映射 |
| 优化 FPGA 时序 | `optimize-chisel-fpga-timing` | 受周期契约约束的修改候选、功能验证及实现结果比较 |

例如，增加分支预测功能时，可以先整理现有取指与重定向设计，再闭合预测信息的传递、更新和失效规则，随后实现 RTL、补充定向测试并核对文档。任务输入、允许修改范围和验收要求由你提供。

Skill 的完整用法与提示词见 [用户指南](USER_GUIDE.md#9-skill-使用方式)。

## 开始使用

运行平台为 **Windows x86-64**。需要可用的 Codex 环境，以及支持 `codex plugin` 命令组的 Codex CLI。模型访问和相关账户由使用者准备，插件包不附带模型、账户或 API 凭据。

工具脚本要求 Python 3.10 以上、Git 2.30 以上。执行 Chisel 仿真时还需要 Java、sbt、Verilator、C++ 编译器和 Make 等工具；获取 Vivado 实现结果时需要相应安装和许可证。具体版本、配置入口和诊断方式见 [环境契约](environment/README.md)。

### 已收到 ZIP 交付包

将包解压到完整路径均为 ASCII 的目录，例如 `E:\tools\waterhand`，再按包内 `README.md` 安装。中文包路径当前不受支持；包路径含英文空格、处理器项目路径含中文和空格的场景已实测通过。安装说明的源码见 [PACKAGE_README.md](PACKAGE_README.md)，其中包含包内安装命令、首次调用示例和验收步骤。

### 从源码仓库安装

在本仓库根目录打开 PowerShell：

```powershell
.\scripts\initialize.cmd
```

命令会检查环境，校验插件和 Skill，运行工具测试，构建安装包，再通过本地 marketplace 安装插件。成功后，在目标处理器项目中打开新的 Codex 会话。

正式构建要求 Git 工作树干净。开发期间需要测试未提交修改时，显式使用：

```powershell
.\scripts\initialize.cmd --allow-dirty
```

### 第一次调用

在已有处理器项目中，可以从一次范围明确的只读审查开始：

```text
使用 $design-chisel-processor 只读审查当前项目的取指与重定向设计。
先读取项目 AGENTS.md、相关 Architecture、Design 和源码。
追踪重定向请求的产生、寄存器边界、消费位置和失效行为。
列出设计缺口、证据路径和需要补充的定向测试，区分文档约定与已验证行为。
本次只输出审查结果。
```

新项目的协作规则初始化、文档组织、实现和时序工作流见 [用户指南](USER_GUIDE.md)。

## 产品如何与工程配合

Codex 提供会话、模型推理、上下文、文件编辑和工具调用。Skill 提供处理器工程方法、输入输出要求和检查项；配套脚本负责工具探测、参数转发、进程级环境及结构化结果。

处理器项目自身的 `AGENTS.md`、Architecture、Design、源码和验证结果决定项目事实。项目文件与 Git 历史由该项目维护。产品运行依赖 Codex，不提供独立的 Agent 执行服务。

设计审查结果需要结合项目测试和实现证据判断。工具级测试验证本插件的脚本行为，处理器的功能、性能和时序分别由具体项目验收。

## 常用工具

以下命令从源码仓库或解压后的包根目录运行：

```powershell
.\scripts\doctor.cmd --profile package
.\scripts\doctor.cmd --profile chisel
.\scripts\doctor.cmd --profile vivado
.\scripts\run.cmd check-docs E:\projects\my-cpu --json
.\scripts\chisel-run.cmd E:\projects\my-cpu -- sbt -batch test
```

请将示例项目路径替换为实际位置。`doctor` 报告缺失工具和恢复提示；`chisel-run` 为单次命令准备 Windows 工具链环境。工具路径可通过 `PROCESSOR_SKILLS_*` 变量指定，详见 [用户指南](USER_GUIDE.md#4-明确工具路径)。外部工具由使用者安装和配置。

## 源码开发与打包

仓库维护 Skill、插件元数据、脚本、工具测试及产品文档。修改前先读取 [AGENTS.md](AGENTS.md)；当前产品定位和边界见 [V3 产品总纲](PRODUCT_PLAN/V3/PRODUCT_PLAN.md)与[产品和实验边界](PRODUCT_PLAN/V3/RUNNABLE_PRODUCT_AND_EXPERIMENT_BOUNDARY.md)。

```powershell
.\scripts\run.cmd validate-skills
.\scripts\run.cmd test-tools
.\scripts\build.cmd
```

`build.cmd` 包含结构校验与工具测试。默认产物位于 `.runtime/processor-development-skills/dist/`：

| 产物 | 用途 |
|---|---|
| `processor-development-skills-<version>.zip` | 可解压安装的插件交付包 |
| 同名 `.zip.sha256` | ZIP 校验值 |
| `marketplace/` | 源码初始化使用的本地插件源 |

包内 `README.md` 由仓库中的 `PACKAGE_README.md` 生成，两份入口分别面向仓库读者和交付包使用者。`USER_GUIDE.md` 作为共同的操作参考随包分发。

ZIP 内含本地 marketplace 清单，解压后即可注册并安装。`PACKAGE_MANIFEST.json` 记录源码 commit、dirty 状态、逐文件 hash 和 payload hash。构建使用固定文件顺序、时间戳和 UTF-8/LF 文本；相同输入产生相同 ZIP 校验值。

交付包包含插件、Skill、运行工具、环境契约和用户文档。源码测试、产品计划、日志、缓存和 A/B 实验证据保留在各自的仓库或实验目录。构建选项见 [用户指南](USER_GUIDE.md#5-构建)。

## 卸载

在源码仓库或解压后的包根目录运行：

```powershell
.\scripts\uninstall.cmd
```

该命令移除本产品插件及专用 marketplace，仓库、解压目录与用户处理器项目文件继续保留。

## 许可证

除另有标注的第三方材料外，本仓库的代码、Skill、模板和文档采用木兰宽松许可证，第 2 版，SPDX 标识为 `MulanPSL-2.0`。完整条款见 [LICENSE](LICENSE)。再分发时应附带许可证并保留相关声明；外部工具和用户处理器项目遵循各自的许可证。
