from numpy import random


def ic(graph, ini_activated):
    activated = ini_activated.copy()
    visited = set(ini_activated.copy())

    while len(activated) > 0:
        new_activated = []
        for u in activated:
            for v, w in graph.get(u, []):
                if v in visited:
                    continue
                rd = random.uniform()
                if rd < w:
                    new_activated.append(v)
                    visited.add(v)
        activated = new_activated
    return visited
