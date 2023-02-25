

import requests
from bs4 import BeautifulSoup

webpage = requests.get("https://naver.com")

soup = BeautifulSoup(webpage.content,"html.parser")
crawl = soup.select('#NM_THEME_CONTAINER > div.group_topstory > div:nth-of-type(1) > div > a.topstory_info > strong')

for i in crawl:
  print(i.getText())