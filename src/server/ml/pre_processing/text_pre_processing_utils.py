import re
import string
import urllib2

from bs4 import BeautifulSoup
from goose import Goose
from nltk.tokenize.texttiling import TextTilingTokenizer
from HTMLParser import HTMLParser

from src.server.ml.pre_processing import pre_processing_db_quries
from src.server.utils.db.tools import db_utils

punc_reg = re.compile('[%s]' % re.escape(string.punctuation))


def load_pp_html_to_db():
    url_records = db_utils.db_select(pre_processing_db_quries.url_from_applications_table)
    for url_record in url_records:
        try:
            pp_html = urllib2.urlopen(url_record.get("pp_url"), timeout=2).read().decode('utf-8')
            db_rows = []
            db_row = [url_record.get("pp_url"), pp_html, "PENDING", "200", "HTTP OK 200"]
            db_rows.append(db_row)
            pre_processing_db_quries.insert_pp_url_html_process_status_url_return_code_return_value(db_utils, db_rows)

        except Exception as e:
            print(e)
            code = -1;
            db_rows = []
            if hasattr(e, 'code'):
                code = e.code
            db_row = [url_record.get("pp_url"), "NO_RESPONSE", "{0}".format(code), "{0}".format(e)]
            db_rows.append(db_row)
            pre_processing_db_quries.insert_pp_url_process_status_url_rerturn_code_return_value(db_utils, db_rows)


def clean_pp_html(url, pp_html):
    ret_val = ''
    try:
        print("processing the following url {}".format(url))
        g = Goose()
        ret_val = g.extract(raw_html=pp_html).cleaned_text
    except Exception as e:
        print(e)

    if ret_val == '':
        try:
            soup = BeautifulSoup(pp_html)
            ret_val = soup.body.get_text()
        except Exception as ee:
            print(ee)
    return ret_val


def clean_pp_html_records():
    pp_html_records = db_utils.db_select(pre_processing_db_quries.pp_pending_200_table)
    for pp_html_record in pp_html_records:
        result = clean_pp_html(pp_html_record.get("pp_url"), pp_html_record.get("html"))
        db_rows = [["HTML_CLEANED", "NA", result, pp_html_record.get("id")]]
        pre_processing_db_quries.update_pp_process_status_process_status_details_clean_html(db_utils, db_rows)


def split_or_bypass_pp():
    pp_html_records = db_utils.db_select(pre_processing_db_quries.clean_htmls_table)
    for html_record in pp_html_records:
        try:
            clean_pp = html_record.get("clean_html")
            is_defective = is_defective_pp(clean_pp)
            if not is_defective:
                pqragraphs = split_pp_to_paragraphs(clean_pp)
                db_rows = []
                for i, paragraph in enumerate(pqragraphs):
                    db_row = [paragraph.strip(), html_record.get("pp_url"), i, html_record.get("id")]
                    db_rows.append(db_row)
                pre_processing_db_quries.insert_pp_paragraphs(db_utils, db_rows)

                db_rows = [["PP_SPLITTED_OK", html_record.get("id")]]
                pre_processing_db_quries.update_pp_process_status(db_utils, db_rows)

            else:
                db_rows = [["PP_DEFECTIVE", html_record.get("id")]]
                pre_processing_db_quries.update_pp_process_status(db_utils, db_rows)
        except Exception as e:
            print e


def is_defective_pp(clean_pp):
    low_text = clean_pp.lower()
    if 'privacy' not in low_text or 'function(' in low_text or 'function (' in low_text or 'catch(' in low_text or 'exception(' in low_text \
            or '{' in low_text or 'personnelles' in low_text or 'voor' in low_text or 'servicios' in low_text \
            or 'maggior' in low_text or 'posizione' in low_text or 'werden' in low_text:
        return True
    else:
        return False


def split_pp_to_paragraphs(clean_pp):
    ttt = TextTilingTokenizer()
    paragraphs = ttt.tokenize(clean_pp)
    return paragraphs


# db_utils.exec_command("TRUNCATE privacy_policy, privacy_policy_paragraphs, privacy_policy_paragraphs_prediction")
# load_pp_html_to_db()
clean_pp_html_records()
split_or_bypass_pp()
