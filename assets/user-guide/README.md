# 用户指南素材

本目录保存用户指南引用的截图和短动画，由指南维护者随正文维护。素材取自 2026 年 9 月的处理器开发案例，准备日期为 2026-10-03。六张 PNG 与一份 GIF 均直接复制，原始像素和文件内容保持一致。GIF 为真实截图组成的三幕展示动画，依次呈现草案、审查请求和 Skill 回应，时长 12 秒；原有标题、放大和强调一并保留。

下表的源路径相对于原材料目录 `107/`。来源说明为 `presentation/Figure/素材索引.md`（2026-09-18）、`presentation/逐页内容规划.md` 和 `show/edit/PROCESS_TIMELINE.md`（2026-09-06）。

| 输出 | 源文件 | 案例与使用范围 |
|---|---|---|
| [design-review.gif](design-review.gif) | `presentation/output/page8/page08-截图演示-预览.gif` | 2026 年 9 月分支预测人工案例。展示用户提交草案审查请求，以及 Agent 声明使用 `design-chisel-processor`。三幕来自演示页面，适合说明调用过程。 |
| [design-confirmation.png](design-confirmation.png) | `presentation/Figure/p11-request-focus.png` | 同一案例的用户确认，要求完善草稿并提升为 `Predict.md`。该消息的授权范围是文档。 |
| [design-document.png](design-document.png) | `presentation/Figure/p11-design-excerpt.png` | `Predict.md` 的接口声明及周期语义。用作设计文档产物示例；画面保留查询结果下一拍返回及保存条件。 |
| [implementation.png](implementation.png) | `presentation/Figure/p12-source-focus.png` | `BranchPredictor.scala` 的查询结果保存代码，保留原代码选区。对应分支预测案例，供设计与实现对照。 |
| [verification.png](verification.png) | `presentation/Figure/p12-test.png` | `BranchPredictorSpec.scala` 的定向测试。画面包含请求当拍 `valid=false`、推进一拍后 `valid=true` 的检查，并保留文件名。 |
| [timing-analysis.png](timing-analysis.png) | `presentation/Figure/p14-common-path.png` | 2026-09-16 时序案例，`007-baseline-80mhz` 全核分析报告。展示 80 MHz 核级 OOC 的违例覆盖、端点分类和公共路径。 |
| [timing-result.png](timing-result.png) | `presentation/Figure/p16-timing-complete-reply.png` | 同一时序案例的 `008-branch-mismatch-80mhz` 复测回复，比较 WNS、失败端点与资源。仅适用于该案例的 80 MHz 核级 OOC 条件。 |

图片中的目录、命令、模块和数值属于各自历史项目。它们用于说明任务输入、工程产物和证据呈现；当前工具入口仍以使用者项目约定为准。时序截图保留当时的结果汇总，本次素材准备没有重新执行仿真或 Vivado。分支预测文档和代码截图展示当时的产物，不能据此证明原始文档整理过程已经录制。

图中关键文字已按原图查看，GIF 三帧均已检查。宽幅文档和时序报告适合点击查看原图；嵌入指南时保留图片链接与简短说明。替换或移除素材时同步更新指南引用和本表。
