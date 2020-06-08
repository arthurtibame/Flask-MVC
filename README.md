![Alt text](/tree.jpg "Path tree")

# Path introduction
1）最上層 web 目錄是項目名稱，一個項目內可以有多個模塊(這邊叫app)，也就是應用，每個應用下有自己的setting，初始化文件，MVC架構。 

2）runserver.py：與應用模塊平級，作为項目啟動文件

3）第二级app目錄：模塊名稱

       controller目錄：MVC中的C,主要存放視圖函數

       model目錄：MVC中的M,主要存存放實體文件, 映射db中table

       templates：MVC中的V，存放html文件

       static：靜態文件,存放html、css、 js 等

       __init__.py:模块初始化文件，Flask 程序对象的创建必须在 __init__.py 文件里完成， 然后我们就可以安全導入package

       setting.py:配置文件、 database 等等

# Code demonstration step by step

## 1、先把项目运行起来：

### 1） 寫入__init__.py文件，創建項目對象如下
```python
from flask import Flask

#创建项目对象
app = Flask(__name__)
```
### 2） 在runserver.py
```python
from app import app

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
```
### 測試runserver.py
```cmd
python runserver.py
```

## 2、修改配置文件
### 2.1）修改setting.py文件，增加db連接參數如下 (這邊使用sqlite3)
```python
import os
#開啟debug
DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#sqlite3 
DATABASE = 'myweb.sqlite' # 檔案名稱
SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(r"C:/python/web/app/", DATABASE)
```
### 2.2）讓項目讀取配置文件 (讀取setting)
修改__init__.py:改為如下内容:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#import  os
#print os.environ.keys()
#print os.environ.get('FLASKR_SETTINGS')
#加载配置文件内容
app.config.from_object('app.setting')     #模块下的setting文件名，不用加py后缀 
app.config.from_envvar('FLASKR_SETTINGS')   #環境變亮，指向配置文件setting的路径

#创建数据库对象 
db = SQLAlchemy(app)
```
### 注意：FLASKR_SETTINGS环境变量需要手工单独设置，window下可以在命令行中输入：
```cmd
C:\python\web> set FLASKER_SETTINGS=C:\python\web\app\setting.py
```
## 設計Database
### 在model 目錄下創建 User.py, Category.py
### 1) User.py:
```python
from app import db

class User(db.Model):
    __tablename__ = 'b_user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(16))

    def __init__(self,username,password):
        self.username  = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username
```
### 2) Category.py
```python
from app import db

class Category(db.Model):
    __tablename__ = 'b_category'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),unique=True)
    content = db.Column(db.String(100))

    def __init__(self,title,content):
        self.title = title
        self.content = content
    def __repr__(self):
        return '<Category %r>' % self.title
```
### 3）创建数据库和表
cmd cd到项目runserver.py 目錄下(這裡為 C:\python\web) 進入python shell
輸入如下
```cmd
Python 3.7.4 (default, June 09 2020, 09:44:00) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more nformation.
>>> from app import db
>>> db.create_all()
>>>
```
這邊會發現在目錄 app 下會新增myweb.sqlite 檔案 但是裡面包含剛剛設立的table (b_user, b_category)

所以這邊要修改app目錄下的 __init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#创建项目对象
app = Flask(__name__)

#import  os
#print os.environ.keys()
#print os.environ.get('FLASKR_SETTINGS')
app.config.from_object('app.setting')     #模块下的setting文件名，不用加py后缀 
app.config.from_envvar('FLASKR_SETTINGS')   #环境变量，指向配置文件setting的路径

#创建数据库对象 
db = SQLAlchemy(app)

#app 導入後才能import 
from app.model import User, Country, Category
```
## 請注意這邊一定要將 import 放置 db variable 下面
### 在做跟這面一樣的事情 db.create_all()
```cmd
Python 3.7.4 (default, June 09 2020, 09:44:00) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more nformation.
>>> from app import db
>>> db.create_all()
>>>
```
## 3. 增加template: 登入頁面
在template 目錄下新增三個html
layout.html
```html
<!doctype html>
<title>Flaskr</title>
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
<div class=page>
    <h1>Flaskr</h1>
    <div class=metanav>
        {% if not session.logged_in %}
        <a href="{{ url_for('login') }}">log in</a>
        {% else %}
        <a href="{{ url_for('logout') }}">log out</a>
        {% endif %}
    </div>
    {% for message in get_flashed_messages() %}
    <div class=flash>{{ message }}</div>
    {% endfor %}
    {% block body %}{% endblock %}
</div>
```

login.html
```html
{% extends "layout.html" %}
{% block body %}
  <h2>Login</h2>
  {% if error %}<p class=error><strong>Error:</strong> {{ error }}{% endif %}
  <form action="{{ url_for('login') }}" method=post>
    <dl>
      <dt>Username:
      <dd><input type=text name=username>
      <dt>Password:
      <dd><input type=password name=password>
      <dd><input type=submit value=Login>
    </dl>
  </form>
{% endblock %}
```
show_entries.html:
```html
{% extends "layout.html" %}
{% block body %}
  {% if session.logged_in %}
    <form action="{{ url_for('add_entry') }}" method='POST' class=add-entry>
      <dl>
        <dt>Title:
        <dd><input type=text size=30 name=title>
        <dt>Text:
        <dd><textarea name=text rows=5 cols=40></textarea>
        <dd><input type=submit value=Share>
      </dl>
    </form>
  {% endif %}
  <ul class=entries>
  {% for entry in entries %}
    <li><h2>{{ entry.title }}</h2>{{ entry.content|safe }}
  {% else %}
    <li><em>Unbelievable.  No entries here so far</em>
  {% endfor %}
  </ul>
{% endblock %}
```
在static 新增 style.css
```css
body            { font-family: sans-serif; background: #eee; }
a, h1, h2       { color: #377BA8; }
h1, h2          { font-family: 'Georgia', serif; margin: 0; }
h1              { border-bottom: 2px solid #eee; }
h2              { font-size: 1.2em; }

.page           { margin: 2em auto; width: 35em; border: 5px solid #ccc;
                  padding: 0.8em; background: white; }
.entries        { list-style: none; margin: 0; padding: 0; }
.entries li     { margin: 0.8em 1.2em; }
.entries li h2  { margin-left: -1em; }
.add-entry      { font-size: 0.9em; border-bottom: 1px solid #ccc; }
.add-entry dl   { font-weight: bold; }
.metanav        { text-align: right; font-size: 0.8em; padding: 0.3em;
                  margin-bottom: 1em; background: #fafafa; }
.flash          { background: #CEE5F5; padding: 0.5em;
                  border: 1px solid #AACBE2; }
.error          { background: #F0D6D6; padding: 0.5em; }
```
## 新增 controller
### 在controller 目錄下新增 blog_message.py
blog_message.py
```python
from app.model.User import  User
from app.model.Category import Category
import os

from app import app,db
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g

@app.route('/')
def show_entries():
    categorys = Category.query.all()
    return render_template('show_entries.html',entries=categorys)

@app.route('/add',methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    title = request.form['title']
    content = request.form['text']
    category = Category(title,content)
    db.session.add(category)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=request.form['username']).first()
        passwd = User.query.filter_by(password=request.form['password']).first()

        if user is None:
            error = 'Invalid username'
        elif passwd is None:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
```
## 最後在app目錄下的__init__.py 導入model
```python
from app.controller import blog_manage
```
### 所以最終我們的__init__.py 如下
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#创建项目对象
app = Flask(__name__)

#import  os
#print os.environ.keys()
#print os.environ.get('FLASKR_SETTINGS')
app.config.from_object('app.setting')     #模块下的setting文件名，不用加py后缀 
app.config.from_envvar('FLASKR_SETTINGS')   #环境变量，指向配置文件setting的路径

#创建数据库对象 
db = SQLAlchemy(app)

#app 導入後才能import 
from app.model import User, Country, Category

#只有在app对象之后声明，用于导入view模块
from app.controller import blog_manage
```

## 所以只要增加Controller 或是 Model 都要到 __init__.py 這邊導入!

## 5. Try it !
```cmd
C:\python\web>python runserver.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 265-498-339
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [09/Jun/2020 03:29:41] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [09/Jun/2020 03:29:41] "GET /static/style.css HTTP/1.1" 200 -
127.0.0.1 - - [09/Jun/2020 03:29:42] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [09/Jun/2020 03:29:49] "GET /login HTTP/1.1" 200 -
127.0.0.1 - - [09/Jun/2020 03:29:49] "GET /static/style.css HTTP/1.1" 200 -
127.0.0.1 - - [09/Jun/2020 03:29:55] "POST /login HTTP/1.1" 200 -
```


















