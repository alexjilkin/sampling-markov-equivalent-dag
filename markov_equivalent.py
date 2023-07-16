import itertools
import random
import igraph as ig
import networkx as nx
import numpy as np
from count import C, FP, count, get_maximal_cliques, v_func
from utils import plot
# from cdt.metrics import get_CPDAG

# U is a the essential graph
def get_markov_equivalent_topological_orders(U: nx.Graph):
    def get_topological_order(UCCG: nx.Graph):
        AMO = count(UCCG)

        clique_tree = nx.junction_tree(UCCG)
        maximal_cliques = get_maximal_cliques(clique_tree)
        r = maximal_cliques[0]

        # Maximal clique drawn with probability proportional to v_func
        p = list(map(lambda v: v_func(UCCG, r, v, clique_tree) / AMO, maximal_cliques))
        v = maximal_cliques[np.random.choice(np.arange(len(p)), p=p)]

        K = set(v)
        to = list(K)

        permutations = list(itertools.permutations(to))
    
        # uniformly drawn permutation of ι(v) without prefix in FP(v, T )
        is_good_to = False
        while not is_good_to:
            to = random.choice(permutations)
            is_good_to = True

            for fp in FP(clique_tree, r, v):
                if (np.array_equal(to[:len(fp)], fp)):
                    is_good_to = False
        
        for H in C(UCCG, K):
            to += get_topological_order(H)

        return to
    
    # pre-process
    count(U)
    # Gets the UCCGs from the essential graph
    UCCGs = [U.subgraph(component) for component in nx.connected_components(U)]
    UCCGs = list(filter(lambda UCCG: len(UCCG.nodes) > 1, UCCGs))
        
    tos = [get_topological_order(UCCG) for UCCG in UCCGs]

    return tos

def get_markov_equivalent(G: ig.Graph) -> ig.Graph:
    # A = nx.DiGraph()

    # # Nodes should be sorted, as later get_CPDAG returns an adjecency matrix according to it (row = node)
    # A.add_nodes_from(np.arange(len(G.vs)))

    # for e in G.es:
    #     A.add_edge(e.source, e.target)

    # essential_g_l = nx.from_numpy_array(get_CPDAG(A), create_using=nx.DiGraph)

    # # Create a networkx graph to be used with count()
    # U_l = nx.Graph()
    # U_l.add_nodes_from(np.arange(len(G.vs)))

    # for (source, target) in essential_g_l.edges:
    #     if essential_g_l.has_edge(target, source):
    #         U_l.add_edge(source, target)

    essential_g = CPDAG(G)
    U = nx.Graph()
    U.add_nodes_from(np.arange(len(G.vs)))

    for e in essential_g.es:
        U.add_edge(e.source, e.target)

    tos = get_markov_equivalent_topological_orders(U)

    if len(tos) == 0:
        return G
    
    equivalent_G = ig.Graph(directed=True)
    equivalent_G.add_vertices(len(G.vs))

    for to in tos:
        
        for (source, target) in U.edges:
            if (source not in to or target not in to):
                continue
            if (to.index(source) < to.index(target)):
                equivalent_G.add_edge(source, target)
            else:
                equivalent_G.add_edge(target, source)

    for e in G.es:
        if not (equivalent_G.are_connected(e.source, e.target) or equivalent_G.are_connected(e.target, e.source)):
            equivalent_G.add_edge(e.source, e.target)

    return equivalent_G

def is_strongly_protected(G: ig.Graph, G_lines: ig.Graph, e: ig.Edge):
    a, b = e.source, e.target

    # a
    a_parents = list(G.predecessors(a))
    for c in a_parents:
        if not G.are_connected(c, b) and not G.are_connected(b, c):
            return True
            
    # b
    b_parents = list(G.predecessors(b))
    for c in b_parents:
        if c != a and not G.are_connected(c, a) and not G.are_connected(a, c):
            return True
        
    # c
    b_parents = list(G.predecessors(b))
    for c in b_parents:
        if (c != a and G.are_connected(a, c)):
            return True
    # d
    a_lines_neighbors = list(G_lines.neighbors(a))
    a_neighbors = list(G.neighbors(a))
    for c1, c2 in itertools.combinations(a_lines_neighbors, 2):
        if (G.are_connected(c1, b) and G.are_connected(c2, b)):
            return True
    for c1, c2 in itertools.combinations(a_neighbors, 2):
        if (G.are_connected(c1, b) and G.are_connected(c2, b)):
            return True
        
    return False


def CPDAG(D: ig.Graph):
    G_i = D.copy()
    G_lines = ig.Graph()
    G_lines.add_vertices(len(G_i.vs))
    
    G_i_plus_1 = undirect_non_strongly_protected_arrows(G_i, G_lines)

    while(len(G_i.es) != len(G_i_plus_1.es)):
        G_i = G_i_plus_1.copy()     
        G_i_plus_1 = undirect_non_strongly_protected_arrows(G_i, G_lines)

    return G_lines

def undirect_non_strongly_protected_arrows(G: ig.Graph, G_lines: ig.Graph):
    new_G = G.copy()

    for e in G.es:
        if not is_strongly_protected(G, G_lines, e):
            G_lines.add_edge(e.source, e.target)
            new_G.delete_edges([(e.source, e.target)])

    return new_G