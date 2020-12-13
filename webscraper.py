import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

#Mar 1, 2020 to Oct 27,2020

url_stem = "https://www.wsj.com/news/archive/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

urls = [line.split('\n')[0] for line in open("article_urls.txt",'r').readlines()]

test_url = urls[0]
result = requests.get(test_url,headers=headers)
src = result.content
soup = BeautifulSoup(src,'lxml')
links = soup.find_all("a")

for link in links:
    try:
        if len(link.attrs['class']) == 0:
            print(link.attrs['href'])
    except KeyError:
        pass


