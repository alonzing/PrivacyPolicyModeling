import cgi
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from src.server.utils.db.tools import db_utils


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        p = self.path.split("?")
        path = p[0][1:].split("/")
        params = {}
        if len(p) > 1:
            params = cgi.parse_qs(p[1], True, True)

        if path[0] == '':
            ret_html = '<html><table border=\'1\'>{0}</table></html>'
            query = "select id,html,clean_html,pp_url from privacy_policy where pp_url in (\
                            select pp_url from applications where category in (\
                            select category from applications where category like '%GAME%' group by category order by category asc ) \
                            group by pp_url) order by id"
            url_records = db_utils.db_select(query)
            main_table = "<tr><td>Application ID</td><td>URL</td><td>View</td></tr>"
            for url_record in url_records:
                main_table += "<tr><td>{0}</td><td><a href='{1}'>{1}</a></td><td><a href='/view_html?id={2}'>View Clean</a></td></tr>".format(
                    url_record.get('id'),
                    url_record.get('pp_url'),
                    url_record.get('id'))

            self.wfile.write(ret_html.format(main_table))
        elif path[0] == 'view_html':
            query = "select clean_html from privacy_policy where id={0}".format(params['id'][0])
            url_records = db_utils.db_select(query)
            self.wfile.write(url_records[0]['clean_html'])
        elif path[0] == 'show_paragraphs_and_pp':
            ret_html = '<html><table border=\'1\'>{0}</table></html>'
            query = "select privacy_policy_id,pp_url from privacy_policy_paragraphs group by privacy_policy_id,pp_url order by privacy_policy_id asc"
            url_records = db_utils.db_select(query)
            main_table = "<tr><td>Privacy Policy ID</td><td>URL</td><td>View</td></tr>"
            for url_record in url_records:
                main_table += "<tr><td>{0}</td><td><a href='{1}'>{1}</a></td><td><a href='/view_pp_and_paragraphs?id={2}'>View Paragraphs</a></td></tr>".format(
                    url_record.get('privacy_policy_id'),
                    url_record.get('pp_url'),
                    url_record.get('privacy_policy_id'))
            self.wfile.write(ret_html.format(main_table))
        elif path[0] == 'show_defective_pp':
            None
        elif path[0] == 'view_pp_and_paragraphs':
            ret_html = '<html><table border=\'1\'>{0}</table></html>'
            query = "select * from privacy_policy_paragraphs where privacy_policy_id={0} order by index asc".format(
                params['id'][0])
            paragraphs_records = db_utils.db_select(query)
            main_table = "<tr><td>Paragraph #</td><td>Paragraph Text</td></tr>"
            for paragraph_record in paragraphs_records:
                main_table += "<tr><td>{0}</td><td>{1}</td></tr>".format(
                    paragraph_record.get('index'),
                    paragraph_record.get('paragraph'))
            self.wfile.write(ret_html.format(main_table))

        else:
            self.wfile.write("ERROR")


server = HTTPServer(('', 8080), RequestHandler)

server.serve_forever();
