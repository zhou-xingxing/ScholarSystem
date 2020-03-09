from flask import Flask, render_template, request,Blueprint
import pymysql
import requests
import json
from collections import Counter
import wordsExtra_zsf
from appScholar_Compare import compare
import simRecommend_zsf
#创建Blueprint对象以便在appall中注册
app = Blueprint("appscholarinfo",__name__)

#个人详细页面的路由--余晓
@app.route('/scholarinfo')
def scholarinfo():
    #获取要点击查询的学者学校，姓名和专业以便确定学者
    school = request.args.get('school');
    name = request.args.get('name');
    major = request.args.get('major');
    #创建数据库连接
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                                 charset="utf8")
    cursor = connection.cursor()
    #在表中查询结果，用result保存
    sql = "select * from %s where name='%s' and college='%s'" % (school, name, major)
    cursor.execute(sql)
    result = cursor.fetchone()
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
    for line in text2:
        for i in wordsplitscholarfield:
            for j in i:
                if j in line.strip().split(":")[0]:
                    subjectone=[line.strip().split(":")[0].split('（')[0],line.strip().split(":")[1].split(" ")[0],line.strip().split(":")[1].split(" ")[1],line.strip().split(":")[1].split(" ")[2],line.strip().split(":")[1].split(" ")[3],line.strip().split(":")[1].split(" ")[4]]
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
        dict_word = wordsExtra_zsf.deal_srchp2(result[14], result[16])
        paper_search_key1 = list(dict_word.keys())
        paper_search_num1 = list(dict_word.values())
    except:
        dict_word={}

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
    compare_ans=compare(partner_list2,"",1)
    # 'all_name': all_name,
    # 'achivement_list': achivement_list,
    # 'achivement_list2': achivement_list2,
    # 'cited_list': cited_list,
    # 'paper_search_list': paper_search_list,
    # 'achive_minyear': achiveminiyear,
    # 'achive_maxyear': achivemaxyear,
    # 'cited_minyear': cited_minyear,
    # 'cited_maxyear': cited_maxyear,
    com_all_name=compare_ans['all_name']
    com_achivement_list=compare_ans['achivement_list']
    com_achivement_list2=compare_ans['achivement_list2']
    com_cited_list=compare_ans['cited_list']
    com_paper_search_list=compare_ans['paper_search_list']
    com_achive_minyear=compare_ans['achive_minyear']
    com_achive_maxyear=compare_ans['achive_maxyear']
    com_cited_minyear=compare_ans['cited_minyear']
    com_cited_maxyear=compare_ans['cited_maxyear']

    id_rescholar = scholarid
    Nstart = 0
    recommend_list = simRecommend_zsf.scholar_Recommend(id_rescholar, Nstart)

    return render_template("scholarinfo.html",scholarname=scholarname,scholarschool=scholarschool,scholarmajor=scholarmajor
                           ,scholarid=scholarid,scholarfield=scholarfield,cited_num=cited_num,achievement_num=achievement_num,
                           Hpoint=Hpoint,Gpoint=Gpoint,achievement_list=achievement_list,achievement_list2=achievement_list2
                           ,cited_list=cited_list,partner_list=partner_list,paper_name_list=paper_name_list,paper_info_list=paper_info_list,paperlen=len(paper_info_list),
                           paper_search_key=paper_search_key,paper_search_num=paper_search_num,collaborate_org=collaborate_org,rela_center=rela_center_data,rela_partner=rela_partner_data,subject=subject,
                           com_all_name=com_all_name,com_achivement_list=com_achivement_list,com_achivement_list2=com_achivement_list2,com_cited_list=com_cited_list,
                           com_paper_search_list=com_paper_search_list,com_achive_minyear=com_achive_minyear,com_achive_maxyear=com_achive_maxyear,
                           com_cited_minyear=com_cited_minyear,com_cited_maxyear=com_cited_maxyear,recommend_list=recommend_list)
