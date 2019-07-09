import requests
import urllib.request
import time
import pdb
import csv
from bs4 import BeautifulSoup

def span_filter(span):
    children = span.findChildren()
    if len(children) > 1:
        return False
    if "#" in children[0]["href"]: 
        return False
    
    type_col = span.findParent().findParent().find_all(class_='col3')[0]
    if len(type_col.findChildren()) < 1:
        return False
    elif span.findParent().findParent().find_all(class_='col3')[0].findChildren()[0]['title'] == 'French suited cards':
        return True

def complete_links(span):
    return span.findChild()['href'].replace('..', 'https://www.pagat.com')

def content_filter(content):
    # what do we need to do in terms of preventing a bunch of garbage ending up in our data?
    if content.name == 'h1' or content.name == 'ul':
        return False
    return True

def content_manipulation(content):
    if content.name == 'h2':
        return f"\n<{kabobify(content.text)}>"
    return content.text

def kabobify(text):
    return text.lower().replace(' ', '-').replace(',', '').replace('/', '')

url = "https://www.pagat.com/alpha/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
# pdb.set_trace()

spans = list(filter(span_filter, soup.find_all(class_="lname")))
game_links = list(map(complete_links, spans))
# pdb.set_trace()

for link in game_links:
    game_response = requests.get(link)
    game_soup = BeautifulSoup(game_response.content, "html.parser")
    title = game_soup.findChildren('h1')[0].text.strip()

    text = ''
    content = game_soup.find_all(class_="mainContent")[0]
    content_parts = map(content_manipulation, filter(content_filter, content.findChildren()))
    for text_item in content_parts:
        text = text + text_item
    
    with open(f"card-games/{kabobify(title)}.txt", mode='w') as card_game:
        csv_writer = csv.writer(card_game, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([f"<title>{title}</title>", text])