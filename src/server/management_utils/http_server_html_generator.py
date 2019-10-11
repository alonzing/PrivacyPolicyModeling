class HttpServerHTMLGenerator:
    """
    Generates the HTML for the debug_http_server.
    """
    def __init__(self):
        pass

    @staticmethod
    def generate_main_table(url_records):
        ret_html = '<html><head><meta charset="utf-8"/></head><table border=\'1\'>{0}</table></html>'
        main_table = "<tr><td>Application ID</td><td>URL</td><td>View</td></tr>"
        for url_record in url_records:
            main_table += "<tr>" \
                          "<td>{0}</td>" \
                          "<td><a href='{1}'>{1}</a></td>" \
                          "<td><a href='/view_html?id={2}'>View Clean</a></td></tr>".format(url_record.get('id'),
                                                                                            url_record.get('pp_url'),
                                                                                            url_record.get('id'))
        return ret_html, main_table

    @staticmethod
    def generate_show_paragraphs(paragraphs_records):
        ret_html = '<html><head><meta charset="utf-8"/></head><table border=\'1\'>{0}</table></html>'
        main_table = "<tr><td>Paragraph #</td><td>Paragraph Text</td></tr>"
        for paragraph_record in paragraphs_records:
            main_table += "<tr><td>{0}</td><td>{1}</td></tr>".format(
                paragraph_record.get('index'),
                paragraph_record.get('paragraph'))
        return ret_html, main_table

    @staticmethod
    def generate_main_paragraphs_table(url_records):
        ret_html = '<html><head><meta charset="utf-8"/></head><table border=\'1\'>{0}</table></html>'
        main_table = "<tr><td>Privacy Policy ID</td><td>URL</td><td>View</td></tr>"
        for url_record in url_records:
            main_table += "<tr>" \
                          "<td>{0}</td>" \
                          "<td><a href='{1}'>{1}</a></td>" \
                          "<td><a href='/view_pp_and_paragraphs?id={2}'>View Paragraphs</a></td>" \
                          "</tr>"\
                .format(url_record.get('privacy_policy_id'), url_record.get('pp_url'),
                        url_record.get('privacy_policy_id'))
        return ret_html, main_table
