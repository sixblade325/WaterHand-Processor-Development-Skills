# PA3-DEFECT-018：中文交付包路径导致 Chisel 适配器编译失败

状态：按用户决定接受为已知限制，文档处理完成  
发现日期：2026-09-06  
来源：ZIP 交付包补充验收

## 产品责任

Windows 用户在支持的路径下解压插件后，包内 `scripts/chisel-run.cmd` 应能完成环境准备和项目仿真。2026-09-06 用户明确决定通过交付文档声明中文包路径限制，不额外实现中文包路径适配。

## 输入身份

- 插件：`processor-development-skills`，版本 `0.1.0`。
- ZIP SHA-256：`c04538c85343ca9cba3c1985cb992191268ccbe165f0076c6f8e81d8aa8e4e7c`。
- `sourceCommit`：`d2007e08a5b5daf05319b2e0025d9e0de426bb64`。
- `sourceDirty`：`true`，属于开发构建。
- Windows 11 x86-64；Python 3.12.12；MSYS2 UCRT64 GCC 15.2.0。

## 复现与证据

将同一个 ZIP 解压到包含中文的目录，以该目录中的 `scripts/chisel-run.cmd` 对独立 SmokeCounter 工程运行 `sbt -batch test`。

首次运行在 `_compile_adapter` 构建 `which.cpp` 时失败，退出码为 `4`。底层 GCC/ld 返回 `1`，报告无法打开位于中文包路径下的 `which.tmp.exe`。尚未进入 Chisel elaboration 或 Verilator 仿真。

`tools/processor_skills/chisel.py` 将源文件和输出文件的绝对路径直接交给外部编译器。当前临时 `subst` 处理覆盖用户项目目录，适配器编译发生在此之前，包目录缺少对应路径兼容处理。

同一 ZIP 解压到 ASCII 目录后，包内入口完成了两类项目路径的 elaboration、Verilator 编译和仿真：包含中文与空格的项目目录、较长 ASCII 项目目录。用例覆盖计数递增、模 4 回绕和再次复位。

原始证据位于仓库 `.runtime/readme-delivery-smoke/full-acceptance/`：

- `package-chisel-unicode.json`：中文包路径的首次失败。
- `package-unicode-repeat.json`：中文包路径的复验。
- `runtime-ascii/package-runtime-results.json`：ASCII 包路径下的验收汇总。
- `runtime-ascii/package-chisel-unicode.json`：中文用户项目路径的成功对照。
- `runtime-ascii/package-chisel-long.json`：长用户项目路径的成功对照。

上述材料验证的是指定 ZIP 和当前工具链，不能据此外推其他外部工具版本。

## 影响与当前支持条件

用户可以完成插件注册、安装和 Skill 文件校验，随后在执行 Chisel 工作时遇到此故障。安装成功及 `doctor` 通过均未覆盖适配器实际编译。

当前支持条件是将包解压到完整路径均为 ASCII 的目录；包路径含英文空格已实测通过，用户项目路径仍可包含中文、空格或较长根路径。该条件已写入 `PACKAGE_README.md`、`README.md`、`USER_GUIDE.md` 和 `environment/README.md`。

## 用户决定与处理结果

1. 中文包路径作为已知限制接受，不纳入当前适配开发。
2. 交付包在安装步骤之前明确完整 ASCII 路径要求、示例路径和失败表现。
3. 保留上述失败与成功证据，后续验收以文档声明的路径范围为准。
4. 本次处理仅修改文档，没有修改路径适配代码，也不将原有失败标记为已修复。

既有用户项目路径适配与测试继续保留。未来是否扩大支持范围，由新的明确需求决定。
