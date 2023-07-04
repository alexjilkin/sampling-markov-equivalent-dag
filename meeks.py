import igraph as ig
from utils import plot

def is_storgly_protected(G: ig.Graph, e: ig.Edge):
    a, b = e.source, e.target

    # a
    a_parents = list(G.predecessors(a))
    c = a_parents[0]
    if len(a_parents) == 1 and not G.are_connected(c, b) and not G.are_connected(b, c):
        return True
    
    # b
    b_parents = list(G.predecessors(b))
    c = a_parents[0]
    if len(b_parents) == 1 and not G.are_connected(c, a) and not G.are_connected(a, c):
        return True
    
    # c
    a_parents = list(G.predecessors(a))
    if len(b_parents) == 1:
        c = a_parents[0]
        if (G.are_connected(c, b)):
            return True
    
    # d
    a_parents = list(G.predecessors(a))
    if (len(a_parents) == 2):
        c1 = a_parents[0]
        c2 = a_parents[1]
        if (G.are_connected(c1, b) and G.are_connected(c2, b)):
            return True
    

def CPDAG(D: ig.Graph):
    G_i = D
    G_i_plus_1 = None

    while not G_i.isomorphic(G_i_plus_1):
        G_i_plus_1 = G_i.copy()

        for e in G_i_plus_1:
            if (is_storgly_protected(G_i_plus_1, e)):
                print(e)
                plot(G_i_plus_1)