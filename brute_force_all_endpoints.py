import json
import os
from time import sleep

import requests
from requests.exceptions import ConnectionError

from scrape import change_ip

YELLOW_PAGE_URL = 'https://itp.ne.jp'

PERSISTENCE_FILE = 'urls.json'

if os.path.isfile(PERSISTENCE_FILE):
    with open(PERSISTENCE_FILE, 'r') as r:
        ALL_URL_DICT = json.load(fp=r)
else:
    ALL_URL_DICT = dict()


def forge_brute_force_url(request_id):
    return 'https://itp.ne.jp/{}/genre_dir/'.format(request_id)


def write_to_persistence():
    print('Writing to persistence.')
    with open(PERSISTENCE_FILE, 'w') as w:
        json.dump(obj=ALL_URL_DICT, fp=w, indent=4, ensure_ascii=True)


def main():
    for i in range(100000):
        print('Iteration {}'.format(i))
        try:
            url = forge_brute_force_url(i)
            process_url(url)
            url = forge_brute_force_url('0' + str(i))
            process_url(url)
            sleep(0.1)

            if i % 100 == 0:
                write_to_persistence()

        except ConnectionError:
            print('We got blocked!!')
            change_ip()


def process_url(url):
    if url in ALL_URL_DICT:
        print('URL = {} already fetched. Skipping.'.format(url))
    else:
        response = requests.get(url)
        status = (response.status_code == 200)
        ALL_URL_DICT[url] = status
        print('-> URL = {}, STATUS = {}'.format(url, status))


if __name__ == '__main__':
    main()
