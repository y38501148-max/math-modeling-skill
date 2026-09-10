# MathModelAgent 工作流借鉴与校正

本次优化固定参考 [jihe520/MathModelAgent](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/README.md)，提交 `83d8783187a2d29dda1b046cb667009cc50c8203`，读取日期 2026-09-10。完整阅读 10 个 SKILL 入口、数学建模规范、论文检查脚本、技能配置及许可说明，共 14 个文件；下载内容逐一用 Git blob SHA 校验，见 [机器可读来源](workflow-sources.json)。后端 agent、前端应用及整套 Typst 文档未做全面运行验证。

模板目录确认 17 个 Typst 入口和 17 个 LaTeX 入口，覆盖 14 个中文与 3 个英文模板族。本次仅核对树中入口存在，未逐套阅读/编译，也未将模板复制到技能包；不据此宣称这些模板符合当前比赛规定。

## 采用的设计与落点

| 固定来源 | 可迁移的设计 | 本技能实现 |
| --- | --- | --- |
| [1start-mathmodel](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/1start-mathmodel/SKILL.md) | 从规划到验收的阶段交接、任务状态 | [项目工作流](project-workflow.md)：按范围选择阶段，记录恢复点及变更影响 |
| [2analysis-modeling](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/2analysis-modeling/SKILL.md) | 假设预检、数据字典、给代码的数学接口 | 任务单增加实现交接；主问下覆盖所有子任务与非编号要求 |
| [3coding-visual](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/3coding-visual/SKILL.md) | 逐问运行、保存中间结果、图表数据追踪 | [计算实现](computing.md)：实现差异、缓存失效、实际运行状态 |
| [4drawio](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/4drawio/SKILL.md) | 方法图与统计图分工、源图可编辑 | [图表指南](visualization.md)：按图意选工具，保留图源与数据 |
| [5writing](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/5writing/SKILL.md) | 结果约束论文、图文位置、摘要最后定稿 | [论文写作](paper-writing.md) 与交付验收，兼容用户现有工程 |
| [6verity](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/6verity/SKILL.md) | 内容一致性、编译、PDF 逐页检查 | [交付验收](delivery-review.md)：区分 PASS/FAIL/NOT_RUN/N/A |
| [writing_check.sh](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/6verity/scripts/writing_check.sh) | 对论文与结果做自动辅助检查 | 原创 [证据检查器](evidence-checker.md)，按文件哈希与字段数值核对 |
| [doctor](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/doctor/SKILL.md) | 在开始前识别缺失环境 | 仅检查当前交付需要的工具，不要求完整工具栈 |
| [figure templates](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/mathmodel-figure-templates/SKILL.md) / [typst-author](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/typst-author/SKILL.md) | 图源与多格式输出；语法需对照文档并编译 | 图示生成与嵌入按安装版本验证，不硬编码上游沙箱路径 |
| [规范库](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/skills/_references/math_modeling_norms.md) | 常见建模/代码错误提示 | 补充图、几何、接口与依赖验证，保留已有本科案例的数学纠错 |

## 未直接采用及原因

1. **反复确认排版引擎、固定阶段全跑。** 用户已明确选择时沿用；现成论文或单问任务无需重建目录、空报告和全部章节。
2. **按编号限制需求、要求后问必有提升。** 原编号用于组织，未编号需求也要覆盖。同一目标下放宽约束只保证最优值不劣，可能因约束不活跃而相等；据此诊断，不改变题意以强求提升。
3. **把样本数、试验次数和图表比例当通用阈值。** 模型适用性取决于数据结构和可验证证据；重复次数取决于不确定性目标；图数量服务论证。上游关于获奖论文图表占比的表述未在本次审阅中找到可复核统计依据，未采纳。
4. **用任意数字命中文稿判断数值一致。** 上游检查脚本对 JSON 数值做字符串命中提示，不能确认指标、题号、单位和版本。新脚本精确核对显式字段，仍诚实注明不能解析正文语义；语义一致由逐项审读完成。
5. **规则扫描混同文本问题和方法披露。** “示例数据”、代码路径或 AI 字样可能是必要说明；不能当作一律删除的正文污染。保留合成标识、限制与赛事要求的 AI 披露。
6. **单文件/路径/编译约定过强。** 单文件论文可以有效；LaTeX 资源搜索不普遍相对于包含它的章节文件；宏与动态引用需真实编译判定。两遍 xelatex 不涵盖所有 bibliography 工作流。对应 [graphicx 官方包](https://www.ctan.org/pkg/graphicx) 文档与项目编译结果核验。
7. **缺少编译或视觉检查仍可能写 PASS。** 无法运行与已通过不同；缺关键证据时交付状态为未完成，不因为记下原因就称可提交。
8. **库接口与数学经验过度泛化。** SciPy 字典 ineq 与线性约束上下界语义分开，见计算实现的官方链接；模型数值稳定不构成全局最优证明。保留既有技能对熵权重要性、PCA 方向、数据泄漏和仿真自证的限制，不机械叠加“推荐组合”。

## 权利与验证边界

上游根目录未识别统一许可证，但 [docs/md/License.md](https://github.com/jihe520/MathModelAgent/blob/83d8783187a2d29dda1b046cb667009cc50c8203/docs/md/License.md) 列明个人免费、商业用途及分发限制。不能将该项目当作任意复制再许可的 MIT 仓库。本次只学习公开工作流思路，独立撰写文字、数据契约和 Python 检查器；没有复制分发其 SKILL 全文、脚本、模板、字体或图像。第三方的限制不因本仓库原创内容采用 MIT 而改变。

保留两个原始资料仓库的 14 篇本科重点论文、9 组案例、35 条研读来源和文件目录索引；它们与新增工作流来源分表记录。新增工作流审阅不增加论文阅读数量，也不代表复现了 MathModelAgent 的完整产品或全部模板。

## 实现层补充审阅

后续已读取四个本科/MCM模板族、绘图入口及三个具体图脚本。详见[模板实现评析](template-implementation-review.md)及[50条源文件台账](implementation-review.json)。这些是源码静态审阅，未执行上游排版工具；新版的原创求解/图文交接由[算法实验](algorithm-lab.md)独立验证。
