from collections import deque

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
def isPEO(V):
    RN = [None] * (len(V) + 1)
    parent = [None] * (len(V) + 1)
    for i, v in enumerate(V, 1):
        RN[v] = set()
        for j in range(0, i-1):
            #print(v,V[j])
            if G[V[j]].out & {v}:
                RN[v] |= {V[j]}
                parent[v] = V[j]
                #print("r",RN[v])
    for v in V:
        if(parent[v] != None and not RN[v] - {parent[v]} <= RN[parent[v]]):
            #print(v," ",RN[v]," ",parent[v])
            return False
    return True


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
class CliqueTreeNode:
    def __init__(self, cliqueSet):
        self.n = []
        self.clique = cliqueSet


def preOrder(v, T, C, RN, parent, createdSets):

    if RN[v] == C[parent[v]]:
        C[parent[v]].clique |= {v}
        C[v] = C[parent[v]]
    else:
        C[v] = CliqueTreeNode(RN[v] | {v})
        C[v].n.append(C[parent[v]])
        C[parent[v]].n.append(C[v])
        createdSets.append(C[v])
    #print(v," ",T[v].children," ", parent[v]," ", RN[v])
    for i in T[v].children:
        preOrder(i, T, C, RN, parent, createdSets)

def makeTree(G, PEO):
    RN = [None] * (len(PEO) + 1)
    parent = [None] * (len(PEO) + 1)
    for i, v in enumerate(PEO, 1):
        RN[v]=set()
        for j in range(0, i-1):
            if G[PEO[j]].out & {v}:
                RN[v] |= {PEO[j]}
                parent[v] = PEO[j]

    T = [TreeNode() for i in range(len(PEO)+1)]
    for v in PEO:
        if parent[v]:
            T[parent[v]].addChild(v)

    C = [None] * (len(PEO)+1)

    v = PEO[0]
    C[v] = CliqueTreeNode({v})
    createdCliques = []

    for i in T[v].children:
        preOrder(i, T, C, RN, parent, createdCliques)

    for q in createdCliques:
        print(q.clique)
    cliqueValue = {}
    for i, q in enumerate(createdCliques):
        cliqueValue[q]=i

    pivots = deque()
    cliqueChain = [set(createdCliques)]
    while(len(cliqueChain)<len(createdCliques)):
        for i, c in enumerate(cliqueChain):
            Xc = c
            if(len(Xc)!=1): break
        if len(pivots) == 0:
            Vl = None
            qMax = -1
            for q in Xc:
                if(qMax<cliqueValue[q]):
                    Vl = q
                    qMax = cliqueValue[q]

            Xc -= {Vl}
            cliqueChain.insert(i+1,{Vl})
            V = {Vl}
            pass
        else:
            x = pivots.pop()
            print("x",x)
            V = set()
            for q in createdCliques:
                if({x} & q.clique): V |= {q}
            Xa = None
            Xai = 0
            Xb = None
            Xbi = 0
            for j, q in enumerate(cliqueChain):
                if(V & q):
                    if(Xa == None):
                        Xa, Xai = q, j
                    Xb, Xbi = q, j
            cliqueChain.insert(Xai+1,Xa & V)
            Xa -= V
            print("Xa", Xa)
            cliqueChain.insert(Xbi+1,Xb & V)
            Xb -= V
            if len(Xb)==0:
                cliqueChain.pop(Xbi+2)
            if len(Xa)==0:
                cliqueChain.pop(Xai)

            print("Xb",Xb)
            pass
        print(cliqueChain)
        print("pivots", pivots)
        for v in V:
            for u in v.n:
                if u not in V:
                    pivots.extend(v.clique & u.clique)
                    print("v.n", v.n, "u.n", u.n)
                    u.n.remove(v)
                    v.n.remove(u)
                    print("v.n", v.n, "u.n", u.n)

    for v in PEO:
        state = 0
        for q in cliqueChain:
            print(q)
            if next(iter(q)).clique & {v}:
                if state == 0: state = 1
                if state == 2: return False
            else:
                if state == 1: state = 2

    return True
    #for c in createdCliques:
      #  print(c)


(V, L) = loadWeightedGraph("graphs-lab4/chordal/example-fig5")

G = [Node() for i in range(V + 1)]
for l in L:
    G[l[0]].addNode(l[1])
    G[l[1]].addNode(l[0])

path = lexBFS(G, V)
print(path)
print(checkLexBFS(G, path))
#print(isPEO(path))
makeTree(G, path)
