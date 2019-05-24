from src.server.utils.db.tools import DBUtils


class CrawlerDBHandler:

    def __init__(self):
        self.db_util = DBUtils()

    def insert_to_application_table(self, db_row):
        self.db_util.exec_command(
            "INSERT INTO applications (name,developer,category,dev_url, pp_url) "
            "SELECT '{0[0]}','{0[1]}','{0[2]}','{0[3]}','{0[4]}' "
            "WHERE NOT EXISTS ("
            "SELECT name FROM applications WHERE name = '{0[0]}');".format(db_row))
