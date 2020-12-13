import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

dir = "covid_articles_urls"
for file in os.listdir(dir):
    cur_date = Path('covid_articles_urls/'+file).stem
    print(cur_date)
    cur_set_of_urls = open(dir + "/" + file,'r').readlines()
    f = open("covid_articles_summaries/" + cur_date + ".txt.txt",'w')
    for url in cur_set_of_urls:
        try:
            if requests.get(url.strip('\n'),headers=headers).status_code == 200:
                src = requests.get(url.strip('\n'),headers=headers).content
                soup = BeautifulSoup(src,'lxml')
                meta_tags = soup.find_all('meta')
                for tag in meta_tags:
                    try:
                       if tag.attrs["name"] == "article.summary":
                           f.write(tag.attrs["content"] + '\n')
                           break
                    except KeyError:
                        pass
        except requests.exceptions.MissingSchema:
            pass




