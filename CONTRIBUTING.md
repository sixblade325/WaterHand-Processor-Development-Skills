# 参与维护

本仓库维护六项处理器开发 Skill、配套脚本和使用文档。修改前先读取 [AGENTS.md](AGENTS.md) 及受影响 Skill 的正文和参考资料。

## 提交问题与修改

在 [Issues](https://github.com/sixblade325/WaterHand-Processor-Development-Skills/issues) 中提供版本、Skill 名称、任务输入、预期结果和实际结果。出现脚本错误时附命令、Python 版本与退出信息；案例来自用户工程时，选取足以说明问题的片段并移除私人信息。

修改 Skill 时说明原规则在哪种输入下产生问题，以及修改后的适用范围。保留事实归属、设计者授权和证据要求。六项 Skill 的方法分别由自己的目录维护，新增规则前先检查已有职责是否能够容纳。

提交 Pull Request 时概述问题、最终改动和验证结果。脚本变化应增加覆盖对应输入、输出或失败路径的测试；文档变化应核对链接、图片和与 Skill 正文的一致性。

## 本地检查

使用 Git 和 Python 3.10 或更新版本，以下检查只依赖 Python 标准库。在仓库根目录执行：

```sh
python maintenance/check_release.py
python -m unittest discover -s maintenance -p 'test_*.py'
python -m unittest discover -s skills/organize-processor-docs/scripts -p 'test_*.py'
python -m unittest discover -s skills/trace-vivado-timing-to-rtl/scripts -p 'test_*.py'
```

[公开文件检查器](maintenance/check_release.py)核对插件元数据、六项 Skill、资源与文档链接。[GitHub Actions](.github/workflows/ci.yml)在 Linux、macOS 和 Windows 上运行检查与测试。它们验证文件、脚本和分发条件，处理器功能、物理时序及模型行为需要另行评测。

`Logs/`、`PRODUCT_PLAN/`、`.runtime/` 和历史 Skill 压缩包仅在维护者本地保留。它们不参与上述检查，也不进入发行包。`report/` 公开维护三份历史交付 PDF，原稿与排版素材留在本地。

## 素材与许可

用户指南只引用 `assets/user-guide/` 中维护的媒体。[素材说明](assets/user-guide/README.md)记录历史案例、源文件和适用范围。更新截图时保留真实文字，说明画面属于输入、产物、执行记录还是结果汇总。

新增文件遵循仓库的 [MulanPSL-2.0 许可证](LICENSE)。引入第三方材料时保留其来源与许可信息；具体用户工程的事实和源码留在该工程中。

## 构建与发布

[发行包构建器](maintenance/build_release.py)从指定 Git 提交读取文件，按公开文件清单生成 ZIP、`SHA256SUMS` 和 `release-manifest.json`，并在解压后重新校验。相同提交与输入会生成相同包内容，工作树中的未提交修改不参与构建。

```sh
python maintenance/build_release.py --ref HEAD --version 3.1.0 --output .runtime/release
```

发布一个新版本时：

1. 更新 `.codex-plugin/plugin.json`、`skills/MANIFEST.md` 和 `CHANGELOG.md` 中的版本信息；用户指南包含固定版本命令时同步更新。
2. 运行全部检查和测试，检查公开目录、历史报告与素材范围。
3. 提交改动并推送，确认该提交的 CI 通过；从这个提交构建发行包。
4. 创建 `v<version>` tag，指向相同提交，将 ZIP、校验和及构建清单附到 GitHub Release。
5. 下载公开附件，核对 SHA-256、清单中的 source commit、解压后的文件及脚本测试。

Release notes 说明改动、安装入口和实际验证范围。已发布 tag 与附件保持稳定，后续修复使用新版本。
