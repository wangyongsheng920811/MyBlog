from flask import Flask
from flask import render_template
import config
from exts import db
from functools import wraps
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import make_response
from models import User
from models import Article
from models import Comment

import os
import datetime
import random


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper


def get_article(articles, tag, articles_range={}):
    page_title = tag
    if tag != 'index' and tag != 'details':
        tag = 'category_page'
    page_name = tag + '.html'
    print(page_name)
    if session.get('user_id') == 1:
        return render_template(page_name, id=1, page_title=page_title, **articles, **articles_range)
    else:
        return render_template(page_name, page_title=page_title, **articles, **articles_range)


@app.route('/')
def index():
    articles = {
        'articles': Article.query.order_by('-create_time').all()
    }
    articles_range = {
        'articles_range': Article.query.order_by('-click_number').limit(10).all()
    }
    return get_article(articles, 'index', articles_range)


@app.route('/<tag>/')
def tags(tag):
    # tag_list = {
    #     'python': 'Python',
    #     'linux': 'Linux',
    #     'windows': 'Windows',
    #     'web': '前端',
    #     'ci': '持续集成',
    #     'other': '其他',
    # }
    if tag in ['Python', 'Linux', 'Windows', '前端', '持续集成', '其他']:
        articles = {
            'articles': Article.query.filter(Article.category == tag).order_by('-create_time').all()
        }
        return get_article(articles, tag)
    else:
        return redirect(url_for('index'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter(User.username == user_name, User.password == password, User.id == 1).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return '用户名或密码错误'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    print(request.method)
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password = request.form.get('password1')
        user = User(email=email, username=user_name, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/write/', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'GET':
        return render_template('write_article.html', id=1)
    else:
        print(request.form)
        category = request.form.get('select')
        title = request.form.get('title')
        contents = request.form.get('textarea')
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        article = Article(category=category, title=title, click_number=1, content=contents, author_id=user_id, author=user)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))


# 定义一个过滤器，只返回指定行数的html文字
def html_filter(html):
    # contents = re.findall(r'<p>.*</p>', html, re.M)
    return html[:300]


app.add_template_filter(html_filter, 'html_filter')


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


# 接收ck上传文件
@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")

    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload', rnd_name)

        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'

        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'

    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)

    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@app.route('/details/<article_id>/', methods=['GET', 'POST'])
def details(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    article.click_number = article.click_number + 1
    db.session.commit()

    if request.method == 'POST':
        content = request.form.get('comment')
        # print(content)
        comment = Comment(content=content, article_id=article.id, article=article)
        db.session.add(comment)
        db.session.commit()
        # return redirect(url_for('index'))
    comment_list = Comment.query.filter(Comment.article == article).order_by('-create_time').all()
    articles = {
        'articles': article,
        'comments': comment_list
    }
    print(articles)
    return get_article(articles, tag='details')


if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0',port=8080)
