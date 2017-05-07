from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from conf.settings import SQLALCHEMY_DATABASE_URI
from modules.models import Category, Links, User, Role, Article, Description, Rotate
from modules.common import get_datetime
from sqlalchemy import or_


class SqlHelper(object):
    def __init__(self):
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        self.session = Session()

    def category(self):
        """
        返回所有分类的列表，类似 ['shell', 'mysql', 'python']
        :return: 返回分类
        """
        return self.session.query(Category.name, Category.basename).all()
        # return self.session.query(Category.name).all()

    def get_all_article(self):
        return self.session.query(Article).all()

    def get_articles_count(self):
        return self.session.query(Article).count()

    def get_description(self):
        return self.session.query(Description.content).order_by(Description.pub_date.asc()).all()

    def links(self):
        """
        友情链接
        :return:
        """
        return self.session.query(Links.name, Links.callback_url).all()
        # return self.session.query(Links.name, Links.callback_url).order_by(Links.pub_date.asc()).all()[0:2]

    def regist(self, username, password, email, role='ordinary'):
        """
        注册用户，从首页注册的都是普通用户，后台注册可以指定是什么用户
        :return:
        """
        # self.session.add(User(username=username, password=password, email=email))
        # self.session.add(Role(name='ordinary'))
        # self.session.commit()
        try:
            role_list = []
            user = User(username=username, password=password, email=email, create_date=get_datetime())
            role_obj = self.session.query(Role).filter(Role.name == role).first()
            print(role_obj.id)
            if role_obj is not None:
                role = role_obj
                role_list.append(role)
            else:
                role = Role(name='ordinary')
                self.session.add(role)
                self.session.commit()

            user.roles = role_list
            self.session.add(user)
            self.session.commit()
            return True
        except IntegrityError as e:
            return False

    def change_user_email(self, username, email):
        try:
            self.session.query(User).filter(User.username == username).update({"email": email})
            self.session.commit()
            return True
        except Exception as e:
            return False

    def change_user_passwd(self, username, password):
        try:
            self.session.query(User).filter(User.username == username).update({"password": password})
            self.session.commit()
            return True
        except Exception as e:
            return False

    def get_user_info(self, username):
        """
        返回用户信息
        :param username: 传入用户名
        :return:
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_category_articles(self, category):
        """
        返回当前分类下的文章信息
        :param category:
        :return:
        """
        return self.session.query(Category).filter(Category.name == category).first()

    def get_category_articles_by_basename(self, basename):
        return self.session.query(Category).filter(Category.basename == basename).first()

    def get_article_byid(self, id):
        return self.session.query(Article).filter(Article.id == id).first()

    def get_category_info_by_basename(self, basename):
        return self.session.query(Category).filter(Category.basename == basename).first()

    def get_category_articles_count(self, category_id):
        # return len(self.session.query(Category).filter(Category.basename==basename).first().articles)
        return self.session.query(Article).filter(Article.category_id == category_id).count()

    def get_recent_article(self):
        return self.session.query(Article).order_by(Article.pub_date.desc()).all()

    def get_most_click_articles(self):
        return self.session.query(Article).order_by(Article.click_count.desc()).all()

    def add_article_click_count(self, article_id):
        self.session.query(Article).filter(Article.id == article_id).update(
            {"click_count": Article.click_count + 1})
        self.session.commit()

    def search_article_by_keyword(self, keyword):
        return self.session.query(Article).filter(or_(Article.title.like('%'+keyword+'%'), Article.content.like('%'+keyword+'%'))).all()


    def get_last_article_byid(self, current_id):
        try:
            sql = 'select id from articles where id = (select id from articles where id < %s order by id desc limit 1)' % current_id
            return self.session.execute(sql).fetchone()[0]
        except TypeError as e:
            return current_id

    def get_next_article_byid(self, current_id):
        try:
            sql = 'select id from articles where id = (select id from articles where id > %s order by id asc limit 1)' % current_id
            return self.session.execute(sql).fetchone()[0]
        except TypeError as e:
            return current_id

    def collect_articles(self, article_id, user):
        try:
            user_obj = self.get_user_info(user)
            article_obj = self.get_article_byid(article_id)
            # print(type(user))
            user_obj.collections.append(article_obj)
            self.session.add(user_obj)
            self.session.commit()

            return True
        except Exception as e:
            return False

    def collected_articles(self, user):
        return self.session.query(User).filter(User.username == user).scalar()

    def get_rotates(self):
        return self.session.query(Rotate).order_by(Rotate.pub_date.desc()).all()

    def __del__(self):
        self.session.close()

if __name__ == '__main__':
    obj = SqlHelper()
    print(obj.get_rotates())
