from flask import Flask, render_template, request, Blueprint
import datetime, pymysql
from appScholar_Compare import compare
app = Blueprint("scholar_compare_route", __name__)

@app.route('/compare')
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
    results = compare("",allscholarinfo,2)
    return render_template("compare.html",comparescholar= results,length=length)