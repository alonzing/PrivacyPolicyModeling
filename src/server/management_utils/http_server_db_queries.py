main_table_query = "SELECT id,html,clean_html,pp_url FROM privacy_policy WHERE pp_url IN (\
                            SELECT pp_url FROM applications WHERE category in (\
                            SELECT category from applications GROUP BY category ORDER BY category ASC ) \
                            GROUP BY pp_url) ORDER BY id"


def clean_html_query(pp_id):
    return "SELECT clean_html from privacy_policy WHERE id={0}".format(pp_id)


paragraphs_table_query = "SELECT privacy_policy_id,pp_url from privacy_policy_paragraphs" \
                   " GROUP BY privacy_policy_id,pp_url ORDER BY privacy_policy_id ASC"


def paragraph_query(pp_id):
    return "SELECT * from privacy_policy_paragraphs WHERE privacy_policy_id={0} ORDER BY index ASC".format(pp_id)
