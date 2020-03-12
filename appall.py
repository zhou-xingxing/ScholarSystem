from flask import Flask
from app import app as app1
from appscholarinfo import app as appscholar
from appSearch_Result import app as appSearch_Result
from scholar_compare_route import app as scholarcompare
from recommend import app as recommened
from appScholar_Compare import app as compare
# 创建flask对象
app =  Flask(__name__)
# 使用blueprint注册之前创建的flask对象 app1主要包含跟路由和反馈 appscholar主要是学者详细信息的路由 appSearch_Resukt包含查询结果接口
app.register_blueprint(app1)
app.register_blueprint(appscholar)
app.register_blueprint(appSearch_Result)
app.register_blueprint(scholarcompare)
app.register_blueprint(recommened)
app.register_blueprint(compare)


# 以下为管理员附加代码——申林
import os
from flask import Flask, url_for, redirect, render_template, request, abort,session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_babelex import Babel
from flask_admin import helpers as admin_helpers
# Create Flask application
app.config.from_pyfile('config.py')
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
db = SQLAlchemy(app)
# 配置页面中文显示
babel = Babel(app)


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# 角色类，分为普通用户和超级用户
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

# 用户类，同为用户数据表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    def __str__(self):

        return self.email

# 反馈类，同为反馈数据表
class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    scholar_name = db.Column(db.String(255))
    scholar_school = db.Column(db.String(255))
    fd_type = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    receive = db.Column(db.SmallInteger, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)
    state = db.Column(db.SmallInteger, nullable=False, default=0)

    def __repr__(self):
        return '<feedback_id %r>' % (self.id)

# Setup Flask-Security
# 将角色和用户封装调用flask安全模式
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
# 继承view，对权限做区分
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# Flask views
# 将admin路由重定向到首页
@app.route('/admin/',endpoint='/',redirect_to='/')#,endpoint='/',redirect_to='/'
# 此函数不会执行
def index():
    print("已经重定向到首页")
    # return render_template("index.html")
    return redirect(url_for('index', next=request.url))

# Create admin
admin = flask_admin.Admin(
    app,
    '管理员界面',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
class FeedbackView(MyModelView):
    column_labels = dict(
        scholar_name=u'学者姓名',
        scholar_school=u'学者所在机构',
        fd_type=u'反馈类型',
        content=u'反馈内容',
        email=u'电子邮件',
        receive=u'是否接收回复',
        time=u'反馈时间',
        state=u'审核状态',
    )

# 将需要的view加入页面显示，暂时只加入反馈表
# admin.add_view(MyModelView(Role, db.session))
# admin.add_view(MyModelView(User, db.session))
admin.add_view(FeedbackView(Feedback, db.session,name=u'反馈'))
# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

if __name__ == '__main__':
    app.run()
