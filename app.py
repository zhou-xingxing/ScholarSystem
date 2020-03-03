from flask import Flask, render_template, request, Blueprint
import datetime, pymysql

app = Blueprint("app", __name__)


@app.route('/')
def index():
    return render_template("index.html")


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
    # 插入数据
    try:
        sql = "insert into feedback(id,scholar_name,scholar_school,fd_type,content,email,receive) values (%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(sql, [id + 1, name, school, fd_type, content, email, receive])
        # print('Successful')
        SuccessOrNot = True
        connection.commit()
    except:
        # print('Failed')
        SuccessOrNot = False
        connection.rollback()

    cursor.close()
    connection.close()

    return render_template("feedback_result.html", SuccessOrNot=SuccessOrNot)
