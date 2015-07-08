import math
import collections
import numpy as np
#import matplotlib.pyplot as plt
import sys


def count_dict(sample_dict_jieba):
    from collections import Counter
    from collections import OrderedDict
    import itertools
    ptt_pushes_freq_bypush = {}
    for uid, push_list in sample_dict_jieba.iteritems():
        push = push_list[0]
        a = zip(*push_list)[1]
        push_gram = list(itertools.chain(*a))
        count = Counter(push_gram)
        temp = []
        for w, c in count.most_common():
            temp.append((w, c))
        id_count = Counter(dict(temp))
        ptt_pushes_freq_bypush[uid] = dict(id_count)

    return ptt_pushes_freq_bypush


def hasCHword(word):
    return any(u'\u4e00' <= c <= u'\u9fff' for c in word.decode('utf-8'))


def topNword(word_list, n):
    select = []
    count = 0
    for w, c in word_list:
        if hasCHword(w):
            select.append((w, c))
            count += 1
        if count == n:
            return select
        
def bottomNword(word_list, n):
    select = []
    count = 0
    for w, c in reversed(word_list):
        if hasCHword(w):
            select.append((w, c))
            count += 1
        if count == n:
            return select

def ch_num_dict(word_list):
    count_dict = {}
    for w in word_list:
        len(w)

def weighted_jaccard(l1, l2):
    if len(l1) != len(l2):
        return -1
    num = 0
    den = 0
    for i in xrange(len(l1)):
        num += np.minimum(l1[i], l2[i])
        den += np.maximum(l1[i], l2[i])
        #num += min(l1[i], l2[i])
        #den += max(l1[i], l2[i])

    #wj = np.float64(num) / den 
    
    #wj = np.float64(num) / den
    #print num, den
    #wj = float(num) / den 
    wj = np.divide(np.float64(num), den)

    return wj

def def_jaccard(l1, l2):
    a = 0
    b = 0
    c = 0
    d = 0
    for i in xrange(len(l1)):
        a += l1[i] * l2[i]
        b += l1[i] * l1[i]
        c += l2[i] * l2[i]
        d += 1
    #cos_sim = (a / (math.sqrt(b) * math.sqrt(c)))
    ej_sim = (float(a) / (b + c - a))
    return ej_sim

import pickle
ip_dict = pickle.load(open("ip_dict.pickle", "rb"))
sel_list = [x for x in ip_dict.items() if len(x[1]) >= 2]
def has_same_ip(u1, u2):
    for u in sel_list:
        if len(set(u[1]).intersection(set((u1,u2)))) > 1:
            return True

    return False
