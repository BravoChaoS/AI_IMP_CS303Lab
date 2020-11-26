import argparse
import sys
from time import time

from models.lt import lt
from models.ic import ic
from models.read import get_graph, get_seed

N = 10000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-s', '--seed', type=str, default='seeds.txt')
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()

    # print(args.file_name, args.seed, args.model, args.time_limit, sep='\n')

    network_graph, inverse_network_graph, n = get_graph(args.file_name)
    initial_activated = get_seed(args.seed)

    ans = 0

    t0 = time()
    tl = int(args.time_limit)
    cnt = 0
    if args.model == 'IC':
        while cnt <= N and time() - t0 + 4 < tl:
            ans += len(ic(network_graph, initial_activated))
            cnt += 1
    else:
        while cnt <= N and time() - t0 + 4 < tl:
            ans += len(lt(network_graph, inverse_network_graph, initial_activated))
            cnt += 1

    print(ans / cnt)
    sys.stdout.flush()
