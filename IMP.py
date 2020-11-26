import argparse
import sys

from models.imm import IMM
from models.read import get_graph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='test/network.txt')
    parser.add_argument('-k', '--seed_number', type=int, default=1)
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()

    # print(args.file_name, args.seed, args.model, args.time_limit, sep='\n')

    g, ig, n = get_graph(args.file_name)
    imm = IMM()
    e = 0.2
    l = 5
    seeds = imm.run(args.model, g, ig, e, l, n, args.seed_number, args.time_limit)
    for u in seeds:
        print(u)

    sys.stdout.flush()
