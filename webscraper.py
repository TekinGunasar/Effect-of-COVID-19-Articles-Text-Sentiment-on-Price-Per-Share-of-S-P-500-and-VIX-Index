import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from pathlib import Path

#Mar 1, 2020 to Oct 27,2020

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}

for file in os.listdir("covid_articles_urls"):
    cur_set_of_urls = open("covid_articles_urls/" + file,'r').readlines()
    cur_date = Path('covid_articles_urls/' + file).stem
    f = open("covid_articles_summaries/" + cur_date + ".txt.txt",'w')
    print(cur_date)
    for url in cur_set_of_urls:
        try:
            req = requests.get(url.strip('\n'),headers=headers)
            src = req.content
            soup = BeautifulSoup(src,'lxml')
            meta_tags = soup.find_all("meta")
            for meta_tag in meta_tags:
                try:
                    if meta_tag.attrs["name"] == "article.summary":
                        f.write(meta_tag.attrs["content"] + "\n")
                except KeyError:
                    pass
        except UnicodeWarning:
            pass
        except UnicodeError:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.URLRequired:
            pass
        except requests.exceptions.TooManyRedirects:
            pass
        except requests.exceptions.InvalidSchema:
            pass
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidURL:
            pass
        except requests.exceptions.ChunkedEncodingError:
            pass
        except requests.exceptions.ContentDecodingError:
            pass
        except requests.exceptions.StreamConsumedError:
            pass
        except requests.exceptions.RetryError:
            pass
        except requests.exceptions.RequestException:
            pass
        except requests.exceptions.BaseHTTPError:
            pass
        except requests.exceptions.BaseHTTPError:
            pass

