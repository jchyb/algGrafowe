from dimacs import *
from queue import PriorityQueue

(V, L) = loadWeightedGraph("graphs-lab3/path")


class Node:
    def __init__(self):
        self.edges = {}  # słownik par mapujący wierzchołki do których są krawędzie na ich wagi
        self.active = True

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight  # dodaj krawędź do zadanego wierzchołka
        # o zadanej wadze; a jeśli taka krawędź
        # istnieje, to dodaj do niej wagę

    def delEdge(self, to):
        del self.edges[to]  # usuń krawędź do zadanego wierzchołka


def display(G):
    for i in range(1, len(G)):
        if G[i].active:
            print(i)
            for j in G[i].edges:
                print("  ", j, " ", G[i].edges[j])

def mergeVertices(G, x, y):
    for i in G[y].edges:
        if i != x:
            #print(i,",",x)
            G[x].addEdge(i, G[y].edges[i])
            G[i].addEdge(x, G[y].edges[i])
    sum = 0
    for i in G[y].edges:
        sum += G[y].edges[i]
        #print(i," ",y)
        G[i].delEdge(y)
    G[y].active = False
    #print("  lol ")
    return G, sum

def minimumCutPhase(G, length):
    v=0
    for i in range(1, len(G)+1):
        if G[i].active:
            v = i
            break
    S = {}
    addedList = []
    I = [False for i in range(0,len(G)+1)]
    Q=PriorityQueue()
    Q.put((0, v))

    while length != 0:
        x = Q.get()[1]
        #print(x)
        if not I[x]:
            length -= 1
            addedList.append(x)
            I[x] = True
            for y in G[x].edges:
                S[y] = S.get(y, 0) + G[x].edges[y]
                if not I[y]:
                    Q.put((-S[y], y))

    return addedList[-2], addedList[-1]

def stoerWagner(G,length):
    minCut = 1e20
    while length!=1:
        #print("   ",length)
        a, b = minimumCutPhase(G, length)
        length -= 1
        G, sum = mergeVertices(G, a, b)
        minCut = min(minCut,sum)

    return minCut


G = [Node() for i in range(V+1)]

for (x, y, c) in L:
    G[x].addEdge(y, c)
    G[y].addEdge(x, c)

print(stoerWagner(G,V))