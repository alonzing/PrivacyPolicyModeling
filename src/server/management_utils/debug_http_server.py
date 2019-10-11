import cgi
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import http_server_db_handler
from http_server_html_generator import HttpServerHTMLGenerator


class RequestHandler(BaseHTTPRequestHandler):
    """
    This class is for more convenient debugging.
    Used to see if the split to paragraphs worked as expected.
    """
    def __init__(self, request, client_address, server):
        self.db_query_handler = http_server_db_handler.HttpServerDBHandler()
        self.id_param_dict = {'view_html': self.view_html,
                              'view_pp_and_paragraphs': self.view_pp_and_paragraphs}
        self.no_param_dict = {'show_paragraphs_and_pp': self.show_paragraphs_and_pp}
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def view_html(self, pp_id):
        url_records = self.db_query_handler.clean_html_query(pp_id)
        # self.wfile.write(url_records[0]['clean_html'])
        ret_html = '<html><head><meta charset="utf-8"/></head>{0}</html>'
        self.wfile.write(ret_html.format(url_records[0]['clean_html']))

    def show_paragraphs_and_pp(self):
        url_records = self.db_query_handler.paragraphs_table_query()
        ret_html, main_table = HttpServerHTMLGenerator.generate_main_paragraphs_table(url_records)
        self.wfile.write(ret_html.format(main_table))

    def view_pp_and_paragraphs(self, pp_id):
        paragraphs_records = self.db_query_handler.paragraph_by_id_query(pp_id)
        ret_html, main_table = HttpServerHTMLGenerator.generate_show_paragraphs(paragraphs_records)
        self.wfile.write(ret_html.format(main_table))

    def main_pp_table(self):
        url_records = self.db_query_handler.main_table_query()
        ret_html, main_table = HttpServerHTMLGenerator.generate_main_table(url_records)
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


http_server = HTTPServer(('', 8181), RequestHandler)

http_server.serve_forever()
