from src.server.utils.db.tools import DBUtils


class HttpServerDBHandler:

    def __init__(self):
        self.db_util = DBUtils()
        self.main_table_query_str = "SELECT id,html,clean_html,pp_url FROM privacy_policy WHERE pp_url IN (\
                            SELECT pp_url FROM applications WHERE category in (\
                            SELECT category from applications GROUP BY category ORDER BY category ASC ) \
                            GROUP BY pp_url) ORDER BY id"
        self.paragraphs_table_query_str = "SELECT privacy_policy_id,pp_url from privacy_policy_paragraphs" \
                                          " GROUP BY privacy_policy_id,pp_url ORDER BY privacy_policy_id ASC"

    def main_table_query(self):
        return self.db_util.db_select(self.main_table_query_str)

    def clean_html_query(self, pp_id):
        query = "SELECT clean_html FROM privacy_policy WHERE id={0}".format(pp_id)
        return self.db_util.db_select(query)

    def paragraphs_table_query(self):
        return self.db_util.db_select(self.paragraphs_table_query_str)

    def paragraph_by_id_query(self, pp_id):
        query = "SELECT * FROM privacy_policy_paragraphs WHERE privacy_policy_id={0} ORDER BY index ASC".format(pp_id)
        return self.db_util.db_select(query)

    def paragraph_by_url_query(self, url):
        query = "SELECT * FROM privacy_policy_paragraphs WHERE pp_url LIKE \'{0}\' ORDER BY index ASC".format(url)
        return self.db_util.db_select(query)

    def metadata_by_url_query(self, url):
        query = r"SELECT * FROM applications WHERE pp_url LIKE '{0}'".format(url)
        return self.db_util.db_select(query)

    def prediction_query_by_url(self, url):
        query = """SELECT name, developer, category, dev_url, applications.pp_url, index
                    FROM applications, privacy_policy_paragraphs
                    WHERE privacy_policy_paragraphs.pp_url LIKE '{0}'
                    AND name = (SELECT name
                                FROM applications 
                                WHERE pp_url LIKE '{0}' LIMIT 1)
                    AND privacy_policy_paragraphs.pp_url LIKE applications.pp_url""".format(url)
        return self.db_util.db_select(query)
