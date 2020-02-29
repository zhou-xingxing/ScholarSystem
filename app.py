from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def index():
    print("Linux test git")
    return  render_template("index.html")



# 反馈页面
@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

if __name__ == '__main__':
    app.run()
