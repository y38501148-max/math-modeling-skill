# 数学建模 Skill

面向**本科国赛、MCM/ICM 和课程建模项目**的中文 Codex 技能，覆盖题目拆解、模型选择、编程求解、结果验证、论文写作和优秀论文复盘。

由 [zhanwen/MathModel](https://github.com/zhanwen/MathModel) 与 [personqianduixue/Math_Model](https://github.com/personqianduixue/Math_Model) 的资料整理形成。重点研读 **14 篇论文、9 个题目**，对照 **7 份评阅材料**；全量索引 **9,893 个文件条目**，按 Git blob SHA 对应 **7,724 个独立内容**。这些文件数量不代表论文数量或已读全文数量。

## 本次工作流优化

参考 [jihe520/MathModelAgent](https://github.com/jihe520/MathModelAgent) 的 10 个技能入口和相关规范/检查代码，补强完整项目交接、歧义预检、实现与实验、图表溯源、论文编译和逐页验收。保持本科国赛与美赛重点，沿用已有偏好，并支持单问及局部修改。

- 新增阶段恢复与上游变更传播，避免继续使用过期结果。
- 新增原创结果证据检查器，核对文件 SHA-256、JSON 指标字段、百分比换算和显示容差。
- 验收明确区分已通过、失败、未执行和不适用；不以脚本通过代替论文或模型完整验证。
- 独立整理上游规则，未复制其模板和脚本。具体采用、修正和阅读边界见 [工作流来源评析](math-modeling/references/workflow-source-review.md)。

## 直接阅读

- [SKILL.md](math-modeling/SKILL.md)：实际执行入口。
- [本科案例分析](math-modeling/references/casebook.md)：同题不同解、关键优点、具体问题与迁移方法。
- [研究报告](docs/研究报告.md)：两个仓库的整理方法、主要发现与技能设计。
- [来源地图](math-modeling/references/source-map.md)：分类、固定提交、阅读范围和原文链接。
- [验证报告](docs/validation-report.md)：测试结果、局部复核与未覆盖范围。

## 使用

将 `math-modeling/` 作为一个技能目录安装，调用名称为 `$math-modeling`，界面名称为“数学建模”。自动选择保持默认开启。

示例：

> 使用 $math-modeling 分析这道本科建模题和附件。先给各问交付物、约束、数据检查与基线模型，再完成可运行求解和验证。

> 使用 $math-modeling 检查这篇论文的数学模型、结果表和摘要，重点核对是否有自证、约束遗漏或百分比表达错误。

> 使用 $math-modeling 比较 2018 国赛 B 的两种调度思路，解释状态建模、可行性验证和上界评估，并复现一个小规模例子。

仅需要某一小问、摘要或复盘时，技能按该范围工作，不要求生成整套文件。

## 安装与 GitHub 同步

选择希望长期保存的目录克隆。macOS/Linux 可将技能目录链接到本机技能路径，使本地技能与仓库使用同一份文件：

```bash
git clone https://github.com/y38501148-max/math-modeling-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/math-modeling-skill/math-modeling" "${CODEX_HOME:-$HOME/.codex}/skills/math-modeling"
```

若已有同名技能，先比较或备份，避免覆盖。也可直接复制 `math-modeling/`；复制安装需自行同步后续变更。安装后在新会话调用。

更新克隆：

```bash
git -C math-modeling-skill pull --ff-only
```

这是一份固定来源快照，**没有后台自动同步任务**。技能内容的 GitHub 更新和来源仓库更新是两件事；更新来源时需要重新索引并审阅新内容。

## 目录

```text
math-modeling/
  SKILL.md
  agents/openai.yaml
  references/
    project-workflow.md     完整项目、阶段交接与恢复
    computing.md            实现、实验与环境
    visualization.md        数据图与方法图
    delivery-review.md      编译、逐页查看与交付验收
    evidence-checker.md     数值证据工具契约
    workflow-source-review.md / workflow-sources.json
    model-selection.md      按问题结构选模型
    validation.md           可行性、样本外、数值与仿真检验
    paper-writing.md        从结果证据组织论文
    casebook.md             14 篇论文的 9 组案例
    source-map.md           来源与范围
    sources.json            35 条研读/上下文来源记录
    catalog.jsonl.gz         两仓库的文件元数据索引
    inventory-summary.json  目录统计
    schedule-checker.md      检查器的数据契约与局限
  scripts/
    catalog.py
    check_schedule.py
    check_evidence.py
  assets/
    modeling-brief.md
    schedule-example.json
    evidence-example/       合成指标与台账示例
docs/
tests/
```

## 辅助脚本

Python 3.9+，只用标准库，无 API Key、账户或联网依赖。

```bash
python3 math-modeling/scripts/catalog.py search --query "2018 A229" --unique
python3 math-modeling/scripts/catalog.py source P08
python3 math-modeling/scripts/check_schedule.py math-modeling/assets/schedule-example.json
python3 math-modeling/scripts/check_evidence.py math-modeling/assets/evidence-example/manifest.json
python3 -m unittest discover -s tests -v
```

结果证据工具通过仅表示声明的文件和字段一致，不证明模型正确或正文完整；完整验收还需语义检查、真实编译和页面审阅。当前 **37 项标准库工具测试通过**。

索引检索是路径/标题的元数据搜索，不是 PDF 全文搜索。调度检查器检查显式声明的独占资源、工序、日历、时长和时间窗；它不是完整 RGV 求解器，也不能证明最优或替代题意核验。

## 资料与质量边界

重点学习可解释的问题转化与验证设计，同时纠正历史资料中可确认的问题，例如 `min/max`、达成比例/最优差距、百分点、边界条件和 ARIMA 记号。优秀论文的收录标签不等于每个公式正确；本项目没有逐篇验证奖项，也没有复现历史论文的全部赛题结果。

本仓库仅包含原创技能说明、分析、脚本和文件级来源元数据。**不收录上游论文、书籍、课件、数据附件或第三方源程序全文。** 根目录 [MIT 许可证](LICENSE) 适用于本仓库原创内容，不改变所链接资料的权利归属。来源状态详见 [NOTICE.md](NOTICE.md)。
