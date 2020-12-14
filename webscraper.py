import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os

#Mar 1, 2020 to Oct 27,2020
url_stem = "https://www.wsj.com/news/archive/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

for file in os.listdir("covid_articles_urls"):
    print(file)
    cur_set_of_urls = open("covid_articles_urls/" + file,'r').readlines()
    f = open("covid_articles_urls/" + file,'w')
    open("covid_articles_urls/" + file,'w').close()
    for url in cur_set_of_urls:
        if url.startswith("https://"):
            f.write(url)

