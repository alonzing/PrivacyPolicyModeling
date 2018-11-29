def update_pp_process_status(db_utils, db_rows):
	db_utils.exec_command("UPDATE privacy_policy SET process_status = %s where id=%s", db_rows)

def update_pp_process_status_process_status_details_clean_html(db_utils, db_rows):
	db_utils.exec_command("UPDATE privacy_policy SET \
						 process_status = %s,process_status_details = %s,clean_html = %s \
						 where id=%s", db_rows)


def insert_pp_paragraphs(db_utils, db_rows):
	db_utils.exec_command("INSERT INTO privacy_policy_paragraphs \
                                       (paragraph,pp_url,index,privacy_policy_id) \
                                       VALUES \
                                       (%s,%s,%s,%s)", db_rows)


def insert_pp_url_process_status_url_rerturn_code_return_value(db_utils, db_rows):
	db_utils.exec_command("INSERT INTO privacy_policy \
	            (pp_url,process_status,url_return_code,url_return_value)\
	            VALUES \
	            (%s,%s,%s,%s)", db_rows)


def insert_pp_url_html_process_status_url_return_code_return_value(db_utils, db_rows):
	db_utils.exec_command("INSERT INTO privacy_policy \
	            (pp_url,html,process_status,url_return_code,url_return_value)\
	            VALUES \
	            (%s,%s,%s,%s,%s)", db_rows)


url_from_applications_table = "select pp_url from applications where pp_url <> 'none' and pp_url not in" \
							  "(select pp_url from privacy_policy group by pp_url ) group by pp_url"


pp_pending_200_table = "select id,pp_url,html from privacy_policy where process_status='PENDING' and url_return_code=200"

clean_htmls_table = "select id,clean_html,pp_url from privacy_policy where url_return_code=200 and process_status='HTML_CLEANED'"