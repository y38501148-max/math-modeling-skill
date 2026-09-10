# 数学建模 Skill

面向**本科国赛、MCM/ICM和课程建模**的中文Codex技能，覆盖题目拆解、模型选型、算法实现、结果验证、论文写作与交付。

综合参考 [zhanwen/MathModel](https://github.com/zhanwen/MathModel)、[personqianduixue/Math_Model](https://github.com/personqianduixue/Math_Model) 和 [jihe520/MathModelAgent](https://github.com/jihe520/MathModelAgent)。技能内容为独立整理与实现，不分发上游论文、教材或模板全文。

## 写作经验与成稿样例更新

根据两份用户PDF，重整[论文写作指南](math-modeling/references/paper-writing.md)：区分重述、分析和建模前准备，补充标题、逐问摘要、关键词、符号表、图表解释与明确答案；保留必要验证，不按条数美化优缺点。检查7页经验分享及成稿15个相关原页，记录[采用范围、修正及模板差异](math-modeling/references/writing-source-review.md)。仅更新说明，不把成稿作为已验证标准答案，也不分发原PDF。

## 2026国赛格式更新

根据用户提供的`format2026.doc`及核对后的官方文件，增加[2026国赛专用规则](math-modeling/references/cumcm-2026-format.md)，接入项目启动、写作、模板选择和交付验收。覆盖页面与双版本、正文无目录且不超过30页、完整代码附录、匿名、两个电子文件各自20MB上限，以及AI声明和详情PDF。仅按赛事/年份启用；不改变MCM/ICM或课程项目要求。原始文件未收入仓库。

## 三仓库全面优化

- **算法**：盘点1,478个代码文件，取得并校验199个核心文件，静态审阅197个，整理输入契约、适用条件、实现风险与MATLAB/Python迁移。文件包含辅助程序和重复内容，不等于197种算法。
- **论文**：关键章节研读扩大到21篇、15组题目；新增葡萄酒评价、碎纸复原、系泊系统、开放小区、半管滑道和地理概率模型，累计查看15个关键PDF原页。
- **实例技能**：在10个技能入口及相关规范的基础上，进一步读50个模板/绘图实现文件，提炼阶段交接、排版验收和真实结果绑定。
- **可运行验证**：新增原创算法实验与半管滑道微型交付链；60项测试通过，并实际编译运行上游Floyd程序的正例和负边反例。

详细证据、采用与修正、未覆盖范围见[三仓库全量优化报告](docs/三仓库全量优化报告.md)。所有计数区分目录索引、源码审阅与实际执行；没有声称全文读完或复现三个仓库所有程序。

## 阅读入口

| 用途 | 文件 |
|---|---|
| 实际技能入口 | [SKILL.md](math-modeling/SKILL.md) |
| 完整项目与阶段恢复 | [项目工作流](math-modeling/references/project-workflow.md) |
| 模型选择与算法契约 | [模型选型](math-modeling/references/model-selection.md)、[算法指南](math-modeling/references/algorithm-playbook.md) |
| 原创可运行例 | [算法实验](math-modeling/references/algorithm-lab.md)、[半管交付示例](math-modeling/assets/lab-example/manuscript.md) |
| 同题不同解、公式与代码复盘 | [原9组案例](math-modeling/references/casebook.md)、[新增6组案例](math-modeling/references/casebook-expanded.md) |
| 第三个仓库的具体实现 | [模板/图脚本评析](math-modeling/references/template-implementation-review.md) |
| 固定版本与阅读状态 | [来源地图](math-modeling/references/source-map.md) |
| 测试及实际数值 | [验证报告](docs/validation-report.md)、[本轮结果](math-modeling/assets/lab-example/results.json) |

## 使用与安装

调用名称为 `$math-modeling`，界面名称为“数学建模”。支持完整求解，也支持单问、局部代码修复、论文复盘或写作，不强制从头重做。

> 使用 $math-modeling 分析这道本科建模题与附件。先核对各问交付物、数据和约束，再完成可运行基线、改进、独立验证和论文结果。

> 使用 $math-modeling 审查这段MATLAB代码。解释数学对象，构造退化或边界反例，区分原程序执行和独立重实现。

> 使用 $math-modeling 复盘这篇论文，把模型公式、附录代码、数据和结果表逐项对应，找出可迁移结构与需要重算的结论。

选择长期保存目录克隆；macOS/Linux可以链接安装，使技能与本地仓库为同一份：

```bash
git clone https://github.com/y38501148-max/math-modeling-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/math-modeling-skill/math-modeling" "${CODEX_HOME:-$HOME/.codex}/skills/math-modeling"
```

已有同名技能时先比较或备份；也可复制`math-modeling/`，复制安装需自行同步。安装后在新会话调用。更新使用`git -C math-modeling-skill pull --ff-only`。

本项目是固定来源快照，没有后台自动同步任务。来源仓库更新与技能更新分别核验，不能自动采用未经审阅的新结论。

## 脚本与验证

以下检索/检查脚本只需Python标准库，无账户、API Key或网络依赖：

```bash
python3 math-modeling/scripts/catalog.py search --query "2018 A229" --unique
python3 math-modeling/scripts/catalog.py source P25
python3 math-modeling/scripts/catalog.py source A196
python3 math-modeling/scripts/catalog.py source T057
python3 math-modeling/scripts/check_schedule.py math-modeling/assets/schedule-example.json
python3 math-modeling/scripts/check_evidence.py math-modeling/assets/evidence-example/manifest.json
```

可选数值实验需NumPy/SciPy，生成图文还需Matplotlib：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install numpy scipy matplotlib
.venv/bin/python math-modeling/scripts/modeling_lab.py --out work/lab-result
.venv/bin/python math-modeling/scripts/check_evidence.py work/lab-result/evidence.json
.venv/bin/python -m unittest discover -s tests -v
```

三仓库优化时，完整依赖环境下60项测试通过。后续2026格式与写作资料更新仅修改技能说明，核验技能结构、内部链接及资料采用范围。没有数值依赖时21项数值测试会明确跳过。实验只用合成参数，另有P25表数的局部算术检查；结果不代表真实赛题成绩。生成过程写入独立目录并覆盖同名演示文件。

索引为两个资料库的9,893条文件元数据、7,724个blob，不提供PDF全文搜索。`source`支持论文、算法、模板实现三层台账；第三仓库没有混入论文目录统计。证据检查器只核对声明的文件和数值字段，调度检查器只核对已编码的事件约束，两者均不能证明模型完整或最优。

## 来源与权利

固定提交和阅读/运行范围见[来源地图](math-modeling/references/source-map.md)、[算法台账](math-modeling/references/algorithm-review.json)、[模板实现台账](math-modeling/references/implementation-review.json)。未执行全部MATLAB程序，未复现所有历史论文，未编译上游排版模板，未逐篇核实奖项。历史优秀论文和示例技能也需要验证。

根目录[MIT许可证](LICENSE)适用于本项目原创说明、代码和合成示例，不改变上游权利归属；参见[NOTICE.md](NOTICE.md)。
