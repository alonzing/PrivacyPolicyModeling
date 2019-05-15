import json
import random
import string
import threading
import traceback
from multiprocessing.pool import ThreadPool

from modified_play_scraper.lists import CATEGORIES, COLLECTIONS
from src.server.crawler import modified_play_scraper as play_scraper
from src.server.crawler.crawler_db_handler import CrawlerDBHandler
from src.server.utils.db.tools import db_utils

crawler_db_handler = CrawlerDBHandler()


def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def _scrape_category(collection_value, category_value):
    for page in range(400):
        try:
            results = play_scraper.collection(collection=collection_value, category=category_value,
                                              detailed=True, page=page)
            for result in results:
                url = result.get('developer_url')
                pp_url = result.get('developer_pp_address')

                # Replaces ' with '' to support strings with ' in SQL queries
                db_row = [str(result.get('app_id')).replace('\'', '\'\''),
                          str(result.get('developer_id')).replace('\'', '\'\''), result.get(
                        'category')[0], url, pp_url]

                crawler_db_handler.insert_to_application_table(db_row)
        except:
            # Must NOT print anything to stdout from thread
            pass


def scrape_gplay_to_db_by_search(words_file_name):
    status_file_name = 'words_files_status.txt'
    try:
        with open(status_file_name, 'r') as status_file:
            status_dict = json.load(status_file)
    except (IOError, ValueError):
        status_dict = {}

    if words_file_name not in status_dict:
        status_dict[words_file_name] = 0

    text_file = open(words_file_name, "r")
    keywords = [keyword.strip() for keyword in text_file.readlines()[status_dict[words_file_name]:]]
    text_file.close()
    for i, keyword in enumerate(keywords):
        if i % 5 == 0:
            with open(status_file_name, 'w') as status_file:
                json.dump(status_dict, status_file)

        print("Current Keyword: {}".format(keyword))
        try:
            results = play_scraper.search(query=keyword)
            for result in results:
                url = result.get('developer_url')
                pp_url = result.get('developer_pp_address')

                # Replaces ' with '' to support strings with ' in SQL queries
                db_row = [str(result.get('app_id')).replace('\'', '\'\''),
                          str(result.get('developer_id')).replace('\'', '\'\''), result.get(
                        'category')[0], url, pp_url]
                crawler_db_handler.insert_to_application_table(db_row)

        except Exception as e:
            traceback.print_exc()


def _on_finished_task(_, collection, category):
    print('Task with collection value {} and category_value {} is done.'.format(collection, category))


def scrape_gplay_to_db(num_of_threads=1):
    from functools import partial

    # TODO Keep track of progress

    pool = ThreadPool(num_of_threads)
    categories = CATEGORIES
    results = []
    for collection_value in COLLECTIONS:
        for category_value in categories:
            try:
                results.append(pool.apply_async(_scrape_category, (collection_value, category_value),
                                                callback=partial(_on_finished_task, collection=collection_value,
                                                                 category=category_value)))
                # print('An async scraping task with collection value {0} and category_value {1} has been added '
                #       'to the thread pool.'.format(collection_value, category_value))
            except threading.ThreadError:
                print('Error starting thread with collection value {0}.'.format(collection_value))
    pool.close()
    pool.join()


if __name__ == '__main__':
    # scrape_gplay_to_db(1)
    scrape_gplay_to_db_by_search('words.txt')
