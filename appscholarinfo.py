from flask import Flask, redirect, session, render_template, request, Blueprint
import pymysql
import requests
import json
from collections import Counter
import wordsExtra_zsf
from appScholar_Compare import compare
import simRecommend_zsf
import nameTest_zsf
#创建Blueprint对象以便在appall中注册
app = Blueprint("appscholarinfo",__name__)


#个人详细页面的路由--余晓
@app.route('/scholarinfo')
def scholarinfo():
    #获取要点击查询的学者学校，姓名和专业以便确定学者
    school = request.args.get('school')
    name = request.args.get('name')
    major = request.args.get('major')
    scholarid = request.args.get('scholarid')
    print('scholarid:', scholarid)
    # 如果没有scholarid，就用姓名-学校-学院的方式查找
    if not scholarid:
        #创建数据库连接
        connection = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                                     charset="utf8")
        cursor = connection.cursor()
        #在表中查询结果，用result保存
        sql = "select * from %s where id between 1 and 2500 and name='%s' and college='%s'" % (school, name, major)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()


    # 如果传入了scholarid，就用scholarid多表并联查询
    else:
        # 创建数据库连接
        conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                               charset="utf8")
        cls = conn.cursor()
        sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
        cls.execute(sql1)
        conn.commit()
        results = cls.fetchall()
        SQL = ""
        for i in results:
            sql = "select * from %s where id between 1 and 2500 and scholarid='%s' " % (i[0], scholarid)
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
        # 在表中查询结果，用result保存
        cls.execute(SQL + ';')
        conn.commit()
        result = cls.fetchone()
        # print('result:', result)
        # 如果有scholarid却没有搜索到result，说明数据库中无此学者，直接跳转到搜索页
        if not result:
            # session['oldpath'] = request.path  # 保存当前路由
            return redirect("/Search_result?keyword=%s&type=%s" % (scholarid, str(5)))

    #对查询的结果每一个字段进行分割并处理传到前端页面
    scholarname = result[1]  #姓名
    scholarschool =result[2]  # 学校
    scholarmajor = result[3]  #专业
    scholarid = result[4]  #id
    cited_num = result[6]  #引用量
    achievement_num = result[7]  #成果数
    Hpoint = result[8]  #H指数
    Gpoint = result[9]   #G指数
    #str ="{'其他': '62', '专著': '43', '其他会议数': '195', '北大核心期刊': '6', 'CSCD期刊数': '5', '中国科技核心': '10', 'SCI期刊数': '16', 'EI期刊数': '29', 'SCIE期刊数': '25', 'SSCI期刊数': '1', '其他期刊数': '113'}"
    #对要使用eval函数的标签进行try并跑出异常操作
    try:
        scholarfield = eval(result[5])  #研究领域
    except:
        scholarfield = []
    try:
        achievement_list = eval(result[10])  #成果列表
    except:
        achievement_list = []
    try:
        achievement_list2 = eval(result[11])  #按照年份的成果数量字典
    except:
        achievement_list2 = []
    try:
        cited_list = eval(result[12])  #引用量
    except:
        cited_list = []
    try:
        partner_list = eval(result[13])  #合租学者
    except:
        partner_list = []
    try:
        paper_name_list = eval(result[14])  #论文名
    except:
        paper_name_list = []
    try:
        paper_info_list = eval(result[15])  #论文信息
    except:
        paper_info_list = []
    try:
        paper_search_list = eval(result[16])  #论文关键词
    except:
        paper_search_list = []
    try:
        collaborate_org = eval(result[17])  #合作机构
    except:
        collaborate_org = []
    #学科映射_申林
    subject=[]
    file2 = open("subjectname.txt", "r", encoding='utf-8')
    text2 = file2.readlines()
    wordsplitscholarfield=[]
    for fieldone in scholarfield:
        wordsplitscholarfield.append(wordsExtra_zsf.wordsplit(fieldone))
        print(fieldone)
        if "计算" in fieldone or "算法" in fieldone or "理论" in fieldone or "数据" in fieldone or "信息" in fieldone or "软件" in fieldone or "智能" in fieldone:
            wordsplitscholarfield.append(['计算'])
    # print(wordsplitscholarfield)
    for line in text2:
        for i in wordsplitscholarfield:
            for j in i:
                if j in line.strip().split(":")[0] and len(j)>1:
                    subjectone=[line.strip().split(":")[0].split('（')[0],line.strip().split(":")[1].split(" ")[0],line.strip().split(":")[1].split(" ")[1],line.strip().split(":")[1].split(" ")[2],line.strip().split(":")[1].split(" ")[3],line.strip().split(":")[1].split(" ")[4]]
                    if subjectone not in subject:
                        subject.append(subjectone)

    paper_search_all=[]
    for i in range(len(paper_search_list)):
        for j in range(len(paper_search_list[i])):
            paper_search_all.append(paper_search_list[i][j])
    paper_search_list = Counter(paper_search_all)
    paper_search_key=[]
    paper_search_num=[]
    # 调用方哥的单词抽取函数
    # 传入参数为数据库中原始字符串，返回值为抽取的单词字典
    try:
        # result[14], result[16]分别对应数据库中paper_name_list、paper_name_list字段
        dict_word = wordsExtra_zsf.deal_srchp2(result[14], result[16])
        paper_search_key1 = list(dict_word.keys())
        paper_search_num1 = list(dict_word.values())
    except:
        dict_word={}
        paper_search_key1 = list(dict_word.keys())
        paper_search_num1 = list(dict_word.values())

    # paper_search_key: 词云图的文本
    # paper_search_num：词云图的文本频率，用来控制词的大小
    if len(paper_search_key1)>30:
        paper_search_key = paper_search_key1[:30]
        paper_search_num = paper_search_num1[:30]
    else:
        paper_search_key = paper_search_key1
        paper_search_num = paper_search_num1


    # 关系网络图部分
    # 中心学者结点
    rela_center_data = {
        "name": scholarname,
        # 中心学者的这个值没有实际意义，但必须要有，可以给每个中心点设一固定值
        "corpnum": 100,
        # 所在机构
        "in": scholarschool,
    }
    # 合作学者结点
    rela_partner_data = []
    for i in partner_list:
        # 检测防止合作列表中有学者本人
        if i['name'] == scholarname:
            continue
        else:
            if 'corpnum' not in i.keys():
                i['corpnum'] = 1
            rela_partner_data.append(i)
    #删除掉查询不到的论文
    del_i=[]
    for i in range(len(paper_name_list)):
        if '层次分析法' in paper_name_list[i]:
            del_i.append(i)
    #倒序删除，避免影响前面顺序
    del_i.reverse()
    for i in del_i:
        paper_name_list.pop(i)
        paper_info_list.pop(i)

    #合作学者的对比
    #同时加入本人的信息
    selfinfo={
        "name":scholarname,
        "in":scholarschool,
        "id":scholarid,
    }
    partner_list2=partner_list
    partner_list2.append(selfinfo)

    # 关系网络升级版-只传名字
    # 同一学校的合作学者
    same_school_partner=[]
    for i in rela_partner_data:
        if scholarschool in i["in"]:
            same_school_partner.append(i["name"])
    # 同一paper的合作学者
    same_paper_partner=[]
    same_paper_partner2=nameTest_zsf.corpbypaper(scholarname,scholarschool)
    # 检测防止合作列表中有学者本人
    for i in same_paper_partner2:
        if i==scholarname:
            continue
        else:
            same_paper_partner.append(i)

    #统计点击次数在首页推荐
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="search_count", user="root", password="12345678",
                                 charset="utf8")
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO `search_count`.`search_count`(`name`, `school`, `college`, `scholarid`, `searchcount`) VALUES ('%s', '%s', '%s', '%s', 1)" % (name, school, major,scholarid)
        cursor.execute(sql)
        connection.commit()
    except:
        sql = "update `search_count`.`search_count` set searchcount=searchcount+1 where scholarid = '%s';"%(scholarid)
        cursor.execute(sql)
        connection.commit()

    recommend_list = simRecommend_zsf.scholar_Recommend(scholarid, 0)

    return render_template("scholarinfo.html",scholarname=scholarname,scholarschool=scholarschool,scholarmajor=scholarmajor
                           ,scholarid=scholarid,scholarfield=scholarfield,cited_num=cited_num,achievement_num=achievement_num,
                           Hpoint=Hpoint,Gpoint=Gpoint,achievement_list=achievement_list,achievement_list2=achievement_list2
                           ,cited_list=cited_list,partner_list=partner_list,paper_name_list=paper_name_list,paper_info_list=paper_info_list,paperlen=len(paper_info_list),
                           paper_search_key=paper_search_key,paper_search_num=paper_search_num,collaborate_org=collaborate_org,rela_center=rela_center_data,rela_partner=rela_partner_data,subject=subject,
                           partner_list2=partner_list2,same_school_partner=same_school_partner,same_paper_partner=same_paper_partner)


#个人详细页面的路由--翟胜方--通过合作学者直接跳转  后面并入晓哥的路由1
# @app.route('/scholarinfo2')
# def scholarinfo2():
#     #获取要点击查询的学者ID以便确定学者
#     scholarid = request.args.get('scholarid');
#     #创建数据库连接
#     conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
#                                  charset="utf8")
#     cls = conn.cursor()
#     sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
#     cls.execute(sql1)
#     conn.commit()
#     results = cls.fetchall()
#     SQL = ""
#     for i in results:
#         sql = "select * from %s where scholarid='%s' " % (i[0], scholarid)
#         if i != results[-1]:
#             sql += " UNION "
#         SQL += sql
#     # 在表中查询结果，用result保存
#     cls.execute(SQL + ';')
#     conn.commit()
#     result = cls.fetchone()
#     # print('并行查找 result:', result)
#
#     #对查询的结果每一个字段进行分割并处理传到前端页面
#     scholarname = result[1]  #姓名
#     scholarschool =result[2]  # 学校
#     scholarmajor = result[3]  #专业
#     scholarid = result[4]  #id
#     cited_num = result[6]  #引用量
#     achievement_num = result[7]  #成果数
#     Hpoint = result[8]  #H指数
#     Gpoint = result[9]   #G指数
#     #str ="{'其他': '62', '专著': '43', '其他会议数': '195', '北大核心期刊': '6', 'CSCD期刊数': '5', '中国科技核心': '10', 'SCI期刊数': '16', 'EI期刊数': '29', 'SCIE期刊数': '25', 'SSCI期刊数': '1', '其他期刊数': '113'}"
#     #对要使用eval函数的标签进行try并跑出异常操作
#     try:
#         scholarfield = eval(result[5])  #研究领域
#     except:
#         scholarfield = []
#     try:
#         achievement_list = eval(result[10])  #成果列表
#     except:
#         achievement_list = []
#     try:
#         achievement_list2 = eval(result[11])  #按照年份的成果数量字典
#     except:
#         achievement_list2 = []
#     try:
#         cited_list = eval(result[12])  #引用量
#     except:
#         cited_list = []
#     try:
#         partner_list = eval(result[13])  #合租学者
#     except:
#         partner_list = []
#     try:
#         paper_name_list = eval(result[14])  #论文名
#     except:
#         paper_name_list = []
#     try:
#         paper_info_list = eval(result[15])  #论文信息
#     except:
#         paper_info_list = []
#     try:
#         paper_search_list = eval(result[16])  #论文关键词
#     except:
#         paper_search_list = []
#     try:
#         collaborate_org = eval(result[17])  #合作机构
#     except:
#         collaborate_org = []
#     #学科映射_申林
#     subject=[]
#     file2 = open("subjectname.txt", "r", encoding='utf-8')
#     text2 = file2.readlines()
#     wordsplitscholarfield=[]
#     for fieldone in scholarfield:
#         wordsplitscholarfield.append(wordsExtra_zsf.wordsplit(fieldone))
#     for line in text2:
#         for i in wordsplitscholarfield:
#             for j in i:
#                 if j in line.strip().split(":")[0]:
#                     subjectone=[line.strip().split(":")[0].split('（')[0],line.strip().split(":")[1].split(" ")[0],line.strip().split(":")[1].split(" ")[1],line.strip().split(":")[1].split(" ")[2],line.strip().split(":")[1].split(" ")[3],line.strip().split(":")[1].split(" ")[4]]
#                     subject.append(subjectone)
#
#     paper_search_all=[]
#     for i in range(len(paper_search_list)):
#         for j in range(len(paper_search_list[i])):
#             paper_search_all.append(paper_search_list[i][j])
#     paper_search_list = Counter(paper_search_all)
#     paper_search_key=[]
#     paper_search_num=[]
#     # 调用方哥的单词抽取函数
#     # 传入参数为数据库中原始字符串，返回值为抽取的单词字典
#     try:
#         dict_word = wordsExtra_zsf.deal_srchp2(result[14], result[16])
#         paper_search_key1 = list(dict_word.keys())
#         paper_search_num1 = list(dict_word.values())
#     except:
#         dict_word={}
#
#     if len(paper_search_key1)>30:
#         paper_search_key = paper_search_key1[:30]
#         paper_search_num = paper_search_num1[:30]
#     else:
#         paper_search_key = paper_search_key1
#         paper_search_num = paper_search_num1
#
#
#     # 关系网络图部分
#     # 中心学者结点
#     rela_center_data = {
#         "name": scholarname,
#         # 中心学者的这个值没有实际意义，但必须要有，可以给每个中心点设一固定值
#         "corpnum": 100,
#         # 所在机构
#         "in": scholarschool,
#     }
#     # 合作学者结点
#     rela_partner_data = []
#     for i in partner_list:
#         # 检测防止合作列表中有学者本人
#         if i['name'] == scholarname:
#             continue
#         else:
#             if 'corpnum' not in i.keys():
#                 i['corpnum'] = 1
#             rela_partner_data.append(i)
#     #删除掉查询不到的论文
#     del_i=[]
#     for i in range(len(paper_name_list)):
#         if '层次分析法' in paper_name_list[i]:
#             del_i.append(i)
#     for i in del_i:
#         paper_name_list.pop(i)
#         paper_info_list.pop(i)
#
#     #合作学者的对比
#     #同时加入本人的信息
#     selfinfo={
#         "name":scholarname,
#         "in":scholarschool,
#         "id":scholarid,
#     }
#     partner_list2=partner_list
#     partner_list2.append(selfinfo)
#     compare_ans=compare(partner_list2,"",1)
#     # 'all_name': all_name,
#     # 'achivement_list': achivement_list,
#     # 'achivement_list2': achivement_list2,
#     # 'cited_list': cited_list,
#     # 'paper_search_list': paper_search_list,
#     # 'achive_minyear': achiveminiyear,
#     # 'achive_maxyear': achivemaxyear,
#     # 'cited_minyear': cited_minyear,
#     # 'cited_maxyear': cited_maxyear,
#     com_all_name=compare_ans['all_name']
#     com_achivement_list=compare_ans['achivement_list']
#     com_achivement_list2=compare_ans['achivement_list2']
#     com_cited_list=compare_ans['cited_list']
#     com_paper_search_list=compare_ans['paper_search_list']
#     com_achive_minyear=compare_ans['achive_minyear']
#     com_achive_maxyear=compare_ans['achive_maxyear']
#     com_cited_minyear=compare_ans['cited_minyear']
#     com_cited_maxyear=compare_ans['cited_maxyear']
#
#
#
#
#
#     return render_template("scholarinfo.html",scholarname=scholarname,scholarschool=scholarschool,scholarmajor=scholarmajor
#                            ,scholarid=scholarid,scholarfield=scholarfield,cited_num=cited_num,achievement_num=achievement_num,
#                            Hpoint=Hpoint,Gpoint=Gpoint,achievement_list=achievement_list,achievement_list2=achievement_list2
#                            ,cited_list=cited_list,partner_list=partner_list,paper_name_list=paper_name_list,paper_info_list=paper_info_list,paperlen=len(paper_info_list),
#                            paper_search_key=paper_search_key,paper_search_num=paper_search_num,collaborate_org=collaborate_org,rela_center=rela_center_data,rela_partner=rela_partner_data,subject=subject,
#                            com_all_name=com_all_name,com_achivement_list=com_achivement_list,com_achivement_list2=com_achivement_list2,com_cited_list=com_cited_list,
#                            com_paper_search_list=com_paper_search_list,com_achive_minyear=com_achive_minyear,com_achive_maxyear=com_achive_maxyear,
#                            com_cited_minyear=com_cited_minyear,com_cited_maxyear=com_cited_maxyear)
