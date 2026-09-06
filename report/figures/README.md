# 报告插图

本目录由设计报告维护者管理，保存正文插图及其可编辑源。后续修改覆盖同名文件，历史由 Git 保存；报告移除插图时一并检查其引用和导出文件。

| 图 | 内容与依据 | 文件 |
|---|---|---|
| 封面标识 | 用户提供的产品 logo，不计入正文图号 | [PNG](logo.png) |
| 图 1 | 第 2.2 节的产品组成、工程师权限及调用关系 | [可编辑源](fig-01-product-architecture.drawio)、[PNG](fig-01-product-architecture.drawio.png)、[SVG](fig-01-product-architecture.drawio.svg) |
| 图 2 | 第 5.4 节的 BHT 同拍读旧值案例 | [可编辑源](fig-02-decision-to-evidence.drawio)、[PNG](fig-02-decision-to-evidence.drawio.png)、[SVG](fig-02-decision-to-evidence.drawio.svg) |

两图为根据正式材料绘制的关系示意。PNG 用于 Markdown 浏览和当前 LaTeX 排版，SVG 保留供矢量排版；两种导出均嵌入 draw.io 编辑数据，同时保留独立源文件。封面、目录与正文排版由 [DESIGN_REPORT.tex](../DESIGN_REPORT.tex) 维护。

图 1 以 [产品总纲](../../PRODUCT_PLAN/V3/PRODUCT_PLAN.md) 和报告第 2 章为依据。产品框内包含 Skill Package 与 Execution Support Kit，Agent 开发工具、用户项目和外部工具链分别表达。双向箭头表示读写交互；工程师可直接维护项目材料。

图 2 依据素材中保存的 [Predict.md](../../../show/素材/static/evidence/Predict.md)、[BranchPredictorSpec.scala](../../../show/素材/static/evidence/BranchPredictorSpec.scala)，以及[工程师决定摘录](../../../show/素材/static/evidence/session-excerpts.json)。人工案例的验证范围见[《实验补充说明》](../EXPERIMENT_SUPPLEMENT.md)第 4 节。图中“返回旧值 1”指同拍提交查询与更新后，下一拍返回的查询结果；后续查询通过调整 PC 抵消 GHT 变化，再检查同一表项的新值 2。工程师确认设计与授权实现分别保留，图中不声明最终验收已获接受。

## 导出

本机已检测到的 draw.io Desktop 为 `D:\Draw.io\draw.io.exe`。在本目录执行以下 PowerShell 命令可复现导出；其他机器使用其本地安装路径。

```powershell
$drawioExe = 'D:\Draw.io\draw.io.exe'
foreach ($name in @('fig-01-product-architecture', 'fig-02-decision-to-evidence')) {
    foreach ($format in @('png', 'svg')) {
        $drawioArgs = @('-x', '-f', $format, '-e', '-b', '12', '-o', "$name.drawio.$format", "$name.drawio")
        if ($format -eq 'png') { $drawioArgs += @('-s', '3') }
        $exportProcess = Start-Process -FilePath $drawioExe -ArgumentList $drawioArgs -WorkingDirectory $PWD.Path -WindowStyle Hidden -Wait -PassThru
        if ($exportProcess.ExitCode -ne 0) { throw "导出失败：$name / $format" }
    }
}
```
