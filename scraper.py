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
        return f"\n<{content.text.lower().replace(' ', '-')}>"
    return content.text



url = "https://www.pagat.com/alpha/"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
# pdb.set_trace()

spans = filter(span_filter, soup.find_all(class_="lname"))
game_links = map(complete_links, spans)


with open('card_games.csv', mode='w') as card_games:
    employee_writer = csv.writer(card_games, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for link in list(game_links)[0:2]:
        game_response = requests.get(link)
        game_soup = BeautifulSoup(game_response.text, "html.parser")
        title = game_soup.findChildren('h1')[0].text.strip()

        text = ''
        content = game_soup.find_all(class_="mainContent")[0]
        content_parts = map(content_manipulation, filter(content_filter, content.findChildren()))
        for text_item in content_parts:
            text = text + text_item

        employee_writer.writerow([f'\n\n<title>{title}</title>', text])