'''
Useful functions
'''

from itertools import combinations

def computeAverageReconstructionError(component_adj, mySummary):
    reconstructionError = 0

    summarySupernodes = mySummary.getVertices()
    numberOfComponents = len(mySummary.getComponents())
    
    for supernodeId in summarySupernodes:
        ##Compute internal reconstruction error##
        supernode = mySummary.getSupernode(supernodeId)

        #Internal adjacency of the supernode
        internal_adj = (2*supernode.getInternalEdges())/(supernode.cardinality*(supernode.cardinality-1))

        #For each possible couple of supernode components, we update the reconstruction error
        #with respect to the ground truth
        possibleSupernodeComponentCouple = list(combinations(supernode.getComponents(), 2))

        for supernode_couple in possibleSupernodeComponentCouple:
            c1 = supernode_couple[0]
            c2 = supernode_couple[1]
            trueAdjacency = component_adj[c1].get(c2, 0)
            reconstructionError += abs((trueAdjacency)-(internal_adj))
        ##...end internal reconstruction error

        ##Compute external reconstruction error##

        #For each neighbour of supernode update the reconstruction error
        for n in supernode.getConnections():
            
            supernodeN = mySummary.getSupernode(n)

            #External adjacency between nodes in S3 and nodes in its neighbour n
            external_adj = supernode.getWeight(n)/(supernode.cardinality*supernodeN.cardinality)

            #For each possible couple between supernode components and n components, we update the reconstruction error
            #with respect to the ground truth
            for c1 in supernodeN.getComponents():
                for c2 in supernode.getComponents():
                    trueAdjacency = component_adj[c1].get(c2, 0)
                    reconstructionError += abs((trueAdjacency)-(external_adj))    

        ##...end compute external reconstruction error


    return reconstructionError/(numberOfComponents**2)