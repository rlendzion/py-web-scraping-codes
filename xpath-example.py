# use xpath to parse data from a website

from lxml import html
import requests
import numpy as np

# disabled
i = 0
while i > 0:
    url = ('https://allegro.pl/mapa-strony/kategorie')
    page = requests.get(url)
    tree = html.fromstring(page.content)
    cats = tree.xpath('//a[@class="_w7z6o"]/text()')
    a = np.asarray(cats)
    print (np.shape(a))
    a = np.reshape(a, (2044,1)) # reshape to a matrix
    print (np.shape(a))