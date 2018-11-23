import random
import string
import sys
import threading

import play_scraper
from play_scraper import lists

from src.server.utils.db.tools import db_utils


def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def _scrape_category(collection_value, categories):
    for category_value in categories:
        for page in range(400):
            try:
                db_rows = []
                results = play_scraper.collection(collection=collection_value, category=category_value,
                                                  detailed=True, page=page)
                for result in results:
                    url = result.get('developer_url')
                    pp_url = result.get('developer_pp_address')

                    db_row = [result.get('app_id'), result.get('developer_id'), category_value, url, pp_url]
                    db_rows.append(db_row)
                db_utils.exec_command('INSERT INTO applications \
                     (name,developer,category,dev_url, pp_url)\
                     VALUES \
                     (%s,%s,%s,%s,%s)', db_rows)
                # print ("added rows {0} for category {1} collection {2} page {3} ".format(len(db_rows), category_value,
                #                                                                          collection_value, page))
            except:
                # Must NOT print anything to stdout from thread
                pass


def scrape_gplay_to_db_by_search():
    text_file = open("/Users/alonsinger/git/my-privacypolicy-thesis/book1.txt", "r")
    lines = text_file.readlines()
    text_file.close()
    for line_index in range(2649, len(lines)):
        print("word with index {0} = {1}".format(line_index, lines[line_index]))
        try:
            db_rows = []
            results = play_scraper.search(query=lines[line_index])
            for result in results:
                url = result.get('developer_url')
                pp_url = result.get('developer_pp_address')

                db_row = [result.get('app_id'), result.get('developer_id'), result.get('category'), url, pp_url]
                db_rows.append(db_row)
            print("save results: {0}".format(len(results)))
            db_utils.exec_command("INSERT INTO applications \
                 (name,developer,category,dev_url, pp_url)\
                 VALUES \
                 (%s,%s,%s,%s,%s)", db_rows)
        except Exception as e:
            print(e)
            e = sys.exc_info()[0]


def scrape_gplay_to_db():
    categories = play_scraper.categories()
    threads = []
    for collection_value in play_scraper.lists.COLLECTIONS:
        print('fetching for {0}'.format(collection_value))
        try:
            collection_thread = threading.Thread(target=_scrape_category, args=(collection_value, categories,))
            collection_thread.start()
            print('Thread with collection value {0} has started.'.format(collection_value))
            threads.append(collection_thread)
        except threading.ThreadError:
            print('Error starting thread with collection value {0}.'.format(collection_value))

    for collection_thread in threads:
        collection_thread.join()


if __name__ == '__main__':
    scrape_gplay_to_db()
    # scrape_gplay_to_db_by_search()
