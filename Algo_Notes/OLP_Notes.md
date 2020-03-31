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
