from src.server.utils.db.tools import DBUtils


class PreProcessingDBHandler:

    def __init__(self):
        self.db_util = DBUtils()
        self.url_from_applications_table = "select DISTINCT pp_url from applications where pp_url <> 'none' group by " \
                                           "pp_url "
        # TODO: Add LIMIT and STATUS column filters
        self.pp_pending_200_table = "select id,pp_url,html from privacy_policy where process_status='PENDING' and " \
                                    "url_return_code=200 "

        self.clean_htmls_table = "select id,clean_html,pp_url from privacy_policy where url_return_code=200 and " \
                                 "process_status='HTML_CLEANED' "

        self._update_pp_process_status_str = "UPDATE privacy_policy SET process_status = %s where id=%s"

    def insert_db_http_ok(self, url_record, pp_html):
        db_rows = [[url_record.get("pp_url"), pp_html, "PENDING", "200", "HTTP OK 200"]]
        self.db_util.exec_command("INSERT INTO privacy_policy (pp_url,html,process_status,url_return_code,"
                                  "url_return_value) VALUES (%s,%s,%s,%s,%s)", db_rows)

    def insert_db_no_respond(self, url_record, code, e):
        db_rows = [[url_record.get("pp_url"), "NO_RESPONSE", "{0}".format(code), "{0}".format(e)]]
        self.db_util.exec_command("INSERT INTO privacy_policy (pp_url,process_status,url_return_code,"
                                  "url_return_value) VALUES (%s,%s,%s,%s)", db_rows)

    def update_html_cleaned(self, result, pp_html_record):
        db_rows = [["HTML_CLEANED", "NA", result, pp_html_record.get("id")]]
        self.db_util.exec_command("UPDATE privacy_policy SET process_status = %s,process_status_details = %s, "
                                  "clean_html = %s where id=%s", db_rows)

    def insert_pp_paragraphs(self, db_rows):
        self.db_util.exec_command("INSERT INTO privacy_policy_paragraphs (paragraph,pp_url,index,privacy_policy_id) "
                                  "VALUES (%s,%s,%s,%s)", db_rows)

    def pp_split_ok(self, html_record):
        db_rows = [["PP_SPLITTED_OK", html_record.get("id")]]
        self._update_pp_process_status_query(db_rows)

    def pp_defective(self, html_record):
        db_rows = [["PP_DEFECTIVE", html_record.get("id")]]
        self._update_pp_process_status_query(db_rows)

    def _update_pp_process_status_query(self, db_rows):
        self.db_util.exec_command(self._update_pp_process_status_str, db_rows)
