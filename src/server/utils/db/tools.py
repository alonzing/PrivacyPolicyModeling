import logging
import sys
import time
import traceback

import psycopg2
import psycopg2.extras

working_db_name = "postgres"
working_db_host = "localhost"
working_db_user = "postgres"
working_db_password = "1"


class DBUtils:
    def __init__(self):
        pass

    def get_db_connection(self):
        conn = None
        count = 0
        try:
            conn = psycopg2.connect(
                    "dbname='{}' user='{}' host='{}' password='{}'".format(working_db_name, working_db_user,
                                                                             working_db_host, working_db_password))
            time.sleep(1)
            return conn
        except:
            while conn is None and count < 10:
                try:
                    conn = psycopg2.connect(
                        "dbname='{}' user='{}' host='{}' password='{}'".format(working_db_name, working_db_user,
                                                                                 working_db_host, working_db_password))
                except:
                    time.sleep(1)
                    count += 1
            if conn is None:
                uinput = raw_input("Postgres is down, press to continue...")
                while True:
                    if uinput == ' ':
                        break
                    uinput = raw_input("")
                return self.get_db_connection()

    def exec_command(self, sql, value_list=None):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            if value_list is None:
                cur.execute(sql, value_list)
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

    def exec_command_with_result(self, sql, value_list=None):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute(sql, value_list)
            result = cur.fetchall()
            cur.close()
            conn.commit()
        except Exception as e:
            print(e)
            logging.exception(sys.exc_info()[0])
        finally:
            if conn is not None:
                conn.close()
        return result

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
                conn.close()


db_utils = DBUtils()
