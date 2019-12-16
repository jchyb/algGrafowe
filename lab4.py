from dimacs import *

class Node:
    def __init__(self):
        self.out = set()

    def addNode(self, to):
        self.out.add(to)

def lexBFS(G, V):
    sets = [{}]
    sets[0] = set(range(1, V+1))
    path = []
    while sets:
        v = sets[-1].pop()
        #print(v," ",sets)
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
        #print(newsets)
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

(V, L) = loadWeightedGraph("graphs-lab4/chordal/house")

G = [Node() for i in range(V+1)]
for l in L:
    G[l[0]].addNode(l[1])
    G[l[1]].addNode(l[0])

path = lexBFS(G,V)
print(path)
print(checkLexBFS(G, path))