import pycrfsuite

def read_file(file_name):
    sents = []
    with open(file_name,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for idx,l in enumerate(lines) :
            if l[0]==';' and lines[idx+1][0]=='$':
                this_sent = []
            elif l[0]=='$' and lines[idx-1][0]==';':
                continue
            elif l[0]=='\n':
                sents.append(this_sent)
            else :
                this_sent.append(tuple(l.split()))
    return sents

def read_file_kor(file_name):
    pass

train_sents = read_file("../data/conll2002_esp.train")
test_sents = read_file("../data/conll2002_esp.test")

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        #자질 추출

    ]
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        # 자질 추출

    else:
        features.append('BOS')

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        # 자질 추출

    else:
        features.append('EOS')

    return features

def add_features_to_sent(sent):
    new_sent = sent
    return new_sent

def sent2features(sent):
    sent = add_features_to_sent(sent)
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]

#data에서 자질 추출
X_train = []
y_train = []

X_test = []
y_test = []

#중간 출력

#모델 학습

#모델 로드

def make_tag_idx(ans_seq):
    B_num = 0
    all_answer_start = []
    all_answer_end = []
    all_answer_tag = []

    for sent in ans_seq:
        start_idx = []
        end_idx = []
        tag_set = []
        tag_num = 0
        flag = 0

        for tag in sent:
            try:
                if flag == 1 and tag[0] != 'I':
                    end_idx.append(tag_num - 1)
                    flag = 0
            except:
                print()

            if tag[0] == 'B':
                B_num = B_num + 1
                start_idx.append(tag_num)
                tag_set.append(tag[2:4])
                flag = 1
            tag_num = tag_num + 1

        if flag == 1:
            end_idx.append(tag_num - 1)

        all_answer_start.append(start_idx)
        all_answer_end.append(end_idx)
        all_answer_tag.append(tag_set)

    return (all_answer_start, all_answer_end, all_answer_tag, B_num)


def eval(pred_seq, ans_seq):  # changed

    TP = 0

    (all_answer_start, all_answer_end, all_answer_tag, answer_num) = make_tag_idx(ans_seq)
    (all_pred_start, all_pred_end, all_pred_tag, pred_num) = make_tag_idx(pred_seq)

    for i in range(0, len(ans_seq)):
        for j in range(0, len(all_pred_start[i])):
            for k in range(0, len(all_answer_start[i])):
                if all_pred_start[i][j] == all_answer_start[i][k] and all_pred_end[i][j] == all_answer_end[i][k] and \
                                all_pred_tag[i][j] == all_answer_tag[i][k]: TP = TP + 1

    return (TP, pred_num, answer_num)

def write_prediction(file_name, sents, preds):
    with open(file_name,'w', encoding='utf-8') as f:
        for s, s_p in zip(sents,preds):
            f.write(";\n$\n")
            for t, p in zip(s,s_p) :
                cmp = '' if t[2]==p else '*'
                f.write(t[0]+' '+t[1]+' cor:'+t[2]+' pred:'+p+cmp+'\n')
            f.write('\n')
#모델 평가

#Precision, Recall, F1score