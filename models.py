# _*_ coding:utf-8 _*_
# @Author : wangyongsheng
# @Email  : wys920811@163.com
# @Time   :2018/4/2 20:39


from exts import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(36), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('article'))
#
# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     author = db.relationship('User', backref=db.backref('question'))
#
#
# class Answer(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     content = db.Column(db.Text, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
#     create_time = db.Column(db.DateTime, default=datetime.now)
#     question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))
#     author = db.relationship('User', backref=db.backref('answers'))
