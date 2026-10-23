# User guide media

[中文](README.md) | English

This directory contains screenshots and a short animation referenced by the user guides. The guide maintainer keeps them aligned with the text. The material comes from processor development examples in September 2026 and was prepared on October 3, 2026. Six PNGs and one GIF were copied directly, preserving their original pixels and file contents. The 12-second GIF presents three screenshots: a draft, a review request, and the Skill response. Original titles, zooming, and emphasis are retained. Images preserve Chinese text; the English guide supplies English captions.

Source paths below are relative to the original `107/` material directory. Source records are `presentation/Figure/素材索引.md` (2026-09-18), `presentation/逐页内容规划.md`, and `show/edit/PROCESS_TIMELINE.md` (2026-09-06).

| File | Source | Example and scope |
|---|---|---|
| [design-review.gif](design-review.gif) | `presentation/output/page8/page08-截图演示-预览.gif` | Human-guided branch prediction example, September 2026. Shows a draft review request and the Agent declaring use of `design-chisel-processor`. The three frames come from a presentation page and illustrate invocation. |
| [design-confirmation.png](design-confirmation.png) | `presentation/Figure/p11-request-focus.png` | The same example's user confirmation asks for the draft to be completed and promoted to `Predict.md`. This message authorizes document work. |
| [design-document.png](design-document.png) | `presentation/Figure/p11-design-excerpt.png` | Interface declarations and cycle semantics from `Predict.md`, including next-cycle lookup responses and their retention conditions. Illustrates a design document artifact. |
| [implementation.png](implementation.png) | `presentation/Figure/p12-source-focus.png` | Lookup-result retention code in `BranchPredictor.scala`, with the original selection preserved. Supports comparison between the design and implementation. |
| [verification.png](verification.png) | `presentation/Figure/p12-test.png` | A directed test in `BranchPredictorSpec.scala`, showing `valid=false` on the request cycle and `valid=true` after advancing one cycle. The filename is retained. |
| [timing-analysis.png](timing-analysis.png) | `presentation/Figure/p14-common-path.png` | Whole-core analysis from the 2026-09-16 timing example, `007-baseline-80mhz`. Shows violation coverage, endpoint classification, and common paths under 80 MHz core OOC conditions. |
| [timing-result.png](timing-result.png) | `presentation/Figure/p16-timing-complete-reply.png` | Retest summary for `008-branch-mismatch-80mhz` in the same example. Compares WNS, failing endpoints, and resources within that example's 80 MHz core OOC conditions. |

Directories, commands, modules, and values in these images belong to their historical projects. They illustrate task inputs, engineering artifacts, and evidence presentation. Current tool entrypoints remain those declared by the user's project. Timing screenshots preserve historical summaries; simulation and Vivado were not rerun when preparing this media. The branch prediction document and code images show artifacts from that time and do not establish that the original document organization process was recorded.

Key text and all three GIF frames were visually checked during the original media preparation. Wide documents and timing reports are best inspected at full size. Keep image links and concise captions in the guides. When replacing or removing media, update the guide references and both editions of this table.
