import json

import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

YELLOW_PAGE_URL = 'https://itp.ne.jp'


def get_sub_regions_from_main_tab(soup, class_name='region47', tag='li'):
    sub_region_dict = dict()
    for li in soup.find('div', {'class': class_name}).find_all(tag, {'class': 'list-btn'}):
        sub_url = li.contents[0].attrs['href']
        sub_name = str(li.contents[0].contents[0])
        print('->', sub_name, sub_url)
        sub_region_dict[sub_name] = sub_url
    print('Found {0} for this region.'.format(len(sub_region_dict)))
    return sub_region_dict


def get_sub_regions(region_url):
    response = requests.get(region_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, 'html.parser')
    # return get_sub_regions_from_main_tab(soup, 'region47', 'li')
    return get_sub_regions_from_main_tab(soup, 'area-all', 'p')


def main():
    response = requests.get(YELLOW_PAGE_URL)
    assert response.status_code == 200
    regions_dict = dict()
    soup = BeautifulSoup(response.content, 'html.parser')
    regions = soup.find('div', {'class': 'txt-table'}).find_all('a')
    for region in regions:
        if not isinstance(region, NavigableString):
            region_name = str(region.contents[0])
            url = YELLOW_PAGE_URL + str(region.attrs['href'])
            print(region_name, url)
            sub_regions = get_sub_regions(region_url=url)
            regions_dict[region_name] = dict()
            regions_dict[region_name]['url'] = url
            regions_dict[region_name]['sub_region'] = sub_regions

    with open('regions.json', 'wb') as w:
        w.write(json.dumps(regions_dict, ensure_ascii=False, indent=4).encode('utf8'))


if __name__ == '__main__':
    main()
