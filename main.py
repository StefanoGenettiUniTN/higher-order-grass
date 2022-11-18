import sys
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx

######################################################
"""
Read the hypergraph from input.txt
"""
######################################################
inputFile = open('input.txt','r')

#Read number of hyperedges
card_x = int(inputFile.readline())

#Read hyperedges
input_hypergraph = dict()
for i in range(card_x):
    input_hyperedge = [int(x) for x in inputFile.readline().split()]
    input_hyperedge_id = input_hyperedge[0]
    input_hyperedge_card = input_hyperedge[1]

    input_hypergraph[input_hyperedge_id] = ()

    for j in range(input_hyperedge_card):
        input_node = int(inputFile.readline())
        input_hypergraph[input_hyperedge_id] += (input_node,)

myHypergraph = hnx.Hypergraph(input_hypergraph)

print(myHypergraph)

