**Principle of Alpha Design 框架 Victor**

“Man is a creature that became successful because he was able to make sense of his environment and develop rules more effectively than his natural competitors could. “

-Igor Tulchinsky

**I. 定义**
Alpha在金融领域，基本定义为阿尔法系数，一般为基金绝对回报和无风险投资收益的差值。
在量化交易领域，Alpha指代一种预测模型，通过对金融工具的价格，风险，收益进行预测，统计关系套利，配置迭代等实现更高的alpha系数；

这种对alpha的探索和优化，实际就是资产组合选择问题的另一种表达形式。所谓，[资产组合选择] ，是优化一组资产的财富分配和长期增长的解法问题，是一直以来量化金融领域的核心。在探索这个问题的道路上，主要形成了两个学派: 其一，基于马科维茨和其所在金融界发展出的均值方差理论。其二，本质起源于信息论的资本增长理论。

在资产管理行业中，众所周知的Mean-Variance Theory着重于单期（批量）投资组合选择，通过权衡投资组合的预期收益（即，均值）和风险（即，方差），在投资者的风险收益偏好下，构筑最优。另一方面，Capital Growth Theory侧重于多期或连续投资组合的选择，旨在最大化投资组合的预期增长率或预期对数收益。

虽然这两种理论都解决了投资组合选择的任务，但是对于我们追求的迭代性的投资策略来说，后者更适用这种本质便是连续性决策问题的基本环境。
