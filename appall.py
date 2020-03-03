from flask import Flask
from app import app as app1
from appscholarinfo import app as appscholar
from appSearch_Result import app as appSearch_Result

app =  Flask(__name__)
app.register_blueprint(app1)
app.register_blueprint(appscholar)
app.register_blueprint(appSearch_Result)

if __name__ == '__main__':
    app.run()
