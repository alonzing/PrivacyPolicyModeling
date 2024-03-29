import os
import re
import string
import urllib2

from BeautifulSoup import BeautifulSoup
from goose import Goose
import tempfile
from langid.langid import LanguageIdentifier, model
from nltk.tokenize.texttiling import TextTilingTokenizer
from unidecode import unidecode

from contractions_dict import ContractionsDict
from pre_processing_db_handler import PreProcessingDBHandler
from src.server.utils.db.tools import db_utils

punc_reg = re.compile('[{}]'.format(re.escape(string.punctuation)))
db_handler = PreProcessingDBHandler()
special_cases = string.punctuation + string.digits


def load_pp_from_db(batch_size):
    """
    Searches for unprocessed pp from db
    :param batch_size: the number of pp_url to retrieve from db
    :return: url_records
    """
    url_records = db_utils.db_select(db_handler.sql_get_urls_from_applications_table(batch_size))
    if len(url_records) == 0:
        return None
    db_handler.update_application_not_new(url_records)
    return url_records


def insert_single_pp_html_to_db(pp_url, db_no_respond):
    """
    Opens a pp url and inserts his html page into the db
    :param pp_url: a url of the privacy policy
    :param db_no_respond: a container to store the error code if there will be when it will try open the url
    :return: the pp id in privacy_policy table and the pp html
    """
    pp_id = None
    pp_html = None
    try:
        pp_html = urllib2.urlopen(pp_url, timeout=5).read().decode('utf-8')
        pp_id = db_handler.insert_db_http_ok(pp_url, pp_html)
        print("url " + pp_url + " was opened successfully")
    except Exception as e:
        print(e)
        code = -1
        if hasattr(e, 'code'):
            code = e.code
            db_no_respond.append([pp_url, code, e])
    if pp_id is None:
        return None, None
    else:
        return pp_id[0], pp_html


def load_pp_html_to_db(url_records):
    """
    Loads limited number of HTML files from new (unprocessed) URLs to the privacy_policy table.
    :param url_records:
    :return: url_records_http_ok
    """
    url_records_http_ok = []
    db_no_respond = []
    if len(url_records) == 0:
        return
    for url_record in url_records:
        pp_id, pp_html = insert_single_pp_html_to_db(url_record.get('pp_url'), db_no_respond)
        if pp_id is not None:
            url_records_http_ok.append({'pp_url': url_record.get('pp_url'), 'html': pp_html, 'id': pp_id})
    db_handler.insert_db_no_respond(db_no_respond)
    return url_records_http_ok


def clean_pp_html(url, pp_html):
    """
    Cleans the privacy policy html of html tags
    :param url: the pp url
    :param pp_html: the pp html
    :return: the clean html
    """
    ret_val = ''
    try:
        print("processing the following url {}".format(url))
        tempfile.tempdir = os.getcwd()
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


def clean_pp_html_records(pp_html_records):
    """
    Cleans every pp html in the list as input, checks each with status and stores in the privacy_policy table
    :param pp_html_records: list of pp html
    :return: list of cleaned pp html records
    """
    cleaned_pp_records = []
    defective_html_records = []
    if len(pp_html_records) == 0:
        return cleaned_pp_records
    for pp_html_record in pp_html_records:
        result = clean_pp_html(pp_html_record.get("pp_url"), pp_html_record.get("html"))
        if is_defective_pp(result):
            defective_html_records.append(pp_html_record)
        else:
            pp_html_record['clean_html'] = result
            cleaned_pp_records.append(pp_html_record)
    db_handler.pp_defective(defective_html_records)
    db_handler.update_html_cleaned(cleaned_pp_records)
    return cleaned_pp_records


def split_or_bypass_pp(cleaned_html_records):
    """
    Splits pp to paragraphs and stores into db, stores all paragraphs in privacy_policy_paragraphs
    :param cleaned_html_records:
    :return:
    """
    if len(cleaned_html_records) == 0:
        return
    db_rows = []
    pp_split_failed_records = []
    pp_html_split_ok_records = []
    # preparing for the expansion of contractions
    contractions_dict = dict((re.escape(k.lower()), v) for k, v in ContractionsDict.contractions.iteritems())
    pattern = re.compile("|".join(contractions_dict.keys()), re.IGNORECASE)
    for html_record in cleaned_html_records:
        try:
            clean_pp = html_record.get("clean_html")
            paragraphs = split_pp_to_paragraphs(clean_pp, contractions_dict, pattern)
            for i, paragraph in enumerate(paragraphs):
                paragraph_with_pp_id = paragraph.strip() + ' $' + str(html_record.get("id")[0]) + '$'
                db_rows.append([paragraph_with_pp_id, html_record.get("pp_url"), i, html_record.get("id")])
            pp_html_split_ok_records.append(html_record)

        except Exception as e:
            print e
            pp_split_failed_records.append(html_record)

    db_handler.insert_pp_paragraphs(db_rows)
    db_handler.pp_split_failed(pp_split_failed_records)
    db_handler.pp_split_ok(pp_html_split_ok_records)


def is_defective_pp(clean_pp):
    """
    Checks if a pp is defective, eliminate javascript and non-english pp - using nlp language detection
    :param clean_pp: clean pp
    :return: True if defective, otherwise False
    """
    low_text = clean_pp.lower()
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    language_detect = identifier.classify(clean_pp)
    if low_text is None or language_detect[0] != "en" or (language_detect[0] == "en" and language_detect[1] < 0.9) or \
            'privacy' not in low_text or 'class=' in low_text or 'function(' in low_text or \
            'function (' in low_text or 'catch(' in low_text or 'exception(' in low_text \
            or '{' in low_text:
        return True
    else:
        return False


def split_pp_to_paragraphs(clean_pp, contractions_dict, pattern):
    """
    Uses TextTilingTokenizer to split to paragraphs, the
    privacy policy document should be pre-processed (HTML cleaned) before reaching this function.
    :param clean_pp: clean pp before expansion of contractions and special cases
    :param contractions_dict: a dictionary that includes all varieties of contractions and their expansion
    :param pattern: pattern for the expansion of contractions
    :return: list of paragraphs
    """
    clean_pp = clean_pp_advanced(clean_pp, contractions_dict, pattern)
    ttt = TextTilingTokenizer()
    paragraphs = ttt.tokenize(clean_pp)
    return paragraphs


def clean_pp_advanced(clean_pp, contractions_dict, pattern):
    """
    Gets a clean pp of tags and returns new pp cleaned of special cases and expended of contractions
    :param clean_pp: the clean pp
    :param contractions_dict: a dictionary that includes all varieties of contractions and their expansion
    :param pattern: pattern for the expansion of contractions
    :return: new clean pp
    """
    # Converting non-ascii to their nearest ascii code
    clean_pp = unidecode(clean_pp)
    # Expansion of contractions
    clean_pp = pattern.sub(lambda m: contractions_dict[re.escape(m.group(0).lower())], clean_pp)
    # Removes all punctuation and digits
    clean_pp = clean_pp.translate(None, special_cases)
    return clean_pp

