import json
import random
import string
import sys
import threading
from multiprocessing.pool import ThreadPool

import play_scraper
from play_scraper import lists

from src.server.utils.db.tools import db_utils


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
                db_row = [str(w).replace('\'', '\'\'') for w in [result.get('app_id'), result.get('developer_id'),
                                                                 result.get('category'), url, pp_url]]

                db_utils.exec_command(
                    "INSERT INTO applications (name,developer,category,dev_url, pp_url) "
                    "SELECT '{0[0]}','{0[1]}','{0[2]}','{0[3]}','{0[4]}' "
                    "WHERE NOT EXISTS ("
                    "SELECT name FROM applications WHERE name = '{0[0]}');".format(db_row))
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
        status_dict[words_file_name] += 1

        print("Current Keyword: {}".format(keyword))
        try:
            results = play_scraper.search(query=keyword)
            for result in results:
                url = result.get('developer_url')
                pp_url = result.get('developer_pp_address')

                # Replaces ' with '' to support strings with ' in SQL queries
                db_row = [str(w).replace('\'', '\'\'') for w in [result.get('app_id'), result.get('developer_id'),
                                                                 result.get('category'), url, pp_url]]
                db_utils.exec_command(
                    "INSERT INTO applications (name,developer,category,dev_url, pp_url) "
                    "SELECT '@{0[0]}', '@{0[1]}', '@{0[2]}', '@{0[3]}', '@{0[4]}' "
                    "WHERE NOT EXISTS ("
                    "SELECT name FROM applications WHERE name = '@{0[0]}' );".format(db_row))

        except Exception as e:
            print(e)
            e = sys.exc_info()[0]


def _on_finished_task(_, collection, category):
    print('Task with collection value {} and category_value {} is done.'.format(collection, category))


def scrape_gplay_to_db(num_of_threads=1):
    from functools import partial

    pool = ThreadPool(num_of_threads)
    categories = play_scraper.categories()
    results = []
    for collection_value in play_scraper.lists.COLLECTIONS:
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
