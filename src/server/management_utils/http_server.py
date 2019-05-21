import json

from psycopg2.extras import DictRow

import http_server_db_handler
from flask import Flask, request

from src.server.ml.pre_processing.text_pre_processing_utils import load_pp_html_to_db, clean_pp_html_records, \
    split_or_bypass_pp, insert_single_pp_html_to_db

http_server = Flask(__name__)
db_query_handler = http_server_db_handler.HttpServerDBHandler()


@http_server.route('/pp-paragraphs', methods=['GET'])
def get_pp_paragraphs_by_url():
    url = request.args.get('url', default=None, type=str)
    paragraphs_records = db_query_handler.paragraph_by_url_query(url)
    paragraph_list = [dict(paragraph_record) for paragraph_record in paragraphs_records]
    for response_dict in paragraph_list:
        response_dict['index'] = int(response_dict['index'])
    response = json.dumps(paragraph_list)
    return response


@http_server.route('/pp-metadata', methods=['GET'])
def get_metadata_by_url():
    url = request.args.get('url', default=None, type=str)
    metadata = db_query_handler.metadata_by_url_query(url)
    return json.dumps(metadata)


def place_holder_response(url):
    response = {
        'table': [
            {
                'parameter': 'Number of Paragraphs',
                'value': 12,
                'categoryValue': 12
            },
            {
                'parameter': 'Number of Topics',
                'value': 5,
                'categoryValue': 10
            },
            {
                'parameter': 'Missing Material Paragraphs',
                'value': 7,
                'categoryValue': 5
            }
        ],
        'score': 5
    }
    paragraphs_records = db_query_handler.paragraph_by_url_query(url)
    paragraph_list = [{'index': int(paragraph_record['index']),
                       'value': paragraph_record['paragraph'],
                       'score': 0.3} for paragraph_record in paragraphs_records]
    response['paragraphs'] = paragraph_list
    return response


@http_server.route('/pp-prediction', methods=['GET'])
def get_pp_prediction_by_url():
    url = request.args.get('url', default=None, type=str)
    url_record_http_ok = load_pp_html_to_db([{'pp_url': url}])

    if url_record_http_ok:
        # http status was 200: OK
        cleaned_pp_records = clean_pp_html_records(url_record_http_ok)
        split_or_bypass_pp(cleaned_pp_records)
    return json.dumps(place_holder_response(url))
    # response = place_holder_response(url)
    # return json.dumps(response)


if __name__ == '__main__':
    http_server.run(debug=True)