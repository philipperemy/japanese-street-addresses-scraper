import json
import logging
from glob import glob

from new_scrape import run_scrape


def run():
    files = glob('regions/*.json')
    for json_file in files:
        with open(json_file, 'rb') as j:
            data = json.load(j)
            for region_name, region_data in data.items():
                print(region_name)
                urls = region_data['sub_region']['level_2']
                urls = sorted(list(set(urls)))  # make sure no redundancy.
                for url in urls:
                    logging.info('MAIN - REQUESTING {0}'.format(url))
                    run_scrape(url)


if __name__ == '__main__':
    run()
