import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

#Mar 1, 2020 to Oct 27,2020

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

urls = [line.split('\n')[0] for line in open("page_urls.txt",'r').readlines()]

keywords = ["covid","coronavirus","ventilator","virus","covid","covid-19","cases","ventilators"
            "pandemic","containment","spread","vaccine","epidemic","social","quarantine"
            "distancing","mask","face-masks","masks","lockdown"]

for url in urls:
    print(url)
    date_split = url.split("/")
    year = month = date_split[len(date_split)-3]
    month = date_split[len(date_split)-2]
    day = date_split[len(date_split)-1].split("?")[0]
    f = open("covid_articles/" + year + "-" + month + "-" + day + ".txt",'w')
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')
    links = soup.find_all("a")
    for link in links:
        try:
            if len(link.attrs['class']) == 0:
                article_title = link.text.lower()
                for word in article_title.split(" "):
                    if word in keywords:
                        f.write(link.attrs['href']+'\n')
                        break
        except:
            pass




