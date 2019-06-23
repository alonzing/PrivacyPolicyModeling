import os
import shutil
import time
import graphlab as gl

from src.server.utils.db.tools import db_utils


def build_s_frame_from_db(script):
    paragraph_records = db_utils.db_select(script)
    paragraphs_list = [paragraph_record.get("paragraph") for paragraph_record in paragraph_records]
    sframe = gl.SFrame(paragraphs_list)
    return sframe


def get_all_paragraphs_from_db():
    return "select count(*) as ccc,paragraph from privacy_policy_paragraphs \
                                                group by paragraph order by ccc desc"


def get_paragraphs_from_db_for_single_pp_url(pp_url):
    return "select paragraph, index from privacy_policy_paragraphs where pp_url like '{}'" \
           "order by index asc".format(pp_url)


def get_word_frequency(docs):
    """
    Returns the frequency of occurrence of words in an SArray of documents
    Args:
      docs: An SArray (of dtype str) of documents
    Returns:
      An SFrame with the following columns:
       'word'      : Word used
       'count'     : Number of times the word occured in all documents.
       'frequency' : Relative frequency of the word in the set of input documents.
    """

    # Use the count_words function to count the number of words.
    docs_sf = gl.SFrame()
    docs_sf['words'] = gl.text_analytics.count_words(docs)

    # Stack the dictionary into individual word-count pairs.
    docs_sf = docs_sf.stack('words',
                            new_column_name=['word', 'count'])

    # Count the number of unique words (remove None values)
    docs_sf = docs_sf.groupby('word', {'count': gl.aggregate.SUM('count')})
    docs_sf['frequency'] = docs_sf['count'] / docs_sf["count"].sum()
    return docs_sf


def get_freq_words(docs4freq):
    docs_count = get_word_frequency(docs4freq['X1'])
    print (docs_count)
    docs_count = docs_count.sort(['count', 'frequency', 'word'], ascending=False)
    freq_words = docs_count[docs_count['count'] >= 10]
    freq_words.print_rows(num_rows=100)
    return freq_words


def build_docs_for_modeling(in_docs, sframe_raw_filename):
    # Remove stop words and convert to bag of words
    in_docs = gl.text_analytics.count_words(in_docs['X1'])
    in_docs = in_docs.dict_trim_by_keys(gl.text_analytics.stopwords(), exclude=True)
    freq_words = get_freq_words(gl.load_sframe(sframe_raw_filename))
    in_docs = in_docs.dict_trim_by_keys(freq_words['word'], exclude=False)
    in_docs = in_docs.dict_trim_by_keys(['information', 'data', 'privacy'], exclude=True)
    return in_docs


def build_model(in_docs, topic_count):
    model = gl.topic_model.create(in_docs, num_topics=topic_count,
                                  num_iterations=100)
    return model


def build_model_and_print(in_docs, topic_count):
    model = build_model(in_docs, topic_count)
    print (model)
    print (model.get_topics(output_type='topic_words'))
    print (model.get_topics().print_rows(num_rows=100))
    return model


def model_pp(sframe_raw_filename, sframe_filename, model_filename, predictions_filename,
             script=get_all_paragraphs_from_db(), single_predict=False, topic_count=100, save_from=0):
    if not os.path.exists(sframe_filename):
        print("Building SFrame file...")
        sframe_raw = build_s_frame_from_db(script)
        print('SFRAME PATH ' + sframe_raw_filename)
        sframe_raw.save(sframe_raw_filename)
        sframe_for_modeling = build_docs_for_modeling(sframe_raw, sframe_raw_filename)
        sframe_for_modeling.save(sframe_filename)
        print("Building SFrame files...completed")
    else:
        sframe_for_modeling = gl.load_sframe(sframe_filename)

    if not os.path.exists(model_filename):
        print("Building topic model...")
        model = build_model_and_print(sframe_for_modeling, topic_count)
        model.save(model_filename)
        print("Building topic model...completed")
    else:
        model = gl.load_model(model_filename)

    if not os.path.exists(predictions_filename) is None:
        print("Building predictions...")
        docs_res = sframe_raw
        docs_res['res'] = model.predict(sframe_for_modeling)
        docs_res['res_prob'] = model.predict(sframe_for_modeling, output_type='probability')
        docs_res.save(predictions_filename.format(topic_count))
        print("Building predictions...completed")
    else:
        docs_res = gl.load_sframe(predictions_filename)

    total_docs = len(docs_res)
    single_predict_rows = []
    db_rows = []
    records_count = 0

    docs_res_res = docs_res['res']
    docs_res_prob = docs_res['res_prob']
    docs_parg = docs_res['X1']
    for i in range(save_from, total_docs):
        x = docs_res_res[i]
        db_row = [topic_count,
                  x,
                  docs_res_prob[i][x],
                  docs_parg[i]]

        db_rows.append(db_row)
        if single_predict:
            result_dict = {
                'topic': db_row[1],
                'probability': db_row[2],
                'paragraph_text': db_row[3]
            }
            single_predict_rows.append(result_dict)

        if records_count == 1000 or i == total_docs - 1:
            records_count = 0
            db_utils.exec_command("INSERT INTO privacy_policy_paragraphs_prediction \
                                (running_id,topic_id,probability,paragraph)\
                                                   VALUES (%s,%s,%s,%s)", db_rows)
            db_rows = []
            time.sleep(1)
            print("saved up to {} out of {}".format(i, total_docs))
        else:
            records_count += 1

    if single_predict:
        return single_predict_rows
    else:
        return topic_count


def build_prediction_results(topic_count, model_file_name):
    model = gl.load_model(model_file_name)
    root_results_dir = 'my-privacypolicy-thesis/results{}'.format(topic_count)
    if os.path.exists(root_results_dir):
        shutil.rmtree(root_results_dir)
    os.makedirs(root_results_dir)

    results_html_file = open(root_results_dir + "/results.html", "w+")
    results_html_file.write("<html><table border='1'><tr><td>Topic Number</td><td>Words</td><td>Paragraphs</td></tr>")
    print('started phase 1 of build predictions results')
    paragraphs_html_list = []
    for i in range(topic_count):
        paragraphs_html_list.append("<html><table border='1'>")
        words_list = model.get_topics(num_words=20, output_type='topic_words')['words'][i]
        print_words_list = ', '.join(words_list)
        paragraphs_url = "<a href='./paragraphs_topic_{}.html'>paragraphs</a>".format(i)
        results_html_file.write(
            "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(i, print_words_list, paragraphs_url))
        print('{} out of {}'.format(i + 1, topic_count))
    results_html_file.write("</table></html>")
    results_html_file.close()

    print('started phase 2 of build predictions results')
    for topic_id in range(0, topic_count):
        results_records = db_utils.db_select(
            "select probability,paragraph from privacy_policy_paragraphs_prediction "
            "where running_id= {} and topic_id={} "
            "group by paragraph,probability "
            "order by probability desc".format(topic_count, topic_id))
        topic_html = "<html><table border='1'><tr><td>Probability</td><td>Paragraph</td></tr>"
        for results_record in results_records:
            topic_html += "<tr><td>{:.4f}</td><td>{}</td></tr>".format(results_record.get('probability'),
                                                                       results_record.get('paragraph'))
        topic_html += "</table></html>"
        paragraphs_html_file = open(root_results_dir + "/paragraphs_topic_{}.html".format(topic_id), "w+")
        paragraphs_html_file.write(topic_html)
        print('{} out of {}'.format(topic_id + 1, topic_count))
    print("done")


def get_filenames(sframe_raw_working_dir, sframe_working_dir, model_working_dir, predictions_working_dir):
    sframe_raw_filename = sframe_raw_working_dir + os.path.sep + 'paragraphs.sfrm.raw'
    sframe_filename = sframe_working_dir + os.path.sep + 'paragraphs.sfrm'
    model_filename = model_working_dir + os.path.sep + 'paragraphs.mdl'
    predictions_filename = predictions_working_dir + os.path.sep + 'paragraphs.prd'
    return sframe_raw_filename, sframe_filename, model_filename, predictions_filename


def build_topics_models():
    working_dir = 'models_and_data{0}run_{1}'.format(os.path.sep, 'test')
    os.makedirs(working_dir)
    print('directory {0} was created'.format(working_dir))
    sframe_raw_filename, sframe_filename, model_filename, predictions_filename = \
        get_filenames(working_dir, working_dir, working_dir, working_dir)
    topic_count = model_pp(sframe_raw_filename, sframe_filename, model_filename, predictions_filename)
    build_prediction_results(topic_count, model_filename)


def build_from_exists_modeling(pp_url, pp_id):
    working_dir = 'models_and_data{0}run_{1}'.format(os.path.sep, "pp_" + str(pp_id))
    working_model_dir = 'models_and_data{0}run_{1}'.format(os.path.sep, 'test')
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    sframe_raw_filename, sframe_filename, model_filename, predictions_filename = \
        get_filenames(working_dir, working_dir, working_model_dir, working_dir)
    script = get_paragraphs_from_db_for_single_pp_url(pp_url)
    single_predict_rows = model_pp(sframe_raw_filename, sframe_filename, model_filename, predictions_filename, script,
                                   single_predict=True)
    shutil.rmtree(working_dir)
    return single_predict_rows


if __name__ == '__main__':
    build_topics_models()
    # pp_url = 'http://christianchannel.us/privacy-policy/'
    # build_from_exists_modeling(pp_url, 1940)
