import argparse
import sys
from lt import lt
from models.ic import ic

N = 1000


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

    return g, ig


def get_seed(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    return list(map(int, lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()

    # print(args.file_name, args.seed, args.model, args.time_limit, sep='\n')

    network_graph, inverse_network_graph = get_graph(args.file_name)
    initial_activated = get_seed(args.seed)
    # print(initial_activated)

    # for key, value in network_graph.items():
    #     print(key, ':')
    #     print(value)

    ans = 0

    if args.model == 'IC':
        for i in range(N):
            ans += ic(network_graph, initial_activated)
    else:
        for i in range(N):
            ans += lt(network_graph, inverse_network_graph, initial_activated)

    print(ans / N)
    sys.stdout.flush()
