import argparse
import sys
from time import time

from models.lt import lt
from models.ic import ic
from models.read import get_graph, get_seed

N = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()

    # print(args.file_name, args.seed, args.model, args.time_limit, sep='\n')

    n, m, network_graph, inverse_network_graph = get_graph(args.file_name)
    initial_activated = get_seed(args.seed)
    # print(initial_activated)

    # for key, value in network_graph.items():
    #     print(key, ':')
    #     print(value)

    ans = 0

    t0 = time()
    tl = int(args.time_limit)
    if args.model == 'IC':
        while time() - t0 + 2 < tl:
            ans += ic(network_graph, initial_activated)
            N += 1
    else:
        while time() - t0 + 2 < tl:
            ans += lt(n, network_graph, inverse_network_graph, initial_activated)
            N += 1

    print(ans / N)
    sys.stdout.flush()
