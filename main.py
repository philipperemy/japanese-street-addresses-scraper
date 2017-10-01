import json
import logging
import random
from glob import glob

from new_scrape import change_ip
from new_scrape import run_scrape

SEED = 42


def run_random():
    files = glob('regions/*.json')
    all_urls = []
    for json_file in files:
        with open(json_file, 'rb') as j:
            data = json.load(j)
            for region_name, region_data in data.items():
                print(region_name)
                urls = region_data['sub_region']['level_2']
                urls = sorted(list(set(urls)))  # make sure no redundancy.
                all_urls.extend(urls)

    # shuffle !!
    random.seed(SEED)
    random.shuffle(all_urls)
    change_ip()
    query_iterations = 0
    for i, url in enumerate(all_urls):
        if query_iterations % 30 == 1:
            logging.info('IP SWITCHING.')
            change_ip()  # we do not want to fire all our IPs. So lets switch from time to time.
        logging.info('({1}/{2}) MAIN - REQUESTING {0}'.format(url, i, len(all_urls)))
        status = run_scrape(url)
        if status:
            query_iterations += 1


# def run():
#     files = glob('regions/*.json')
#     for json_file in files:
#         with open(json_file, 'rb') as j:
#             data = json.load(j)
#             for region_name, region_data in data.items():
#                 print(region_name)
#                 urls = region_data['sub_region']['level_2']
#                 urls = sorted(list(set(urls)))  # make sure no redundancy.
#                 for i, url in enumerate(urls):
#                     if i % 10 == 0:
#                         logging.info('IP SWITCHING.')
#                         change_ip()  # we do not want to fire all our IPs. So lets switch from time to time.
#                     logging.info('({1}/{2}) MAIN - REQUESTING {0}'.format(url, i, len(urls)))
#                     run_scrape(url)


if __name__ == '__main__':
    run_random()
