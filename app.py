from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    print('申林-测试')
    print('zsf test')
    print('zst test2 for merge')
    return '高校学者发现系统!'


if __name__ == '__main__':
    app.run()
