from flask import Flask, render_template, request,Blueprint
import pymysql
import requests
import json
app = Blueprint("appSearch_Result",__name__)


@app.route('/appSearch_result')
def appSearch_result():
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",charset="utf8")
    cursor = connection.cursor()
    cursor.execute('select * from 北京大学 where scholarid is not null')
    result = cursor.fetchone()
    # for i in range(18):
    #     print(result[i])
    scholarname = result[1]
    scholarschool = result[2]
    scholarmajor = result[3]
    scholarid = result[4]
    scholarfield = eval(result[5])
    cited_num = result[6]
    achievement_num = result[7]
    Hpoint = result[8]
    Gpoint = result[9]
    str = "{'其他': '62', '专著': '43', '其他会议数': '195', '北大核心期刊': '6', 'CSCD期刊数': '5', '中国科技核心': '10', 'SCI期刊数': '16', 'EI期刊数': '29', 'SCIE期刊数': '25', 'SSCI期刊数': '1', '其他期刊数': '113'}"
    achievement_list = eval(str)
    achievement_list2 = result[11]
    cited_list = result[12]
    partner_list = eval(result[13])
    paper_name_list = eval(result[14])
    paper_info_list = eval(result[15])
    paper_search_list = result[16]
    collaborate_org = eval(result[17])
    return render_template("search_result.html", scholarname=scholarname, scholarschool=scholarschool,
                           scholarmajor=scholarmajor
                           , scholarid=scholarid, scholarfield=scholarfield, cited_num=cited_num,
                           achievement_num=achievement_num,
                           Hpoint=Hpoint, Gpoint=Gpoint, achievement_list=achievement_list,
                           achievement_list2=achievement_list2
                           , cited_list=cited_list, partner_list=partner_list, paper_name_list=paper_name_list,
                           paper_info_list=paper_info_list,
                           paper_search_list=paper_search_list, collaborate_org=collaborate_org)