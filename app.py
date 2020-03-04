from flask import Flask, render_template, request, Blueprint
import datetime, pymysql

app = Blueprint("app", __name__)


@app.route('/')
def index():
    file1 = open("schoolname.txt", "r", encoding='utf-8')
    list_row = file1.readline().split('\', \'')
    list_school = []
    list_location = []
    for i in range(len(list_row)):
        list_school.append(list_row[i].split('\': \'')[0])
        list_location.append(list_row[i].split('\': \'')[1])

    list_985 = []
    list_211 = []
    list_us = []

    for i in range(len(list_row)):
        if list_location[i] == '中国 985 + 研究所 + 港澳台':
            list_985.append(list_school[i].strip("'"))
        elif list_location[i] == '中国 211 + 其他':
            list_211.append(list_school[i].strip("'"))
        else:
            list_us.append(list_school[i].strip("'"))
    file1.close()

    return render_template("index.html",list_985=list_985,list_211=list_211,list_us=list_us)


# 反馈页面
@app.route('/feedback')
def feedback():
    return render_template("feedback.html")


# 处理反馈
@app.route('/handlefeedback', methods=['GET', 'POST'])
def handlefeedback():
    # 反馈学者姓名，学术机构、反馈类型，反馈内容，邮箱，是否接受反馈
    name = request.form.get('name')
    school = request.form.get('school')
    fd_type = request.form.get('type')
    content = request.form.get('content')
    email = request.form.get('email')
    receive = request.form.get('receive')
    if receive == 'on':
        receive = 1
    else:
        receive = 0
    # print(name, school, fd_type, content, email, receive)
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="feedback", user="root", password="12345678",
                                 charset="utf8")
    cursor = connection.cursor()
    # 查询当前id
    cursor.execute("select max(id) from feedback")
    result = cursor.fetchone()
    id = int(result[0])
    row=0
    # 插入数据
    try:
        sql = "insert into feedback(id,scholar_name,scholar_school,fd_type,content,email,receive) values (%s,%s,%s,%s,%s,%s,%s) "
        row=cursor.execute(sql, [id + 1, name, school, fd_type, content, email, receive])
        # print('Successful')
        connection.commit()
    except:
        # print('Failed')
        SuccessOrNot = False
        connection.rollback()
    if row==1:
        SuccessOrNot = True
    else:
        SuccessOrNot = False

    cursor.close()
    connection.close()

    return render_template("feedback_result.html", SuccessOrNot=SuccessOrNot)
