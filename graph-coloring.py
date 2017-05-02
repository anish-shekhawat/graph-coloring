import networkx as nx
import matplotlib.pyplot as plt

class Node:
    color= None
    key= None

    def __init__(self, k):
        self.key = k
    def __str__(self):
        return "(key=" + str(self.key) + ", color=" + str(self.color) + ")\n"
    def __repr__(self):
        return self.__str__()

class Graph:
    edges= set()
    nodes= []
    nodesFromKeys = {}
    graph= {}
    G = nx.Graph()

    colors = set(range(1, 40))
    _dbg = False

    def __init__(self):
        pass

    def addNode(self, node):
        self.nodes.append(node)
        self.nodesFromKeys[node.key] = node
        self.graph[node.key] = set()

    def addUndirectedEdge(self, N1, N2):
        try:
            self.graph[N1.key].add(N2)
        except:
            self.graph[N1.key] = set([N2])
        try:
            self.graph[N2.key].add(N1)
        except:
            self.graph[N2.key] = set([N1])

    def __str__(self):
        return str(self.graph)

    def buidGraph(self):
        with open("input.col", "r") as infile:
            for line in infile.readlines():
                if line.startswith("e"):
                    li = line.split()
                    self.addUndirectedEdge(self.nodesFromKeys[int(li[1])], self.nodesFromKeys[int(li[2])])
                    self.G.add_edge(li[1], li[2])
                elif line.startswith("p") and "edge" in line:
                    n = int(line.split()[2])
                    for i in range(1, n+1):
                        N = Node(i)
                        self.addNode(N)

    def color(self):
        self.nodes = sorted(self.nodes, key=self.getdegree)

        while len(self.nodes) != 0:

            node = self.nodes.pop()
            color = self.findSmallestNotInNeighboors(node)
            node.color = color
        return self.nodesFromKeys.values()

    def findSmallestNotInNeighboors(self, node):
        c = set(self.colors)
        for n in self.graph[node.key]:
            if n.color is not None:
                try:
                    c.remove(n.color)
                except KeyError:
                    pass # The color has already been taken out ? Just don't care
        if self._dbg:
            print c, len(c)
        if 0 == len(c):
            return None
        return c.pop()

    def getdegree(self, node):
        key = node.key
        return len(self.graph[key])


if __name__ == '__main__':
    register_graph = Graph()
    register_graph.buidGraph()
    #print str(G)
    print register_graph.color()
    colors = [register_graph.nodesFromKeys.get(int(node)).color for node in register_graph.G.nodes()]
    print colors
    nx.draw(register_graph.G, cmap=plt.get_cmap('jet'), node_color=colors)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display
