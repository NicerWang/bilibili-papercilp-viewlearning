import random
import numpy as np
import jieba
import csv
from scipy.stats import norm
import math
import matplotlib.pyplot as plt

# 所有需要的全局模型变量
stopwords = []
comments = []
test_set = []

pos_cnt = 0
neg_cnt = 0
pos_words = 0
neg_words = 0

pos_rate = 0
neg_rate = 0

pos_dict = {}
neg_dict = {}

pos_len = []
neg_len = []
pos_len_mean = 0
neg_len_mean = 0
pos_len_std = 0
neg_len_std = 0


def initialize():
    # 加载词典
    jieba.load_userdict("dict.txt")
    # 加载停用词
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                stopwords.append(line.strip("\n"))
    # 导入评论内容
    in_file = open("comments.csv", "r", encoding="utf-8")
    csv_reader = csv.reader(in_file, dialect="excel")
    for comment in csv_reader:
        if len(comment) == 0:
            continue
        comments.append(comment)
    # 处理评论内容
    for comment in comments:
        keys = jieba.cut(comment[0].upper(), cut_all=True)
        length = len(comment[0])
        comment[0] = []
        for j in keys:
            if j in stopwords or len(j) == 0 or j == " ":
                continue
            comment[0].append(j)
        comment.append(length)


def train(test_mode: bool = False):
    global pos_cnt, pos_words, neg_words, neg_cnt, pos_rate, neg_rate, pos_len_mean, pos_len_std, neg_len_mean, neg_len_std, test_set, pos_dict, neg_dict, pos_len, neg_len
    pos_len = []
    neg_len = []
    pos_dict = {}
    neg_dict = {}
    pos_cnt = 0
    neg_cnt = 0
    pos_words = 0
    neg_words = 0

    if test_mode:
        random.shuffle(comments)
        test_set = comments[0:50]
        train_set = comments[50:]
    else:
        train_set = comments

    for comment in train_set:
        if len(comment[0]) < 2:
            continue
        if comment[1] == "1":
            pos_cnt = pos_cnt + 1
            pos_len.append(comment[2])
            for word in comment[0]:
                pos_words = pos_words + 1
                if word not in pos_dict.keys():
                    pos_dict[word] = 1
                else:
                    pos_dict[word] = pos_dict[word] + 1
        else:
            neg_cnt = neg_cnt + 1
            neg_len.append(comment[2])
            for word in comment[0]:
                neg_words = neg_words + 1
                if word not in neg_dict.keys():
                    neg_dict[word] = 1
                else:
                    neg_dict[word] = neg_dict[word] + 1
    pos_rate = pos_cnt / (pos_cnt + neg_cnt)
    neg_rate = neg_cnt / (pos_cnt + neg_cnt)
    pos_len_mean = np.mean(pos_len)
    neg_len_mean = np.mean(neg_len)
    pos_len_std = np.std(pos_len, ddof=1)
    neg_len_std = np.std(neg_len, ddof=1)

    if test_mode:
        return test(test_set)

def bayes(content, length):
    test_pos = test_neg = 0
    theta_pos = norm.cdf(length + 2, pos_len_mean, pos_len_std) - norm.cdf(length - 2, pos_len_mean, pos_len_std)
    theta_neg = norm.cdf(length + 2, neg_len_mean, neg_len_std) - norm.cdf(length - 2, neg_len_mean, neg_len_std)
    if theta_pos != 0 and theta_neg != 0:
        test_pos = 3 * math.log(theta_pos)
        test_neg = 3 * math.log(theta_neg)

    if len(content) < 1:
        return None

    for word in content:
        if word not in pos_dict:
            test_pos = test_pos + math.log(1 / pos_words)
        else:
            test_pos = test_pos + math.log((pos_dict[word] + 1) / pos_words)
        if word not in neg_dict:
            test_neg = test_neg + math.log(1 / neg_words)
        else:
            test_neg = test_neg + math.log((neg_dict[word] + 1) / neg_words)
    isPostive = None
    if test_pos >= test_neg:
        isPostive = True
    else:
        isPostive = False
    return isPostive

def test(test_set):
    error_cnt = 0
    test_cnt = 0
    for comment in test_set:
        isPositive = bayes(comment[0],comment[2])
        if isPositive is None:
            continue
        test_cnt = test_cnt + 1
        if comment[1] == "1":
            if isPositive is not True:
                error_cnt = error_cnt + 1
        else:
            if isPositive:
                error_cnt = error_cnt + 1
    return 1 - error_cnt / test_cnt

def judge(new_comment):
    keys = []
    l = len(new_comment)
    for j in jieba.cut(new_comment.upper(), cut_all=False):
        if j in stopwords or len(j) == 0 or j == " ":
            continue
        keys.append(j)
    isPostive = bayes(keys, l)
    return isPostive



def predict():
    new_comments = []
    in_file = open("comments_predict.csv", "r", encoding="utf-8")
    csv_reader = csv.reader(in_file, dialect="excel")
    predict_dict_pos = {}
    predict_dict_neg = {}
    for comment in csv_reader:
        if len(comment) == 0:
            continue
        predict_dict_pos[comment[0]] = 0
        predict_dict_neg[comment[0]] = 0
        new_comments.append(comment)
    for new_comment in new_comments:
        if judge(new_comment[1]) is True:
            predict_dict_pos[new_comment[0]] = predict_dict_pos[new_comment[0]] + 1
        else:
            predict_dict_neg[new_comment[0]] = predict_dict_neg[new_comment[0]] + 1
    return predict_dict_pos,predict_dict_neg


if __name__ == "__main__":
    initialize()
    # rate = 0
    # n = 500
    # for i in range(n):
    #     rate = rate + train(True)
    # print(str(n) + "次测试平均正确率为：")
    # print(rate / n)

    train()
    pos,neg = predict()
    time = []
    result = []
    for i in pos.keys():
        print(i)
        pi = pos[i]
        ni = neg[i]
        print(pi / (pi + ni))
        print(ni / (pi + ni))
        time.append(i[3:])
        result.append(pi)
    plt.plot(time,result,color="red",marker="o")
    plt.title("Changing Views towards Paperclip by Bayes")
    plt.xlabel("time(y-m-d)")
    plt.ylabel("Percentage of Attacking(%)")
    plt.ylim(0,100)
    plt.show()

