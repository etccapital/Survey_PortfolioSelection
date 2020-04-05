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

线上资产组合选择（*OLPS*)，是优化一组资产的财富分配和长期增长的解法问题，是一直以来量化金融和金融工程实践领域的核心。在探索这个问题的道路上，主要形成了两个学派: 其一，基于马科维茨和其所在金融界发展出的均值方差理论。其二，本质起源于信息论的资本增长理论。

在资产管理行业中，众所周知的均值方差理论（*Mean-Variance Theory*）着重于单期（批量）投资组合选择，通过权衡投资组合的预期收益（即，均值）和风险（即，方差），在投资者的风险收益偏好下，构筑最优。另一方面，资本增长理论（*Capital Growth Theory*）侧重于多期或连续投资组合的选择，旨在最大化投资组合的预期增长率或预期对数收益。

虽然这两种理论都解决了投资组合选择的任务，但是对于我们追求的迭代性的投资策略来说，后者更适用这种本质便是连续性决策问题的基本环境。

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

This article provides a comprehensive survey of online portfolio selection algorithms belonging
to the above categories. To the best of our knowledge, this is the first survey that includes the above
three categories and the meta-learning algorithms as well. Moreover, we are the first to explicitly
discuss the connection between the online portfolio selection algorithms and Capital Growth Theory, and illustrate their underlying trading ideas. In the following sections, we also clarify the scope
of this article and discuss some related existing surveys in the literature.

