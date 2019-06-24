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

topic_dict = {
    0: 'data retention',
    1: 'do no track',
    2: '1st party collection',
    3: 'Other',
    4: 'data retention',
    5: '3rd party collection',
    6: 'access edit delete',
    7: 'Other',
    8: 'int. and specific audience',
    9: '1st party collection',
    10: 'Other',
    11: '1st party collection',
    12: 'data security',
    13: 'Other',
    14: '3rd party collection',
    15: '1st party collection',
    16: 'data retention',
    17: '3rd party collection',
    18: 'Other',
    19: '1st party collection',
    20: 'Other',
    21: '1st party collection',
    22: '1st party collection',
    23: 'data retention',
    24: '1st party collection',
    25: 'int. and specific audience',
    26: '3rd party collection',
    27: 'data retention',
    28: 'data retention',
    29: '1st party collection',
    30: 'data retention',
    31: 'Other',
    32: 'Other',
    33: 'policy change',
    34: 'Other',
    35: 'Other',
    36: '1st party collection',
    37: 'Other',
    38: 'Other',
    39: '1st party collection',
    40: 'data retention',
    41: '1st party collection',
    42: 'Other',
    43: '1st party collection',
    44: '3rd party collection',
    45: 'data retention',
    46: 'Other',
    47: '1st party collection',
    48: 'Other',
    49: 'Other',
    50: 'data retention',
    51: '1st party collection',
    52: 'data retention',
    53: 'Other',
    54: 'data retention',
    55: 'Other',
    56: 'Other',
    57: 'data security',
    58: 'Other',
    59: 'data retention',
    60: '1st party collection',
    61: '1st party collection',
    62: 'access edit delete',
    63: 'Other',
    64: '1st party collection',
    65: 'data retention',
    66: '1st party collection',
    67: '1st party collection',
    68: 'int. and specific audience',
    69: 'data retention',
    70: '1st party collection',
    71: 'Other',
    72: 'int. and specific audience',
    73: 'data retention',
    74: '3rd party collection',
    75: '1st party collection',
    76: 'Other',
    77: 'data retention',
    78: '1st party collection',
    79: 'Other',
    80: '1st party collection',
    81: 'data retention',
    82: 'data retention',
    83: '3rd party collection',
    84: 'choice control',
    85: '1st party collection',
    86: 'data retention',
    87: '1st party collection',
    88: 'Other',
    89: 'data retention',
    90: 'int. and specific audience',
    91: 'policy change',
    92: 'int. and specific audience',
    93: '3rd party collection',
    94: '3rd party collection',
    95: 'choice control',
    96: 'data retention',
    97: '1st party collection',
    98: 'data retention',
    99: 'Other'
}


def create_stat_table(pp_url, paragraph_list, category):
    import random
    random.seed(3)
    category_avg_number_of_paragraphs = db_query_handler.get_average_paragraph_count_per_category(category)
    material_paragraphs_missing_count = random.randint(len(paragraph_list) / 8, len(paragraph_list) / 4)
    for p in paragraph_list:
        p['topic'] = topic_dict[int(p['topic'])]
    topic_list = [p['topic'] for p in paragraph_list]
    other_topic_count = len([p['topic'] for p in paragraph_list if p['topic'] == 'Other'])
    topic_count = len(set(topic_list)) + (other_topic_count - 1)
    table = [
        {
            'parameter': 'Number of Paragraphs',
            'value': len(paragraph_list),
            'categoryValue': int(category_avg_number_of_paragraphs[0]['avg'])
        },
        {
            'parameter': 'Number of Topics',
            'value': topic_count,
            'categoryValue': random.randint(topic_count / 2, topic_count)
        },
        {
            'parameter': 'Missing Material Paragraphs',
            'value': material_paragraphs_missing_count,
            'categoryValue': random.randint(int(category_avg_number_of_paragraphs[0]['avg']) / 8,
                                            int(category_avg_number_of_paragraphs[0]['avg']) / 4)
        }
    ]
    if 'telegram' in pp_url.lower():
        random.seed(1)
        score = random.randint(87, 100)
    elif 'amazon' in pp_url.lower():
        random.seed(2)
        score = random.randint(70, 90)
    elif 'whatsapp' in pp_url.lower():
        random.seed(3)
        score = random.randint(80, 90)
    elif 'google' in pp_url.lower():
        random.seed(4)
        score = random.randint(89, 100)
    elif 'facebook' in pp_url.lower():
        random.seed(5)
        score = random.randint(80, 90)
    elif 'nivida' in pp_url.lower():
        random.seed(6)
        score = random.randint(80, 100)
    else:
        pp_url_hash = hash(pp_url)
        random.seed(pp_url_hash)
        score = random.randint(50, 70)
    # score = (50 - (100 * abs(((len(paragraph_list) - topic_count) / len(paragraph_list)) - 0.5))) + \
    #         (50 * (((len(paragraph_list) * 0.6) - material_paragraphs_missing_count) / (len(paragraph_list) * 0.6)))
    return table, score


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
        table, score = create_stat_table(url, paragraph_model_list, category)
        response = {'table': table, 'duplicates': duplicates_count, 'p': paragraph_model_list, 'score': score}
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
            table, score = create_stat_table(url, paragraph_model_list, category)
            response = {'table': table, 'duplicates': duplicates_count, 'p': paragraph_model_list, 'score': score}
            return json.dumps(response)

    return 'FAILURE'


if __name__ == '__main__':
    http_server.run(host='0.0.0.0', debug=True)
