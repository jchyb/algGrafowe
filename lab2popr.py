from dimacs import *
from collections import deque

(V, L) = loadDirectedWeightedGraph("graphs-lab3/clique20")

def bfs(v,rGraph,wMat):
    d = deque()
    visited = [False for i in range(V)]
    parent = [-1 for i in range(V)]
    d.append(v)
    while len(d) != 0:
        el = d.popleft()
        visited[el] = True
        for i in range(len(rGraph[el])):
            if not visited[rGraph[el][i]] and wMat[(el,rGraph[el][i])][0] - wMat[(el,rGraph[el][i])][1] > 0:
                visited[rGraph[el][i]] = True
                d.append(rGraph[el][i])
                parent[rGraph[el][i]]= el
    return parent

def fordFulkenson(L, u, v):
    rGraph = [[] for i in range(V)]
    wMat = {}
    for l in L:
        rGraph[l[0] - 1].append(l[1] - 1)
        rGraph[l[1] - 1].append(l[0] - 1)

        wMat[(l[0] - 1, l[1] - 1)] = [l[2], 0]
        wMat[(l[1] - 1, l[0] - 1)] = [0, 0]


    fMax=0
    while True:
        parent = bfs(u,rGraph, wMat)

        if parent[v]==-1: break

        i = v
        par = parent[i]
        fDelta = wMat[(par,i)][0] - wMat[(par,i)][1]
        while (i != 0):
            par = parent[i]
            fDelta = min(fDelta, wMat[(par,i)][0] - wMat[(par,i)][1])
            i = par
        i = V-1
        while i != 0:
            par = parent[i]
            wMat[(par,i)][1] += fDelta
            wMat[(i,par)][1] -= fDelta
            i = par

        fMax += fDelta
    return fMax

minCut = 1e14
for i in range(len(L)):
    for j in range(len(L)):
        if i != j:
            minCut = min(minCut, fordFulkenson(L,0,V-1))
print(minCut)