import json

import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

YELLOW_PAGE_URL = 'https://itp.ne.jp'


def get_soup(url):
    response = requests.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_sub_sub_region(sub_region_url):
    soup = get_soup(sub_region_url)
    refine_block = [b for b in soup.find_all('div', {'class': 'refineBlock'}) if 'address_narrowing' in str(b)]
    if len(refine_block) == 0:
        return []
    refine_block = refine_block[0]
    links = [a.attrs['href'] for a in refine_block.find_all('a')]
    links = list(filter(lambda x: x.startswith('/'), links))
    links = [YELLOW_PAGE_URL + link for link in links]
    return links


def get_sub_regions(region_url, include_all_sub_regions=True):
    soup = get_soup(region_url)
    all_links_1 = [a.attrs['href'] for a in soup.find('section', {'class': 'Japamap'}).find_all('a')]
    all_links_1 = sorted(list(filter(lambda x: 'http' in x, all_links_1)))
    resp = dict()
    all_links_2 = []
    for link in all_links_1:
        all_links_2.extend(get_sub_sub_region(link))
    resp['level_1'] = all_links_1
    resp['level_2'] = all_links_2
    print('Found {0} links for level 1'.format(len(all_links_1)))
    print('Found {0} links for level 2'.format(len(all_links_2)))
    return resp


def main(include_all_sub_regions=True, output_filename='region.json'):
    response = requests.get(YELLOW_PAGE_URL)
    assert response.status_code == 200
    regions_dict = dict()
    soup = BeautifulSoup(response.content, 'html.parser')
    regions = soup.find('div', {'class': 'txt-table'}).find_all('a')
    for region in regions:
        print('-' * 80)
        if not isinstance(region, NavigableString):
            region_name = str(region.contents[0])
            url = YELLOW_PAGE_URL + str(region.attrs['href'])
            print(region_name, url)
            sub_regions = get_sub_regions(region_url=url, include_all_sub_regions=include_all_sub_regions)
            regions_dict[region_name] = dict()
            regions_dict[region_name]['url'] = url
            regions_dict[region_name]['sub_region'] = sub_regions

    with open(output_filename, 'wb') as w:
        w.write(json.dumps(regions_dict, ensure_ascii=False, indent=4).encode('utf8'))


if __name__ == '__main__':
    main(include_all_sub_regions=True, output_filename='region.json')
