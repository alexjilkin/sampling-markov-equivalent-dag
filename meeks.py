import itertools
import igraph as ig
from utils import plot

def is_storgly_protected(G: ig.Graph, e: ig.Edge):
    a, b = e.source, e.target

    # a
    a_parents = list(G.predecessors(a))
    for c in a_parents:
        if not G.are_connected(c, b) and not G.are_connected(b, c):
            # print(a, b)
            # plot(G)
            return True
            
    # b
    b_parents = list(G.predecessors(b))
    for c in b_parents:
        if c != a and not G.are_connected(c, a) and not G.are_connected(a, c):
            # print(a, b)
            # plot(G)
            return True
        
    # c
    a_parents = list(G.predecessors(a))
    for c in a_parents:
        if (G.are_connected(c, b)):
            # print(a, b)
            # plot(G)
            return True
    
    # d
    a_parents = list(G.predecessors(a))
    for c1, c2 in itertools.product(a_parents, repeat=2):
        if (c1 != c2 and G.are_connected(c1, b) and G.are_connected(c2, b)):
            # print(a, b)
            # plot(G)
            return True
    

def undirect_not_strongly_protected(G: ig.Graph, G_lines: ig.Graph):
    new_G = G.copy()

    for e in G.es:
        if not is_storgly_protected(new_G, e):
            G_lines.add_edge(e.source, e.target)
            new_G.delete_edges([(e.source, e.target)])

    # plot(new_G)
    return new_G, G_lines

def CPDAG(D: ig.Graph):
    G_i = D.copy()
    G_lines = ig.Graph()
    G_lines.add_vertices(len(G_i.vs))

    G_i_plus_1, G_lines = undirect_not_strongly_protected(G_i, G_lines)

    # while not G_i.isomorphic(G_i_plus_1):
    while(len(G_i.es) != len(G_i_plus_1.es)):
    # for i in range(20):
        G_i = G_i_plus_1.copy()     
        G_i_plus_1, G_lines = undirect_not_strongly_protected(G_i, G_lines)
        
    return G_lines
