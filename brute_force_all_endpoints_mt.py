import json
import os
from multiprocessing import Lock

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

LOCK = Lock()


def parallel_function(f, sequence, num_threads=None):
    from multiprocessing import Pool
    pool = Pool(processes=num_threads)
    result = pool.map(f, sequence)
    cleaned = [x for x in result if x is not None]
    pool.close()
    pool.join()
    return cleaned


def forge_brute_force_url(request_id):
    return 'https://itp.ne.jp/{}/genre_dir/'.format(request_id)


def write_to_persistence():
    print('Writing to persistence.')
    with open(PERSISTENCE_FILE, 'w') as w:
        json.dump(obj=ALL_URL_DICT, fp=w, indent=4, ensure_ascii=True)


def main():
    steps = 300
    for i in range(0, 100000, steps):
        all_urls = []
        range_j = range(i, i + steps)
        all_urls.extend([forge_brute_force_url(j) for j in range_j])
        all_urls.extend([forge_brute_force_url('0' + j) for j in range_j])
        all_urls = sorted(list(set(all_urls) - set(ALL_URL_DICT.keys())))

        if len(all_urls) > 0:
            status_codes = parallel_function(process_url, all_urls, num_threads=4)
            for status_code, url in zip(status_codes, all_urls):
                ALL_URL_DICT[url] = status_code
            write_to_persistence()

        try:
            url = forge_brute_force_url(i)
            process_url(url)
            url = forge_brute_force_url('0' + str(i))
            process_url(url)

            if i % 100 == 0:
                write_to_persistence()

        except ConnectionError:
            print('We got blocked!!')
            change_ip()


def process_url(url):
    response = requests.get(url)
    status = (response.status_code == 200)
    print('-> URL = {}, STATUS = {}'.format(url, status))
    return status


if __name__ == '__main__':
    main()
