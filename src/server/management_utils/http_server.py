import json

from flask import Flask, request
from flask_cors import CORS
import http_server_db_handler

http_server = Flask(__name__)
CORS(http_server)
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


def place_holder_response(url):
    response = {
        'app_category': 'kfir',
        'dev_url': 'http://fs.com',
        'num_of_paragraphs': 12,
        'num_of_topics': 5,
        'num_of_missing_paragraphs': 7,
        'num_of_paragraphs_category_value': 12,
        'num_of_topics_category_value': 10,
        'num_of_missing_paragraphs_category_value': 5
    }
    paragraphs_records = db_query_handler.paragraph_by_url_query(url)
    paragraph_list = [dict(paragraph_record) for paragraph_record in paragraphs_records]
    for paragraph_dict in paragraph_list:
        paragraph_dict['index'] = int(paragraph_dict['index'])
        paragraph_dict.pop('id')
        paragraph_dict.pop('privacy_policy_id')
        paragraph_dict.pop('pp_url')
    response['paragraphs'] = paragraph_list
    return response


@http_server.route('/pp-prediction', methods=['GET'])
def get_pp_prediction_by_url():
    url = request.args.get('url', default=None, type=str)
    response = place_holder_response(url)
    return json.dumps(response)

    # TODO: modeling

    # rows = db_query_handler.prediction_query_by_url(url)
    # resp = [dict(row) for row in rows]
    # for response_dict in resp:
    #     response_dict['index'] = int(response_dict['index'])
    # return json.dumps(resp)


if __name__ == '__main__':
    http_server.run(debug=True)
