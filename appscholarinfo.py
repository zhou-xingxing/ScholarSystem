from flask import Flask, render_template, request,Blueprint
import pymysql
import requests
import json
from collections import Counter
import wordsExtra_zsf

app = Blueprint("appscholarinfo",__name__)

@app.route('/scholarinfo')
def scholarinfo():
    school = request.args.get('school');
    name = request.args.get('name');
    major = request.args.get('major');
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                                 charset="utf8")
    cursor = connection.cursor()

    sql = "select * from %s where name='%s' and college='%s'" % (school, name, major)
    cursor.execute(sql)
    result = cursor.fetchone()
    scholarname = result[1]
    scholarschool =result[2]
    scholarmajor = result[3]
    scholarid = result[4]
    cited_num = result[6]
    achievement_num = result[7]
    Hpoint = result[8]
    Gpoint = result[9]
    #str ="{'其他': '62', '专著': '43', '其他会议数': '195', '北大核心期刊': '6', 'CSCD期刊数': '5', '中国科技核心': '10', 'SCI期刊数': '16', 'EI期刊数': '29', 'SCIE期刊数': '25', 'SSCI期刊数': '1', '其他期刊数': '113'}"
    try:
        scholarfield = eval(result[5])
    except:
        scholarfield = []
    try:
        achievement_list = eval(result[10])
    except:
        achievement_list = []
    try:
        achievement_list2 = eval(result[11])
    except:
        achievement_list2 = []
    try:
        cited_list = eval(result[12])
    except:
        cited_list = []
    try:
        partner_list = eval(result[13])
    except:
        partner_list = []
    try:
        paper_name_list = eval(result[14])
    except:
        paper_name_list = []
    try:
        paper_info_list = eval(result[15])
    except:
        paper_info_list = []
    try:
        paper_search_list = eval(result[16])
    except:
        paper_search_list = []
    try:
        collaborate_org = eval(result[17])
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

    return render_template("scholarinfo.html",scholarname=scholarname,scholarschool=scholarschool,scholarmajor=scholarmajor
                           ,scholarid=scholarid,scholarfield=scholarfield,cited_num=cited_num,achievement_num=achievement_num,
                           Hpoint=Hpoint,Gpoint=Gpoint,achievement_list=achievement_list,achievement_list2=achievement_list2
                           ,cited_list=cited_list,partner_list=partner_list,paper_name_list=paper_name_list,paper_info_list=paper_info_list,paperlen=len(paper_info_list),
                           paper_search_key=paper_search_key,paper_search_num=paper_search_num,collaborate_org=collaborate_org,rela_center=rela_center_data,rela_partner=rela_partner_data,subject=subject)

