import random
import numpy as np
import jieba
import csv
from scipy.stats import norm

jieba.load_userdict("dict.txt")
# 停用词
stopwords = []
with open("cn_stopwords.txt", "r", encoding="utf-8") as f:
    while True:
        line = f.readline()
        if not line:
            break
        else:
            stopwords.append(line.strip("\n"))
# 假定各个维度独立
comments = []
in_file = open("comments_new.csv", "r", encoding="utf-8")
csv_reader = csv.reader(in_file, dialect="excel")
for comment in csv_reader:
    if len(comment) == 0:
        continue
    comments.append(comment)


for comment in comments:
    keys = jieba.cut(comment[0].upper(), cut_all=True)
    length = len(comment[0])
    comment[0] = []
    for j in keys:
        if j in stopwords or len(j) == 0 or j == " ":
            continue
        comment[0].append(j)
    comment.append(length)

total_rate = 0
for i in range(0,1000):
    random.shuffle(comments)
    test_set = comments[0:100]
    pos_rate = 0
    neg_rate = 0
    pos_words = 0
    neg_words = 0
    pos_dict = {}
    neg_dict = {}
    rate_dict = {}
    train_set = comments[100:]
    total_pos = 0
    n = len(comments)

    length_pos = []
    length_neg = []
    for comment in train_set:
        if len(comment[0]) < 2:
            continue
        if comment[1] == "1":
            total_pos = total_pos + 1
            length_pos.append(comment[2])
            for word in comment[0]:
                pos_words = pos_words + 1
                if word not in pos_dict.keys():
                    pos_dict[word] = 1
                else:
                    pos_dict[word] = pos_dict[word] + 1
        else:
            length_neg.append(comment[2])
            for word in comment[0]:
                neg_words = neg_words + 1
                if word not in neg_dict.keys():
                    neg_dict[word] = 1
                else:
                    neg_dict[word] = neg_dict[word] + 1
    total_neg = n - total_pos
    pos_rate = total_pos / n
    neg_rate = total_neg / n
    pos_len_mean = np.mean(length_pos)
    neg_len_mean = np.mean(length_neg)
    pos_len_std = np.std(length_pos, ddof=1)
    neg_len_std = np.std(length_neg, ddof=1)

    ErrorCnt_test = 0
    testCnt = 0
    for comment in test_set:
        test_pos = (norm.cdf(comment[2] + 2, pos_len_mean, pos_len_std) - norm.cdf(comment[2] - 2, pos_len_mean,
                                                                                   pos_len_std)) ** 2
        test_neg = (norm.cdf(comment[2] + 2, neg_len_mean, neg_len_std) - norm.cdf(comment[2] - 2, neg_len_mean,
                                                                                   neg_len_std)) ** 2
        if len(comment[0]) == 0:
            continue

        for j in comment[0]:
            if j not in pos_dict:
                test_pos = test_pos * 1 / pos_words
            else:
                test_pos = test_pos * (pos_dict[j] + 1) / pos_words
            if j not in neg_dict:
                test_neg = test_neg * 1 / neg_words
            else:
                test_neg = test_neg * (neg_dict[j] + 1) / neg_words
        isPostive = True
        testCnt = testCnt + 1
        if test_pos <= test_neg * 1.5:
            isPostive = False
        else:
            isPostive = True
        if comment[1] == "1":
            if isPostive is not True:
                ErrorCnt_test = ErrorCnt_test + 1
        else:
            if isPostive:
                ErrorCnt_test = ErrorCnt_test + 1
    total_rate += 1 - ErrorCnt_test / testCnt

print(total_rate / 1000)


# for i in range(0,10):
#     s = input("输入评论")
#
#
#     keys = []
#     l = len(s)
#     for j in jieba.cut(s.upper(), cut_all=False):
#         if j in stopwords or len(j) == 0 or j == " " or checkAlpha(j):
#             continue
#         keys.append(j)
#
#     test_pos = (norm.cdf(l + 3, pos_len_mean, pos_len_std) - norm.cdf(l - 3, pos_len_mean,
#                                                                                  pos_len_std)) ** 2
#     test_neg = (norm.cdf(l + 3, neg_len_mean, neg_len_std) - norm.cdf(l - 3, neg_len_mean,
#                                                                                  neg_len_std)) ** 2
#     if l == 0:
#         continue
#
#     for j in keys:
#         if j not in pos_dict:
#             test_pos = test_pos * 1 / pos_words
#         else:
#             test_pos = test_pos * (pos_dict[j] + 1) / pos_words
#         if j not in neg_dict:
#             test_neg = test_neg * 1 / neg_words
#         else:
#             test_neg = test_neg * (neg_dict[j] + 1) / neg_words
#     isPostive = True
#     if test_pos <= test_neg:
#         isPostive = False
#     else:
#         isPostive = True
#     print(keys)
#     print(isPostive)