# -*- coding:utf-8 -*-
import jieba
#from rake_nltk import Rake
from jieba import posseg
from jieba import analyse
textrank = analyse.textrank
tfidf = analyse.extract_tags
#textrankE = Rake()


# 判断是否有中文
def is_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

# 输入为字符串
# 输出名词性分词列表
def wordsplit(str):
    words = posseg.cut(str)
    anslist = []
    for word in words:
        # print('word:', word.word, 'flag', word.flag)
        # 过滤其中名词性分词
        # if word.flag in ['n', 'ns', 'nz', 'nt', 'ng', 'un']:
        anslist.append(word.word)
    return anslist


# 只对研究点分析进行处理并提取名词
# 直接输入数据库中的字符串,返回统计字典
def deal_srchp(textsource):
    all_list = []
    textlist = eval(textsource)
    textlist = sum(textlist, [])
    for t1 in textlist:
        # 判断是否有中文
        if is_contain_chinese(t1):
            words = posseg.cut(t1)
            for word in words:
                if word.flag in ['n' ,'ns' ,'nz' ,'nt', 'ng', 'un'] and word.word!=t1:
                    all_list.append(word.word)
        all_list.append(t1)
    dict_cnt = {}
    for item in all_list:
        if item in dict_cnt:
            dict_cnt[item]+=1
        else:
            dict_cnt[item]=1
    return dict_cnt



# 直接输入数据库中的字符串,返回统计字典
# 加入对论文题目的关键词抽取
def deal_srchp2(titlesource, textsource):
    all_list = []
    try:
        titlesource = eval(titlesource)
        textlist = sum(eval(textsource), [])
    except:
        titlesource = []
        textlist = []

    # 对论文题目进行关键词抽取
    for t1 in titlesource:
        # 判断是否有中文
        if is_contain_chinese(t1):
            keywords = textrank(t1, allowPOS=('n', 'ns', 'nz', 'nt', 'ng', 'un'))
        # 如果是英文则采用nltk进行关键词抽取：效果不好
        else:
            keywords = []
            pass

        all_list.extend(keywords)

    # 对研究点列表进行词性提取
    for t1 in textlist:
        # 判断是否有中文
        if is_contain_chinese(t1):
            words = posseg.cut(t1)
            for word in words:
                if word.flag in ['n', 'ns', 'nz', 'nt', 'ng', 'un'] and word.word != t1:
                    all_list.append(word.word)
        all_list.append(t1)

    # 生成统计字典
    dict_cnt = {}
    for item in all_list:
        if item in dict_cnt:
            dict_cnt[item] += 1
        else:
            dict_cnt[item] = 1
    return  dict_cnt

if __name__ == '__main__':
    print(deal_srchp2(input('请输出需要统计的标题'), input('请输出需要统计的研究点')))
    # print(wordsplit(input('请输入需要拆分的字符')))

    # 待实现：如何提取英文名词词组？

    # while 1:
    #     str0 = input('输入：')
    #     print(wordsplit(str0))


    # titlesource1 = "['宗教与国际热点问题——宗教因素对冷战后国际热点问题和重大冲突的深层影响', '“基督教中国化”三思', '“四种取代宗教说”反思', '论克罗齐和柯林武德的历史观念', '当代中国宗教关系研究刍议——基于国内外研讨现状的理论与政策探讨', '文化寻根的一种哲学尝试——卡西尔神话与语言研究述评', '“中国无宗教论”反思', '共建和谐世界的中国文化资源——我国前辈学者探索成果评述', '在宗教与文化的交汇点上', '再论宗教-文化观的方法论意义']"
    # textsource1 = "[[], ['Pipeline processing', 'Algorithm design and analysis', 'multiple filtering', 'Educational institutions', 'Similarity join'], ['knowledge bases', 'entity search', 'SPARQL query'], ['Query Evaluation', 'Data Partitioning'], ['Query Evaluation', 'Data Partitioning'], ['capacity constraint', 'location selection', 'spatial database'], ['capacity constraint', 'location selection', 'spatial database'], ['Big data', 'Interactive query'], ['Big data', 'Interactive query'], ['Keyword Search']]"
    # textsource2 = "[['Spectral Clustering', 'Constraint Propagation'], ['pattern clustering', 'spatial mismatch', 'image representation', 'image sequences', 'image matching', 'image classification'], ['Spectral Clustering', 'Constraint Propagation'], ['pattern clustering', 'spatial mismatch', 'image representation', 'image sequences', 'image matching', 'image classification'], ['pattern clustering', 'graph theory', 'image representation'], ['Ensemble learning', 'Probabilistic latent semantic analysis', 'Rival penalized competitive learning'], ['constraint propagation', 'image clustering'], ['visual keywords', 'automatic image annotation', 'image annotation', 'kernel methods'], ['Gaussian mixture', 'Regularization theory', 'iterative algorithm', 'Model selection', 'automatic model selection'], ['minimum cross-entropy', 'curve detection', 'Time series prediction', 'Regularization theory', 'Model selection']]"
    # textsource3 = "[['渗透性', '弥漫性', '宗教因素', '热点问题', '冷战后'], ['社会实践', '中国化', '基督教'], ['宗教说'], ['历史学家', '历史过程', '柯林武德', '克罗齐', '历史思想', '历史观念'], ['当代中国', '关系研究'], ['卡西尔', '语言概念', '语言研究', '西方近代哲学', '哲学观念', '哲学体系'], ['梁启超', '利玛窦'], ['宗教对话', '中国文化', '和谐世界'], ['宗教文化', '卡西尔', '非理性主义', '汤因比', '文化结构', '文化观念'], ['文化观', '方法论意义']]"
    # titles = input('请输入标题列表字符串：')
    # texts = input('请输入研究点列表字符串')
    # #
    # '''
    # print("hello")
    #
    # r = Rake()
    # # tes1
    # text2= "['Microwave Absorption Enhancement and Complex Permittivity and Permeability of Fe Encapsulated within Carbon Nanotubes', 'CdS quantum dots sensitized TiO2 nanotube-array photoelectrodes', 'Preparation and structure analysis of titanium oxide nanotubes', 'Trititanate Nanotubes Made via a Single Alkali Treatment.', 'Repeated growth and bubbling transfer of graphene with millimetre-size single-crystal grains using platinum', 'Deriving Carbon Atomic Chains from Graphene', 'Formation Mechanism of H2Ti3O7 Nanotubes', 'The structure of trititanate nanotubes ', 'Quantitative Analysis of Current-Voltage Characteristics of Semiconducting Nanowires: Decoupling of Contact Effects', 'Stability of Carbon Nanotubes: How Small Can They Be?']"
    # text2 = ' '.join(eval(text2))
    # my_test = 'My father was a self-taught mandolin player. He was one of the best string instrument players in our town. He could not read music, but if he heard a tune a few times, he could play it. When he was younger, he was a member of a small country music band. They would play at local dances and on a few occasions would play for the local radio station. He often told us how he had auditioned and earned a position in a band that featured Patsy Cline as their lead singer. He told the family that after he was hired he never went back. Dad was a very religious man. He stated that there was a lot of drinking and cursing the day of his audition and he did not want to be around that type of environment.'
    # test1= 'Microwave Absorption Enhancement and Complex Permittivity and Permeability of Fe Encapsulated within Carbon Nanotubes'
    # r.extract_keywords_from_text(text2)
    # print(r.get_ranked_phrases())
    # print("==============================")
    # print(r.get_ranked_phrases_with_scores())
    # print("===========================")
    # # print(r.stopwords)
    # print("=============================")
    # # print(r.get_word_degrees())
    # '''
    #
    # # print('拆分统计字典_只用研究点列表', sorted(deal_srchp(textsource3).items(), key=lambda x: x[1], reverse=True)[:30])
    # # print()
    # print('拆分统计字典，使用研究点列表和论文题目关键词抽取',
    #       sorted(deal_srchp2(titles, texts).items(), key=lambda x: x[1], reverse=True)[:30])

'''
text = "[['循环经济', '系统协调', '可持续发展', '城市可持续发展'], ['系统动力学', '可持续发展', '复杂系统'], ['市场失效', '外部性', '解决方法', '交通拥堵'], ['燃油经济性', '政策措施', '政策体系', '新能源汽车', '燃油消耗量', '燃油消耗'], ['利益相关者分析', '燃油经济性', '经济研究', '影响评价'], ['企业管理人员', '影响因素分析', '问卷调查', '气候变化'], ['企业管理人员', '行为意愿', '统计分析', '气候变化'], ['出口退税率', '钢铁行业'], ['环境经济学', '经济学分析', '外部性', '自然环境', '信息技术产品'], ['合作博弈', '治理研究', '线性优化', '京津冀']]"
textlist = eval(text)
print(type(textlist))
# 降维列表
textlist2 = sum(textlist, [])
# print(textlist2)

for item in textlist2:
    print(' ')
    print(item)
    # 分词并存入列表
    res1 = jieba.lcut(item)
    print('分词', res1)
    # 词性提取
    res2 = posseg.lcut(item)
    print('词性提取', res2)
    res2n = []
    for res2one in posseg.cut(item):
        if res2one.flag in ['n' ,'ns' ,'nz' ,'nt', 'ng', 'un']:
            res2n.append(res2one.word)
    print('其中名词为：', res2n)
    # 基于tfidf算法的关键词抽取
    keywords = tfidf(item)
    print('tfid关键词抽取', keywords)
    keywords2 = textrank(item)
    print('textrank关键词抽取', keywords2)
    '''

# title = '宗教与国际热点问题——宗教因素对冷战后国际热点问题和重大冲突的深层影响'
# keywords2_1 = textrank(title)
# keywords2_2 = textrank(title, allowPOS=('n' ,'ns' ,'nz' ,'nt', 'ng', 'un'))
# print('title 关键词抽取', keywords2_1)
# print('title 关键词抽取 过滤', keywords2_2)



# 根据字典值排序
# dic1SortList = sorted( dic1.items(),key = lambda x:x[1],reverse = True)






