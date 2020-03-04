from flask import Flask, render_template, request,Blueprint
import pymysql
import requests
import json
import time
#创建Blueprint对象以便在appall中注册
app = Blueprint("appSearch_Result",__name__)

#查询列表接口
@app.route('/Search_result')
def appSearch_result():
    #获取查询的参数 包含查询的关键字，以及查询的类型
    keyword = request.args.get('keyword')
    search_type = request.args.get('type')
    start_time = time.time()  # 开始时间

    #创建查询对象
    conn = pymysql.connect(host="39.106.96.175", port=3306, db="scholar_info", user="root", password="12345678",
                           charset="utf8")
    cls = conn.cursor()
    # 获取当前所有表（学校）
    sql1 = "select table_name from information_schema.tables where table_schema='scholar_info'"
    cls.execute(sql1)
    conn.commit()
    results = cls.fetchall()
    # print(results)
    SQL = ""
    name = keyword
    #第1种方式，name为关键词，按照姓名来查询
    if search_type == "1":
        for i in results:
            sql = "select * from %s where id between 1 and 2500 and name='%s'" % (i[0], name)
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
    # 第2种方式，name为关键词，按照专业来查询
    elif search_type == "2":
        for i in results:
            sql = "select * from %s where id between 1 and 2500 and college LIKE '%s'" % (i[0] , '%'+name+'%')
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
    # 第3种方式，name为关键词，按照学者学校来查询
    elif search_type == "3":
            sql = "select * from %s where id between 1 and 2500" % (name)
            SQL += sql
    # 第2种方式，name为关键词，按照学者研究方向来查询
    elif search_type == "4":
        for i in results:
            sql = "select * from %s where id between 1 and 2500 and field LIKE '%s'" % (i[0] , '%'+name+'%')
            if i != results[-1]:
                sql += " UNION "
            SQL += sql
    #从表中查询 用result保存查询结果
    try:
        cls.execute(SQL + ';')
        conn.commit()
        result = cls.fetchall()
        end_time = time.time()  # 结束时间
        print("time:", (end_time - start_time))  # 结束时间-开始时间
        length = len(result)
    except:
        result=[]
        length=0;
    #返回到查询列表页面，并将查询的结果和条数传入进去
    return render_template('search_result.html',result=result,length=length)