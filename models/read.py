def get_graph(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    n, m = map(int, lines[0].split())
    g = {}
    ig = {}
    # print(len(lines))

    for line in lines[1:m]:
        par = line.split()
        u, v, w = int(par[0]), int(par[1]), float(par[2])

        g[u] = g.get(u, []) + [(v, w)]
        ig[v] = ig.get(v, []) + [(u, w)]

    # print(lines[m])
    return g, ig, n


def get_seed(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    return list(map(int, lines))
