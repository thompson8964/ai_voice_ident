import re
from bs4 import BeautifulSoup
import requests

def getwebscrapestring(url):
    #url = r"https://realpython.com/python-web-scraping-practical-introduction/#interact-with-html-forms"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)

    return[p.text for p in soup.find_all("p")]
