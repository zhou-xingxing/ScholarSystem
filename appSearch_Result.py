from flask import Flask, render_template, request,Blueprint
import pymysql
import requests
import json
import time
import page_utils
app = Blueprint("appSearch_Result",__name__)


@app.route('/Search_result')
def appSearch_result():
    keyword = request.args.get('keyword')
    #scholarid=request.args.get('scholarid')
    search_type = request.args.get('type')
    start_time = time.time()  # 开始时间
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"  # 获取当前所有表（学校）
    cls.execute(sql1)
    conn.commit()
    results = cls.fetchall()
    #print(results)
    SQL = ""
    name = keyword
    need_part = '`id`,`name`,`school`,`college`,`field`,`achievement_num`'
    if search_type == "1":
        for i in results:
            sql = "select %s from %s where id between 1 and 2500 and name='%s'" % (need_part,i[0], name)
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
    elif search_type == "2":
        for i in results:
            sql = "select %s from %s where id between 1 and 2500 and college LIKE '%s'" % (need_part,i[0] , '%'+name+'%')
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
    elif search_type == "3":
            sql = "select %s from %s where id between 1 and 2500" % (need_part,name)
            SQL += sql
    elif search_type == "4":
        for i in results:
            sql = "select %s from %s where id between 1 and 2500 and field LIKE '%s'" % (need_part,i[0] , '%'+name+'%')
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
    elif search_type == "5":
        for i in results:
            sql = "select %s from %s where id between 1 and 2500 and scholarid='%s'" % (need_part,i[0],name)
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
        #return render_template('scholarinfo.html',result=result,length=length)
    # print(SQL+';')
    try:
        cls.execute(SQL + ';')
        conn.commit()
        result = cls.fetchall()
        end_time = time.time()  # 结束时间
        print("time:", (end_time - start_time))  # 结束时间-开始时间
        length = len(result)
    except:
        result=[]
        length=0
    #把研究领域的['','']去掉
    listresults = []
    for reone in result:
        if reone[4]:
            newstr = (reone[4].replace('[\'', ' ').replace('\']', ' ').replace('\', \'', ', '))
            newtuple = (reone[0], reone[1], reone[2], reone[3], newstr, reone[5])
        else:
            newtuple = (reone[0], reone[1], reone[2], reone[3], reone[4], reone[5])
        listresults.append(newtuple)
    end_time = time.time()  # 结束时间
    print("time:", (end_time - start_time))  # 结束时间-开始时间

    #实现翻页
    li = []
    for i in range(1, length):
        li.append(i)
    pager_obj = page_utils.Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=10)
    html = pager_obj.page_html()
    listresult = listresults[pager_obj.start:pager_obj.end]

    return render_template('search_result.html',result=listresult,length=length,html=html)