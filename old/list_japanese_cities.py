import requests
from bs4 import BeautifulSoup

response = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_Japan')

assert response.status_code == 200

soup = BeautifulSoup(response.content, 'html.parser')

for tr in soup.find_all('tr'):
    r = tr.contents
    if len(r) == 17:
        try:
            english_name = r[1].contents[0].contents[0]
            japanese_name = r[3].contents[0].contents[0].contents[0]
            print(english_name, japanese_name)
        except:
            pass
