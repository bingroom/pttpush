import pickle
import json

##Pre-read data

with open('/Users/joekaojoekao/PycharmProjects/push/github/gossiping_push.pickle', 'rb') as f:
    #ptt_pushes = json.load(f)
    ptt_pushes_tuple = pickle.load(f)    

with open('/Users/joekaojoekao/PycharmProjects/push/github/gossiping_pushes_json.txt', 'rb') as fout:
    cleaned_ptt_pushes = json.load(fout)
    fout.close()
    
import jieba
import jieba.analyse
jieba.set_dictionary('dict.txt.big')
jieba.analyse.set_stop_words('stopword_pool/merged_stopword.txt')

with open('/Users/joekaojoekao/PycharmProjects/push/github/gossiping_push_jieba_json.txt', 'rb') as fout:
    ptt_pushes = json.load(fout)
    fout.close()
    
with open('/Users/joekaojoekao/PycharmProjects/push/github/merged_gossiping_push_jieba_json.txt', 'rb') as fout:
    merged_ptt_pushes = json.load(fout)
    fout.close()

with open('/Users/joekaojoekao/PycharmProjects/push/github/gossiping_push_jieba_freq_byID_sorted_json.txt', 'rb') as fout:
    ptt_pushes_freq_byID_sorted = json.load(fout)
    fout.close()
    
with open('/Users/joekaojoekao/PycharmProjects/push/github/gossiping_push_jieba_freq_all_sorted_json.txt', 'rb') as fout:
    ptt_pushes_freq_all_sorted = json.load(fout)
    fout.close()


import numpy as np
import json
#set gt_numword (meaningful), gt_numpush (active)
NUM_WORD_GT = 4
NUM_PUSH_GT = 1

new_pushes = {}
for k in cleaned_ptt_pushes.keys():
    gt_push = [x for x in cleaned_ptt_pushes[k] if len(x) > NUM_WORD_GT]
    if len(gt_push) > 0:
        new_pushes[k] = gt_push

user_list = []
for k in new_pushes.keys():
    if len(new_pushes[k]) > NUM_PUSH_GT:
        user_list.append(k)
        
print len(cleaned_ptt_pushes)
print len(new_pushes)
print len(user_list)


##set threshold to generate stop words
word = ptt_pushes_freq_all_sorted.keys()

W_PERCENT = 0.025 #0.025
## setting for stopword & rareword percentage
stopwords = [x for x in word if ptt_pushes_freq_all_sorted[x] >= ptt_pushes_freq_all_sorted[word[int(len(word) * W_PERCENT)]]]
rarewords = [x for x in word if ptt_pushes_freq_all_sorted[x] <= ptt_pushes_freq_all_sorted[word[int(len(word) * (1-W_PERCENT))]]] #0.975

## stop word list
sw_list = [x for x in stopwords] 
## rare word list
rw_list = [x for x in rarewords] 
print 'total word', len(word)
print 'stop word', len(sw_list)
print 'rare word', len(rw_list)


sw_count_dict = {}
for w in sw_list:
    sw_count_dict.setdefault(len(w),[]).append(w)


K_NUMWORD = 6
selected_sw = []
for k in sw_count_dict.keys()[0:K_NUMWORD]:
    print 'num_word:',k,'\t',len(sw_count_dict[k])
    selected_sw += sw_count_dict[k]
print len(selected_sw)


##make SW vector


general_vec = {}

for uid in user_list: # for each user id
    user_len = sum(ptt_pushes_freq_byID_sorted[uid].values()) #total word freq
    #print sum(v.values())
    if user_len > 0:
        #vec = [jvc_grams_count[idx].get(w, 0) for w in new_sw_list] #stopword without function words
        
        vec = [ptt_pushes_freq_byID_sorted[uid].get(w, 0) for w in selected_sw]
        g_vec = [float(x) / user_len for x in vec]
        general_vec[uid] = g_vec

import combination as gb
import random
import pttfunc

N = 3
SAMPLE_NUM = 500 ##if too small  avg+3sd cannot get anything
n_sim_all = []
for n in xrange(N):
    ##sample fixed num of users and generate all combinations?


    r_list = random.sample(user_list, SAMPLE_NUM)
    #random_gv = dict((k, v) for k, v in r_list)
    r_gv = [(k, general_vec[k]) for k in r_list]
    comb = gb.getCombination(SAMPLE_NUM)

    ##calculate similarity for each user pair

    sim_list = np.array((0.0, 0.0, 0.0))
    for cb in comb:
        idx1 = cb[0]
        idx2 = cb[1]
        #k1, v1 = random_gv.items()[idx1]
        #k2, v2 = random_gv.items()[idx2]
        v1 = r_gv[idx1][1]
        v2 = r_gv[idx2][1]
        wj_sw = pttfunc.weighted_jacarrd(v1, v2)
        #sim_list = np.append(sim_list, np.array((k1, k2, wj_sw), dtype=mtype))
        sim_list = np.vstack((sim_list, np.array((round(float(idx1),1), round(float(idx2),1), wj_sw))))


    ##generate user pushes and sim file

    sim_list = sim_list[1:]
    sim_list = sim_list[sim_list[:,2].argsort()]
    sim_list = sim_list[::-1]


    temp = []
    for idx1, idx2, sim in sim_list:
        temp.append((user_list[int(idx1)], user_list[int(idx2)], sim))

    sim_list = temp
    #n_sim_all.append(sim_list)
    
    #df = pd.DataFrame(sim_list)
    sim_only = [x[2] for x in sim_list]
    #n_sim_all.append(sim_only)
    AVG_3SD = float(np.mean(sim_only, out=1) + np.std(sim_only, out=1)*3)

    AVG_3SD = 0 #generate all, select later
    
    sel = [(x[0], x[1]) for x in sim_list if x[2] >= AVG_3SD]
    #print sel
    #print len(sel)
    sel_user = list(set([y for x in sel for y in x]))
    #print sel_user

    sel_sim = [(x[0], x[1], x[2]) for x in sim_list if x[2] >= AVG_3SD]
    with open('/Users/joekaojoekao/PycharmProjects/push/github/visualized/select_sim500_' + str(n+1) + '.txt', 'wb') as fout1:
        for sim in sel_sim:
            line = sim[0] + ',' + sim[1] + ',' + str(sim[2])+'\n'
            fout1.write(line.encode('utf-8'))
    fout1.close()

    with open('/Users/joekaojoekao/PycharmProjects/push/github/visualized/select_pushes500_' + str(n+1) + '.txt', 'wb') as fout2:
        for k in sel_user:
            for v in new_pushes[k]:
                if k == '':
                    continue
                line = k + '\t' + v +'\n'
                fout2.write(line.encode('utf-8'))
    fout2.close()
    
    print n