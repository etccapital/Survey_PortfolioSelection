In recent years, machine learning has been applied to various applications in finance (Gy¨orfi et al.,
2012), including On-line Portfolio Selection, which aims to sequentially allocate capital among a
set of assets, such that the investment return can be maximized in the long run (Kelly, 1956). It
has attracted increasing attention from both academia and industry, and several machine learning
algorithms have been proposed (Li and Hoi, 2014), including traditional algorithms (Cover, 1991;
Helmbold et al., 1998; Agarwal et al., 2006; Borodin et al., 2004; Gy¨orfi et al., 2006, 2008), and
recent state-of-the-art online learning algorithms (Li et al., 2011, 2012, 2013, 2015). Unlike other
application domains in machine learning where various open-source packages are available, very
few open-source toolkits exist for on-line portfolio selection, primarily due to the confidential
nature of financial industry. Consequently, it is difficult for researchers to evaluate new algorithms
for comprehensive comparisons with existing ones.

**1. INTRODUCTION** 

线上资产组合选择（*OLPS*)，是优化一组资产的财富分配和长期增长的解法问题，是一直以来量化金融和金融工程实践领域的核心。在探索这个问题的道路上，主要形成了两个学派: 其一，基于马科维茨和其所在金融界发展出的均值方差理论。其二，本质起源于信息论的资本增长理论。在资产管理行业中，众所周知的均值方差理论（*Mean-Variance Theory*）着重于单期（批量）投资组合选择，通过权衡投资组合的预期收益（即，均值）和风险（即，方差），在投资者的风险收益偏好下，构筑最优。另一方面，资本增长理论（*Capital Growth Theory*）侧重于多期或连续投资组合的选择，旨在最大化投资组合的预期增长率或预期对数收益。虽然这两种理论都解决了投资组合选择的任务，但是对于我们追求的迭代性的投资策略来说，后者更适用这种本质便是连续性决策问题的基本环境。

通过连续性选择资产池以实现特定风险-回报目标，线上资产组合成为了资产组合管理的自然和核心人物。为了解决这个问题，几大种类的算法
相继被提出。例如，最经典的“跟随赢家”策略，以资产理论为基石，旨在最大限度靠近大盘中的最优策略的收益增长率（log return）。第二种策略，
称为“跟随败者”，是一种将资产分配比重由大盘赢家转为败者的策略。这看起来或许有些反直觉，但其逻辑在于败者必将触底反弹，回归均值收益，在实际操作中往往能赢得极高收益。第三种策略，名为“规律套利”，旨在通过历史数据样本来驱动对市场的走势预测，并以此直接优化资产组合。以上三种策略纵有不同，他们的核心管理思路是相同的————资产组合单策略。有所谓“荟萃分析策略”，便是一种集合多种策略/资产类型为一体的。

此文章将在上述策略领域提供一个完整的线上资产组合选择算法回顾。


**I.1. SCOPE**

首先，我们需要将此Survey的“资产组合选择”与其他金融工程的研究主题分离。*ACM Survey*，旨在应用机器学习技巧进行金融
时间序列的预测，实现单类资产的交易。例如：增强学习，神经网络，基因算法，决策树和支持矢量机，提升和专家配重等。此类
金融工程中的过往论文与此篇survey的关键区别，在于它们的重心是预测未来价格走势以实现单类资产交易，而我们的目的是直接
在一套资产类别中寻求优化。

其次，此文章将重点强调资产组合的“线上”性——也就是，所有相关市场信息相继到来，而任何资产分配决策必须即刻做出。考虑到此，
我们的文章重点将在于探讨多期、连续的资产组合论文。在此问题下，目标被设定为最大化特定交易区间的log回报，
而资产组合需要特定交易区间的末期进行调仓。

最后，我们将重点探讨资产组合选择的算法面，并给读者一份对现有的资产组合选择策略领域架构性理解。

**OUTLINE**

*Section 2* 将正式赋予线上资产选择问题的数学定义，并探讨几个重要的实际问题。

*Section 3* 主要介绍产业内的重点算法
-3.1 基准算法
-3.2 跟随赢家
-3.3 跟随败者
-3.4 规律套利
-3.5 荟萃学习

*Section 4* 探讨现有算法与资产增长理论的核心交易理念

*Section 5* 谈论几个领域内的重点问题

*Section 6* 总结与未来方向展望

**2.1 Problem Setting**

Consider a financial market with m assets, we invest our wealth over all the assets in the market
for a sequence of n trading periods. The market price change is represented by a m-dimensional
price relative vector xt ∈ Rm+ , t = 1, . . . , n, where the ith element of tth price relative vector, xt,i,
denotes the ratio of tth closing price to last closing price for the ith assets. Thus, an investment
in asset i on period t increases by a factor of xt,i. We also denote the market price changes from
period t1 to t2 (t2 > t1) by a market window, which consists of a sequence of price relative vectors
xt2
t1 = {xt1 , . . . , xt2}, where t1 denotes the beginning period and t2 denotes the ending period. One
special market window starts from period 1 to n, that is, xn
1 = {x1, . . . , xn}.
At the beginning of the tth period, an investment is specified by a portfolio vector bt, t =
1, . . . , n. The ith element of tth portfolio, bt,i, represents the proportion of capital invested in the
ith asset. Typically, we assume a portfolio is self-financed and no margin/short is allowed. Thus, a
portfolio satisfies the constraint that each entry is non-negative and all entries sum up to one, that
is, bt ∈ m, where m =

b : b  0, b⊤1 = 1
	
. Here, 1 is the m-dimensional vector of all 1s,
and b⊤1 denotes the inner product of b and 1. The investment procedure from period 1 to n is
represented by a portfolio strategy, which is a sequence of mappings as follows:

b1 =
1
m
1, bt : R
m(t−1)
+ → m, t = 2, 3, . . . , n,
where bt = bt
􀀀
xt−1
1

denotes the portfolio computed from the past market window xt−1
1 . Let us
denote the portfolio strategy for n periods as bn
1 = {b1, . . . , bn}.
For the tth period, a portfoliomanager apportions its capital according to portfolio bt at the opening
time, and holds the portfolio until the closing time. Thus, the portfolio wealth will increase by a
factor of b⊤
t xt =
Pm
i=1 bt,ixt,i. Since this model uses price relatives and re-invests the capital, the
portfolio wealth will increase multiplicatively. From period 1 to n, a portfolio strategy bn
1 increases
the initial wealth S0 by a factor of
Qn
t=1 b⊤
t xt, that is, the final cumulative wealth after a sequence
of n periods is
Sn (bn
1 ) = S0
Yn
t=1
b⊤
t xt = S0
Yn
t=1
Xm
i=1
bt,ixt,i.
Since the model assumes multi-period investment, we define the exponential growth rate for a strategy
bn
1 as,
Wn (bn
1 ) =
1
n
log Sn (bn
1 ) =
1
n
Xn
t=1
log bt · xt.
Finally, let us combine all elements and formulate the online portfolio selection model. In a portfolio
selection task the decision maker is a portfolio manager, whose goal is to produce a portfolio
strategy bn
1 in order to achieve certain targets. Following the principle as the algorithms shown in
Table I, our target is to maximize the portfolio cumulative wealth Sn. The portfolio manager computes
the portfolio strategy in a sequential fashion. On the beginning of period t, based on previous
market window xt−1
1 , the portfolio manager learns a new portfolio vector bt for the coming price
relative vector xt, where the decision criterion varies among differentmanagers/strategies. The portfolio
bt is scored using the portfolio period return bt · xt. This procedure is repeated until period


