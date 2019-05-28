import logging
import sys
import time
import traceback

import psycopg2
import psycopg2.extras
import psycopg2.pool


working_db_name = "postgres"
working_db_host = "localhost"
working_db_user = "postgres"
working_db_password = "1"


class DBUtils:
    def __init__(self):
        self.pool = psycopg2.pool.ThreadedConnectionPool(1, 6, user=working_db_user, password=working_db_password, host=working_db_host, database=working_db_name)

    def get_db_connection(self):
        try:
            conn = self.pool.getconn()
            time.sleep(1)
            return conn
        except:
            uinput = raw_input("Postgres is down, press to continue...")
            while True:
                if uinput == ' ':
                    break
                uinput = raw_input("")
            self.pool = psycopg2.pool.ThreadedConnectionPool(1, 6, user=working_db_user, password=working_db_password,
                                                             host=working_db_host, database=working_db_name)
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
            self.pool.putconn(conn)
        except Exception as e:
            print(e)
            logging.exception(sys.exc_info()[0])
        # finally:
        #     if conn is not None:
        #         conn.close()

    def exec_command_with_result(self, sql, value_list=None):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute(sql, value_list)
            result = cur.fetchall()
            cur.close()
            conn.commit()
            self.pool.putconn(conn)
        except Exception as e:
            print(e)
            logging.exception(sys.exc_info()[0])
        # finally:
        #     if conn is not None:
        #         conn.close()
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
            self.pool.putconn(conn)
            return rows
        except:
            logging.exception(sys.exc_info()[0])
        # finally:
        #     if conn is not None:
        #         conn.close()


db_utils = DBUtils()
