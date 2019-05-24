

# Statuses
from src.server.utils.db.tools import DBUtils

HTTP_OK_200 = 'HTTP OK 200'
HTML_CLEANED = 'HTML_CLEANED'
PENDING = 'PENDING'
PP_DEFECTIVE = 'PP_DEFECTIVE'
PP_SPLIT_OK = 'PP_SPLIT_OK'
NO_RESPONSE = 'NO_RESPONSE'
NA = 'NA'
PP_SPLIT_FAILED = 'PP_SPLIT_FAILED'


class PreProcessingDBHandler:

    def __init__(self):
        self.db_util = DBUtils()
        self._url_from_applications_table = "select DISTINCT pp_url from applications where pp_url <> 'none' and " \
                                            "is_new = true group by pp_url "

        # TODO: Add LIMIT and STATUS column filters
        self._pp_pending_200_table = "select id,pp_url,html from privacy_policy where process_status='{}' and " \
                                     "url_return_code=200 ".format(PENDING)

        self._clean_html_files = "select id,clean_html,pp_url from privacy_policy where url_return_code=200 and " \
                                 "process_status='{}' and " \
                                 "not(process_status='{}' or process_status='{}') ".format(HTML_CLEANED, PP_SPLIT_OK,
                                                                                           PP_SPLIT_FAILED)

        self._update_pp_process_status_str = "UPDATE privacy_policy SET process_status = %s where id=%s"
        self._update_is_new = "UPDATE applications SET is_new = false where pp_url='{}'"

    def sql_get_cleaned_html_files(self, limit=None):
        return self._clean_html_files if not limit \
            else self._clean_html_files + ' limit {}'.format(limit)

    def sql_get_urls_from_applications_table(self, limit=None):
        return self._url_from_applications_table if not limit \
            else self._url_from_applications_table + ' limit {}'.format(limit)

    def sql_get_pending_raw_html_files_from_privacy_policy_table(self, limit=None):
        return self._pp_pending_200_table if not limit \
            else self._pp_pending_200_table + ' limit {}'.format(limit)

    def update_application_not_new(self, url_record):
        self.db_util.exec_command(self._update_is_new.format(url_record))

    def insert_db_http_ok(self, pp_url, pp_html):
        return self.db_util.exec_command_with_result("""INSERT INTO privacy_policy (pp_url,html,process_status,url_return_code,"""
                                  """url_return_value) VALUES (%s,%s,%s,%s,%s) RETURNING id """, (pp_url, pp_html, PENDING, "200", HTTP_OK_200))

    def insert_db_no_respond(self, pp_url, code, e):
        db_rows = [[pp_url, NO_RESPONSE, "{}".format(code), "{}".format(e)]]
        self.db_util.exec_command("INSERT INTO privacy_policy (pp_url,process_status,url_return_code,"
                                  "url_return_value) VALUES (%s,%s,%s,%s)", db_rows)

    def update_html_cleaned(self, result, pp_html_record):
        db_rows = [[HTML_CLEANED, NA, result, pp_html_record.get("id")]]
        self.db_util.exec_command("UPDATE privacy_policy SET process_status = %s,process_status_details = %s, "
                                  "clean_html = %s where id=%s", db_rows)

    def insert_pp_paragraphs(self, db_rows):
        self.db_util.exec_command("INSERT INTO privacy_policy_paragraphs (paragraph,pp_url,index,privacy_policy_id) "
                                  "VALUES (%s,%s,%s,%s)", db_rows)

    def pp_split_ok(self, html_record):
        db_rows = [[PP_SPLIT_OK, html_record.get("id")]]
        self._update_pp_process_status_query(db_rows)

    def pp_split_failed(self, html_record):
        db_rows = [[PP_SPLIT_FAILED, html_record.get("id")]]
        self._update_pp_process_status_query(db_rows)

    def pp_defective(self, html_record):
        db_rows = [[PP_DEFECTIVE, html_record.get("id")]]
        self._update_pp_process_status_query(db_rows)

    def _update_pp_process_status_query(self, db_rows):
        self.db_util.exec_command(self._update_pp_process_status_str, db_rows)

