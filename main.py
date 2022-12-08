import sys
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import pandas as pd
import numpy as np
import summary
from itertools import combinations
from higher_order_grass import kgs_greedy
from higher_order_grass import kgs_sample_pairs_constant
from higher_order_grass import kgs_sample_pairs_proportional
from higher_order_grass import kgs_linear_check
from higher_order_grass import kcgs_condense
from function import computeAverageReconstructionError

#Unfortunately it seems that hypernetx does not allow
#to compute in constant time the adjacency between two
#nodes in the hypergraph. In this work the adjacency
#between two nodes is the number of hyperedges shared
#between the two nodes. As a result we instantiate this
#additional structure "component_adj" which is a
#dictionary of dictionaries such that:
# component_adj[5][2] = adjacency degree between node
#                       5 and node 2
component_adj = dict()

######################################################
"""
Prepare LesMis dataset
"""
######################################################
#Retrive LesMis dataset
lm = hnx.LesMis()

volumes = lm.volumes
names = lm.df_names.set_index('Symbol')
scenes = lm.df_scenes

#generate a hypergraph studying the relationship between volumes. The edges are
#the volumes and the characters who appear in each volume are the nodes
### Construct the edges as a dictionary named by the name of the Volume
volume_edges = dict()
for v in range(1,6):
    volume_edges[v] = set(scenes.loc[scenes.Volume == v]['Characters'])
### Construct a hypergraph made up of volume_edges
myHypergraph = hnx.Hypergraph(volume_edges,name='Volumes')
for node in myHypergraph.nodes:
    myHypergraph.nodes[node].name = names.loc[node]['FullName']
    myHypergraph.nodes[node].description = names.loc[node]['Description']

#HV_collapsed = HV.collapse_nodes(return_equivalence_classes=True)

#bigNode = HV_collapsed[1]["JV:4"]
#print(bigNode)

#for node in HV.nodes():
    #print(node)

#print("---")

#for node in HV_collapsed[0].nodes():
#    print(node)
#    print(f"node uid {node} = {node.uid}")
#    print(HV_collapsed[1][node.uid])


##Initialize component_adj
for node in myHypergraph.nodes:
    component_adj[node] = dict()

for edge in myHypergraph.edges():
    edge_node_set = edge.elements.keys()
    possibleNodeCouples = combinations(edge_node_set, 2)
    for couple in possibleNodeCouples:
        if couple[1] in component_adj[couple[0]]:
            component_adj[couple[0]][couple[1]] += 1
        else:
            component_adj[couple[0]][couple[1]] = 1
        
        if couple[0] in component_adj[couple[1]]:
            component_adj[couple[1]][couple[0]] += 1
        else:
            component_adj[couple[1]][couple[0]] = 1

##...end initialize component_adj

######################################################
"""
Create initial summary such that each component of the original
hypergraph is a supernode
"""
######################################################
xpoints = np.array([])
ypoints = np.array([])
for i in range(0, 10):
    k=i+1
    xpoints = np.append(xpoints, k)
    mySummary = summary.Summary()

    #Add components
    for c in myHypergraph.nodes:
        mySummary.addComponent(c)

    #Add initial hyperedges
    for h in myHypergraph.edges():
        elements = []
        for n in h:
            supernodeId = mySummary.getComponentSupernodeId(n)        
            elements.append(supernodeId)
        
        mySummary.insertHyperedge(elements)

    #print(mySummary.summaryHypergraph)
    ######################################################

    kgs_greedy(component_adj, mySummary, k)
    #kgs_sample_pairs_constant(component_adj, mySummary, 3, 2)
    #kgs_sample_pairs_proportional(component_adj, mySummary, 3, 0.5)
    #kgs_linear_check(component_adj, mySummary, 3)
    #kcgs_condense(component_adj, mySummary, 3)

    avg_rec_err = computeAverageReconstructionError(component_adj, mySummary)
    print(avg_rec_err)
    ypoints = np.append(ypoints, avg_rec_err)

plt.plot(xpoints, ypoints)
plt.show()

######################################################
"""
Write the summary on output.txt
"""
######################################################
outputFile = open('output.txt','w')
outputFile.write("HYPEREDGES")
outputFile.write("\n")
for output_hyperedge in mySummary.summaryHypergraph.edges():
    outputFile.write(f"ID: {output_hyperedge.uid}")
    outputFile.write("\n")
    outputFile.write("Components: [ ")
    for output_node in output_hyperedge:
        outputFile.write(str(output_node))
        output_node_obj = mySummary.getSupernode(output_node)
        output_node_intersection_profile = output_node_obj.getIntersectionProfile(output_hyperedge.uid)
        outputFile.write(f"({output_node_intersection_profile})")
        outputFile.write(" ")
    outputFile.write("]\n")

outputFile.write("---")
outputFile.write("\n")
outputFile.write("SUPERNODES")
outputFile.write("\n")
for output_supernode in mySummary.getVertices():
    supernode_obj = mySummary.getSupernode(output_supernode)
    outputFile.write(str(supernode_obj))
    outputFile.write("\n")
######################################################