import requests
from bs4 import BeautifulSoup

url = "https://www.oschina.net/news"
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'referer': 'https://www.oschina.net/'
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content.decode(), 'html.parser')

for item in soup.select('div[class="item clear"]'):
    try:
        print(item.div.a.get_text(), item.div.a['href'], item.img['src'],
              item.find_all("div", class_="sc text text-gradient summary")[0].get_text())
    except IndexError as e:
        print(item.div.a.get_text(), item.div.a['href'], item.img['src'],
              item.find_all("div", class_="summary")[0].get_text())
    except Exception as e:
        pass
