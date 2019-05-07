import json

import http_server_db_handler
from flask import Flask, request

http_server = Flask(__name__)
db_query_handler = http_server_db_handler.HttpServerDBHandler()


@http_server.route('/pp-paragraphs', methods=['GET'])
def get_pp_paragraphs_by_url():
    url = request.args.get('url', default=None, type=str)
    paragraphs_records = db_query_handler.paragraph_by_url_query(url)
    paragraph_list = [paragraph_record.get('paragraph') for paragraph_record in paragraphs_records]
    response = json.dumps(paragraph_list)
    return response


@http_server.route('/pp-metadata', methods=['GET'])
def get_metadata_by_url():
    url = request.args.get('url', default=None, type=str)
    metadata = db_query_handler.metadata_by_url_query(url)
    return json.dumps(metadata)


@http_server.route('/pp-prediction', methods=['GET'])
def get_pp_prediction_by_url():
    url = request.args.get('url', default=None, type=str)
    rows = db_query_handler.prediction_query_by_url(url)
    resp = [dict(row) for row in rows]
    for response_dict in resp:
        response_dict['index'] = int(response_dict['index'])
    return json.dumps(resp)


if __name__ == '__main__':
    http_server.run(debug=True)
