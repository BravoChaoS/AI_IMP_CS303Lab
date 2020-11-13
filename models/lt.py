from numpy import random


def lt(n, graph, inv_graph, ini_activated):
    activated = ini_activated.copy()
    visited = set(ini_activated.copy())

    theta = random.randn(n)

    while activated:
        new_activated = []
        for u in activated:
            for v, w in graph.get(u, []):
                if v in visited:
                    continue
                tot = 0
                for ut, wt in inv_graph.get(v, []):
                    if ut in visited:
                        tot += wt
                if tot > theta[v]:
                    new_activated.append(v)
                    visited.add(v)
        activated = new_activated
    return len(visited)
