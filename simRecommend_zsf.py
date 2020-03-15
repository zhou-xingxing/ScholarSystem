# -*- coding: UTF-8 -*-
import re
import nltk
from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk.probability import FreqDist
# import pandas as pd
# import datetime
# import gensim
import pymysql
from gensim import corpora, models, similarities
# import logging
from collections import defaultdict
import json
import time
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 文本预处理：去停词、去符号（没有词干化）
# 输入为一句话的字符串，返回值为该句处理之后的词列表
def text_deal(s1):
    s1 = s1.lower()
    s1 = s1.strip()
    s1 = re.sub(r'\(.*?\)', '', s1)
    s1 = re.sub(r'[,;.:?\'"“”\[\]%]', '', s1)
    s1 = re.sub(r'[\-]', ' ', s1)
    words = nltk.word_tokenize(s1)
    without_stopwords = [word for word in words if word not in stopwords.words('english')]
    return without_stopwords


# 思路：将学者排名前10（或者10以内）论文名称组合为一个词语列表，对所有词语列表进行计算
# 根据一位学者的论文名称组合列表，输出除了自己之外最匹配的学者名字。
# 输入：str（学者scholarID），Nstart 从第几位顺位的学者开始往后数3位推荐
# 输出：str（前3个最匹配的学者[id,name,school]列表）
def scholar_Recommend(id_test='CN-B2746FCJ', Nstart=0):
    # 读入映射字典、tfidf词典、tfidf模型、tfidf索引
    file = open('corpusModel\dict_index2id.txt', 'r', encoding='utf8')
    js = file.read()
    dict_index2id = json.loads(js)
    file.close()

    dictionary = corpora.Dictionary.load('corpusModel\dic.txt')
    tfidf_m  = models.TfidfModel.load('corpusModel\\tfidf_m.txt')
    tfidf_index = similarities.MatrixSimilarity.load('corpusModel\\tfidf_index')

    # 先从字典中查找有无对应id，如果没有再从数据库中找
    if id_test in dict_index2id.values():
        # 根据值从字典取键
        index1 = int(list(dict_index2id.keys())[list(dict_index2id.values()).index(id_test)])
        # 如果索引中有对应ID，直接从索引中获取向量
        corpus = corpora.MmCorpus('corpusModel\corpus.txt')
        ans_list = tfidf_index[corpus[index1]]
        id_list = []
        # 除去本人，从Nstart数处开始推荐3位
        for ans in ans_list[1+Nstart:1 + Nstart+3]:
            id_list.append(dict_index2id[str(ans[0])])


    else:
        print('原字典中无此scholarID，去数据库中搜索...')
        conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                               charset="utf8")
        cls = conn.cursor()
        sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
        cls.execute(sql1)
        conn.commit()
        results = cls.fetchall()
        SQL = ''
        for i in results:
            sql = "select paper_search_list from %s where scholarid='%s' " % (i[0], id_test)
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
        # try:
        cls.execute(SQL + ';')
        conn.commit()
        result = cls.fetchall()
        try:
            text_test = str(result[0][0])  # 此处注意传入的数据格式！！！
        except :
            print('simRe报错：数据库中无此学者')
            return None
        # except:
        #     result = []
        #     length = 0
        #     print('search failed !')
        #     return 0

        # 对查询得到的研究点数据进行处理
        # 去中文
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        english = re.sub(pattern, '', text_test)
        # print('english', english)
        text_test = text_deal(english)
        # print('text_test', text_test)
        ans_list = tfidf_index[dictionary.doc2bow(text_test)]
        id_list = []
        # 除去本人，从Nstart数处开始推荐3位
        for ans in ans_list[1 + Nstart: 1 + Nstart+3]:
            id_list.append(dict_index2id[str(ans[0])])

    # 使用IDlist从数据库中寻找学者的姓名、学校信息
    return_list = []
    for id in id_list:
        # 从数据库中以ID来查询该学者的name、school
        conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                               charset="utf8")
        cls = conn.cursor()
        sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
        cls.execute(sql1)
        conn.commit()
        results = cls.fetchall()
        SQL = ''
        for i in results:
            sql = "select name,school,college,field from %s where scholarid='%s' " % (i[0], id)
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
        cls.execute(SQL + ';')
        conn.commit()
        results = cls.fetchall()
        # print('查询结果：', results)
        return_list.append([id, results[0][0], results[0][1], results[0][2], eval(results[0][3])])

    return return_list
    pass

# 模型更新函数，每运行一遍会更新模型并存入文件
# 通过TFIDF算法计算数据库中的所有数据，生成索引和映射字典并保存
def model_Cal():
    dict_index2id = {}
    start_time = time.time()  # 开始时间

    # 从数据库搜索所有研究点和学者id
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
    cls.execute(sql1)
    conn.commit()
    results = cls.fetchall()
    SQL = ''
    for i in results:
        sql = "select paper_search_list,scholarid from %s where paper_search_list != '' " %    i[0]
        if i != results[-1]:
            sql += " UNION "
        SQL+=sql
    try:
        cls.execute(SQL + ';')
        conn.commit()
        result = cls.fetchall()
        print('search end')
        length = len(result)
    except:
        result = []
        length=0
        print('search failed !')

    # 开始tfidf算法
    # 文本预处理
    # 将搜索的id赋给对应索引的字典
    texts = []
    for i in range(len(result)):
        dict_index2id[i] = result[i][1]  #
        # 去中文
        pattern = re.compile(r'[\u4e00-\u9fa5]')
        english = re.sub(pattern, '', result[i][0])
        texts.append(text_deal(english))

    js = json.dumps(dict_index2id)
    file = open('corpusModel\dict_index2id.txt', 'w', encoding='utf8')
    file.write(js)
    file.close()
    print('文本预处理、映射字典建立完毕')

    # 计算词频，去除频率为1的单词
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token]+=1
    texts = [[token for token in text if frequency[token] > 1] for text in texts]  # if frequency[token] > 1
    print('计算词频并筛选完毕')

    # 生成tfidf词典
    dictionary = corpora.Dictionary(texts)
    dictionary.save('corpusModel\dic.txt')
    # 建立语料库
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('corpusModel\corpus.txt', corpus)
    # 建立tfidf模型
    tfidf_m = models.TfidfModel(corpus)
    corpus_tfidf = tfidf_m[corpus]
    tfidf_m.save('corpusModel\\tfidf_m.txt')
    # 建立tfidf索引
    tfidf_index = similarities.Similarity(r'corpusModel\corpus_m', corpus_tfidf, len(dictionary))
    # 设置推荐个数
    tfidf_index.num_best = 31   # 设置30组备选推荐学者
    tfidf_index.save('corpusModel\\tfidf_index')
    print('模型建立完毕')
    print('总用时：', time.time()-start_time)


if __name__ == '__main__':
    # print(text_deal(input()))
    # print(scholar_Recommend(Nstart=0))
    model_Cal()  # 首次使用需要先运行本函数：计算模型并存储索引
    #id = input('请输入需要推荐的学者scholarID')
    #print('前3相似学者的信息为：', scholar_Recommend(id))   # 'CN-B2746FCJ'
    #pass