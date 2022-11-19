# higher-order-grass
Extension of the graph summarization algorithm put forward by LeFevre and Terzi in their work "GraSS: Graph Structure Summarization" to the higher order domain. The aim of this project is to develop an algorithmic solution node aggregation based for the hypergraph summarization problem. The code is written in Python programming language.

## Problem description
### Problem 1: k-Gs
Given an input graph $H(X,E)$ and integer $k$, find a summary graph $\pmb{S}$ for $H$ with at most $k$ supernodes $\pmb(X)$ $(|\boldsymbol{X}| \leq k)$, such that the $\mathit{Re}(H|\pmb{S})$ is minimized.

### Problem 2: k-CGs
Given an input graph $H(X,E)$ and integer $k$, find a summary graph $\pmb{S}$ for $H$ with supernodes $\pmb{X}$ such that $\mathit{Re(H|\pmb{S})}$ is minimized and for every $X' \in \pmb(X)$ $|X'| \geq k$.

## Contents:
- `higher_order_grass.py`: in this file we provide our implementation proposal for the algorithms proposed by LeFevre and Terzi applied in the context of higher order interactions
  - `k-Gs greedy`: baseline *Greedy* algorithm
- `main.py`: in this file we provide a sample program which executes our summarization algorithm in order to summarize a given hypergraph. The output summary is written in a file `output.txt`. The input hypergraph is read from `input.txt`. The file structure of `input.txt` is described in the following section "Input format"

## Input format
- The first line contains an integer `E` which indicates the number of hyperedges.
- For each of these hyperedges there is a couple of numbers `e_id` `e_card` separated by a white space. `e_id` is the hyperedge identifier; `e_card` is the number of nodes which populate the hyperedge `e_id`.
  - The following `e_card` rows reports an integer `node_id` which is the unique identifier of the node which belongs to relationship `e_id`
<br>
An example of input file is proposed in input.txt .
