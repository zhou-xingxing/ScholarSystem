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

# 测试关系网络传参
@app.route('/relation')
def testrelation():
    # 中心学者结点
    center_data = {
        "name": "罗贯中",
# 中心学者的这个值没有实际意义，但必须要有，可以给每个中心点设一固定值
        "corpnum": 100,
        "in": "三国test",
    }
    # 合作学者结点
    datalist = [{"name": "诸葛亮", "corpnum": 80, "in": "蜀国"}, {"name": "刘备", "corpnum": 60, "in": "蜀国"},
                {"name": "曹操", "corpnum": 50, "in": "魏国"},{"name": "关羽", "corpnum": 50, "in": "蜀国"},
                {"name": "赵云", "corpnum": 40, "in": "蜀国"}, {"name": "孙权", "corpnum": 20, "in": "吴国"},
                {"name": "张飞", "corpnum": 10, "in": "蜀国"}]

    # 结点数组
    local_data = []
    # 连接数组
    local_links = []
    # 种类
    local_category = []
    # 设置categories一人一个种类，方便以不同颜色区分
    # 先把中心放进去
    local_category.append({
        "name": center_data["name"]
    })
    local_data.append({
        "name": center_data["name"],
        # 图形大小
        "symbolSize": center_data["corpnum"],
        "value": center_data["corpnum"],
        "category": center_data["name"],
        # 禁止拖动
        "draggable": False,
        "in": center_data["in"],
    })

    for i in datalist:
        local_category.append({
            "name": i["name"]
        })
        local_data.append({
            "name": i["name"],
            "symbolSize": i["corpnum"],
            "value": i["corpnum"],
            "category": i["name"],
            "draggable": True,
            "in": i["in"],
        })
        local_links.append({
            "source": center_data["name"],
            "target": i["name"],
            "value": i["corpnum"]
        })
    return render_template("RelationNet_test.html",rela_categories=local_category, rela_dates=local_data, rela_links=local_data)
