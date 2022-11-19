# higher-order-grass
Extension of the graph summarization algorithm put forward by LeFevre and Terzi in their work "GraSS: Graph Structure Summarization" to the higher order domain. The aim of this project is to develop an algorithmic solution node aggregation based for the hypergraph summarization problem. The code is written in Python programming language.

##Problem description
### Problem 1: k-Gs
Given an input graph $H(X,E)$ and integer $k$, find a summary graph $\pmb{S}$ for $H$ with at most $k$ supernodes $\pmb(X)$ $(|\boldsymbol{X}| \leq k)$, such that the $\mathit{Re}(H|\pmb{S})$ is minimized.

### Problem 2: k-CGs
Given an input graph $H(X,E)$ and integer $k$, find a summary graph $\pmb{S}$ for $H$ with supernodes $\pmb{X}$ such that $\mathit{Re(H|\pmb{S})}$ is minimized and for every $X' \in \pmb(X)$ $|X'| \geq k$.

## Contents:
- `higher_order_grass.py`: in this file we provide our implementation proposal for the algorithms proposed by LeFevre and Terzi applied in the context of higher order interactions
  - `k-Gs greedy`: baseline *Greedy* algorithm
