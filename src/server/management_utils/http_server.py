import json
import http_server_db_handler
from flask import Flask, request
from flask_cors import CORS

from src.server.ml.pre_processing.text_pre_processing_utils import load_pp_html_to_db, clean_pp_html_records, \
    split_or_bypass_pp
from src.server.ml.topic_modeling.pp_topic_modeling import build_from_exists_modeling

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
                       'topic': 0.3} for paragraph_record in paragraphs_records]

    response['paragraphs'] = paragraph_list
    return response


def create_stat_table(paragraph_list, category):
    category_avg_number_of_paragraphs = db_query_handler.get_average_paragraph_count_per_category(category)
    table = [
        {
            'parameter': 'Number of Paragraphs',
            'value': len(paragraph_list),
            'categoryValue': int(category_avg_number_of_paragraphs[0]['avg'])
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
    ]
    return table


def duplicate_count_per_category(url, category, paragraph_model_list):
    duplicates_count = [
        db_query_handler.get_duplicate_paragraphs_per_category(url, category, p['paragraph_text'])[0]['count'] for p
        in paragraph_model_list]
    return sum(duplicates_count)


@http_server.route('/app-categories', methods=['GET'])
def get_app_categories():
    categories = db_query_handler.get_categories()
    return json.dumps(categories)


@http_server.route('/pp-prediction', methods=['GET'])
def get_pp_prediction_by_url():
    url = request.args.get('url', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    url_record_http_ok = load_pp_html_to_db([{'pp_url': url}])

    if url_record_http_ok:
        # http status was 200: OK
        pp_id = url_record_http_ok[0].get('id')[0]
        cleaned_pp_records = clean_pp_html_records(url_record_http_ok)
        split_or_bypass_pp(cleaned_pp_records)
        paragraph_model_list = build_from_exists_modeling(url, pp_id)
        duplicates_count = duplicate_count_per_category(url, category, paragraph_model_list)
        table = create_stat_table(paragraph_model_list, category)
        response = {'table': table, 'duplicates': duplicates_count, 'p': paragraph_model_list}
        return json.dumps(response)
    return 'FAILURE'


if __name__ == '__main__':
    http_server.run(debug=True)
