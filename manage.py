# _*_ coding:utf-8 _*_
# @Author : wangyongsheng
# @Email  : wys920811@163.com
# @Time   :2018/4/2 20:39


from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from MyBlog import app
from exts import db
from models import User
from models import Article

# 数据库迁移顺序：模型-》迁移文件-》表
# 命令行:
# python manage.py db init
# ->python manage.py db migrate
# ->python manage.py db upgrade
# 表新增字段时不需再执行init
# 使用flask migrate 创建数据库、数据库迁移  不再使用db.create_all()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
