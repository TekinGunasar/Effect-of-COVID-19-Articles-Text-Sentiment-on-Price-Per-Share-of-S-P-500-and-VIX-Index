import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

dir = "covid_articles_urls"
for file in os.listdir(dir):
    f = open("covid_articles_summaries/" + file+".txt",'w+')



