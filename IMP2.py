import multiprocessing as mp
import time
import sys
import argparse
import os
import random
import math
import numpy as np

INACTIVE = 0
BEING_ACTIVE = 1
ACTIVED = 2

class Graph:

    def __init__(self, index):
        
        self.index = index

        self.in_degree = 0

        self.out_degree = 0

        self.neighbor = []

        self.state = 0

        self.threshold = 0

        self.weight_total = 0
    
# def func(a):
    # return a.out_degree

def sampling(graph_list_reverse, n, k, em, l, model):
    start = time.perf_counter()
    R = []
    LB = 0
    emStar = math.sqrt(2)*em
    hello = 0
    count = 0
    for i in range(1, int(math.log2(n))):
        x = n/math.pow(2, i)
        theta_i = cal_lambda(emStar, n, k, l, LB)/x
        while(len(R) <= theta_i):
            v = random.randint(1, n)
            start = time.perf_counter()
            rr, a = sampling_rr(graph_list_reverse, v, model)
            R.append(rr)
            count += a
            # R.append(sampling_rr(graph_list_reverse, v, model)[0])
            end = time.perf_counter()
            hello += (end-start)
        S_i, fr = node_selection(R, n, k)
        if n*fr >= (1+emStar)*x:
            LB = n*fr/(1+emStar)
            break
    # print("1:", hello)
    theta = cal_lambdaStar(l, n, k, em)/LB
    while(time.perf_counter()-start < time_limit-20 and len(R)<=100 * theta):
        v = random.randint(1, n)
        start = time.perf_counter()
        rr, a = sampling_rr(graph_list_reverse, v, model)
        count += a
        R.append(rr)
        # R.append(sampling_rr(graph_list_reverse, v, model)[0])
        end = time.perf_counter()
        hello += end-start
    # print(theta)
    # print("2:", hello)
    # print("3:", count)
    return R

def node_selection(R, n, k):
    node_count = []
    node_contain_rr = []
    rr_available = []
    Sk = []
    for i in range(0, n+1):
        node_count.append(0)
        node_contain_rr.append([])
    node_count[0] = -1
    for i in range(0, len(R)):
        rr_available.append(True)
        rr = R[i]
        for nd in rr:
            node_count[nd] += 1
            node_contain_rr[nd].append(i)
    for i in range(0, k):
        fr = max(node_count)
        select_node = node_count.index(fr)
        Sk.append(select_node)
        for rr1 in node_contain_rr[select_node]:
            if(rr_available[rr1]):
                rr_available[rr1] = False
                for nd1 in R[rr1]:
                    node_count[nd1] -= 1
    count = 0
    for i in range(0, len(R)):
        if(not rr_available[i]):
            count += 1
    # for i in range(0, n+1):
    #     if node_count[i]<0:
    #         print(node_count[i])
    return Sk, count/len(R)

def cal_log_n_k(n, k):
    val = 0
    for i in range(1, k+1):
        val+=math.log(n-k+i)
        val-=math.log(i)
    return val

def cal_lambda(emStar, n, k, l, LB):
    return (2+2*emStar/3)*(cal_log_n_k(n, k)+l*math.log(n)+math.log(math.log2(n)))*n/math.pow(emStar, 2)

def cal_lambdaStar(l, n, k,  em):
    alpha = math.sqrt(l*math.log(n) + math.log(2))
    beta = math.sqrt((1-1/2.718)*(cal_log_n_k(n, k)+l*math.log(n)+math.log(2)))
    return 2*n*math.pow(((1-1/2.718)*alpha + beta), 2)*math.pow(em, -2)

def sampling_rr(graph_list_reverse, v, model):
    if(model == 'IC'):
        return sampling_icrr(graph_list_reverse, v)
    else:
        return sampling_ltrr(graph_list_reverse, v)

def sampling_icrr(graph_list_reverse, v):
    activity_node = []
    rr_node = set()
    # sum = 0
    # count = 0
    # print(len(initial_nodes))
    # graph_list1 = graph_list.copy()
    # count = count + 1
    start = time.perf_counter()
    # for item in graph_list_reverse:
    #     item.state = INACTIVE
    end = time.perf_counter()
    # graph_list_reverse[v].state = ACTIVED
        # activity_node = initial_nodes.copy()
    activity_node.append(graph_list_reverse[v])
    rr_node.add(v)
    # length = len(activity_node)
    while(len(activity_node)>0):
        new_activity_node = []
        for item in activity_node:
            for item1 in item.neighbor:
                a = item1[0]
                # if(graph_list_reverse[a].state == ACTIVED):
                if(a in rr_node):
                    continue
                prob = random.random()
                if(prob<item1[1]):
                    # graph_list_reverse[a].state = ACTIVED
                    new_activity_node.append(graph_list_reverse[a])
                    rr_node.add(a)
        # length = length + len(new_activity_node)
        activity_node = new_activity_node.copy()
        # sum = sum + length
    return list(rr_node), end-start

def sampling_ltrr(graph_list_reverse, v):
    # initial_nodes = []
    # while True:
    #     line = file2.readline()
    #     if not line:
    #         break
    #     line = line.strip()
    #     a = int(line)
    #     graph_list[a].state = ACTIVED
    #     initial_nodes.append(graph_list[a])
    activity_node = v
    rr_node = set()
    rr_node.add(v)
    while(activity_node>=0):
        new_activity_node = -5
        neibr = graph_list_reverse[activity_node].neighbor
        length = len(neibr)
        if(length == 0):
            break
        grf = neibr[random.randint(0, length-1)][0]
        if(grf in rr_node):
            break
        else:
            rr_node.add(grf)
            new_activity_node = grf
        activity_node = new_activity_node
    return list(rr_node), 0

def imm(graph_list_reverse, n, k, em, l, model, time_limit):
    l = l*(1+math.log(2)/math.log(n))
    start = time.perf_counter()
    R = sampling(graph_list_reverse, n, k, em, l, model)
    end = time.perf_counter()
    # print(end-start)
    start = time.perf_counter()
    Sk, x = node_selection(R, n, k)
    end = time.perf_counter()
    # print(end-start)
    return Sk

if __name__ == '__main__':
    '''
    从命令行读参数示例
    '''
    # print("从命令行读参数示例")
    start = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='network.txt')
    parser.add_argument('-k', '--seed_number', type=int, default=5)
    parser.add_argument('-m', '--model', type=str, default='LT')
    parser.add_argument('-t', '--time_limit', type=int, default=60)

    args = parser.parse_args()
    file_name = args.file_name
    seed_number = args.seed_number
    model = args.model
    time_limit = args.time_limit
    # if(model == 'IC'):
    #     print(solve_ic(file_name, seed, model, time_limit))
    # else:
    #     print(solve_lt(file_name, seed, model, time_limit))
    graph_list = []
    graph_list_reverse = []
    file1 = open(file_name)
    line = file1.readline()
    str = line.strip().split(' ')
    n = int(str[0])
    m = int(str[1])
    for i in range(0, n+1):
        graph_list.append(Graph(i))
        graph_list_reverse.append(Graph(i))
    for i in range(0, m):
        line = file1.readline()
        str = line.strip().split(' ')
        a = int(str[0])
        b = int(str[1])
        c = float(str[2])
        graph_list[a].neighbor.append((b, c))
        graph_list[a].out_degree = graph_list[a].out_degree + 1
        graph_list[b].in_degree = graph_list[b].in_degree + 1
        graph_list_reverse[b].neighbor.append((a,c))
        graph_list_reverse[b].out_degree = graph_list_reverse[b].out_degree + 1
        graph_list_reverse[a].in_degree = graph_list_reverse[a].in_degree + 1
    Sk = imm(graph_list_reverse, n, seed_number, 0.5, 1, model, time_limit)
    for item in Sk:
        print(item)