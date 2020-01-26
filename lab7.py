import networkx as nx
from networkx.algorithms.planarity import check_planarity
from networkx.algorithms.flow import maximum_flow
from networkx.algorithms.components import strongly_connected_components
from networkx.algorithms.dag import topological_sort
import dimacs


def planar(V, L):
    G = nx.Graph()
    G.add_nodes_from([i + 1 for i in range(V)])
    G.add_edges_from([(i[0], i[1]) for i in L])
    print(check_planarity(G))


def flow(V, L):
    G = nx.DiGraph()
    G.add_nodes_from([i + 1 for i in range(V)])
    G.add_edges_from([(i[0], i[1]) for i in L])
    for l in L:
        G[l[0]][l[1]]['capacity'] = l[2]
    print(maximum_flow(G, 1, V))

def SAT2(V, L):
    G = nx.DiGraph()
    G.add_nodes_from([i + 1 for i in range(V)])
    G.add_nodes_from([-i - 1 for i in range(V)])
    for l in L:
        G.add_edge(-l[0], l[1])
        G.add_edge(-l[1], l[0])
    SCC = strongly_connected_components(G)
    SSS = {}
    REP = {}
    SSSVal = {}
    t = 0
    for S in SCC:
        print(t)
        T = set()
        for v in S:
            SSS[v] = t
            if (-v) in T:
                return False, None
            T |= {v}
            REP[t] = v
        t += 1
    H = nx.DiGraph()
    H.add_nodes_from(range(1,t))
    for (a, b) in G.edges:
        if SSS[a] != SSS[b] and not H.has_edge(SSS[a], SSS[b]):
            H.add_edge(SSS[a], SSS[b])

    O = topological_sort(H)
    print(O)
    for s in O:
        if SSS[-REP[s]] not in SSSVal:
            SSSVal[s] = False
        else:
            SSSVal[s] = not (SSS[-REP[s]])

    for v in range(-V, V + 1):
        if v != 0:
            print(v, " ", SSS[v])
    print(SSSVal)
    for v in range(-V, V+1):
        if v != 0:
            print(v, " ", SSSVal[SSS[v]])
    for l in L:
        if not (SSSVal[SSS[l[0]]] or SSSVal[SSS[l[1]]]):
            print("False")
    return True, None



(V, L) = dimacs.loadCNFFormula("sat/sat100_200")
print(SAT2(V, L))
