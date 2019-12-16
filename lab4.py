from dimacs import *


class Node:
    def __init__(self):
        self.out = set()

    def addNode(self, to):
        self.out.add(to)


def lexBFS(G, V):
    sets = [{}]
    sets[0] = set(range(1, V + 1))
    path = []
    while sets:
        v = sets[-1].pop()
        # print(v," ",sets)
        path.append(v)
        newsets = []
        for s in sets:
            s1 = set()
            s2 = set()
            for i in s:
                if G[i].out & {v}:
                    s1 |= {i}
                else:
                    s2 |= {i}
            if s2:
                newsets.append(s2)
            if s1:
                newsets.append(s1)
        # print(newsets)
        sets = newsets
    return path


def checkLexBFS(G, vs):
    n = len(G)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n - 1):
        for j in range(i + 1, n - 1):
            Ni = G[vs[i]].out
            Nj = G[vs[j]].out

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True


class TreeNode:
    def __init__(self):
        self.children = []

    def addChild(self, child):
        self.children.append(child)


def preOrder(v, T, C, RN, parent):
    if RN[v] == C[parent[v]]:
        C[parent[v]] |= {v}
        C[v] = C[parent[v]]
    else:
        C[v] = set(RN[v])
        C[v] |= {v}
    print(v," ",T[v].children)
    for i in T[v].children:
        preOrder(i, T, C, RN, parent)


def makeTree(G, PEO):
    RN = [set()] * (len(PEO) + 1)
    parent = [None] * (len(PEO) + 1)
    for i, v in enumerate(PEO, 1):
        for j in range(1, i):
            if G[PEO[j]].out & {v}:
                print(v," ",PEO[j])
                RN[v] |= {PEO[j]}
                parent[v] = PEO[j]

    T = [TreeNode() for i in  range(len(PEO)+1)]
    for v in PEO:
        if parent[v]:
            #print(parent[v]," ",v)
            T[parent[v]].addChild(v)

    C = [None] * (len(PEO)+1)

    v = PEO[0]
    C[v] = {v}


    for i in T[v].children:
        print("ok")
        preOrder(i, T, C, RN, parent)

    for s in C:
        print(s)


(V, L) = loadWeightedGraph("graphs-lab4/interval/example-fig5")

G = [Node() for i in range(V + 1)]
for l in L:
    G[l[0]].addNode(l[1])
    G[l[1]].addNode(l[0])

path = lexBFS(G, V)
print(path)
print(checkLexBFS(G, path))
makeTree(G, path)
