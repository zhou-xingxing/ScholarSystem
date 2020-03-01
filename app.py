from flask import Flask, render_template, request
import datetime

app = Flask(__name__)


@app.route('/')
def index():
    print("Linux test git")
    return render_template("index.html")


# 反馈页面
@app.route('/feedback')
def feedback():
    return render_template("feedback.html")


# 处理反馈
@app.route('/handlefeedback', methods=['GET', 'POST'])
def handlefeedback():
    # 反馈学者姓名，反馈类型，反馈内容，邮箱，是否接受反馈，当前时间
    name = request.form.get('name')
    type = request.form.get('type')
    content = request.form.get('content')
    email = request.form.get('email')
    receive = request.form.get('receive')
    if receive == 'on':
        receive = True
    else:
        receive = False
    time = datetime.datetime.now()
    print(name, type, content, email, receive, time)
    # FeedBack接口待实现
    # SuccessOrNot=FeedBack(name,type,content,email,receive,time)
    SuccessOrNot = True
    return render_template("feedback_result.html",SuccessOrNot=SuccessOrNot)


if __name__ == '__main__':
    app.run()
