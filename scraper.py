import requests
import urllib.request
import time
import pdb
from bs4 import BeautifulSoup

def span_filter(span):
    if len(span.findChildren()) > 1:
        return False
    elif "#" in span.findChildren()[0]["href"]: 
        return False
    else:
        return True



url = "https://www.pagat.com/alpha/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
# pdb.set_trace()

spans = list(filter(span_filter, soup.find_all(class_="lname")))
for span in spans:
    href = span.findChild()['href']
    title = span.findChild().text
    print(title, href)