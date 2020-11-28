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
        self.tl = 60
        self.ts = 0
        self.te = 0

    def run(self, model: str, g: dict, ig: dict, e: float, l: int, n: int, k: int, tl: int):
        self.model = model
        self.g = g
        self.ig = ig
        self.e = e
        self.l = l
        self.n = n
        self.k = k
        self.tl = tl
        self.ts = time.time()

        rrs = self.sampling()
        # print(len(rrs))
        seeds = self.node_selection(rrs)
        return seeds

    def sampling(self):
        # s1 = time.time()
        rrs = []
        tlim = self.tl * 0.75

        s1 = time.time()
        while time.time() - s1 < tlim and len(rrs) < 10000000:
            v = random.randint(1, self.n)
            if self.model == 'IC':
                rrs.append(self.generate_rr_ic(v))
            else:
                rrs.append(self.generate_rr_lt(v))

        # print('sampling', time.time() - s1)
        # print('rrs_len', len(rrs))
        return rrs

    def node_selection(self, rrs):
        # s2 = time.time()
        seeds = []
        node_rr = [[] for i in range(self.n + 1)]
        node_rr_len = [0 for i in range(self.n + 1)]
        vis_rr = [True for i in range(len(rrs))]

        node_rr_len[0] = -1
        for i in range(len(rrs)):
            for nd in rrs[i]:
                node_rr_len[nd] += 1
                node_rr[nd].append(i)

        for i in range(self.k):
            opt = node_rr_len.index(max(node_rr_len))
            seeds.append(opt)
            for j in node_rr[opt]:
                if vis_rr[j]:
                    vis_rr[j] = False
                    for nd in rrs[j]:
                        node_rr_len[nd] -= 1
        # print('node_selection', time.time() - s2)
        return seeds

    def generate_rr_ic(self, v):
        activated = [v]
        visited = [v]

        while len(activated) > 0:
            new_activated = []
            for u in activated:
                for v, w in self.ig.get(u, []):
                    if v in visited:
                        continue
                    rd = random.uniform()
                    if rd < w:
                        new_activated.append(v)
                        visited.append(v)
            activated = new_activated
        return visited

    def generate_rr_lt(self, v):
        activated = v
        visited = [v]

        while activated:
            adj = self.ig.get(activated, [])
            if len(adj) == 0:
                break
            new_activated = adj[random.randint(0, len(adj))][0]
            if new_activated in visited:
                break
            visited.append(new_activated)
            activated = new_activated
        return visited
