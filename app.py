from flask import Flask, render_template, request,Blueprint
import datetime

app = Blueprint("app",__name__)

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
    print(name, school,type, content, email, receive, time)
    # FeedBack接口待实现
    # SuccessOrNot=FeedBack(name,school,type,content,email,receive,time)
    SuccessOrNot = True
    return render_template("feedback_result.html",SuccessOrNot=SuccessOrNot)

# 测试关系网络图
@app.route('/relation')
def relation():
    return render_template("RelationNet_test.html")


