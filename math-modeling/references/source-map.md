# 来源地图与研读边界

检索日期：2026-09-10。两个递归 Git tree 均未截断。文件清单包含数据、图片、缓存文件和压缩包；压缩包未展开，网盘内容未读取。

## 固定快照

| 仓库 | 固定提交 | 文件条目 | 原始文件字节总量 |
| --- | --- | ---: | ---: |
| [zhanwen/MathModel](https://github.com/zhanwen/MathModel) | `cd5be91735ebf11d5ee52eb170e86a6d07131977` | 1955 | 4,457,594,204 |
| [personqianduixue/Math_Model](https://github.com/personqianduixue/Math_Model) | `8783d0d822f89f98aa6182dd933cc2e9f3e2ddce` | 7938 | 5,953,522,844 |

共 9,893 个文件条目，按 Git blob SHA 得到 7,724 个字节级独立内容；两仓库共享 1,013 个 blob，合并后超出首次出现的重复条目为 2,169。加水印、重排版、格式转换的同一论文可能仍有不同 blob，因此不能把 7,724 解释为不同论文数。

## 本科优先的使用顺序

1. 第二个仓库 `2-1国赛题目+论文`：本科/专科国赛题目、论文和附件，按年份进入，再由正文核对组别。
2. 第二个仓库 `5-1国赛官方的评阅要点`：历史评阅材料的转载集合。标题/内容显示为评阅提示，但没有逐份向当前官方服务器验证来源链；不等于当届评分细则或唯一标准答案。
3. 第一个仓库 `美赛论文`：按年份整理，部分有奖项文件名。第二个仓库 `1-1按模型整理的美赛论文`：适合按方法找样本，但跨目录有重复，方法标签要查原文。
4. 两仓库算法、写作、模板目录：用于补充背景和实现，不取代原题与结果验证。
5. 第一个仓库 `国赛论文`、`国赛试题`及第二个仓库 `2-0研赛题目+论文`：大量为研究生竞赛资料。本索引将这些集合保守标为 graduate；这是集合级路由，不声称逐个文件均核验过组别。

路径分类结果：cumcm 2,905，mcmicm 868，graduate 2,866，general 3,254。cumcm 集合含本科与专科材料；本技能的 21 篇核心案例为本科国赛 A/B 与 MCM 题目。`undergraduate` 检索范围包含 cumcm 与 mcmicm，其他范围需显式选择。

## 初次研读（历史记录）

- 核心：14 篇论文、9 个题目，阅读摘要及与建模、算法、验证有关的重点章节；关键公式/表格核对 8 个 PDF 页面。
- 对照：7 份评阅文件，其中 R06 同时包含两道题；另读 4 份核心赛题、4 个代码示例、3 份写作/算法经验材料。
- 35 条来源记录包含以上材料、两个 README 的索引信息与一份嵌套许可证。
- 候选 P09/P10 文本层不足，未纳入核心案例；P11–P14 为研赛，按本科范围排除。候选缺口没有用摘要猜测补齐。
- 本轮完成结构化研读、静态检查与局部数值/数学关系复核，没有运行历史论文的完整程序，也没有复现全部赛题附件结果。
- 获奖等级仅沿用仓库目录/文件名作为线索；没有逐篇核实官方获奖记录，不将收录标签当作正确性保证。

## 来源表

PDF 页是文件页码。更细的读取、图像核验和运行状态在 [sources.json](sources.json)。

| ID | 类型 | 论文/文件 | 重点 PDF 页 |
| --- | --- | --- | --- |
| P01 | paper | [平行束 CT 系统的参数标定及成像](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/A053.pdf) | 1, 2, 4, 5, 6, 7, 10, 14, 17, 19 |
| P02 | paper | [基于单目标优化模型和图像重建算法的 CT 系统研究](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/A156.pdf) | 1, 2, 8, 11, 12, 19, 20, 22 |
| P03 | paper | [“拍照赚钱”的任务定价](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/B104.pdf) | 1, 2, 6, 7, 9, 10, 11, 12, 17 |
| P04 | paper | [基于优化理论的任务定价与分配模型](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/B264.pdf) | 1, 9, 10, 11, 12, 18 |
| P05 | paper | [基于非稳态导热的高温作业专用服装设计](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/A229.pdf) | 1, 7, 8, 11, 14, 16, 17 |
| P06 | paper | [高温作业专用服装设计](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/A401.pdf) | 1, 9, 20, 23, 28 |
| P07 | paper | [基于 0-1 规划的单 RGV 动态调度模型](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/B203.pdf) | 1, 5, 6, 15, 18, 22, 23 |
| P08 | paper | [RGV 的动态调度优化问题](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/B334.pdf) | 1, 4, 5, 6, 7, 8, 15, 16, 17, 18, 19, 21, 24 |
| P15 | paper | [Boarding at the Speed of Flight](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2007%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/B-2053-Outstanding.pdf) | 1, 2, 9, 10, 11, 16, 17, 18, 28, 29 |
| P16 | paper | [Optimization of irrigation time, pipe set placements, and irrigation uniformity for a hand move system](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2006%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/A-883-Outstanding.pdf) | 1, 3, 7, 10, 12, 14, 15 |
| P17 | paper | [Sustainable Energy Assessment](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90%20PCA/C78577-Sustainable%20Energy%20Assessment.pdf) | 1, 6, 12, 13, 14, 16, 17, 22 |
| P18 | paper | [CAFE: Characterization, Analysis, Forecasting, and Evaluation of Energy Profile](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E4%BC%98%E5%8A%A3%E8%A7%A3%E8%B7%9D%E7%A6%BB%E6%B3%95%20Topsis/C72969-CAFE%20Characterization%2C%20Analysis%2C%20Forecasting%2C%20and%20Evaluation%20of%20Energy%20Profile.pdf) | 1, 14, 15, 16, 17, 19, 22, 23 |
| P19 | paper | [Models for Evaluating Airline Overbooking](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%20dynamic%20programming/2002%20B%20O%20Models%20for%20Evaluating%20Airline%20Overbooking.pdf) | 1, 2, 4, 5, 6, 8, 9, 12, 13 |
| P20 | paper | [A Quasi-Sequential Cellular-Automaton Approach to Traffic Modeling](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E5%85%83%E8%83%9E%E8%87%AA%E5%8A%A8%E6%9C%BA%20cellular%20automata/2005%20B%20O%20A%20Quasi-Sequential%20Cellular-Automaton%20Approach%20to%20Traffic%20Modeling.pdf) | 1, 2, 4, 5, 8, 9, 11, 12, 13 |
| R01 | review | [2017数学建模A题评阅要点.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2017%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1A%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf) | 1, 2, 3, 4 |
| R02 | review | [2017数学建模B题评阅要点.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2017%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1B%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf) | 1 |
| R03 | review | [2018高教社杯全国大学生数建模竞赛A题评阅要点.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2018%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9BA%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf) | 1 |
| R04 | review | [2018高教社杯全国大学生数建模竞赛B题评阅要点.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2018%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9BB%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf) | 1, 2 |
| R05 | review | [2015高教社杯全国大学生数学建模竞赛B题评阅要点.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2015%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9BB%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf) | 1 |
| R06 | review | [2013高教社杯全国大学生数学建模竞赛评阅要点.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2013%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9B%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf) | 1, 2 |
| R07 | review | [mcm 2005 judge b.pdf](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E6%8E%92%E9%98%9F%E8%AE%BA%20queuing%20theory/mcm%202005%20judge%20b.pdf) | 1, 2, 5, 6, 7, 8 |
| T01 | problem | [CUMCM-2017-problem-A.docx](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/Problems/A/CUMCM-2017-problem-A.docx) | 文本/目录信息 |
| T02 | problem | [CUMCM-2017-problem-B.docx](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/Problems/B/CUMCM-2017-problem-B.docx) | 文本/目录信息 |
| T03 | problem | [CUMCM-2018-Problem-A-Chinese.docx](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/Problems/2018-A-Chinese/CUMCM-2018-Problem-A-Chinese.docx) | 文本/目录信息 |
| T04 | problem | [CUMCM-2018-Problem-B-Chinese.doc](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/Problems/2018-B-Chinese/CUMCM-2018-Problem-B-Chinese.doc) | 文本/目录信息 |
| A01 | code | [ahp.m](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/AHP%E5%B1%82%E6%AC%A1%E5%88%86%E6%9E%90%E6%B3%95/ahp.m) | 文本/目录信息 |
| A02 | code | [GM_1_1.m](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/GreySystem%E7%81%B0%E8%89%B2%E7%B3%BB%E7%BB%9F/GM_1_1.m) | 文本/目录信息 |
| A03 | code | [solve_lp.m](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/LinearProgramming%EF%BC%88%E6%B7%BB%E5%8A%A0%E4%BA%86%E7%BA%BF%E6%80%A7%E8%A7%84%E5%88%92%E3%80%81%E6%95%B4%E6%95%B0%E8%A7%84%E5%88%92%E7%AD%89%E5%86%85%E5%AE%B9%E7%9A%84%E4%BD%BF%E7%94%A8%E6%A1%88%E4%BE%8B%EF%BC%89/solve_lp.m) | 文本/目录信息 |
| A04 | code | [second_exponential_smoothing.m](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/TimeSeries%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E5%87%BD%E6%95%B0/%E6%8C%87%E6%95%B0%E5%B9%B3%E6%BB%91%E6%B3%95/second_exponential_smoothing.m) | 文本/目录信息 |
| L01 | license | [LICENSE](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/LICENSE) | 文本/目录信息 |
| W01 | writing | [如何写数学建模竞赛论文.md](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E6%8A%80%E5%B7%A7%E7%AF%87/%E5%A6%82%E4%BD%95%E5%86%99%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9B%E8%AE%BA%E6%96%87.md) | 文本/目录信息 |
| W02 | writing | [数学建模应掌握的十类算法.md](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E5%BA%94%E6%8E%8C%E6%8F%A1%E7%9A%84%E5%8D%81%E7%B1%BB%E7%AE%97%E6%B3%95.md) | 文本/目录信息 |
| W03 | writing | [比赛心得.md](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E6%AF%94%E8%B5%9B%E5%BF%83%E5%BE%97.md) | 文本/目录信息 |
| I01 | index | [README.md](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/README.md) | 文本/目录信息 |
| I02 | index | [README.md](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/README.md) | 文本/目录信息 |

## 检索工具

`catalog.jsonl.gz` 是全量文件元数据，包含仓库、固定提交、原路径、Git blob SHA、字节数、路径推断分类和已研读来源 ID。没有论文全文或数据附件。

```bash
python3 scripts/catalog.py stats
python3 scripts/catalog.py search --query "2017 A156" --kind paper
python3 scripts/catalog.py search --query "energy" --scope mcmicm --unique
python3 scripts/catalog.py search --query "AHP" --scope general --kind code
python3 scripts/catalog.py source P19
```

查询为空格分词后的 AND 匹配（不区分英文大小写），检索文件路径和已确认标题，不是全文或语义搜索。`--unique` 合并本次查询命中的同 blob 条目，`matching_aliases` 只列本次命中的路径，不代表全目录所有别名。`--limit` 只截取展示，不改变匹配总数。

固定提交链接使研读结果可追溯。上游更新后若要补充，重新获取 tree、核对重复、阅读新来源并更新分类/证据记录，不直接替换为浮动 master 的结论。

## 内容来源与权利

两仓库根目录未识别到统一许可证；第二个仓库算法子目录有独立 MIT 许可证（L01），不能推定其覆盖论文、书籍和其他目录。本技能只公开原创分析、脚本及文件级引用元数据；不打包原论文、课件、书籍、水印页面、附件数据或第三方源程序。引用保留原作者及来源的权利，历史结论均保持归因。

## 工作流优化的独立来源

MathModelAgent 的技能审阅及固定提交另记在 [工作流来源评析](workflow-source-review.md) 和 [workflow-sources.json](workflow-sources.json)。原始论文目录与 sources.json 保持两仓库的历史索引范围；工作流文件不混入论文统计。

## 本轮三仓库扩展

新增7篇论文后共21篇、15组题目；新增7个原PDF页面核验，累计15页。sources.json现有44条记录；额外2份赛事结果新闻稿按contest-context记录。此前4个代码示例包含在本轮199个核心文件中，不能相加计数。

两个资料库代码盘点1478条，199文件取得并哈希校验，197静态审阅（194个blob），仅A196原C++实际运行。A156绘图/A158大型测试驱动未审阅。见[算法指南](algorithm-playbook.md)、[算法台账](algorithm-review.json)、[完整代码盘点](algorithm-inventory.jsonl.gz)。随书附件与压缩包仍主要是索引级覆盖。

MathModelAgent在前轮入口规范之外新增50个实现文件审阅，详见[实现评析](template-implementation-review.md)与[台账](implementation-review.json)。使用catalog.py source T057可取第三仓库固定链接，但search目录统计仍保持两个资料库范围。

| ID | 文件 | 重点PDF页 | 原页视觉核验 |
|---|---|---|---|
| P21 | [基于排序检验的葡萄酒评价](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2012/A301.pdf) | 2, 3, 4, 5, 6, 7, 20 | 7 |
| P22 | [葡萄酒的质量分析与评价](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2012/A335.pdf) | 1, 9, 10, 11, 28 | 10 |
| P23 | [碎纸复原模型与算法](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2013/B506.pdf) | 3, 4, 5, 6, 7, 16, 17, 18, 19 | 7 |
| P24 | [论文标题（首页占位；内容为系泊系统设计）](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2016/A028.pdf) | 1, 4, 5, 6, 7 | 6 |
| P25 | [小区开放对道路通行的影响](https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2016/B022.pdf) | 1, 19, 20, 24, 25, 26 | 20 |
| P26 | [Designing the Optimal Snowboard Half-Pipe](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2011%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/A-11199-Outstanding.pdf) | 1, 4, 7, 8, 19 | 8 |
| P27 | [Tracking Serial Criminals with a Road Metric](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2010%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/B-7273-Outstanding.pdf) | 1, 4, 5, 6, 11, 17 | 5 |
| R08 | [2011 MCM Press Release—April 15, 2011](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2011%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/Results/2011-Problem-A.pdf) | 1 | 无 |
| R09 | [2010 MCM Press Release—April 1, 2010](https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2010%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/Results/2010_MCM_Problem_B.pdf) | 1 | 无 |

新增题目模型及可复现入口见[案例补充](casebook-expanded.md)。本轮原数值运行、教学例与未覆盖范围见[算法实验说明](algorithm-lab.md)。
