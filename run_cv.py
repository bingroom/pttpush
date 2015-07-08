## import processed push data
with open('/Users/joekaojoekao/PycharmProjects/push/github/visualized/select_pushes101.txt', 'rb') as fin:
    s = fin.read().split('\n')
    lines = []
    for line in s:
        lines.append(line.split('\t'))
    fin.close()

## make a dict
sample_dict = {}
for i in lines:
    if len(i) != 2:
        continue
    uid = i[0]
    push = i[1]
    if uid not in sample_dict:
        sample_dict[uid] = [push]
    else:
        sample_dict[uid].append(push)

## new dict with values containing push & seg_list
import jieba
import jieba.analyse
jieba.set_dictionary('dict.txt.big')
jieba.analyse.set_stop_words('stopword_pool/merged_stopword.txt')
sample_dict_jieba = {}
for uid in sample_dict.keys():
    pushes = sample_dict[uid]
    if len(pushes) > 0:
        sample_dict_jieba[uid] = []
        for push in pushes:
            seg_list = list(jieba.cut(push, cut_all=False))
            sample_dict_jieba[uid].append((push,seg_list))



## filter pushes by setting gt_numword (meaningful), gt_numpush (active)
NUM_WORD_GT = 4
NUM_PUSH_GT = 3 #for 6 fold-cv

new_pushes = {}
for k in sample_dict.keys():
    gt_push = [x for x in sample_dict[k] if len(x) > NUM_WORD_GT]
    if len(gt_push) > 0:
        new_pushes[k] = gt_push

user_list = []
for k in new_pushes.keys():
    if len(new_pushes[k]) >= NUM_PUSH_GT:
        user_list.append(k)
        
print 'origin:', len(sample_dict)
print 'new:', len(new_pushes)
print 'with user:', len(user_list)

##這裡根本沒有作多次cv... dict_user有問題
## Doing cross validation
from sklearn import cross_validation
dict_user = {} #training
dict_user_ans = {} #testing
for uid in user_list:
    training_set = sample_dict_jieba[uid]
    cv = cross_validation.KFold(len(training_set), n_folds=3, indices=True, shuffle=False, random_state=None, k=None)
    
    ## generate all possible train/test set and run
    for traincv, testcv in cv:    
        dict_user[uid] = []
        for i in traincv:
            dict_user[uid].append(training_set[i])
        dict_user_ans[uid] = []
        for i in testcv:
            dict_user_ans[uid].append(training_set[i])
            

## prepare for trainset and testset(ans)
import pttfunc
dict_user_count = pttfunc.count_dict(dict_user) #count the freq
dict_user_count_ans = pttfunc.count_dict(dict_user_ans) #count the freq for ans(test)

## count all using words freq, preparing for generating sorted sw_list 
count_all = Counter()
for v in dict_user_count.values():
    count_all += Counter(v)
from collections import OrderedDict
dict_all_count = OrderedDict(sorted(dict(count_all).items(), key=lambda t: t[1], reverse=True))

## set stopword percentage(in global push)
W_PERCENT = 0.025
word = dict_all_count.keys()
stopwords = [x for x in word if dict_all_count[x] >= dict_all_count[word[int(len(word) * W_PERCENT)]]]
#rarewords = [x for x in word if dict_all_count[x] <= dict_all_count[word[int(len(word) * (1-W_PERCENT))]]] #0.975

## stop word list
sw_list = [x for x in stopwords] 
## rare word list
#rw_list = [x for x in rarewords] 
print 'total word', len(word)
print 'stop word', len(sw_list)
#print 'rare word', len(rw_list)

## select stopword less than 6 word
K_NUMWORD = 6
sw_count_dict = {}
for w in sw_list:
    sw_count_dict.setdefault(len(w),[]).append(w)
selected_sw = []
for k in sw_count_dict.keys()[0:K_NUMWORD]:
    print 'num_word:',k,'\t',len(sw_count_dict[k])
    selected_sw += sw_count_dict[k]
print 'after filter:', len(selected_sw)


## generate training/testing vectors by sw_word freq / total wordfreq
general_vec = {}
for uid in user_list: # for each user id
    user_len = sum([len(x) for x in dict_user_count[uid]]) #total word freq
    if user_len > 0:
        vec = [dict_user_count[uid].get(w, 0) for w in selected_sw]
        g_vec = [float(x) / user_len for x in vec]
        general_vec[uid] = g_vec
        
general_vec_ans = {}
for uid in user_list: # for each user id
    user_len = sum([len(x) for x in dict_user_count_ans[uid]]) #total word freq
    #print sum(v.values())
    if user_len > 0:
        #vec = [jvc_grams_count[idx].get(w, 0) for w in new_sw_list] #stopword without function words
        
        vec = [dict_user_count_ans[uid].get(w, 0) for w in selected_sw]
        g_vec = [float(x) / user_len for x in vec]
        general_vec_ans[uid] = g_vec

##calculate similarity for each user pair

import pttfunc
import numpy as np
sim_list = np.array((0.0, 0.0, 0.0))
for i in xrange(len(user_list)):
    for j in xrange(len(user_list)):
        wj_sw = pttfunc.weighted_jaccard(general_vec[user_list[i]], general_vec_ans[user_list[j]])
        sim_list = np.vstack((sim_list, np.array((round(float(i),1), round(float(j),1), wj_sw))))

#sorting
sim_list = sim_list[1:]
sim_list = sim_list[sim_list[:,2].argsort()]
sim_list = sim_list[::-1]

#make final list
user_sim_list = []
for i, j, sim in sim_list:
    user_sim_list.append((user_list[int(i)], user_list[int(j)] + 'ANS', sim))

## evaluation
a = 0
for i,j,sim in user_sim_list:
    if i == j[:-3] and sim > 0.3:
        a+=1
b = len(user_list)
print float(a)/ b
