from flask import Flask, render_template, request, Blueprint
import datetime, pymysql

app = Blueprint("app", __name__)


@app.route('/')
def index():
    # 打开文件
    file1 = open("schoolname.txt", "r", encoding='utf-8')
    # 文件中以 '清华大学':'中国 + 985 + 研究所 + 港澳台', 的形式存储，
    # 但考虑到有英文学校中有逗号分隔的情况，所以以 ',' 对每一个 学校：所属类型 进行分隔
    list_row = file1.readline().split('\', \'')
    # 存储学校名字
    list_school = []
    # 存储所属类型（985,211,或者us）
    list_location = []
    # 分割后现在存储在list_row中是一个二维数组，第一列是学校名字，第二列是所属类型
    # 将他们分别存入上面两个列表中
    for i in range(len(list_row)):
        list_school.append(list_row[i].split('\': \'')[0])
        list_location.append(list_row[i].split('\': \'')[1])
    # 定义不同类型学校列表
    list_985 = []
    list_211 = []
    list_us = []

    # 将学校按照类型填入上面三个列表中
    for i in range(len(list_row)):
        if list_location[i] == '中国 985 + 研究所 + 港澳台':
            list_985.append(list_school[i].strip("'"))
        elif list_location[i] == '中国 211 + 其他':
            list_211.append(list_school[i].strip("'"))
        else:
            list_us.append(list_school[i].strip("'"))
    # 关闭文件
    file1.close()

    # 统计点击次数在首页推荐
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="search_count", user="root", password="12345678",
                                 charset="utf8")
    cursor = connection.cursor()
    sql = "select * from `search_count` order by searchcount desc limit 10;"
    cursor.execute(sql)
    connection.commit()
    searchresult = cursor.fetchall()
    # print(searchresult)

    # 将分类好的三个列表和推荐热门传回html中
    return render_template("index.html",list_985=list_985,list_211=list_211,list_us=list_us,searchresult=searchresult)


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
    # html的checkbox传回来的是"on"，需要转换一下
    if receive == 'on':
        receive = 1
    else:
        receive = 0
    # print(name, school, fd_type, content, email, receive)
    # 连接数据库
    connection = pymysql.connect(host="39.106.96.175", port=3306, db="feedback", user="root", password="12345678",
                                 charset="utf8")
    cursor = connection.cursor()
    # 查询数据库中当前最大id，以便确定新数据的id
    cursor.execute("select max(id) from feedback")
    result = cursor.fetchone()
    id = int(result[0])
    row=0
    # 插入数据
    try:
        sql = "insert into feedback(id,scholar_name,scholar_school,fd_type,content,email,receive) values (%s,%s,%s,%s,%s,%s,%s) "
        # 执行SQL语句，返回数据库改变的记录数，正常情况下返回1
        row=cursor.execute(sql, [id + 1, name, school, fd_type, content, email, receive])
        # print('Successful')
        connection.commit()
    except:
        print('Failed')
        SuccessOrNot = False
        # 插入数据失败则回滚操作
        connection.rollback()
    # 根据row判断反馈提交是否成功，以便显示不同反馈结果页面
    if row==1:
        SuccessOrNot = True
    else:
        SuccessOrNot = False
    # 关闭连接
    cursor.close()
    connection.close()

    return render_template("feedback_result.html", SuccessOrNot=SuccessOrNot)
