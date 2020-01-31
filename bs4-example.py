# use html.parser to parse data from a website

from bs4 import BeautifulSoup
import requests

# disabled
i = 0
while i > 0:
    url = "https://allegro.pl/mapa-strony/kategorie"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    for i in soup.findAll('a', {"class" : "_w7z6o"}):
        print(i.get('title'))