import numpy as np
import random

class Graph:
    def __init__(self):
        self.nodes = []
        self.nodeRadii = []
        self.edges = []
        self.adjacency_matrix = []
        self.pages = []
        self.visits = []

    def addNode(self, node):
        self.nodes.append([node[0], node[1], 20])

        # Everytime this function is called, we should add a row and add a column to represent the extra node. 
        num_nodes = len(self.nodes)

        # Add a 0 to every row to represent the new node (adding a new column)
        for row in self.adjacency_matrix:
            row.append(0)
        
        # add a new row:
        newRow = [0] * num_nodes
        self.adjacency_matrix.append(newRow)

    def addEdge(self, node1, node2):
        print("Trying to add node", node1, 'and', node2)
        if node1 not in self.nodes or node2 not in self.nodes:
            print("one of the nodes aren't in self.nodes")
            return
        else:
            node1Index = self.nodes.index(node1)
            node2Index = self.nodes.index(node2)
            
            # Make sure no reflexivity
            if node1Index == node2Index:
                return
            
            self.adjacency_matrix[node1Index][node2Index] = 1

            self.edges.append([node1, node2])
    def removeNode(self, i):
        
        self.nodes.pop(i)
        self.adjacency_matrix.pop(i)

        for row in self.adjacency_matrix:
            row.pop(i)
        
    # TODO RemoveEdge Function

    def getTransitionMatrixForPageRank(self):
        numNodes = len(self.nodes)

        transitionMatrix = np.zeros((numNodes, numNodes))
        
        if numNodes == 0:
            return []
        
        adjacencyMatrix = np.array(self.adjacency_matrix)
        
        for i in range(numNodes):
            rowSum = np.sum(adjacencyMatrix[i])
            if rowSum == 0:
                # Apply Laplacian smoothing to that whole row so we don't run into divide by zero errors
                transitionMatrix[i] = np.array([1.0/numNodes] * numNodes)
            else:
                # Calculate transition probabilities
                transitionMatrix[i] = adjacencyMatrix[i]/rowSum

        
        return transitionMatrix
    
    def computePagerank(self):

        transition_matrix = self.getTransitionMatrixForPageRank()
        num_nodes = len(self.nodes)

        # give equal 
        pagerank = np.array([1.0 / num_nodes] * num_nodes)


        # Straight up calculation of PageRank using power iteration and pagerank formula
        for _ in range(100):
            new_pagerank = (1 - 0.85) / num_nodes + 0.85 * np.dot(transition_matrix.T, pagerank)

            pagerank = new_pagerank

        # Update the radius for each node based on the final PageRank values
        for i in range(num_nodes):
            self.nodes[i][2] = 20 + pagerank[i] * 100

    def takeRandomSurferStep(self, currentNode, dampingFactor = 0.85):
        numNodes = len(self.nodes)
        if numNodes == 0:
            return currentNode
        
        if random.random() <= dampingFactor:
            outLinks = []
            for i in range(numNodes):
                if self.adjacency_matrix[currentNode][i] == 1:
                    outLinks.append(i)
            
            if outLinks == []:
                nextNode = random.randint(0, numNodes - 1)
                # TODO Change color
            else:
                nextNode = random.choice(outLinks)
                # TODO Change Color
        else:
            nextNode = random.randint(0, numNodes - 1)
        
        return nextNode

