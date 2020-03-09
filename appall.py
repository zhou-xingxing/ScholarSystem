from flask import Flask
from app import app as app1
from appscholarinfo import app as appscholar
from appSearch_Result import app as appSearch_Result
from scholar_compare_route import app as compare
from recommend import app as recommened
#创建flask对象
app =  Flask(__name__)
#使用blueprint注册之前创建的flask对象 app1主要包含跟路由和反馈 appscholar主要是学者详细信息的路由 appSearch_Resukt包含查询结果接口
app.register_blueprint(app1)
app.register_blueprint(appscholar)
app.register_blueprint(appSearch_Result)
app.register_blueprint(compare)
app.register_blueprint(recommened)
if __name__ == '__main__':
    app.run()
