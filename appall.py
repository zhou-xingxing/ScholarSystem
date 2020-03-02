from flask import Flask
from app import app as app1
from appscholarinfo import app as appscholar

app =  Flask(__name__)
app.register_blueprint(app1)
app.register_blueprint(appscholar)

if __name__ == '__main__':
    app.run()
