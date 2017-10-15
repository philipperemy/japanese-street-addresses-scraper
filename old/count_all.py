import json
import re

import requests
from bs4 import BeautifulSoup

all_count = 0

with open('regions.json', 'rb') as r:
    regions = json.load(r)
    all_sub_region_list = sum([list(v['sub_region'].values()) for v in list(regions.values())], [])
    for sub_region in all_sub_region_list:
        response = requests.get(sub_region)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, 'html.parser')
        h1 = soup.find('h1', {'class': 'searchResultHeader'})
        new_inc = int(re.findall(r'\d+', str(h1.contents[1]))[0])
        all_count += new_inc
        print(new_inc, all_count)
print('FINAL', all_count)
