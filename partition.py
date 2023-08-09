import igraph as ig

def create_pratition(G: ig.Graph):
    G_t: ig.Graph = G.copy()
    partitions = []


    while G.vs > 0:
        outpoints = [v.index for v in G_t.vs if G.degree(v, mode='in') == 0]

        partitions.insert(0, outpoints)

        G_t.delete_vertices(outpoints)
    
    return partitions
    