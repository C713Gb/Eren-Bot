
import requests
from bs4 import BeautifulSoup as soup
import json

class Article(object):
  def __init__(self, link, author, headline, description, date, image):
    self.link = link
    self.author = author
    self.headline = headline
    self.description = description
    self.date = date
    self.image = image

  def __str__(self):
    return "Article \nlink: %s \nauthor: %s \nheadline: %s \ndescription: %s \ndate: %s \nimage: %s" % (self.link, self.author, self.headline, self.description, self.date, self.image) 

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
session = requests.Session()
session.headers['User-Agent'] = USER_AGENT

URL = "https://techcrunch.com/category/startups/"

def techcrunchApiCall():
  html = session.get(URL).text
  soup_result = soup(html,'html.parser')

  content = soup_result.find(id="root")

  list = content.div.div.div.div

  list = list.findAll('div', attrs={'class':'post-block post-block--image post-block--unread'})

  # print('There are {0} articles'.format(len(list)))

  for item in list:
    link = item.header.h2.a['href']
    author = item.div.a.text.strip()
    headline = item.header.h2.a.text.strip()
    date = item.header.time.text.strip()
    desc = item.find('div', attrs={'class':'post-block__content'}).text.strip()
    image = item.footer.figure.img['src']
    article = jsonToArticle(json.dumps({
      'link': link,
      'author': author,
      'headline': headline,
      'date': date,
      'description': desc,
      'image': image
    }))
    print(article)
    break
    
def jsonToArticle(data):
  j = json.loads(data)
  article = Article(**j)
  return article

# techcrunchApiCall()