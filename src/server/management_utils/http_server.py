import json

import http_server_db_handler
from flask import Flask, request

http_server = Flask(__name__)
db_query_handler = http_server_db_handler.HttpServerDBHandler()


@http_server.route('/get-pp')
def home():
    param = request.args.get('url', default=None, type=str)
    paragraphs_records = db_query_handler.paragraph_by_url_query(param)
    paragraph_list = []
    for paragraph_record in paragraphs_records:
        paragraph_list.append(paragraph_record.get('paragraph'))
    response = json.dumps(paragraph_list)
    return response


if __name__ == '__main__':
    http_server.run(debug=True)
