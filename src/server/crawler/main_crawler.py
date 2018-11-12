import sys

import play_scraper
import random
import string

from src.server.utils.db.tools  import db_utils


def init_applications_table():
    db_utils.exec_command("DROP TABLE applications")
    db_utils.exec_command(
        "CREATE TABLE applications (id serial not null primary key, name text, developer text, category name, dev_url text , pp_url text )")


def id_generator(size=6, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def scrape_gplay_to_db_by_search():
    text_file = open("/Users/alonsinger/git/my-privacypolicy-thesis/book1.txt", "r")
    lines = text_file.readlines()
    text_file.close()
    for line_ind in range(2649, len(lines)):
        print("word with index {0} = {1}".format(line_ind, lines[line_ind]))
        try:
            db_rows = []
            results = play_scraper.search(query=lines[line_ind])
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
            # print ("added rows {0} for category {1} collection {2} page {3} ".format(len(db_rows),category_value, collection_value,page))
        except Exception as e:
            print(e)
            e = sys.exc_info()[0]


def scrape_gplay_to_db():
    categories = play_scraper.categories()
    for collection_value in play_scraper.lists.COLLECTIONS:
        print("fetching for {0}".format(collection_value))
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
                    db_utils.exec_command("INSERT INTO applications \
                         (name,developer,category,dev_url, pp_url)\
                         VALUES \
                         (%s,%s,%s,%s,%s)", db_rows)
                    # print ("added rows {0} for category {1} collection {2} page {3} ".format(len(db_rows),category_value, collection_value,page))
                except Exception as e:
                    print(e)
                    e = sys.exc_info()[0]


# init_applications_table()
# scrape_gplay_to_db()
scrape_gplay_to_db_by_search()

#