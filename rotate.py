import requests
from bs4 import BeautifulSoup
from conf.settings import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.common import get_datetime

url = "https://www.oschina.net/news"
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'referer': 'https://www.oschina.net/'
}

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
session = Session()

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content.decode(), 'html.parser')

for item in soup.select('div[class="item clear"]'):
    try:
        title, img_src, article_src, desc = item.div.a.get_text(), item.div.a['href'], item.img['src'], \
                                            item.find_all("div", class_="sc text text-gradient summary")[0].get_text()
    except IndexError as e:
        title, img_src, article_src, desc = item.div.a.get_text(), item.div.a['href'], item.img['src'], \
                                            item.find_all("div", class_="summary")[0].get_text()
    except Exception as e:
        pass
    cur = engine.execute(
        "insert into rotates (title, description, img_src, article_src, pub_date) values (%s, %s, %s, %s, %s)",
        [(title, desc, img_src, article_src, get_datetime())]
    )
