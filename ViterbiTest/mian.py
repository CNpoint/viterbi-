'''
作者：施国峰
'''

import numpy as np

Text_path = r'./output/最终文档.txt'

tag2id,id2tag={},{}
word2id,id2word={},{}
with open(Text_path,'r',encoding='utf-8') as f:
    for line in f.readlines():
        items=line.split('/')
        items = str(items).replace('\\n','')
        items = eval(items)
        # print(items)
        try:
            word,tag=items[0],items[1].rstrip()#删除 string字符串末尾的指定字符(默认为空格)
            # print(word)
            if word not in word2id.keys():
                word2id[word]=len(word2id)
                id2word[len(id2word)]=word
            if tag not in tag2id.keys():
                tag2id[tag]=len(tag2id)
                id2tag[len(id2tag)]=tag
            # print(tag2id)

        except:
            pass

#发射矩阵，转移矩阵计算

word_number = len(word2id)
tag_number = len(tag2id)
# print(word_number)
A = np.zeros((tag_number, word_number))  # 发射矩阵
B = np.zeros((tag_number, tag_number))  # 状态转移矩阵
L = np.zeros(tag_number)  # 初始状态矩阵

pre_tag = ''
with open(Text_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        items = line.split('/')
        wordId, tagId = word2id[items[0]], tag2id[items[1].rstrip()]
        if pre_tag == '':  # 表示是在句首位置，此时统计发射矩阵和初始状态矩阵
            L[tagId] += 1
            A[tagId][wordId] += 1
        else:  # 表示在句中位置，此时统计发射矩阵和状态转移矩阵
            A[tagId][wordId] += 1
            B[tag2id[pre_tag]][tagId] += 1
        if items[0] == '。':  # 说明这个句子结束，到了下一个句子
            pre_tag = ''
        else:
            pre_tag = items[1].rstrip()
# 将矩阵中的值转换成概率
L /= sum(L)
for i in range(tag_number):
    A[i] /= sum(A[i])
    B[i] /= sum(B[i])
# print(A)


#viterbi 算法预测句子中词的词性

def log(v):
    if v==0: #为了避免np.log函数报错
        return np.log(0.00001)
    else:
        return np.log(v)

def viterbi(x,L,A,B):
    try:
        seq2id=[word2id[i] for i in x.split()]
        lay_number=len(seq2id)
        P=np.zeros((lay_number,tag_number))
        D=np.zeros((lay_number,tag_number))
        for i in range(tag_number):
            P[0][i]=log(L[i])+log(A[i][seq2id[0]])
            D[0][i]=-1
        for layer in range(1,lay_number,1):
            for i in range(tag_number): #当前节点
                probilities = []
                for j in range(tag_number):#前一个节点
                    probilities.append(P[layer-1][j]+log(B[j][i])+log(A[i][seq2id[layer]]))
                P[layer][i] = np.max(probilities)
                D[layer][i] = np.argmax(probilities)
        best_seq=[0]*lay_number
        best_seq[lay_number-1]=np.argmax(P[lay_number-1])
        #反推出最优路径
        for layer in range(lay_number-2,-1,-1):
            best_seq[layer]=int(D[layer+1][int(best_seq[layer+1])])
        #求出最终的词性标注结果
        best_seq=[id2tag[best_seq[i]] for i in range(len(best_seq))]
        return best_seq
    except:
        print("查无此词")

if __name__ == '__main__':
    # 举例

    x = '全体 教师 都 很 优秀 。'
    # x = '我 走进 新 中国 。'
    print("处理句子为：",x)
    print("标注结果为:",viterbi(x,L,A,B))
