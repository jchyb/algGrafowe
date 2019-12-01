from dimacs import *
from collections import deque

(V, L) = loadDirectedWeightedGraph("graphs-lab2/flow/grid5x5")

def bfs(v,V,rGraph,wMat):
    d = deque()
    visited = [False for i in range(V)]
    parent = [-1 for i in range(V)]
    d.append(v)
    while len(d) != 0:
        el = d.popleft()
        visited[el] = True
        #print(" ",el)
        for i in range(len(rGraph[el])):
            #print("  ",rGraph[el][i])
            if not visited[rGraph[el][i]] and wMat[(el,rGraph[el][i])][0] - wMat[(el,rGraph[el][i])][1] > 0:
                #print("   ", rGraph[el][i])
                visited[rGraph[el][i]] = True
                d.append(rGraph[el][i])
                parent[rGraph[el][i]]= el
    return parent

def fordFulkenson(L,V, u, v):
    rGraph = [[] for i in range(V)]
    wMat = {}
    for l in L:
        rGraph[l[0] - 1].append(l[1] - 1)
        rGraph[l[1] - 1].append(l[0] - 1)
        wMat[(l[0] - 1, l[1] - 1)] = [l[2], 0]
        wMat[(l[1] - 1, l[0] - 1)] = [0, 0]

    fMax=0
    while True:
        parent = bfs(u, V, rGraph, wMat)

        #for p in parent:
         #   print(p)
        if parent[v]==-1: break

        i = v
        par = parent[i]
        fDelta = wMat[(par,i)][0] - wMat[(par,i)][1]
        #print("fdel",fDelta)
        while (i != u):
            par = parent[i]
            fDelta = min(fDelta, wMat[(par,i)][0] - wMat[(par,i)][1])
            i = par
        i = v
        while i != u:
            par = parent[i]
            wMat[(par,i)][1] += fDelta
            wMat[(i,par)][1] -= fDelta
            i = par

        fMax += fDelta
    return fMax

print(fordFulkenson(L,V,0,V-1))

'''
minCut = 1e14
for i in range(1,V):
    minCut = min(minCut, fordFulkenson(L,V,0,i))
    print(minCut)
print(minCut)
'''