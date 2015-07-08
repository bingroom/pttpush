# -*- coding: utf-8 -*-

##input: training word freq count
##output: cw list
def CW(dict_train_count):    

    from collections import Counter
    count_all = Counter()
    for v in dict_train_count.values():
        count_all += Counter(v)

    from collections import OrderedDict
    tlist = OrderedDict(sorted(dict(count_all).items(), key=lambda t: t[1], reverse=True))
    #sorted_tuple_list_train_count
    ##gen sw (but only from training data)
    word = tlist.keys()
    #print dict(sorted_tuple_list_train_count)
    W_PERCENT = 0.025 #0.025
    ## setting for stopword & rareword percentage
    content_words = [x for x in word if tlist[x] >= tlist[word[int(len(word) * W_PERCENT)]]]
    #rarewords = [x for x in word if tlist[x] <= tlist[word[int(len(word) * (1-W_PERCENT))]]] #0.975

    ## stop word list
    cw_list = [x for x in content_words] 
    ## rare word list
    #rw_list = [x for x in rarewords] 
    print 'total word', len(word)
    print 'stop word', len(cw_list)
    #print 'rare word', len(rw_list)


    cw_count_dict = {}
    for w in cw_list:
        cw_count_dict.setdefault(len(w),[]).append(w)


    j = {}
    K_NUMWORD = 3 #6
    selected_cw = []
    for k in cw_count_dict.keys()[0:K_NUMWORD]:
        print 'num_word:',k,'\t',len(cw_count_dict[k])
        #j[k] = cw_count_dict[k]
        #print json.dumps(j)
        selected_cw += cw_count_dict[k]
    print len(selected_cw)
    
    return selected_cw


##input: training word freq count
##output: aw list
def AW(dict_train_count): #content word

    from collections import Counter
    count_all = Counter()
    for v in dict_train_count.values():
        count_all += Counter(v)

    from collections import OrderedDict
    tlist = OrderedDict(sorted(dict(count_all).items(), key=lambda t: t[1], reverse=True))
    #sorted_tuple_list_train_count
    ##gen sw (but only from training data)
    word = tlist.keys()
    #print dict(sorted_tuple_list_train_count)
    W_PERCENT = 0.025 #0.025
    ## setting for stopword & rareword percentage
    author_words = [x for x in word if tlist[x] <= tlist[word[int(len(word) * (1-W_PERCENT))]]] #0.975

    ## stop word list
    aw_list = [x for x in author_words] 
    ## rare word list
    #rw_list = [x for x in rarewords] 
    print 'total word', len(word)
    print 'rare word', len(aw_list)
    #print 'rare word', len(rw_list)


    aw_count_dict = {}
    for w in aw_list:
        aw_count_dict.setdefault(len(w),[]).append(w)


    j = {}
    K_NUMWORD = 6 #6
    selected_aw = []
    for k in aw_count_dict.keys()[0:K_NUMWORD]:
        print 'num_word:',k,'\t',len(aw_count_dict[k])
        #j[k] = aw_count_dict[k]
        #print json.dumps(j[1])
        selected_aw += aw_count_dict[k]
    print len(selected_aw)
    
    return selected_aw


def cut_sentence(push): ##放入原始文章路徑, 增加斷詞的list
    #text = codecs.open(text_path,"r","utf-8")   #開檔
    PUNCTUATION_TABLE = [
    # start,  stop
    (0x2000, 0x206f),  # General Punctuation
    (0x3000, 0x303f),  # CJK Symbols and Punctuation
    (0xff00, 0xffef),  # Halfwidth and Fullwidth Forms
    (0x00, 0x2f),  # ascii special charactors
    # (0x30, 0x39), # number 0~9
    (0x3a, 0x40),  # ascii special charactors
    (0x5b, 0x60),  # ascii special charactors
    (0x7b, 0xff),  # ascii special charactors
    ]
    PUNCTUATION_RANGE = reduce(lambda x, y: x.union(y), [
                           range(start, stop + 1) for start, stop in PUNCTUATION_TABLE], set())

    push = push.decode('utf-8')
    sent = u""
    #punt_list = ',.!?:;~，。！？：；～'.decode('utf-8')
    #cut_list = "[。，,！……!《》<>\"':：？/?、/|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r ".decode('utf-8')
    import zhon.hanzi # external lib for chinese punc 
    sep_list = "。，,！……!\:：？/?、/|；：？！。，;、~——+％%`:“”＂'‘\n\r ".decode('utf-8')
    #sep_list = list(set(punt_list + cut_list)) #customized punc list
    sent_list = []
       
    for word in push:
        #if ord(word) not in PUNCTUATION_RANGE: #如果文字不是標點符號，就把字加到句子中
            #sent += word
            #print sentence
        #use re.sub |
        if word not in sep_list and word not in zhon.hanzi.punctuation:
            sent += word
        #if word not in zhon.hanzi.punctuation: #中文切法
            #sent += word
        #if ord(word) not in PUNCTUATION_RANGE:
            #sent += word
        else:
            sentence = sent.strip()
            if len(sentence) != 0:
                sent_list.append(sentence) #如果遇到標點符號，把句子加到 text list中
            sent = ""
            #print textList
    sentence = sent.strip()
    sent_list.append(sentence)
    return sent_list#傳回一個文字陣列

def SL(dict_train): #分單push(句內sl) and 全push(文字push)
    """for each push, return the encoding string with 1. line length and 2. list of sentence length"""
    #dict_train
    #print dict_train.values()[0]
    user_sl = {}
    for uid in dict_train.keys():
        user_push = zip(*dict_train[uid])[0]
        
        #print uid
        push_dict = {} #the sentence length info for every push
        for p in user_push:
            #print p.encode('utf-8'), len(p),'@'
            #for c in pttfeat.cut_sentence(p.encode('utf-8')):
                #print c.encode('utf-8'), len(c)
            cut_len = [len(x) for x in cut_sentence(p.encode('utf-8'))]
            #print cut_len, np.mean(cut_len)
            push_dict['full'] = len(p)
            push_dict['cut'] = cut_len
            #print '--'
        if uid not in user_sl:
            user_sl[uid] = [push_dict]
        else:
            user_sl[uid].append(push_dict)
    return user_sl