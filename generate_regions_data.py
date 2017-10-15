import json
import os
from glob import glob

import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

from core_scraper import change_ip

YELLOW_PAGE_URL = 'https://itp.ne.jp'
OUTPUT_DIR = 'regions'


def get_soup(url):
    response = requests.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_soup_vpn(url):
    try:
        return get_soup(url)
    except:
        change_ip()
        try:
            return get_soup(url)
        except:
            print('ERROR COULD NOT FETCH THIS URL {0}'.format(url))
            return None


def get_sub_sub_region(sub_region_url):
    soup = get_soup_vpn(sub_region_url)

    if soup is None:
        return []

    refine_block = [b for b in soup.find_all('div', {'class': 'refineBlock'}) if 'address_narrowing' in str(b)]
    if len(refine_block) == 0:
        return []
    refine_block = refine_block[0]
    links = [a.attrs['href'] for a in refine_block.find_all('a')]
    links = list(filter(lambda x: x.startswith('/'), links))
    links = [YELLOW_PAGE_URL + link for link in links]
    return links


def get_sub_regions(region_url):
    soup = get_soup_vpn(region_url)
    resp = dict()

    if soup is None:
        return resp

    all_links_1 = [a.attrs['href'] for a in soup.find('section', {'class': 'Japamap'}).find_all('a')]
    all_links_1 = sorted(list(filter(lambda x: 'http' in x, all_links_1)))
    all_links_2 = []
    for link in all_links_1:
        print('-> {} [from the map]'.format(link))
        links_found = get_sub_sub_region(link)
        # print('Found links {}'.format(links_found))
        all_links_2.extend(links_found)
    resp['level_1'] = all_links_1
    resp['level_2'] = sorted(list(set(all_links_2)))
    print('Found {0} links for level 1.'.format(len(all_links_1)))
    print('Found {0} links for level 2.'.format(len(all_links_2)))
    return resp


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    json_regions = [v.split('/')[1].split('.')[0] for v in glob(OUTPUT_DIR + '/*.json')]
    soup = get_soup_vpn(YELLOW_PAGE_URL)
    regions = soup.find('div', {'class': 'txt-table'}).find_all('a')
    for region in regions:
        print('-' * 80)
        if not isinstance(region, NavigableString):
            region_name = str(region.contents[0])
            output = {}
            if region_name not in json_regions:
                url = YELLOW_PAGE_URL + str(region.attrs['href'])
                print(region_name, url)
                sub_regions = get_sub_regions(region_url=url)
                output[region_name] = dict()
                output[region_name]['url'] = url
                output[region_name]['sub_region'] = sub_regions

                with open(OUTPUT_DIR + '/{}.json'.format(region_name), 'wb') as w:
                    w.write(json.dumps(output, ensure_ascii=False, indent=4).encode('utf8'))
            else:
                print('REGION ALREADY FETCHED = {0}'.format(region_name))


if __name__ == '__main__':
    main()
