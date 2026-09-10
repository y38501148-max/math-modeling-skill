# 本科论文案例库：借鉴结构，核验结论

选取 14 篇论文，覆盖 9 个题目。以下是重点章节研读，不是全部正文、附录和程序的逐行复现。**论文观察**描述原文，**分析/迁移**是本技能的判断；作者报告的数值不等于本项目已复算的赛题结果。页码均指 PDF 文件页（从 1 开始），不一定等于印刷页码。来源 ID 可通过 `scripts/catalog.py source P01` 查询固定提交与哈希，页码核查记录见 `sources.json`。

## C1．2017 本科国赛 A：先标定，再重建

来源：[P01]、[P02]；题目 [T01]；评阅提示 [R01]。

**论文观察。** P01 用小圆的投影不变性估计探测器间距，从圆与系统的相对运动提取旋转中心与角度，再用滤波反投影重建。重叠投影区使用边缘提取；还设计多边形模板增加特征方向（PDF 4–7、14、17–21 页）。P02 用相邻弦长与观测的比值消去公共增益，分步骤搜索间距、位置和角度；加入噪声重复估计间距（6–8、11–12、19–22 页）。

**优点。** 两者都利用题目模板的特殊几何关系，把参数辨识与图像重建连接起来。P02 给出数值扰动实验，比只宣称模型稳定更可检查；P01 的模板设计明确关注可提取特征的数量和误差。

**对照与修正。** R01 要求针对实际模板标定，核查非中心旋转与噪声，并鼓励自行构造数据检验。P01 第 19 页把非线性超定方程导向智能搜索，但其余弦关系可改写为线性最小二乘，见模型选择指南；不能以“非线性”排除结构化求解。P02 的少量噪声重复只支持所测参数与噪声水平，不能替代整个重建流程的鲁棒性证据。

**迁移。** 先检查参数可辨识性、几何初始化与增益，再用已知真值的合成投影检验整条链。测量噪声与模板形状均做扰动；区分标定误差、重建误差、展示归一化。这里没有复现两篇论文的全部图像和吸收率。

## C2．2017 本科国赛 B：历史定价、任务分配与真实完成不是一件事

来源：[P03]、[P04]；题目 [T02]；评阅提示 [R02]。

**论文观察。** P03 构造位置偏僻程度、会员/任务密度，拟合历史价格，再引入会员信誉、博弈式定价和邻近任务打包（6–12、17 页）。P04 将可接受任务与会员建立二分图，会员限额进入容量约束，用最大流评价某个价格下可分配的任务量，外层再搜价格（8–12 页）。

**优点。** P03 说明如何由地理数据构造可解释特征；P04 将“愿不愿接”与“有没有容量”分开，形成可计算的分配模型。打包改变任务集合后重新评价，比只给聚类图更完整。

**对照与修正。** R02 强调成本控制、会员吸引力、机会均衡以及抢单模拟。P04 第 12 页报告总定价从 57641.5 到 58732.6，完成率从 62.1% 到 86.6%。直接复算为成本约增 1.89%、完成率增 **24.5 个百分点**（相对约增 39.45%）。这不是严格同预算比较，最大流分配也不等于自主抢单的现实结果。P03 用已完成任务拟合来解释失败原因时，也不能把关联直接写成价格的因果作用。

**迁移。** 建三个明确对象：历史价格模型、完成/接受机制、预算下的策略。历史标签用于验证，未来未知难易度不伪装成已知特征；用同预算、同会员容量、同地理范围进行对照，再通过行为模拟或实际验证评估策略。

## C3．2018 本科国赛 A：方程完整比曲线光滑重要

来源：[P05]、[P06]；题目 [T03]；评阅提示 [R03]。

**论文观察。** 两文都采用多层一维非稳态热传导与隐式差分，再搜索厚度。P05 用后向欧拉和厚度组合枚举（7–17 页）；P06 明确构造三对角线性系统并用追赶法求解，比较测量温度和模型温度并改变环境温度分析最优厚度（9、20、23、28 页）。

**优点。** 将热量传递、参数估计、厚度优化分层，保留空间和时间变化；将数值求解流程落到离散方程与程序，而非仅列热传导方程。

**对照与修正。** R03 指出初始、边界和交界面条件不可缺，有限换热边界需估计参数。两文外侧采用给定温度条件，不能直接当作该题有限换热的标准答案。P05 第 8 页边界公式出现时间导数，第 11 页又改为空间导数，移用前须统一物理定义、方向和量纲。第 14 页表格约在 3322–3323 秒越过 44℃，与紧邻文字的“超过 44℃为 260 秒”不一致；若单调升温并持续到 3600 秒，累计超限约 277 秒，须从全时序重算。P06 的拟合残差较小也不能单独验证其边界假设。

**迁移。** 明确两端换热和界面守恒，使用瞬态数据辨识；检查网格收敛、观测扰动以及厚度取整后的约束。持续时间约束是指示函数积分，不是达到阈值的时刻。不能在两篇不同模型给出的厚度之间直接选更薄者。

## C4．2018 本科国赛 B：事件推进、可行时间表与有效上界

来源：[P07]、[P08]；题目 [T04]；评阅提示 [R04]。

**论文观察。** P07 以 0–1 调度选择和每轮所需时长组织模型，考虑单/双工序以及故障，比较两类信息可见性（5–6、15、18、22–23 页）。P08 将系统抽象为多队列状态图，以事件时刻推进；用容量上界比较近似解，并在附录说明短时域精确搜索不能直接扩展到完整班次（5–8、15–19、21 页）。

**优点。** 状态包含剩余加工时间、位置和工序，避免逐秒大量空转；分析能力瓶颈，有助于解释算法结果。模型扩展遵循“无故障单工序→双工序→随机故障”的清晰关系。

**对照与修正。** R04 强调可行性优先，要求结果事件表能够验证。P08 第 7 页文字说双工序取较低产能，公式却写 `max`；较紧的瓶颈界应为 `min`。第 16 页定义相对差距 `|A-U|/U`，表中填的却是达成比例 `A/U`：`382/384≈0.9948`，真正差距约 `0.005208`。原式 `max` 可能仍给出松上界，但不能支撑所述瓶颈解释。此处已核对 PDF 页面。

**迁移。** 将问题约束和启发式决策规则分开；用独立事件检查器验证资源/工序/时限，再评价产量和距上界差距。故障比较使用多场景，报告分布。`check_schedule.py` 提供通用检查基础，具体 RGV 仍须加入移动、清洗、携料、报废与首尾班次语义。

## C5．2007 MCM B：登机瓶颈与可配置仿真

来源：[P15]，来自第一个仓库，PDF 1–2、9–11、16–18、28–29 页。

**论文观察。** 先用排队网络解释过道阻塞，再以座位网格和乘客行为仿真比较登机方案。参数区分行走速度、入舱间隔、放行李时间、座位干扰等；结论同时给方案建议与影响因子的优先级。作者说明排队近似不能充分表达每排有限座位，因此未将其作为主模型。

**优点。** 简化模型用于理解机制，细化模拟用于比较；明确哪些参数来自估计以及模型未覆盖的行为。仿真结构可改变飞机布局与乘客特征。

**分析/迁移。** 借鉴这种层次而非直接复制队列定理及“某方案永远最好”的判断。乘客会出错、家庭会结伴，行李时间也可能相关；在改变这些机制后检查排序。输出平均时间及尾部风险，模拟结论不能写成航空公司的实测改进。

## C6．2006 MCM A：灌溉覆盖、均匀性与局部约束

来源：[P16]，来自第一个仓库，PDF 3、7、10、12、14–15 页。

**论文观察。** 用圆覆盖给初始喷头布局，将灌水累加到空间网格；随机扰动优化均匀性，再组织管道移动计划。作者报告无风假设、喷嘴剖面替代以及尚无实地验证。

**优点。** 几何、物理分布、空间数值评价与操作日程接起来；明确均匀性指标不能描述所有局部差异。

**分析/迁移。** 第 14 页承认边缘区域没有获得所要求的最低水量，却以边缘损伤等理由弱化问题。学习时应保留题目“每处最低水量”的硬约束，不能用均匀度平均分豁免。检查瞬时灌溉率与周期累计水深，细化边界网格，对风和喷头剖面扰动；只能称当前可行解，不能由随机算法运行一次证明布局最优。

## C7．2018 MCM C：两种能源评价—预测链

来源：[P17]、[P18]，来自第二个仓库；分别重点看 PDF 6、12–17、22 页和 14–19、22–23 页。

**论文观察。** P17 将能源指标分层，用 PCA 与 AHP 组合评价并以 ARIMA 外推，预处理特别提醒有些零是真实零。P18 将多维能源数据聚合为概况，用熵权/TOPSIS 评价，以 GPR 与局部 ARMA 组合连接短期波动和长期趋势，再转到州际目标优化。

**优点。** 都把指标定义、评价、预测和政策输出分开；P18 用参数扰动说明局部模型权重和衰减如何改变预测。P17 主动讨论数据含义，比将零一律视作缺失更合理。

**对照与修正。** P17 采用 `ARIMA(p,q,d)` 记号并给 `(4,4,2)`，按其变量定义转为常见软件 `(p,d,q)` 应是 `(4,2,4)`，不能直接复制三元组；本项目核对的是记号，不重估最优阶数。P18 以图形趋势合理解释组合模型，仍需滚动回测和分组件对照才能证明预测改进。其优化把部分硬约束转为惩罚项，也需解释被允许的外部输入/缺口与业务意义。

**迁移。** 明确评价偏好与 PCA 方差的差别；检查零、人口尺度和填补方法。按时间拟合预处理，分别验证评价排名、预测误差、最终决策稳定性。远期目标保留情景不确定性；不能以更多方法或更平滑的图替代验证。

## C8．2002 MCM B：超售方案的事前评估与事后上限

来源：[P19]，PDF 4–9、12–13 页（印刷页 304–309、312–313）。

**论文观察。** 采用预期边际座位收益 EMSR 设定舱位保护量，将超售方案放入订票仿真；另以历史需求重构理想收益机会，评价实际方案。主动说明单航段、价格给定及历史需求可得等简化。

**优点。** 区分“策略事前会怎样”与“知道真实需求后最多能做多好”；讨论售罄后需求记录被截断的问题。

**分析/迁移。** 文件虽放在“动态规划”目录，本文主体选用 EMSR，目录不能代替方法识别。事后完全信息收益是比较基准，不能当作在线可实现策略。迁移到库存/预约时区分潜在需求和观测销量，校准拒绝成本；不沿用文中年代久远的赔偿规则或行业数值。

## C9．2005 MCM B：收费站入口、服务与出口缺一不可

来源：[P20]；评委评论 [R07]。重点为 PDF 4–5、8–9、11–13 页与 R07 第 1–8 页。

**论文观察。** 用准顺序元胞更新区分入口、收费、扩张、合流区域，扫描到达强度与亭数，查看通过时间突增的阈值以及最大等待。R07 指出简单排队模型难以表达换道、服务异质性和出口反堵，并讨论模型比较、敏感性与清晰表达。

**优点。** 在接近拥堵阈值的负载范围比较方案，同时关注平均和个体最坏等待；几何设施变化通过行为规则影响拥堵。

**分析/迁移。** 原文对泊松与指数分布的对比不可直接照抄：计数和间隔是不同随机对象，在泊松过程中二者相容。保留入口之外积压的需求；服务时间不只测试常数；检查更新顺序引入的偏差与守恒。独立重复并显示尾部，避免只统计成功离开的车辆。

## 补充：答案与算法示例如何使用

- [R05]（2015 本科 B）要求真实时空数据支持出租车供需指标和补贴分析，宏观总数不足以替代空间/时段匹配；政策需检验或仿真。本轮候选 P09 文本层不足，未纳入上述 14 篇案例。
- [R06]（2013 本科 A/B）分别强调从视频提取实际车流、碎纸片的方向性距离与程序结果一致。人工干预应报告节点和数量，不能只拿最终复原图充当算法证据。
- [A01] 只返回 AHP 特征向量与最大特征值，不能自动代表完整一致性检验；还需检查正互反矩阵、CR 和输入退化。
- [A02] 先取阈值事件的索引，再对索引序列累加建模；输入输出语义不等于原观测值的预测。
- [A03] 将目标与解均写为列向量却使用 `c*x`，维度不成立；重写时按标量内积处理，并核对最大化转最小化的符号。此结论是静态维度检查，没有在 MATLAB 中运行原文件。
- [A04] 是固定参数的二次指数平滑演示。须对齐一步预测的时间索引，并在留出窗口比较朴素基线，不以同样本绘图证明预测准确。

## 建议的本科练习顺序

先用 C2 学习数据—特征—分配，再用 C4 做可行性和算法比较，用 C3/C1 理解完整机理与参数估计，最后用 C7 学习多阶段综合题。每次只复现一条证据链：小问输入、模型、程序输出、独立检查和一段结果说明。仅研读论文时，可按“问题、假设、转化、算法、验证、失效条件”六栏做笔记。

## 固定版本来源链接

[P01]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/A053.pdf
[P02]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/A156.pdf
[P03]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/B104.pdf
[P04]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/B264.pdf
[P05]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/A229.pdf
[P06]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/A401.pdf
[P07]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/B203.pdf
[P08]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/B334.pdf
[P15]: https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2007%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/B-2053-Outstanding.pdf
[P16]: https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/2006%E7%BE%8E%E8%B5%9B%E7%89%B9%E7%AD%89%E5%A5%96%E5%8E%9F%E7%89%88%E8%AE%BA%E6%96%87%E9%9B%86/A-883-Outstanding.pdf
[P17]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E4%B8%BB%E6%88%90%E5%88%86%E5%88%86%E6%9E%90%20PCA/C78577-Sustainable%20Energy%20Assessment.pdf
[P18]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E4%BC%98%E5%8A%A3%E8%A7%A3%E8%B7%9D%E7%A6%BB%E6%B3%95%20Topsis/C72969-CAFE%20Characterization%2C%20Analysis%2C%20Forecasting%2C%20and%20Evaluation%20of%20Energy%20Profile.pdf
[P19]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%20dynamic%20programming/2002%20B%20O%20Models%20for%20Evaluating%20Airline%20Overbooking.pdf
[P20]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E5%85%83%E8%83%9E%E8%87%AA%E5%8A%A8%E6%9C%BA%20cellular%20automata/2005%20B%20O%20A%20Quasi-Sequential%20Cellular-Automaton%20Approach%20to%20Traffic%20Modeling.pdf
[R01]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2017%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1A%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf
[R02]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2017%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1B%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf
[R03]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2018%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9BA%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf
[R04]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2018%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9BB%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf
[R05]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2015%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9BB%E9%A2%98%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf
[R06]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/5-1%E5%9B%BD%E8%B5%9B%E5%AE%98%E6%96%B9%E7%9A%84%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9/2013%E9%AB%98%E6%95%99%E7%A4%BE%E6%9D%AF%E5%85%A8%E5%9B%BD%E5%A4%A7%E5%AD%A6%E7%94%9F%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9B%E8%AF%84%E9%98%85%E8%A6%81%E7%82%B9.pdf
[R07]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/1-1%E6%8C%89%E6%A8%A1%E5%9E%8B%E6%95%B4%E7%90%86%E7%9A%84%E7%BE%8E%E8%B5%9B%E8%AE%BA%E6%96%87/%E6%8E%92%E9%98%9F%E8%AE%BA%20queuing%20theory/mcm%202005%20judge%20b.pdf
[T01]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/Problems/A/CUMCM-2017-problem-A.docx
[T02]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2017/Problems/B/CUMCM-2017-problem-B.docx
[T03]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/Problems/2018-A-Chinese/CUMCM-2018-Problem-A-Chinese.docx
[T04]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/2-1%E5%9B%BD%E8%B5%9B%E9%A2%98%E7%9B%AE%2B%E8%AE%BA%E6%96%87/2018/Problems/2018-B-Chinese/CUMCM-2018-Problem-B-Chinese.doc
[A01]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/AHP%E5%B1%82%E6%AC%A1%E5%88%86%E6%9E%90%E6%B3%95/ahp.m
[A02]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/GreySystem%E7%81%B0%E8%89%B2%E7%B3%BB%E7%BB%9F/GM_1_1.m
[A03]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/LinearProgramming%EF%BC%88%E6%B7%BB%E5%8A%A0%E4%BA%86%E7%BA%BF%E6%80%A7%E8%A7%84%E5%88%92%E3%80%81%E6%95%B4%E6%95%B0%E8%A7%84%E5%88%92%E7%AD%89%E5%86%85%E5%AE%B9%E7%9A%84%E4%BD%BF%E7%94%A8%E6%A1%88%E4%BE%8B%EF%BC%89/solve_lp.m
[A04]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/TimeSeries%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97%E5%87%BD%E6%95%B0/%E6%8C%87%E6%95%B0%E5%B9%B3%E6%BB%91%E6%B3%95/second_exponential_smoothing.m
[L01]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/3-1%E7%AE%97%E6%B3%95-Algorithms_MathModels/LICENSE
[W01]: https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E6%8A%80%E5%B7%A7%E7%AF%87/%E5%A6%82%E4%BD%95%E5%86%99%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E7%AB%9E%E8%B5%9B%E8%AE%BA%E6%96%87.md
[W02]: https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E6%95%B0%E5%AD%A6%E5%BB%BA%E6%A8%A1%E5%BA%94%E6%8E%8C%E6%8F%A1%E7%9A%84%E5%8D%81%E7%B1%BB%E7%AE%97%E6%B3%95.md
[W03]: https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/%E6%AF%94%E8%B5%9B%E5%BF%83%E5%BE%97.md
[I01]: https://github.com/zhanwen/MathModel/blob/cd5be91735ebf11d5ee52eb170e86a6d07131977/README.md
[I02]: https://github.com/personqianduixue/Math_Model/blob/8783d0d822f89f98aa6182dd933cc2e9f3e2ddce/README.md

## 新增六组案例

[案例补充C10–C15](casebook-expanded.md)：葡萄酒评价（同题两解）、碎纸复原、系泊系统、开放小区交通、半管滑道、地理概率模型。合计新增7篇，连同本页14篇，共21篇关键章节研读。
