import re
import string
import urllib2

from langid.langid import LanguageIdentifier, model
from BeautifulSoup import BeautifulSoup
from goose import Goose
from nltk.tokenize.texttiling import TextTilingTokenizer
from src.server.ml.pre_processing.pre_processing_db_handler import PreProcessingDBHandler
from src.server.utils.db.tools import db_utils
from unidecode import unidecode
from src.server.ml.pre_processing.contractions_dict import ContractionsDict

punc_reg = re.compile('[%s]' % re.escape(string.punctuation))
db_handler = PreProcessingDBHandler()
special_cases = string.punctuation + string.digits


def load_pp_html_to_db():
    url_records = db_utils.db_select(db_handler.url_from_applications_table)
    for url_record in url_records:
        try:
            pp_html = urllib2.urlopen(url_record.get("pp_url"), timeout=5).read().decode('utf-8')
            db_handler.insert_db_http_ok(url_record, pp_html)
        except Exception as e:
            print(e)
            code = -1
            if hasattr(e, 'code'):
                code = e.code
            db_handler.insert_db_no_respond(url_record, code, e)


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
            ret_val = soup.body.getText()
        except Exception as ee:
            print(ee)
    return ret_val


def clean_pp_html_records():
    pp_html_records = db_utils.db_select(db_handler.pp_pending_200_table)
    for pp_html_record in pp_html_records:
        result = clean_pp_html(pp_html_record.get("pp_url"), pp_html_record.get("html"))
        if is_defective_pp(result):
            db_handler.pp_defective(pp_html_record)
        else:
            db_handler.update_html_cleaned(result, pp_html_record)


def split_or_bypass_pp():
    pp_html_records = db_utils.db_select(db_handler.clean_htmls_table)
    # preparing for the expansion of contractions
    contractions_dict = dict((re.escape(k.lower()), v) for k, v in ContractionsDict.contractions.iteritems())
    pattern = re.compile("|".join(contractions_dict.keys()), re.IGNORECASE)
    for html_record in pp_html_records:
        try:
            clean_pp = html_record.get("clean_html")
            paragraphs = split_pp_to_paragraphs(clean_pp, contractions_dict, pattern)
            db_rows = []
            for i, paragraph in enumerate(paragraphs):
                db_rows.append([paragraph.strip(), html_record.get("pp_url"), i, html_record.get("id")])
            db_handler.insert_pp_paragraphs(db_rows)
            db_handler.pp_splitted_ok(html_record)

        except Exception as e:
            print e


def is_defective_pp(clean_pp):
    low_text = clean_pp.lower()
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    language_detect = identifier.classify(clean_pp)
    if language_detect[0] != "en" or (language_detect[0] == "en" and language_detect[1] < 0.9) or \
            'privacy' not in low_text or 'class=' in low_text or 'function(' in low_text or \
            'function (' in low_text or 'catch(' in low_text or 'exception(' in low_text \
            or '{' in low_text or low_text is None:
        return True
    else:
        return False


def split_pp_to_paragraphs(clean_pp, contractions_dict, pattern):
    clean_pp = clean_pp_advanced(clean_pp, contractions_dict, pattern)
    ttt = TextTilingTokenizer()
    paragraphs = ttt.tokenize(clean_pp)
    return paragraphs


def clean_pp_advanced(clean_pp, contractions_dict, pattern):
    # Converting non-ascii to their nearest ascii code
    clean_pp_unicode = clean_pp.decode("utf-8")
    clean_pp = unidecode(clean_pp_unicode)
    # Expansion of contractions
    clean_pp = pattern.sub(lambda m: contractions_dict[re.escape(m.group(0).lower())], clean_pp)
    # Removes all punctuation and digits
    clean_pp = clean_pp.translate(None, special_cases)
    return clean_pp


# cleans DB for deubging
db_utils.exec_command("TRUNCATE privacy_policy, privacy_policy_paragraphs, privacy_policy_paragraphs_prediction")
load_pp_html_to_db()
clean_pp_html_records()
split_or_bypass_pp()
