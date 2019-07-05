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

def complete_links(span):
    return span.findChild()['href'].replace('..', 'https://www.pagat.com')

def content_filter(content):
    # what do we need to do in terms of preventing a bunch of garbage ending up in our data?
    return True

def content_manipulation(content):
    # placeholder for any manipulation we need to do to content
    return content.text



url = "https://www.pagat.com/alpha/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
# pdb.set_trace()

spans = filter(span_filter, soup.find_all(class_="lname"))
game_links = map(complete_links, spans)
# print(list(game_links))

# for span in spans:
#     href = span.findChild()['href']
#     title = span.findChild().text
#     print(title, href)
    # need to go to the link and get the text from there.

for link in list(game_links)[0:2]:
    game_response = requests.get(link)
    game_soup = BeautifulSoup(game_response.text, "html.parser")
    title = game_soup.findChildren('h1')[0].text.strip()

    text = ''
    content = game_soup.find_all(class_="mainContent")[0]
    content_parts = map(content_manipulation, filter(content_filter, content.findChildren()))
    for text_item in content_parts:
        text = text + text_item

    # now we have just a big old text dump we can put somewhere.