from dimacs import *
from collections import deque

(V, L) = loadDirectedWeightedGraph("graphs-lab2/flow/worstcase")
rGraph = [[] for i in range(V)]
wMat = [[[0, 0] for i in range(V)] for j in range(V)]
for l in L:
    rGraph[l[0]-1].append(l[1]-1)
    rGraph[l[1]-1].append(l[0]-1)
    wMat[l[0]-1][l[1]-1][0] = l[2]

def bfs(v):
    print("bfs")
    d = deque()
    visited = [False for i in range(V)]
    parent = [-1 for i in range(V)]
    d.append(v)
    while len(d) != 0:
        el = d.popleft()
        print(el)
        visited[el] = True
        for i in range(len(rGraph[el])):
            print("   ", rGraph[el][i])
            if not visited[rGraph[el][i]] and wMat[el][rGraph[el][i]][0] - wMat[el][rGraph[el][i]][1] > 0:
                print("      ", rGraph[el][i])
                visited[rGraph[el][i]] = True
                d.append(rGraph[el][i])
                parent[rGraph[el][i] ]= el
    return parent

def fordFulkenson():
    fMax=0
    while True:
        parent = bfs(0)
        print("parent")
        for i in parent:
            print("            ", i)

        if (parent[V - 1]==-1): break

        i = V - 1
        par = parent[i]
        print (wMat[par][i][0])
        fDelta = wMat[par][i][0] - wMat[par][i][1]
        while (i != 0):
            par = parent[i]
            fDelta = min(fDelta, wMat[par][i][0] - wMat[par][i][1])
            print("fdel", fDelta, " ",wMat[par][i][0]," ",wMat[par][i][1])
            i = par
        i = V-1
        while (i != 0):
            par = parent[i]
            wMat[par][i][1] += fDelta
            #TODO
            wMat[i][par][1] -= fDelta
            i = par
        print("fmax")
        fMax += fDelta
        print(fMax)
    return fMax

print(fordFulkenson())