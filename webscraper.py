import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

#Mar 1, 2020 to Oct 27,2020

url_stem = "https://www.wsj.com/news/archive/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}
article_urls = []

start_date = datetime(2020,3,1)
periods=240

date_list = [str(date).split(" ")[0].replace("-","/")
            for date in pd.date_range(start_date, periods=periods).tolist()]

for date in date_list:
    cur_url = url_stem+date
    page_number = 1
    while(requests.get(cur_url+"?page="+str(page_number),headers=headers).status_code == 200 and page_number<=2):
        article_urls.append(cur_url+"?page="+str(page_number))
        print(cur_url+"?page="+str(page_number))
        page_number+=1

f = open("article_urls.txt",'w')
for url in article_urls:
    f.write(url + "\n")

