

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

        self._pp_pending_200_table = "select id,pp_url,html from privacy_policy where process_status='{}' and " \
                                     "url_return_code=200 ".format(PENDING)

        self._clean_html_files = "select id,clean_html,pp_url from privacy_policy where url_return_code=200 and " \
                                 "process_status='{}' and " \
                                 "not(process_status='{}' or process_status='{}') ".format(HTML_CLEANED, PP_SPLIT_OK,
                                                                                           PP_SPLIT_FAILED)

        self._update_pp_process_status_str = "UPDATE privacy_policy SET process_status = %s where id=%s"
        self._update_is_new = "UPDATE applications SET is_new = false where pp_url=%s"

    def sql_get_cleaned_html_files(self, limit=None):
        return self._clean_html_files if not limit \
            else self._clean_html_files + ' limit {}'.format(limit)

    def sql_get_urls_from_applications_table(self, limit=None):
        return self._url_from_applications_table if not limit \
            else self._url_from_applications_table + ' limit {}'.format(limit)

    def sql_get_pending_raw_html_files_from_privacy_policy_table(self, limit=None):
        return self._pp_pending_200_table if not limit \
            else self._pp_pending_200_table + ' limit {}'.format(limit)

    def update_application_not_new(self, url_records):
        db_rows = []
        for url_record in url_records:
            db_rows.append([url_record[0]])
        self.db_util.exec_command(self._update_is_new, db_rows)

    def insert_db_http_ok(self, pp_url, pp_html):
        return self.db_util.exec_command_with_result("""INSERT INTO privacy_policy (pp_url,html,process_status,url_return_code,"""
                                  """url_return_value) VALUES (%s,%s,%s,%s,%s) RETURNING id """, (pp_url, pp_html, PENDING, "200", HTTP_OK_200))

    def insert_db_no_respond(self, db_no_responds):
        db_rows = []
        for db_no_respond in db_no_responds:
            db_rows.append([db_no_respond[0], NO_RESPONSE, "{}".format(db_no_respond[1]), "{}".format(db_no_respond[2])])
        self.db_util.exec_command("INSERT INTO privacy_policy (pp_url,process_status,url_return_code,"
                                  "url_return_value) VALUES (%s,%s,%s,%s)", db_rows)

    def update_html_cleaned(self, result_records):
        db_rows = []
        for result_record in result_records:
            db_rows.append([HTML_CLEANED, NA, result_record.get("clean_html"), result_record.get("id")])
        self.db_util.exec_command("UPDATE privacy_policy SET process_status = %s,process_status_details = %s, "
                                  "clean_html = %s where id=%s", db_rows)

    def insert_pp_paragraphs(self, db_rows):
        self.db_util.exec_command("INSERT INTO privacy_policy_paragraphs (paragraph,pp_url,index,privacy_policy_id) "
                                  "VALUES (%s,%s,%s,%s)", db_rows)

    def pp_split_ok(self, html_records):
        self._update_pp_process_status_query(html_records, PP_SPLIT_OK)

    def pp_split_failed(self, html_records):
        self._update_pp_process_status_query(html_records, PP_SPLIT_FAILED)

    def pp_defective(self, html_records):
        self._update_pp_process_status_query(html_records, PP_DEFECTIVE)

    def _update_pp_process_status_query(self, html_records, status):
        db_rows = []
        for html_record in html_records:
            db_rows.append([status, html_record.get("id")])
        self.db_util.exec_command(self._update_pp_process_status_str, db_rows)
