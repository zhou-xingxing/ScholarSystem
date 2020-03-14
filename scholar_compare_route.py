from flask import Flask, render_template, request, Blueprint
import datetime, pymysql
from appScholar_Compare import compare1
app = Blueprint("scholar_compare_route", __name__)
'''学者对比路由，具体思路是获取对比的学者数量，获取填入的学者信息，用compare函数获取对比的数据，
并将数据分字段，利用jinja模板传递给前端页面'''
@app.route('/scholarcompare')
def index():
    length = int(request.args.get('length'))
    allscholarinfo=[]
    for i in range(1,length+1):
        dict_scholar = {}
        agr1 = "name"+ str(i);
        agr2 = "school"+str(i);
        agr3 = "college"+str(i);
        dict_scholar["name"] = request.args.get(agr1)
        dict_scholar["school"] = request.args.get(agr2)
        dict_scholar["college"] = request.args.get(agr3)
        allscholarinfo.append(dict_scholar)
    listresults,compareans,newresults,nodatascholar = compare1(allscholarinfo)
    com_all_name = compareans['all_name']
    com_achivement_list =compareans['achivement_list']
    com_achivement_list2 =compareans['achivement_list2']
    com_cited_list = compareans['cited_list']
    com_achive_minyear =compareans['achive_minyear']
    com_achive_maxyear = compareans['achive_maxyear']
    com_cited_minyear = compareans['cited_minyear']
    com_cited_maxyear = compareans['cited_maxyear']
    return render_template("compare.html",comparescholar= listresults,length=length,newresults=newresults,
                           nodatascholar=nodatascholar,com_all_name=com_all_name,com_achivement_list=com_achivement_list,
                           com_achivement_list2=com_achivement_list2,com_cited_list=com_cited_list,com_achive_minyear=com_achive_minyear,
                           com_achive_maxyear=com_achive_maxyear,com_cited_minyear=com_cited_minyear,com_cited_maxyear=com_cited_maxyear)