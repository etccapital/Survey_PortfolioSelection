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

Portfolio selection, aiming to optimize the allocation of wealth across a set of assets, is a fundamental research problem in computational finance and a practical engineering task in financial
engineering. There are two major schools for investigating this problem, that is, the Mean Variance Theory [Markowitz 1952; Markowitz 1959; Markowitz et al. 2000] mainly from the finance
community and Capital Growth Theory [Kelly 1956; Hakansson and Ziemba 1995] primarily originated from information theory. The Mean Variance Theory, widely known in asset management
industry, focuses on a single-period (batch) portfolio selection to trade off a portfolio’s expected
return (mean) and risk (variance), which typically determines the optimal portfolios subject to the
investor’s risk-return profile. On the other hand, Capital Growth Theory focuses on multiple-period
or sequential portfolio selection, aiming to maximize the portfolio’s expected growth rate, or expected log return. While both theories solve the task of portfolio selection, the latter is fitted to the
“online” scenario, which naturally consists of multiple periods and is the focus of this article.

线上资产组合选择（*OLPS*)，是优化一组资产的财富分配和长期增长的解法问题，是一直以来量化金融和金融工程实践领域的核心。在探索这个问题的道路上，主要形成了两个学派: 其一，基于马科维茨和其所在金融界发展出的均值方差理论。其二，本质起源于信息论的资本增长理论。在资产管理行业中，众所周知的均值方差理论（*Mean-Variance Theory*）着重于单期（批量）投资组合选择，通过权衡投资组合的预期收益（即，均值）和风险（即，方差），在投资者的风险收益偏好下，构筑最优。另一方面，资本增长理论（*Capital Growth Theory*）侧重于多期或连续投资组合的选择，旨在最大化投资组合的预期增长率或预期对数收益。虽然这两种理论都解决了投资组合选择的任务，但是对于我们追求的迭代性的投资策略来说，后者更适用这种本质便是连续性决策问题的基本环境。

Online portfolio selection, which sequentially selects a portfolio over a set of assets in order to
achieve certain targets, is a natural and important task for asset portfolio management. Aiming to
maximize the cumulative wealth, several categories of algorithms have been proposed to solve this
task. One category of algorithms, termed “Follow-the-Winner”, tries to asymptotically achieve the
same growth rate (expected log return) as that of an optimal strategy, which is often based on the
Capital Growth Theory. The second category, named “Follow-the-Loser”, transfers the wealth from
winning assets to losers, which seems contradictory to the common sense but empirically often
achieves significantly better performance. Finally, the third category, termed “Pattern-Matching”
based approach, tries to predict the next market distribution based on a sample of historical data and
explicitly optimizes the portfolio based on the sampled distribution. While the above three categories
are focused on a single strategy (class), there are also some other strategies that focus on combining
multiple strategies (classes), termed as “Meta-Learning Algorithms”. As a brief summary, Table I
outlines the list of main algorithms and corresponding references.

通过连续性选择资产池以实现特定风险-回报目标，线上资产组合成为了资产组合管理的自然和核心人物。为了解决这个问题，几大种类的算法
相继被提出。例如，最经典的“跟随赢家”策略，以资产理论为基石，旨在最大限度靠近大盘中的最优策略的收益增长率（log return）。第二种策略，
称为“跟随败者”，是一种将资产分配比重由大盘赢家转为败者的策略。这看起来或许有些反直觉，但其逻辑在于败者必将触底反弹，回归均值收益，在实际操作中往往能赢得极高收益。第三种策略，名为“规律套利”，旨在通过历史数据样本来驱动对市场的走势预测，并以此直接优化资产组合。

以上三种策略纵有不同，他们的核心管理思路是相同的————资产组合单策略。有所谓“荟萃分析策略”，便是一种集合多种策略/资产类型为一体的。

This article provides a comprehensive survey of online portfolio selection algorithms belonging
to the above categories. To the best of our knowledge, this is the first survey that includes the above
three categories and the meta-learning algorithms as well. Moreover, we are the first to explicitly
discuss the connection between the online portfolio selection algorithms and Capital Growth Theory, and illustrate their underlying trading ideas. In the following sections, we also clarify the scope
of this article and discuss some related existing surveys in the literature.

此文章将在上述策略领域提供一个完整的线上资产组合选择算法回顾。


**I.1. SCOPE**

In this survey, we focus on discussing the empirical motivating ideas of the online portfolio
selection algorithms, while only skimming theoretical aspects (such as competitive
analysis by El-Yaniv [1998] and Borodin et al. [2000] and asymptotical convergence analysis
by Gy¨orfi et al. [2012]). Moreover, various other related issues and topics are excluded from this
survey, as discussed below.

First of all, it is important to mention that the “Portfolio Selection” task in our
survey differs from a great body of financial engineering studies [Kimoto et al. 1993;
ACM Computing Surveys, Vol. V, No. N, Article A, Publication date: December YEAR.
Online Portfolio Selection: A Survey A:3
Merhav and Feder 1998; Cao and Tay 2003; Lu et al. 2009; Dhar 2011; Huang et al. 2011], which
attempted to forecast financial time series by applying machine learning techniques and
conduct single stock trading [Katz and McCormick 2000; Koolen and Vovk 2012], such as reinforcement
learning [Moody et al. 1998; Moody and Saffell 2001; O et al. 2002], neural networks
[Kimoto et al. 1993; Dempster et al. 2001], genetic algorithms [Mahfoud and Mani 1996;
Allen and Karjalainen 1999; Madziuk and Jaruszewicz 2011], decision trees [Tsang et al. 2004],
and support vector machines [Tay and Cao 2002; Cao and Tay 2003; Lu et al. 2009], boosting
and expert weighting [Creamer 2007; Creamer and Freund 2007; Creamer and Freund 2010;
Creamer 2012], etc. The key difference between these existing works and subject area of this survey
is that their learning goal is to make explicit predictions of future prices/trends and to trade on
a single asset [Borodin et al. 2000, Section 6], while our goal is to directly optimize the allocation
among a set of assets.

首先，我们需要将此Survey的“资产组合选择”与其他金融工程的研究主题分离。*ACM Survey*，旨在应用机器学习技巧进行金融
时间序列的预测，实现单类资产的交易。例如：增强学习，神经网络，基因算法，决策树和支持矢量机，提升和专家配重等。此类
金融工程中的过往论文与此篇survey的关键区别，在于它们的重心是预测未来价格走势以实现单类资产交易，而我们的目的是直接
在一套资产类别中寻求优化。

Second, this survey emphasizes the importance of “online” decision for portfolio selection,
meaning that related market information arrives sequentially and the allocation
decision must be made immediately. Due to the sequential (online) nature of this task,
we mainly focus on the survey of multi-period/sequential portfolio selection work, in
which the portfolio is rebalanced to a specified allocation at the end of each trading period
[Cover 1991], and the goal typically is to maximize the expected log return over a sequence
of trading periods. We note that these work can be connected to the Capital Growth Theory
[Kelly 1956], stemmed from the seminal paper of Kelly [1956] and further developed
by Breiman[1960; 1961], Hakansson[1970; 1971], Thorp[1969; 1971], Bell and Cover [1980],
Finkelstein and Whitley [1981], Algoet and Cover [1988], Barron and Cover [1988],
MacLean et al. [1992], MacLean and Ziemba [1999], Ziemba and Ziemba [2007],
Maclean et al. [2010], etc. It has been successfully applied to gambling [Thorp 1962;
Thorp 1969; Thorp 1997], sports betting [Hausch et al. 1981; Ziemba and Hausch 1984;
Thorp 1997; Ziemba and Hausch 2008], and portfolio investment [Thorp and Kassouf 1967;
Rotando and Thorp 1992; Ziemba 2005]. We thus exclude the studies related to the Mean Variance
portfolio theory [Markowitz 1952; Markowitz 1959], which were typically developed for singleperiod
(batch) portfolio selection (except some extensions [Li and Ng 2000; Dai et al. 2010]).

Finally, this article focuses on surveying the algorithmic aspects and providing a structural understanding
of the existing online portfolio selection strategies. To prevent loss of focus, we will
not dig into theoretical details. In the literature, there is a large body of related work for the theory
[MacLean et al. 2011]. Interested researchers can explore the details of the theory from two exhaustive
surveys [Thorp 1997; Maclean and Ziemba 2008], and its history from Poundstone [2005]
and Gy¨orfi et al. [2012, Chapter 1]

