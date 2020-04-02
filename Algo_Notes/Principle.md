**Principle of Alpha Design, 量化设计原则 by Victor Xiao**

“Man is a creature that became successful because he was able to make sense of his environment and develop rules more effectively than his natural competitors could. “

-Igor Tulchinsky

**I. 定义**

Alpha在金融领域，基本定义为阿尔法系数，一般为基金绝对回报和无风险投资收益的差值。
在量化交易领域，Alpha指代一种预测模型，通过对金融工具的价格，风险，收益进行预测，统计关系套利，配置迭代等实现更高的alpha系数；

这种对alpha的探索和优化，实际就是资产组合选择问题的另一种表达形式。所谓，[资产组合选择] ，是优化一组资产的财富分配和长期增长的解法问题，是一直以来量化金融领域的核心。在探索这个问题的道路上，主要形成了两个学派: 其一，基于马科维茨和其所在金融界发展出的均值方差理论。其二，本质起源于信息论的资本增长理论。

在资产管理行业中，众所周知的Mean-Variance Theory着重于单期（批量）投资组合选择，通过权衡投资组合的预期收益（即，均值）和风险（即，方差），在投资者的风险收益偏好下，构筑最优。另一方面，Capital Growth Theory侧重于多期或连续投资组合的选择，旨在最大化投资组合的预期增长率或预期对数收益。

虽然这两种理论都解决了投资组合选择的任务，但是对于我们追求的迭代性的投资策略来说，后者更适用这种本质便是连续性决策问题的基本环境。

**II. 三轴计划**

三轴计划的结构要求我们：首先，应确定此alpha的应用领域，如特定区域金融市场，行业垂直，或是特定金融工具集。以此出发，我们需要确定一个交易频次，以进一步定义自己需要的数据类型。

基本的交易频次分为三种：日内交易，每日调仓，和每周/每月调仓。日内交易通常是高频性position rebalance，要么以特定预设频次调仓，如：每1分钟，5分钟等。要么以交易数据或特定事件驱动。每日调仓如名所指，主要以三种数据使用不同区分：Delay N: 每日以n天前的数据进行调仓。Delay 0 snapshot，以一个特定时间点前的数据进行调仓。MOO/MOC：Market on Open, Market on Close，则是一种针对开盘收盘拍卖区间的交易算法。

当我们确认了一个算法的交易区域及其频次后，我们可以开始践行数据的收集。常见的数据包括：技术面的价格和交易量，基本面的公司数据，宏观层面的GDP，就业率，前面演讲所提到的policy rate, risk-free yield。如果算法复杂度更高，运用如自然语言处理技巧的话，公开市场委员会报告，论文，研报，新闻，甚至推文等字节分析和多媒体分析都可以成为模型的input parameter。

在构筑具体策略模型前，我们还需要确定策略的基本目标和衡量指标，需要考虑的基本上包括几个层面：回报，夏普比率，交易费用，回撤，流动性，风险。

如此，当我们确定了三轴的应用区域，指标，交易频次和数据集后，一个基本的策略思路就形成了。

IV. **一些经典策略**

1. 基准策略*Benchmark*: 是一种追求长期大盘或是获取大盘自筛选性收益形成的算法类型。这种策略的基本假设就是市场有效假说，且大盘长期向上。

   Ex:Buy and hold, Best Stock, Constant Rebalanced Portfolio

2. 跟随赢家*Follow the Winner*：如名所指，旨在不断追随大盘领先者以获取收益的方法。是一种将仓位配比由underperformed资产调至outperformed的资产，以保证长期持有赢家的策略。这种策略的基本假设，是赢者稳赢。

   Ex:Universal Portfolio, Exponential Gradient, Follow the Leader, Follow the Regularized Leader, Aggregate-Type Leader

3. 跟随败者*Follow the Loser*：这种策略的思路与上一策略相反，基本假设是现阶段的败者有机会反弹，并反超其他资产实现收益。如此，这种策略的特点是将outperformed的资产调至underperformed的资产中。

   Ex:Anti-correlation, Passive Aggressive Mean Reversion, Confidence Weighted Mean Reversion, Online Moving Average Reversion.

4. 规律套利*Patterns Arbitrage*：这种套利策略的基本假设与EMH相反，相信市场并非完全随机漫步，存在必然有迹可循的客观规律。如此，并非完全随机的市场时间序列就可以作为寻找规律的数据集。技术分析的根本思路，其实也与此类似。

5. 荟萃学习算法*Meta Learning Algorithm*：
在机器学习中，学习，一般指代对特定代价函数的优化，我们最大化贝叶斯模型的似然估计，最小化神经网络中的平均方差，或是最大化增强学习中的期望回报。荟萃学习，则是优化这种机器学习进程的策略。

   EX:Aggregating Algorithms，Fast Universalization, Online Gradient Updates, Follow the Leading History.




