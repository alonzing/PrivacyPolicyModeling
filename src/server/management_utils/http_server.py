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


def create_stat_table(paragraph_list, category):
    category_avg_number_of_paragraphs = db_query_handler.get_average_paragraph_count_per_category(category)
    topic_count = len(set([int(p['topic']) for p in paragraph_list]))
    table = [
        {
            'parameter': 'Number of Paragraphs',
            'value': len(paragraph_list),
            'categoryValue': int(category_avg_number_of_paragraphs[0]['avg'])
        },
        {
            'parameter': 'Number of Topics',
            'value': topic_count,
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
    result = db_query_handler.get_categories()
    categories = [cat[0] for cat in result]
    return json.dumps(categories)


@http_server.route('/pp-prediction', methods=['GET'])
def get_pp_prediction_by_url():
    url = request.args.get('url', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    pp_id_query_result = db_query_handler.is_pp_url_in_privacy_policy_table(url)

    if len(pp_id_query_result) > 0:
        print('URL in DB')
        paragraph_model_list = build_from_exists_modeling(url, pp_id_query_result[0][0])
        duplicates_count = duplicate_count_per_category(url, category, paragraph_model_list)
        table = create_stat_table(paragraph_model_list, category)
        response = {'table': table, 'duplicates': duplicates_count, 'p': paragraph_model_list, 'score': 50}
        return json.dumps(response)
    else:
        print('URL not in DB')
        # URL not in DB
        url_record_http_ok = load_pp_html_to_db([{'pp_url': url}])
        if url_record_http_ok:
            # http status was 200: OK
            pp_id = url_record_http_ok[0].get('id')[0]
            cleaned_pp_records = clean_pp_html_records(url_record_http_ok)
            split_or_bypass_pp(cleaned_pp_records)
            paragraph_model_list = build_from_exists_modeling(url, pp_id)
            duplicates_count = duplicate_count_per_category(url, category, paragraph_model_list)
            table = create_stat_table(paragraph_model_list, category)
            response = {'table': table, 'duplicates': duplicates_count, 'p': paragraph_model_list, 'score': 50}
            return json.dumps(response)

    return 'FAILURE'


if __name__ == '__main__':
    http_server.run(host='0.0.0.0', debug=True)
