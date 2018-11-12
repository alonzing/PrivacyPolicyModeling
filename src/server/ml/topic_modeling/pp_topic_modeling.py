import graphlab as gl
import os
import shutil

from src.server.utils.db.tools  import db_utils

def build_csv_from_paragraphs():
    
    paragraph_records = db_utils.db_select("select count(*) as ccc,paragraph from privacy_policy_paragraphs \
                                            group by paragraph order by ccc desc");
    #create csv from all files
    rootDir='/Users/alonsinger/git/my-privacypolicy-thesis/Raws/parasplit_alon'
    # iterate over all files in dir
    outF1='/Users/alonsinger/git/my-privacypolicy-thesis/Raws/all_para_alon.csv'
    fw=open(outF1,"w")
    
    print("start to generte CSV")
    for paragraph_record in paragraph_records:
        doc = paragraph_record.get("paragraph")
        doc=doc.replace(",", " ")
        fw.write(doc+"\n")
    fw.close() 
    print("completed to generte CSV")

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


def get_freq_words():
    # Sample SArray
    docs4freq = gl.SFrame.read_csv('/Users/alonsinger/git/my-privacypolicy-thesis/Raws/all_para_alon.csv', header=False)
    docs_count = get_word_frequency(docs4freq['X1'])
    print (docs_count)
    docs_count=docs_count.sort(['count','frequency','word'],ascending=False)   
    freq_words=docs_count[docs_count['count']>=10]
    freq_words.print_rows(num_rows=100)
    return freq_words  

def build_docs_for_modeling(in_docs):
    # Remove stopwords and convert to bag of words
    in_docs = gl.text_analytics.count_words(in_docs['X1'])
    in_docs = in_docs.dict_trim_by_keys(gl.text_analytics.stopwords(), exclude=True)
    freq_words = get_freq_words()
    in_docs = in_docs.dict_trim_by_keys(freq_words['word'], exclude=False)
    in_docs = in_docs.dict_trim_by_keys(['information','data','privacy'], exclude=True)
    return in_docs

def build_model(in_docs,topic_count):
    model = gl.topic_model.create(in_docs,num_topics=topic_count,
                                   num_iterations=600)
    return model

def build_model_and_print(in_docs,topic_count):
    model = build_model(in_docs,topic_count)
    print (model)
    print (model.get_topics(output_type='topic_words'))
    print (model.get_topics().print_rows(num_rows=100))
    return model

def model_pp( topic_count = 100, model_file_name = None, save_from = 0, predictions_file_name = None):
    docs = gl.SFrame.read_csv('/Users/alonsinger/git/my-privacypolicy-thesis/Raws/all_para_alon.csv', header=False)    
    docs_for_modeling = build_docs_for_modeling(docs)
    if model_file_name is None:
        model = build_model_and_print(docs_for_modeling,topic_count)
        model.save("/Users/alonsinger/git/my-privacypolicy-thesis/model{}.mdl".format(topic_count))
    else:
        model = gl.load_model(model_file_name)

    if predictions_file_name is None:
        docs_res = gl.SFrame.read_csv('/Users/alonsinger/git/my-privacypolicy-thesis/Raws/all_para_alon.csv', header=False)    
        docs_res['res'] = model.predict(docs_for_modeling)
        docs_res['res_prob'] = model.predict(docs_for_modeling, output_type='probability') 
        docs_res.save("/Users/alonsinger/git/my-privacypolicy-thesis/model{}.prd".format(topic_count))
    else:
        docs_res = gl.load_sframe(predictions_file_name)
        
    total_docs = len(docs_res)
    db_rows = []
    records_count = 0
    
 #   docs_res.export_csv("/Users/alonsinger/git/my-privacypolicy-thesis/predictions.csv")

    for i in range(save_from,total_docs):
        db_row = [topic_count,\
                  docs_res['res'][i],\
                  docs_res['res_prob'][i][docs_res['res'][i]],\
                  docs_res['X1'][i]]
        db_rows.append(db_row)
          
        if records_count == 100:
            records_count = 0
            db_utils.exec_command("INSERT INTO privacy_policy_paragraphs_prediction \
                                (running_id,topic_id,probability,paragraph)\
                                                   VALUES \
                                                    (%s,%s,%s,%s)",db_rows)  
            db_rows = []
            print("saved up to {}".format(i))
        else:
            records_count+=1
        
 

        
def build_prediction_results(topic_count,model_file_name):   
    model = gl.load_model(model_file_name)   
    root_results_dir='/Users/alonsinger/git/my-privacypolicy-thesis/results{}'.format(topic_count)
    if os.path.exists(root_results_dir):
        shutil.rmtree(root_results_dir) 
    os.makedirs(root_results_dir)
     
    results_html_file = open(root_results_dir+"/results.html","w+")
    results_html_file.write("<html><table border='1'><tr><td>Topic Number</td><td>Words</td><td>Paragraphs</td></tr>")
         
    paragraphs_html_list = []
    for i in range(topic_count):
        paragraphs_html_list.append("<html><table border='1'>")
        words_list = model.get_topics(num_words=20, output_type='topic_words')['words'][i] 
        print_words_list = ', '.join(words_list)       
        paragraphs_url = "<a href='./paragraphs_topic_{}.html'>paragraphs</a>".format(i)
        results_html_file.write("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(i,print_words_list,paragraphs_url))
    results_html_file.write("</table></html>")
    results_html_file.close()
    
    
    for topic_id in range(0,topic_count):
        results_records = db_utils.db_select("select probability,paragraph from privacy_policy_paragraphs_prediction where running_id= {} and topic_id={} group by paragraph,probability order by probability desc".format(topic_count,topic_id))
        topic_html = "<html><table border='1'><tr><td>Probability</td><td>Paragraph</td></tr>"
        for results_record in results_records:
            topic_html += "<tr><td>{:.4f}</td><td>{}</td></tr>".format(results_record.get('probability'),results_record.get('paragraph'))
        topic_html += "</table></html>"  
        paragraphs_html_file = open(root_results_dir+"/paragraphs_topic_{}.html".format(topic_id),"w+")
        paragraphs_html_file.write(topic_html)
   
     
    print("done")

model_pp(model_file_name="/Users/alonsinger/git/my-privacypolicy-thesis/model100.mdl",
         predictions_file_name = "/Users/alonsinger/git/my-privacypolicy-thesis/model100.prd",save_from=17776)
#cProfile.run('build_prediction_results(100,model_file_name="""/Users/alonsinger/git/my-privacypolicy-thesis/model100.mdl""")',filename='alon.cprof') 
#build_prediction_results(100,model_file_name="/Users/alonsinger/git/my-privacypolicy-thesis/model100.mdl")
#build_csv_from_paragraphs()
#model_pp(topic_count = 100)
#cProfile.run('model_pp(model_file_name="""/Users/alonsinger/git/my-privacypolicy-thesis/model100.mdl""")', filename='model_pp.cprof' )
#init_db()
#get_freq_words()



# text_file = open("/Users/alonsinger/git/my-privacypolicy-thesis/paragraphs_words.txt", "w")
# docs = gl.SFrame.read_csv('/Users/alonsinger/git/my-privacypolicy-thesis/Raws/all_para_alon.csv', header=False)    
# print("{0}".format(len(docs['X1'])))
# for x in docs['X1']:
#     text_file.write("{0}\n".format(len(x)))
# text_file.close()
 
          
