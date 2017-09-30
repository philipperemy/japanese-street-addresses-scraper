import logging
import os
import re
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup
from expressvpn import wrapper
from slugify import slugify

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PERSISTENCE_FILENAME = 'persistence.txt'

USE_VPN = True


# Test also this: https://itp.ne.jp/01100/genre_dir/pg/145/?num=20
# This contains email: https://itp.ne.jp/hokkaido/01100/genre_dir/pg/191/?num=20 - for now we miss it!

def mkdir_p(directory_name):
    import os
    import errno

    # the actual code
    try:
        os.makedirs(directory_name)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(directory_name):
            pass


class PaginationEndException(Exception):
    pass


def forge_url(prefix, iteration):
    # http://itp.ne.jp/46201/genre_dir/
    # https://itp.ne.jp/aomori/02201/genre_dir/pg/150/?num=20
    return prefix + 'pg/{}/?num=50'.format(iteration)


def write_entry(fp, el, code):
    logging.info(code + ' ' + el)
    el += '\n'
    fp.write(el.encode('utf8'))
    fp.flush()


def process_one_url(url, address_fp, name_fp, email_fp):
    logging.info('-> {}'.format(url))
    response = requests.get(url)
    sleep(0.1)
    assert response.status_code == 200
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    emails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", str(soup))
    for email in emails:
        write_entry(fp=email_fp, el=email.strip(), code='MAIL')

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
            write_entry(fp=name_fp, el=name_element, code='NAME')

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
                            write_entry(fp=address_fp, el=address, code='ADDR')
                            # logging.info(address)
                            # address += '\n'
                            # W_FP.write(address.encode('utf8'))
                            break


def main(main_url):
    slug = slugify(main_url)
    main_dir = os.path.expanduser('~/Desktop/data/{}/'.format(slug))
    mkdir_p(main_dir)

    with open('{}/addresses.txt'.format(main_dir), 'wb') as address_fp:
        with open('{}/names.txt'.format(main_dir), 'wb') as name_fp:
            with open('{}/emails.txt'.format(main_dir), 'wb') as email_fp:
                for iteration in range(1000000):
                    request_url = forge_url(main_url, iteration)
                    try:
                        process_one_url(request_url, address_fp, name_fp, email_fp)
                        with open(PERSISTENCE_FILENAME, 'a+') as w:
                            w.write(request_url + '\n')
                            w.flush()
                    except requests.exceptions.ConnectionError:
                        logging.error('Received a ConnectionError. Will change IP, wait 10 seconds, then resume.')
                        change_ip()
                        sleep(10)
                    except PaginationEndException:
                        logging.info('No more pages to scrape. Program will end successfully.')
                        break


# process_one_url('https://itp.ne.jp/hokkaido/01100/genre_dir/pg/191/?num=20')


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
    if len(sys.argv) != 2:
        logging.error('Please specify a sub region url as a parameter. '
                      'For example:﻿https://itp.ne.jp/mie/24441/genre_dir/')
        exit(1)
    main(sys.argv[1])
