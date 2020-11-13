import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit

    print(file_name, seed, model, time_limit, sep='\n')
    with open(file_name, 'r') as f:
        network_lines = f.readlines()

    n, m = map(int, network_lines[0].split())
    graph = {}
    print(len(network_lines))

    for line in network_lines[1:m]:
        par = line.split()
        u, v, w = int(par[0]), int(par[1]), float(par[2])

        graph[u] = graph.get(u, []) + [(v, w)]
        graph[v] = graph.get(v, []) + [(u, w)]

    # for key, value in graph.items():
    #     print(key, ':')
    #     print(value)

    sys.stdout.flush()
