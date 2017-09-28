import json

import requests
from bs4 import BeautifulSoup

YELLOW_PAGE_URL = 'https://itp.ne.jp'
BIG_ADDRESS_FILENAME = 'addresses.txt'

W_FP = open(BIG_ADDRESS_FILENAME, 'wb')


class PaginationEndException(Exception):
    pass


def forge_url(prefix, iteration):
    # http://itp.ne.jp/46201/genre_dir/
    # https://itp.ne.jp/aomori/02201/genre_dir/pg/150/?num=20
    return prefix + 'genre_dir/pg/{}/?num=20'.format(iteration)


def process_one_url(url):
    print('->', url)
    response = requests.get(url)
    assert response.status_code == 200
    content = response.content
    if '申し訳ございません' in str(content):  # https://itp.ne.jp/aomori/02201/genre_dir/pg/300/?num=20
        return PaginationEndException()
    soup = BeautifulSoup(content, 'html.parser')
    results = soup.find_all('div', {'class': 'normalResultsBox'})
    for result in results:
        address = str(result.contents[1].contents[3].contents[7].contents[1]) + '\n'
        print(address)
        W_FP.write(address.encode('utf8'))
        # do something here


def main():
    with open('regions.json', 'rb') as r:
        regions = json.load(r)

        for region, sub_regions in regions.items():
            print(region)
            for sub_region, prefix_url in sub_regions.items():
                print(sub_region)
                print(prefix_url)

                try:
                    for iteration in range(1000000):
                        request_url = forge_url(prefix_url, iteration)
                        process_one_url(request_url)
                except PaginationEndException:
                    pass
                except Exception as e:
                    raise e


if __name__ == '__main__':
    main()
