
import re
import tornado.escape

def date(object, t):
    """
    返回datetime.datetime类型的日期
    :param object:
    :param t:
    :return:
    """
    return t.date()


def format_content(object, content, keyword):
    """
    搜索时高亮关键字
    :param object:
    :param content:
    :param keyword:
    :return:
    """
    content=str(content)
    content = re.sub(r'</?\w+[^>]*>','',content)
    tmp = content.split(keyword)
    format_string = '<b class="match term0">%s</b>' % keyword

    res=''
    for num in tmp:
        if not tmp.index(num) + 1 == len(tmp):
            res += num[-20:] + format_string + tmp[tmp.index(num)+1][0:20] + '...'
        else:
            res += num[-20:]
    return tornado.escape.xhtml_unescape(res)

def length(object, alist):
    return len(alist)


from modules.sqlhelper import SqlHelper
def next_article(object, article_id):
    """
    返回当前文章的上篇文章ID
    :param object:
    :param article_id:
    :return:
    """
    return SqlHelper().get_next_article_byid(article_id)

def last_article(object, article_id):
    """
    返回当前文章的下篇文章ID
    :param object:
    :param article_id:
    :return:
    """
    return SqlHelper().get_last_article_byid(article_id)