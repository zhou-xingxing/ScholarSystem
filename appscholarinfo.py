from flask import Flask, render_template, request,Blueprint
import pymysql
app = Blueprint("appscholarinfo",__name__)

@app.route('/scholarinfo')
def scholarinfo():
    connection = pymysql.connect(db='test',user='root',password='root',host='127.0.0.1',port=3306,charset='utf8')
    cursor = connection.cursor()
    cursor.execute('select * from paper')
    result = cursor.fetchall()
    return render_template("scholarinfo.html",result=result)

