import cgi
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import http_server_db_queries

from src.server.utils.db.tools import db_utils


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.id_param_dict = {'view_html': self.view_html,
                              'view_uncleaned_html': self.view_uncleaned_html,
                              'view_pp_and_paragraphs': self.view_pp_and_paragraphs}
        self.no_param_dict = {'show_paragraphs_and_pp': self.show_paragraphs_and_pp}
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def view_html(self, pp_id):
        query = http_server_db_queries.clean_html_query(pp_id)
        url_records = db_utils.db_select(query)
        # self.wfile.write(url_records[0]['clean_html'])
        self.wfile.write(url_records[0])

    def view_uncleaned_html(self, pp_id):
        query = "select html from privacy_policy where id={0}".format(pp_id)
        url_records = db_utils.db_select(query)
        self.wfile.write(url_records[0])

    def show_paragraphs_and_pp(self):
        ret_html = '<html><table border=\'1\'>{0}</table></html>'
        url_records = db_utils.db_select(http_server_db_queries.paragraphs_table_query)
        main_table = "<tr><td>Privacy Policy ID</td><td>URL</td><td>View</td></tr>"
        for url_record in url_records:
            main_table += "<tr><td>{0}</td><td><a href='{1}'>{1}</a></td><td><a href='/view_pp_and_paragraphs?id={2}'>View Paragraphs</a></td></tr>".format(
                url_record.get('privacy_policy_id'),
                url_record.get('pp_url'),
                url_record.get('privacy_policy_id'))
        self.wfile.write(ret_html.format(main_table))

    def view_pp_and_paragraphs(self, pp_id):
        ret_html = '<html><table border=\'1\'>{0}</table></html>'
        query = http_server_db_queries.paragraph_query(pp_id)
        paragraphs_records = db_utils.db_select(query)
        main_table = "<tr><td>Paragraph #</td><td>Paragraph Text</td></tr>"
        for paragraph_record in paragraphs_records:
            main_table += "<tr><td>{0}</td><td>{1}</td></tr>".format(
                paragraph_record.get('index'),
                paragraph_record.get('paragraph'))
        self.wfile.write(ret_html.format(main_table))

    def main_pp_table(self):
        ret_html = '<html><table border=\'1\'>{0}</table></html>'
        url_records = db_utils.db_select(http_server_db_queries.main_table_query)
        main_table = "<tr><td>Application ID</td><td>URL</td><td>View</td><td>View HTML</td></tr>"
        for url_record in url_records:
            main_table += "<tr>" \
                          "<td>{0}</td>" \
                          "<td><a href='{1}'>{1}</a></td>" \
                          "<td><a href='/view_html?id={2}'>View Clean</a></td>" \
                          "<td><a href='/view_uncleaned_html?id={3}'>View HTML</a></td></tr>" \
                .format(url_record.get('id'),
                        url_record.get('pp_url'),
                        url_record.get('id'),
                        url_record.get('id'))
        self.wfile.write(ret_html.format(main_table))

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        p = self.path.split("?")
        path = p[0][1:].split("/")
        params = {}
        if len(p) > 1:
            params = cgi.parse_qs(p[1], True, True)
        if path[0] in self.id_param_dict:
            self.id_param_dict[path[0]](params['id'][0])
        elif path[0] in self.no_param_dict:
            self.no_param_dict[path[0]]()
        else:
            self.main_pp_table()


http_server = HTTPServer(('', 8080), RequestHandler)

http_server.serve_forever()
