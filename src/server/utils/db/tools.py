import logging
import sys
import psycopg2
import psycopg2.extras
import traceback

working_db_name = "postgres"
working_db_host = "localhost"
working_db_user = "postgres"
working_db_password = "1234"


class DBUtils:

    def __init__(self):
        pass

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                "dbname='{}' user='{}' host='{}' password='{}'".format(working_db_name, working_db_user,
                                                                       working_db_host, working_db_password))
            return conn
        except:
            traceback.print_exc()
            logging.error(sys.exc_info()[0])

    def exec_command(self, sql, value_list=None):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            if value_list is None:
                cur.execute(sql)
            else:
                cur.executemany(sql, value_list)
            cur.close()
            conn.commit()
        except Exception as e:
            print(e)
            logging.exception(sys.exc_info()[0])
        finally:
            if conn is not None:
                conn.close()

    def db_select(self, sql, value_list=None):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            if value_list is None:
                cur.execute(sql)
            else:
                cur.execute(sql, value_list)
            rows = cur.fetchall()
            return rows
        except:
            logging.exception(sys.exc_info()[0])
        finally:
            if conn is not None:
                conn.close


db_utils = DBUtils()