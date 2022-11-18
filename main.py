import sys
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import summary

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

######################################################
"""
Create initial summary such that each component of the original
hypergraph is a supernode
"""
######################################################
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

print(mySummary.summaryHypergraph)
######################################################
supernode_c14 = mySummary.getComponentSupernodeId(14)
print("supernode_c14 = "+str(supernode_c14))
supernode_c15 = mySummary.getComponentSupernodeId(15)
print("supernode_c15 = "+str(supernode_c15))

s1 = mySummary.merge(supernode_c14, supernode_c15)
print("s1 = "+str(s1))

print(" ")
print("fine merge 1")
print(" ")

supernode_c16 = mySummary.getComponentSupernodeId(16)
print("supernode_c16 = "+str(supernode_c16))

s2 = mySummary.merge(s1, supernode_c16)
print("s2 = "+str(s2))

print(" ")
print("fine merge 2")
print(" ")
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