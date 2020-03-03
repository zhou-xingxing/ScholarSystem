from flask import Flask, render_template, request, Blueprint
import datetime

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
    # 反馈学者姓名，学术机构、反馈类型，反馈内容，邮箱，是否接受反馈，当前时间
    name = request.form.get('name')
    school = request.form.get('school')
    type = request.form.get('type')
    content = request.form.get('content')
    email = request.form.get('email')
    receive = request.form.get('receive')
    if receive == 'on':
        receive = True
    else:
        receive = False
    time = datetime.datetime.now()
    print(name, school, type, content, email, receive, time)
    # FeedBack接口待实现
    # SuccessOrNot=FeedBack(name,school,type,content,email,receive,time)
    SuccessOrNot = True
    return render_template("feedback_result.html", SuccessOrNot=SuccessOrNot)


