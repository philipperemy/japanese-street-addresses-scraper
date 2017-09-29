import json
import logging
import os
import re
from collections import OrderedDict
from time import sleep

import requests
from bs4 import BeautifulSoup
from expressvpn import wrapper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

YELLOW_PAGE_URL = 'https://itp.ne.jp'

ADDRESS_FP = open('/tmp/addresses.txt', 'wb')
NAME_FP = open('/tmp/names.txt', 'wb')
EMAIL_FP = open('/tmp/emails.txt', 'wb')
PERSISTENCE_FILENAME = 'persistence.txt'

USE_VPN = True


# Test also this: https://itp.ne.jp/01100/genre_dir/pg/145/?num=20
# This contains email: https://itp.ne.jp/hokkaido/01100/genre_dir/pg/191/?num=20 - for now we miss it!


class PaginationEndException(Exception):
    pass


def forge_url(prefix, iteration):
    # http://itp.ne.jp/46201/genre_dir/
    # https://itp.ne.jp/aomori/02201/genre_dir/pg/150/?num=20
    return prefix + 'pg/{}/?num=20'.format(iteration)


def write_entry(fp, el, code):
    logging.info(code + ' ' + el)
    el += '\n'
    fp.write(el.encode('utf8'))


def process_one_url(url):
    logging.info('-> {}'.format(url))
    response = requests.get(url)
    sleep(0.1)
    assert response.status_code == 200
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    emails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", str(soup))
    for email in emails:
        write_entry(fp=EMAIL_FP, el=email.strip(), code='MAIL')

    if len(soup.find_all('p', {'class': 'townkunMessageContent'})) > 0:
        raise PaginationEndException()
    results = soup.find_all('div', {'class': 'normalResultsBox'})
    for result in results:

        # NAME PART
        for possible_tag in ['blueText', 'blackText']:
            name_element = result.find('a', {'class': possible_tag})
            if name_element is None:
                continue
            name_element = str(name_element.contents[0]).strip()
            write_entry(fp=NAME_FP, el=name_element, code='NAME')

        # EMAIL PART
        # email_element = result.find('a', {'class': 'boxedLink emailLink'})
        # if email_element is not None:
        #     email_element = email_element.attrs['onclick'].split(',')[-1] \
        #         .replace("'", '').replace(')', '').replace('(', '').strip()
        #     write_entry(fp=EMAIL_FP, el=email_element, code='MAIL')

        # ADDRESS PART
        if '〒' in str(result):
            cons = result.contents[1].contents
            for con in cons:
                if '〒' in str(con):
                    for c in con:
                        if '〒' in str(c):
                            address = str(c.contents[1]).strip()
                            write_entry(fp=ADDRESS_FP, el=address, code='ADDR')
                            # logging.info(address)
                            # address += '\n'
                            # W_FP.write(address.encode('utf8'))
                            break


# process_one_url('https://itp.ne.jp/hokkaido/01100/genre_dir/pg/191/?num=20')


def main():
    # change_ip()
    with open('regions.json', 'rb') as r:
        regions = OrderedDict(json.load(r))

    sub_regions_already_fetched = []
    if os.path.isfile(PERSISTENCE_FILENAME):
        with open(PERSISTENCE_FILENAME, 'rb') as r:
            lines = [v.decode('utf8').strip() for v in r.readlines()]
            sub_regions_already_fetched.extend(lines)

    for region, sub_regions in regions.items():
        logging.info('REGION: {}'.format(region))
        sub_regions_ordered = OrderedDict(sub_regions)
        for sub_region, prefix_urls in sub_regions_ordered['sub_region'].items():

            if sub_region in sub_regions_already_fetched:
                logging.info('SKIPPING: SUB_REGION ALREADY FETCHED {}'.format(sub_region))
                continue

            logging.info('-' * 80)
            logging.info('SUB_REGION: {}'.format(sub_region))
            logging.info(prefix_urls)
            if isinstance(prefix_urls, str):
                prefix_urls = [prefix_urls]
            for prefix_url in prefix_urls:
                try:
                    for iteration in range(1000000):
                        request_url = forge_url(prefix_url, iteration)
                        try:
                            pass
                            process_one_url(request_url)
                        except requests.exceptions.ConnectionError:
                            logging.info('Received a ConnectionError. Will wait 10 seconds, then resume.')
                            change_ip()
                            sleep(10)
                except PaginationEndException:
                    logging.info('PaginationEndException!')
                except Exception as e:
                    ADDRESS_FP.close()
                    raise e

            with open(PERSISTENCE_FILENAME, 'ab+') as w:
                w.write(sub_region.encode('utf8'))
                w.write('\n'.encode('utf8'))
                w.flush()

            logging.info('SUB_REGION DONE: {}'.format(sub_region))
        logging.info('REGION DONE: {}'.format(region))


# process_one_url('https://itp.ne.jp/hokkaido/01100/genre_dir/pg/191/?num=20')
# exit(1)


def change_ip():
    if not USE_VPN:
        return

    max_attempts = 10
    attempts = 0
    while True:
        attempts += 1
        try:
            logging.info('GETTING NEW IP')
            wrapper.random_connect()
            logging.info('SUCCESS')
            return
        except Exception as e:
            if attempts > max_attempts:
                logging.info('Max attempts reached for VPN. Check its configuration.')
                logging.info('Browse https://github.com/philipperemy/expressvpn-python.')
                logging.info('Program will exit.')
                exit(1)
            logging.info(e)
            logging.info('Skipping exception.')


if __name__ == '__main__':
    main()
