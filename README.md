# Survey_PortfolioSelection

Online portfolio selection is a fundamental problem in computational ﬁnance, which has been extensively studied across several research communities, including ﬁnance, statistics, artiﬁcial intelligence, machine learning, and data mining, etc. This article aims to provide a comprehensive survey and a structural understanding of published online portfolio selection techniques.

**OUTLINE**

*Section 1* 线上资产选择问题，及其领域纵览。

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

**Section I. Overview**

     线上资产组合选择（OLPS)，是优化一组资产的财富分配和长期增长的解法问题，是一直以来量化金融和金融工程实践领域的核心。在探索这个问题的道路上，主要形成了两个学派: 其一，基于马科维茨和其所在金融界发展出的均值方差理论。其二，本质起源于信息论的资本增长理论。在资产管理行业中，众所周知的均值方差理论（Mean-Variance Theory）着重于单期（批量）投资组合选择，通过权衡投资组合的预期收益（即，均值）和风险（即，方差），在投资者的风险收益偏好下，构筑最优。另一方面，资本增长理论（Capital Growth Theory）侧重于多期或连续投资组合的选择，旨在最大化投资组合的预期增长率或预期对数收益。虽然这两种理论都解决了投资组合选择的任务，但是对于我们追求的迭代性的投资策略来说，后者更适用这种本质便是连续性决策问题的基本环境。

*This is derivative work from literature review of a paper, intending to serve as main alpha for the research project developed under ETC Investment Group, Academy Division. The underlying logic and technique follows through with the abstract:*

From an online machine learning perspective, we ﬁrst formulate online portfolio selection as a sequential decision problem, and then survey a variety of state-of-the-art approaches, which are grouped into several major categories, including benchmarks, “Follow-the-Winner” approaches, “Follow-the-Loser” approaches, “Pattern-Matching” based approaches, and “Meta-Learning Algorithms”. In addition to the problem formulation and related algorithms, we also discuss the relationship of these algorithms with the Capital Growth theory in order to better understand the similarities and differences of their underlying trading ideas. This article aims to provide a timely and comprehensive survey for both machine learning and data mining researchers in academia and quantitative portfolio managers in the ﬁnancial industry to help them understand the state-of-the-art and facilitate their research and practical applications. We also discuss some open issues and evaluate some emerging new trends for future research directions.

In recent years, machine learning has been applied to various applications in finance (Gy¨orfi et al., 2012), including On-line Portfolio Selection, which aims to sequentially allocate capital among a set of assets, such that the investment return can be maximized in the long run (Kelly, 1956). It has attracted increasing attention from both academia and industry, and several machine learning algorithms have been proposed (Li and Hoi, 2014), including traditional algorithms (Cover, 1991; Helmbold et al., 1998; Agarwal et al., 2006; Borodin et al., 2004; Gy¨orfi et al., 2006, 2008), and recent state-of-the-art online learning algorithms (Li et al., 2011, 2012, 2013, 2015). Unlike other application domains in machine learning where various open-source packages are available, very few open-source toolkits exist for on-line portfolio selection, primarily due to the confidential nature of financial industry. Consequently, it is difficult for researchers to evaluate new algorithms for comprehensive comparisons with existing ones.
