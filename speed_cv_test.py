import pttfunc
import time
import numpy as np

N_sw = 302
N_user = 203 #20342
zero_percent = 0.9 #0.997056899935
def vec_gen():
 
    import random
    #random.uniform(0.0, 0.9)
    #vec = [random.uniform(0.0, 0.9) for i in range(N_sw)]
    vec = [0.0] * N_sw
    for i in xrange(len(vec)):
        if random.randint(0,9) == 9:
            vec[i] = random.uniform(0.0, 0.9)

    return vec

vec1_list = [vec_gen() for i in range(N_user)]
vec2_list = [vec_gen() for i in range(N_user)]

t_start = time.time()
size = N_user * N_user
sim = np.array(np.arange(size), dtype='float64')
idx = 0
for i in xrange(N_user):
    for j in xrange(N_user):
        sim[idx] = pttfunc.weighted_jaccard(vec1_list[i], vec2_list[j])
        idx += 1
sim = sim[:idx]
t_stop = time.time()

print t_stop - t_start