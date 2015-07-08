# -*- coding: utf-8 -*-
import json
import os
##import processed push data
dir_path = os.getcwd() + '/'
with open(dir_path + 'config.txt', 'rb') as f_conf:
    config = json.load(f_conf)
    f_conf.close()
    
sample_dir = config["sample_dir"]
sample_file = config["sample_file"] 
TEST_SIZE = config["TEST_SIZE"] 
temp_path = config["temp_path"]

##read source file
with open(sample_dir + sample_file, 'rb') as fin:
    s = fin.read().split('\n')
    lines = []
    for line in s:
        lines.append(line.split('\t'))
    fin.close()
print 'read source:',sample_dir + sample_file
    
    
##gen (name, push) pairs
sample_dict = {}
for i in lines:
    #print len(i)
    #if len(i) >= 3:
    if len(i) != 2:
        continue
    uid = i[0]
    push = i[1]
    if uid not in sample_dict:
        sample_dict[uid] = [push]
    else:
        sample_dict[uid].append(push)

##do word segmentation
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

            
import numpy as np
import json
#set gt_numword (meaningful), gt_numpush (active)
NUM_WORD_GT = 4
NUM_PUSH_GT = 3 #for 6 fold-cv

new_pushes = {}
for k in sample_dict.keys():
    gt_push = [x for x in sample_dict[k] if len(x) > NUM_WORD_GT]
    if len(gt_push) > 0:
        new_pushes[k] = gt_push
print 'Pushes filtering (keep only pushes larger than', NUM_WORD_GT, 'words)'
print 'After filtering / Origin push num: ',len(new_pushes) , '/', len(sample_dict)

user_list = []
for k in new_pushes.keys():
    if len(new_pushes[k]) >= NUM_PUSH_GT:
        user_list.append(k)
print 'Users filtering (remove users who post less than', NUM_PUSH_GT, 'pushes)'
print 'After filtering / Previous user num: ',len(user_list) , '/', len(new_pushes.keys())

#print 
#print len(sample_dict)
#print len(new_pushes)
#print len(user_list)
#print user_list


import json

#temp_path = '/Users/joekaojoekao/PycharmProjects/push/github/temp/'
#sample_file = 'select_pushes101'
#write in temp
with open(temp_path + os.path.splitext(sample_file)[0] + '_userlist.txt', 'wb') as f_temp:
    f_temp.write(json.dumps(user_list, indent=2, ensure_ascii=True).encode('utf-8'))
    f_temp.close()
print 'write user list:',temp_path + os.path.splitext(sample_file)[0] + '_userlist.txt'


##gen cv with odd/even
user = {}
user_ans = {}
def crossover_split(training_set):
    odd = training_set[1::2]
    even = training_set[::2]
    return odd, even

for uid in user_list:
    training_set = sample_dict_jieba[uid]
    #cv = cross_validation.ShuffleSplit(len(training_set), n_iter=CV_TIMES, test_size=TEST_SIZE) # 2/3 for train, 1/3 for test, do 3 times  
    #do crossover split
    train, test = crossover_split(training_set)
    
    #for n, (traincv, testcv) in enumerate(cv): #每個user都有3組cv的推文
        
        #train_list = [training_set[i] for i in traincv]
        #test_list = [training_set[i] for i in testcv]
        
        #list_user[n][uid] = train_list
        #list_user_ans[n][uid] = test_list
    user[uid] = train
    user_ans[uid] = test

import json

#temp_path = '/Users/joekaojoekao/PycharmProjects/push/github/temp/'
#sample_file = 'select_pushes101'
#temp_json = (list_user, list_user_ans)
temp_json = (user, user_ans)
with open(temp_path + os.path.splitext(sample_file)[0] + '_cvlist.txt', 'wb') as f_temp:
    f_temp.write(json.dumps(temp_json, indent=2, ensure_ascii=True).encode('utf-8'))
    f_temp.close()

print 'write push data ready to do cross_validation:', temp_path + os.path.splitext(sample_file)[0] + '_cvlist.txt'