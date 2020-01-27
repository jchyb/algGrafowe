import dimacs
class Node:
    def __init__(self):
        self.edges = []
        self.active = True

    def addEdge(self, to):
        self.edges.append(to)


class treeNode:
    def __init__(self, node):
        self.node = node
        self.children = []
    def addChild(self,node):
        newNode = treeNode(node)
        self.children.append(newNode)
        return newNode
    def childrenAmount(self):
        return len(self.children)



def DFS(G, v, visited, low, dfsnum, num, node, allNodes, parent):
    num[0] = num[0] + 1
    visited[v] = True
    dfsnum[v] = num[0]
    low[v] = dfsnum[v]
    for i in G[v].edges:
        if not visited[i]:
            nextNode = node.addChild(i)
            allNodes[i] = nextNode
            DFS(G, i, visited, low, dfsnum, num, nextNode, allNodes, v)
            low[v] = min(low[v], low[i])
        elif parent != i:
            low[v] = min(low[v], dfsnum[i])
    return num

def aCheck(G):
    dfsnum = [None]*(len(G)+1)
    visited = [False for i in range(len(G)+1)]
    low = [None]*(len(G)+1)
    allNodes = [None] * (len(G)+1)
    allNodes[1] = treeNode(1)
    aPoints = set()
    bridges = set()

    DFS(G, 1, visited, low, dfsnum, [0],allNodes[1],allNodes,-1)

    if(len(allNodes[1].children) > 1):
        aPoints |= {1}

    for u in allNodes[1].children:
        if low[u.node] > dfsnum[1]:
            bridges |= {(u.node, 1)}

    for v in range(2,len(G)):
        children = allNodes[v].children
        for u in children:
            if low[u.node] >= dfsnum[v]:
                aPoints |= {v}
            if low[u.node] > dfsnum[v]:
                bridges |= {(u.node, v)}
                print(1)

    return aPoints, bridges

(V, L) = dimacs.loadWeightedGraph("graphs-lab6/articulation/example2")

G = [Node() for i in range(V+1)]

for (a, b, c) in L:
    G[a].addEdge(b)
    G[b].addEdge(a)
print(aCheck(G))
