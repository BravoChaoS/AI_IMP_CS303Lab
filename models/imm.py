import math
import time

from numpy import random


class IMM:
    def __init__(self):
        self.model = 'IC'
        self.lb = 1
        self.g = {}
        self.ig = {}
        self.e = 0
        self.l = 0
        self.n = 0
        self.k = 0
        self.log_cnk = 0
        self.tl = 60

    def run(self, model: str, g: dict, ig: dict, e: float, l: int, n: int, k: int, tl: int):
        self.model = model
        self.g = g
        self.ig = ig
        self.e = e
        self.l = l
        self.n = n
        self.k = k
        self.log_cnk = 0
        self.tl = tl
        for i in range(n - k + 1, n + 1):
            self.log_cnk += math.log(i)
        for i in range(1, k + 1):
            self.log_cnk -= math.log(i)

        rrs = self.sampling()
        seeds, size = self.node_selection(rrs)
        return seeds

    def get_lambda_aster(self):
        alpha = math.sqrt(self.l * math.log(self.n) + math.log(2))
        beta = math.sqrt((1 - 1 / math.e) * (self.log_cnk + self.l * math.log(self.n) + math.log(2)))
        return 2 * self.n * pow(((1 - 1 / math.e) * alpha + beta), 2) * pow(self.e, -2)

    def sampling(self):
        ep = math.sqrt(2) * self.e

        rrs = []
        rnd = int(math.log2(self.n - 1)) + 1
        # print(self.n)
        for i in range(1, rnd):
            x = self.n / math.pow(2, i)
            # print('x: ', x, self.n, i)
            lp = ((2 + 2 * ep / 3) * (
                    self.log_cnk + self.l * math.log(self.n) + math.log(math.log2(self.n))) * self.n) / pow(ep, 2)
            theta = lp / x

            rrs += self.generate_rrs(theta - len(rrs))
            seeds, f = self.node_selection(rrs)

            # print('ep: ', (1 + ep) * x)
            if self.n * f >= (1 + ep) * x:
                self.lb = self.n * f / (1 + ep)
                # print('break', f)
                break

        ls = self.get_lambda_aster()
        theta = ls / self.lb

        if len(rrs) < theta:
            rrs += self.generate_rrs(theta - len(rrs))

        return rrs

    def node_selection(self, rrs):
        seeds = []
        node_rr = [set() for i in range(self.n + 1)]
        seed_rr = set()

        for i in range(len(rrs)):
            rr = rrs[i]
            for u in rr:
                node_rr[u].add(i)

        while len(seeds) < self.k:
            opt = 0
            for i in range(1, len(node_rr)):
                if len(node_rr[i]) > len(node_rr[opt]):
                    opt = i

            seeds.append(opt)
            seed_rr = seed_rr | node_rr[opt]

            for nrr in node_rr:
                nrr.difference_update(node_rr[opt])

        # print(len(rrs), len(seed_rr) / len(rrs))
        return seeds, len(seed_rr) / len(rrs)

    def generate_rrs(self, theta):
        rrs = []
        theta = int(theta)
        random.seed(int(time.time()))
        if self.model == 'IC':
            for j in range(theta):
                v = random.randint(1, self.n)
                rrs.append(self.generate_rr_ic(v))
        else:
            for j in range(theta):
                v = random.randint(1, self.n)
                rrs.append(self.generate_rr_lt(v))
        return rrs

    def generate_rr_ic(self, v):
        activated = [v]
        visited = {v}

        while len(activated) > 0:
            new_activated = []
            for u in activated:
                for v, w in self.ig.get(u, []):
                    if v in visited:
                        continue
                    rd = random.uniform()
                    if rd < w:
                        new_activated.append(v)
                        visited.add(v)
            activated = new_activated
        return visited

    def generate_rr_lt(self, v):
        activated = [v]
        visited = {v}
        theta = {}

        while activated:
            new_activated = []
            for u in activated:
                for v, w in self.ig.get(u, []):
                    if v in visited:
                        continue
                    tot = 0
                    for ut, wt in self.g.get(v, []):
                        if ut in visited and ut not in new_activated:
                            tot += wt
                    if tot > theta.setdefault(v, random.random()):
                        new_activated.append(v)
                        visited.add(v)
            activated = new_activated
        return visited
