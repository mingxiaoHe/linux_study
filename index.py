#!/usr/bin/env python# coding=utf-8import osimport sysimport tornado.httpserverimport tornado.ioloopimport tornado.optionsimport tornado.escapeimport tornado.webimport tornado.genimport timefrom tornado.options import define, optionsfrom modules.sqlhelper import SqlHelperfrom modules.common import get_md5_string, turn_to_intfrom modules import ui_methodsfrom modules.PageHelper import Pager, PageInfo, get_method_pagerBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))sys.path.append(BASE_DIR)define('port', default=8000, help='run on the given port', type=int)DOMAIN = 'http://127.0.0.1:8000'class BaseHandler(tornado.web.RequestHandler):    def __init__(self, application, request, **kwargs):        super(BaseHandler, self).__init__(application, request, **kwargs)        self.sess = SqlHelper()    def get_current_user(self):        return self.get_secure_cookie('user_name')    @property    def get_categories(self):        return self.sess.category()    @property    def get_description(self):        return self.sess.get_description()[0].content    @property    def get_friend_links(self):        return self.sess.links()    def get_user_info(self, username):        return self.sess.get_user_info(username)    def get_category_articles(self, category):        return self.sess.get_category_articles(category)    def get_category_articles_by_basename(self, basename):        return self.sess.get_category_articles_by_basename(basename)    def get_article_byid(self, article_id):        return self.sess.get_article_byid(article_id)    def change_user_email(self, username, email):        return self.sess.change_user_email(username, email)    def change_user_passwd(self, username, password):        return self.sess.change_user_passwd(username, password)    def regist(self, username, password, email):        return self.sess.regist(username, password, email)class IndexHandler(BaseHandler):    @tornado.web.asynchronous    def get(self):        self.render('index/index.html',                    categories=super().get_categories,                    links=super().get_friend_links,                    desc=super().get_description,                    recent_articles=self.sess.get_recent_article()[0:5],                    most_click_articles = self.sess.get_most_click_articles()[0:5],                    linux_code=super().get_category_articles('Linux编程').articles,                    linux_base=super().get_category_articles('Linux基础').articles,                    linux_oper=super().get_category_articles('Linux运维').articles,                    linux_sql=super().get_category_articles('数据库技术').articles                    )class CategoryHandler(BaseHandler):    @tornado.web.asynchronous    def get(self, basename, page):        page = turn_to_int(page, 1)        # 此分类下的所有文章        cate_articles = super().get_category_articles_by_basename(basename).articles        # uri的dirname        dir_uri_name = os.path.dirname(self.request.uri)        # 此分类信息的信息        category = self.sess.get_category_info_by_basename(basename)        # 根据此分类的id查找文章并计算count        count = self.sess.get_category_articles_count(category.id)        # 检测页数是否合法，如果页数超过        page_obj = PageInfo(page, count, per_item=1)        all_page_count = page_obj.all_page_count        if page > all_page_count:            page = all_page_count        elif page <= 0:            page = 1        page_string = Pager(page, all_page_count, dir_uri_name)        self.render('category/category.html',                    cate_articles=cate_articles[page_obj.start:page_obj.end],                    domain=DOMAIN,                    categories=super().get_categories,                    page_string=page_string,                    recent_articles=self.sess.get_recent_article()[0:10],                    )class PostHandler(BaseHandler):    @tornado.web.asynchronous    def get(self, article_id):        # print(self.request.remote_ip)        self.sess.add_article_click_count(article_id)        self.render('post/post.html',                    uri=self.request.uri,                    domain=DOMAIN,                    article=super().get_article_byid(article_id),                    categories=super().get_categories,                    recent_articles=self.sess.get_recent_article()[0:5],                    )class InfoHandler(BaseHandler):    @tornado.web.authenticated    @tornado.web.asynchronous    def get(self):        user_obj = super().get_user_info(super().get_current_user())        self.render('user/info/info.html', categories=super().get_categories,                    recent_articles=self.sess.get_recent_article()[0:10],                    **{'username': user_obj.username, 'domain': DOMAIN, 'email': user_obj.email,                       'roles': user_obj.roles[0]})class ChangeInfoHandler(BaseHandler):    @tornado.web.authenticated    @tornado.web.asynchronous    def get(self):        self.render('user/changeinfo/changeinfo.html',                    recent_articles=self.sess.get_recent_article()[0:10],                    categories=super().get_categories,                    domain=DOMAIN)    def post(self):        rawpass = self.get_argument('rawpass')        email = self.get_argument('user_email')        user_obj = super().get_user_info(super().get_current_user())        if rawpass == user_obj.password:            status = super().change_user_email(user_obj.username, email)            if status:                self.redirect('/user/info')        else:            self.redirect('/user/error')class ChangePassHandler(BaseHandler):    @tornado.web.authenticated    @tornado.web.asynchronous    def get(self):        self.render('user/changepass/changepass.html',                    categories=super().get_categories,                    recent_articles=self.sess.get_recent_article()[0:10],                    username=super().get_current_user(), domain=DOMAIN)    def post(self):        rawpass = self.get_argument('rawpass')        user_pass = self.get_argument('user_pass')        user_pass2 = self.get_argument('user_pass2')        current_user = super().get_current_user()        user_obj = super().get_user_info(current_user)        if user_pass == user_pass2:            if get_md5_string(rawpass) == user_obj.password:                status = super().change_user_passwd(current_user, get_md5_string(user_pass))                if status:                    self.redirect('/user/info')                else:                    self.redirect('/user/error')class LoginHandler(BaseHandler):    @tornado.web.asynchronous    def get(self):        if self.get_secure_cookie('user_name'):            self.redirect('/')        else:            self.render('user/login/login.html',                        recent_articles=self.sess.get_recent_article()[0:10],                        categories=super().get_categories,                        domain=DOMAIN)    @tornado.web.asynchronous    def post(self):        username = self.get_argument('user_name')        password = self.get_argument('user_pass')        user_obj = super().get_user_info(username)        if username == user_obj.username and get_md5_string(password) == user_obj.password:            self.set_secure_cookie('user_name', self.get_argument('user_name'), expires_days=None)            self.redirect('/user/info')        else:            self.redirect('/user/error')class RegistHandler(BaseHandler):    @tornado.web.asynchronous    def get(self):        self.render('user/regist/regist.html',                    recent_articles=self.sess.get_recent_article()[0:10],                    categories=super().get_categories,                    )    def post(self):        username = self.get_argument('user_name')        password = self.get_argument('user_pass')        email = self.get_argument('user_email')        # ret = SqlHelper().regist(username, password, email)        status = super().regist(username, get_md5_string(password), email)        if status:            self.redirect('/user/login')        else:            self.redirect('/user/regist')class ErrorHandler(BaseHandler):    @tornado.web.asynchronous    def get(self):        self.render('user/error/error.html',                    recent_articles=self.sess.get_recent_article()[0:10],                    categories=super().get_categories,                    )class LogoutHandler(BaseHandler):    @tornado.web.asynchronous    def get(self):        self.clear_cookie('user_name')        self.redirect('/user/login')class SearchHandler(BaseHandler):    @tornado.web.asynchronous    def get(self):        keyword = self.get_argument('keyword')        page = self.get_argument('page', default=1)        page = turn_to_int(page, 1)        # 此分类下的所有文章        all_searched_articles = self.sess.search_article_by_keyword(keyword)        # uri的dirname        dir_uri_name = os.path.dirname(self.request.uri) + 'search' + '?keyword=%s&page=' % keyword        count = len(all_searched_articles)        # 检测页数是否合法，如果页数超过        page_obj = PageInfo(page, count, per_item=5)        all_page_count = page_obj.all_page_count        if page > all_page_count:            page = all_page_count        elif page <= 0:            page = 1        page_string = get_method_pager(page, all_page_count, dir_uri_name)        self.render('search/search.html',                    articles=all_searched_articles[page_obj.start:page_obj.end],                    page_string=page_string, keyword=keyword,                    count=count,                    domain=DOMAIN,                    )class AjaxHandler(BaseHandler):    @tornado.web.authenticated    @tornado.web.asynchronous    def post(self, types):        status_success = {'status': True}        status_failure = {'status': False}        if types == 'collect':            article_id = self.get_argument('id')            user = super().get_current_user()            status = self.sess.collect_articles(article_id=article_id, user=user)            if status:                self.write(tornado.escape.json_encode(status_success))                self.finish()            else:                self.write(tornado.escape.json_encode(status_failure))                self.finish()class CollectHandler(BaseHandler):    @tornado.web.authenticated    @tornado.web.asynchronous    def get(self):        self.render('collect/collect.html',                    domain=DOMAIN,                    collections = self.sess.collected_articles(super().get_current_user()).collections,                    )class ArticleHandler(BaseHandler):    @tornado.web.asynchronous    def get(self, page):        page = turn_to_int(page, 1)        # 此分类下的所有文章        all_articles = self.sess.get_all_article()        # uri的dirname        dir_uri_name = os.path.dirname(self.request.uri)        count = self.sess.get_articles_count()        # 检测页数是否合法，如果页数超过        page_obj = PageInfo(page, count, per_item=10)        all_page_count = page_obj.all_page_count        if page > all_page_count:            page = all_page_count        elif page <= 0:            page = 1        page_string = Pager(page, all_page_count, dir_uri_name)        self.render('article/article.html',                    articles=all_articles[page_obj.start:page_obj.end],                    page_string=page_string,                    domain=DOMAIN,                    categories=super().get_categories,                    recent_articles=self.sess.get_recent_article()[0:10],                    )if __name__ == '__main__':    tornado.options.parse_command_line()    settings = {        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),        'static_path': os.path.join(os.path.dirname(__file__), 'static'),        'cookie_secret': 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',        'xsrf_cookies': True,        'debug': True,        'login_url': '/user/login',    }    app = tornado.web.Application(        ui_methods=ui_methods,        handlers=[            (r'/', IndexHandler),            (r'/category/(?P<basename>[0-9a-zA-Z_]+)/(?P<page>-?[0-9]+).html', CategoryHandler),            (r'/user/login', LoginHandler),            (r'/user/regist', RegistHandler),            (r'/user/info', InfoHandler),            (r'/user/logout', LogoutHandler),            (r'/user/error', ErrorHandler),            (r'/user/changeinfo', ChangeInfoHandler),            (r'/user/changepass', ChangePassHandler),            (r'/post/(?P<article_id>\d+).html', PostHandler),            (r'/upload/(.*)', tornado.web.StaticFileHandler, {'path': 'upload'}),            (r'/search', SearchHandler),            (r'/ajax/(?P<types>[0-9a-zA-Z_]+)', AjaxHandler),            (r'/collect/list', CollectHandler),            (r'/article/(?P<page>-?[0-9]+).html', ArticleHandler),        ], **settings    )    http_server = tornado.httpserver.HTTPServer(app)    http_server.listen(options.port)    tornado.ioloop.IOLoop.instance().start()