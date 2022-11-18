import supernode
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
from itertools import combinations

class Summary:
    def __init__(self):
        """
        superList: dictionary{key:=supernode unique identifier ; value:=corresponding supernode object}
        autoincrementId: progressive identifier of the supernodes and hyperedges which populate the data structure. This counter is used to assign auto-increment unique integer identifiers. DO NOT use this attribute to count the number of supernodes which populate the data structure.
        components: dictionary{key:=id of the node of the original graph ; value:=supernode id where the node is in the summary}
        numComponents: number of components of the original graph represented by the summary
        """
        self.superList = {}
        self.autoincrementId = 0
        self.components = {}
        self.numComponents = 0
        self.summaryHypergraph = hnx.Hypergraph()

        #Remark:    supernodes and hyperepdges share the same autoincrementId because according to
        #           hypernetx specifications, it is not possible to have an hyperedge with the same
        #           id of a node

    def addComponent(self, key):
        """
        Add a new component to the summary.
        Consequently a new supernode is created to host the newcomer.
        """
        
        #add 1 to the number of components
        self.numComponents += 1

        #create a supernode with one component
        newSupernode = supernode.Supernode(self.autoincrementId)
        newSupernode.addComponent(key)
        self.superList[self.autoincrementId] = newSupernode

        #link components "key" to the corresponding supernode
        self.components[key] = self.autoincrementId

        #increment the number of supernodes
        self.autoincrementId += 1

    def getSupernode(self, key):
        """
        If supernode with key is in the summary then return
        the Supernode.
        """

        #use the get method to return the Supernode if it
        #exists otherwise it will return None
        return self.superList.get(key)

    def getComponentSupernode(self, componentId):
        """
        Find the supernode which containes the component with id componentId.
        If there it does not exist, return None.
        """
        if componentId in self.components:
            return self.superList.get(self.components[componentId])
        
        return None

    def getComponentSupernodeId(self, componentId):
        """
        Find the id of thesupernode which containes the component with id componentId.
        If there it does not exist, return None.
        """
        if componentId in self.components:
            return self.components[componentId]
        
        return None

    def getVertices(self):
        """
        Return all the supernodes in the summary
        """

        return self.superList.keys()

    def getComponents(self):
        """
        Return all the components represented by the summary
        """

        return self.components.keys()
    
    def insertHyperedge(self, elements):
        newHyperedge = hnx.Entity(self.autoincrementId, elements)
        self.autoincrementId += 1
        self.summaryHypergraph.add_edge(newHyperedge)

        #Update the neighbourhoods of each component of the new hyperedge
        possibleElementsCouples = list(combinations(elements, 2))
        for couple in possibleElementsCouples:
            c1 = couple[0]
            c2 = couple[1]
            
            #Get the corresponding supernodes
            s1 = self.getSupernode(c1)
            s2 = self.getSupernode(c2)

            s1.updateNeighbor(s2.getId(), 1)
            s2.updateNeighbor(s1.getId(), 1)

            s1.setIntersectionProfile(newHyperedge.uid, 1)
            s2.setIntersectionProfile(newHyperedge.uid, 1)
