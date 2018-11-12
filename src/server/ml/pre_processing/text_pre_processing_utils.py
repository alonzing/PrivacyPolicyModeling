
from src.server.utils.db.tools  import db_utils
from goose import Goose
import os
import re
import string
import urllib2 
from BeautifulSoup import BeautifulSoup
import scandir
from nltk.tokenize.texttiling import TextTilingTokenizer
 
punc_reg = re.compile('[%s]' % re.escape(string.punctuation))

def load_pp_html_to_db():
    url_records = db_utils.db_select("select pp_url from applications where pp_url <> 'none' and pp_url not in (select pp_url from privacy_policy group by pp_url ) group by pp_url")
    for url_record in url_records:
        try:
            pp_html = urllib2.urlopen(url_record.get("pp_url"),timeout=2).read().decode('utf-8')
            db_rows = []
            db_row = [url_record.get("pp_url"),pp_html,"PENDING","200","HTTP OK 200"]
            db_rows.append(db_row)
            db_utils.exec_command("INSERT INTO privacy_policy \
                        (pp_url,html,process_status,url_return_code,url_return_value)\
                        VALUES \
                        (%s,%s,%s,%s,%s)",db_rows)
        except Exception as e:
            print(e)
            code = -1;
            db_rows = []
            if hasattr(e, 'code'):
                code=e.code
            db_row = [url_record.get("pp_url"),"NO_RESPONSE","{0}".format(code),"{0}".format(e)]
            db_rows.append(db_row)
            db_utils.exec_command("INSERT INTO privacy_policy \
                        (pp_url,process_status,url_return_code,url_return_value)\
                        VALUES \
                        (%s,%s,%s,%s)",db_rows) 
            
def clean_pp_html(url,pp_html): 
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
         
def process_privacy_policy():                   
    pp_html_records = db_utils.db_select("select id,pp_url,html from privacy_policy where process_status='PENDING' and url_return_code=200")
    for pp_html_record in pp_html_records:
        result = clean_pp_html(pp_html_record.get("pp_url"),pp_html_record.get("html"))
        db_rows = []
        db_row = ["DONE","NA",result,pp_html_record.get("id")]
        db_rows.append(db_row)
        db_utils.exec_command("UPDATE privacy_policy SET \
                     process_status = %s,process_status_details = %s,clean_html = %s \
                     where id=%s",db_rows)
        
def export_clean_privact_policy_to_folder():
    rootDir='/Users/alonsinger/git/my-privacypolicy-thesis/Raws/Raws_alon'
    if not os.path.exists(rootDir):
        os.makedirs(rootDir)
        
    pp_cleanrecords = db_utils.db_select("select id,clean_html from privacy_policy where clean_html <> ''")
    for pp_clean_record in pp_cleanrecords:
        clean_html = pp_clean_record.get("clean_html")
        text_file = open("{}/{}.txt".format(rootDir,pp_clean_record.get("id")), "w")
            
        regex = '\xe2\x80\xa2'
        clean_html = string.replace(clean_html, regex, '')
        text_file.write(clean_html)
        text_file.close()
        
#open file
#read lines
#while line < 100 chars skip

#while last lines <100 chars skip..

#mid lines

#write line to file1
#if line <100 then add to next
#for each line 
#each line in new paragraph
#

def split_pp_to_paragraphs():
    
    text_file = open("/Users/alonsinger/git/my-privacypolicy-thesis/dropped__paragraphs.txt", "w")

    rootDir='/Users/alonsinger/git/my-privacypolicy-thesis/Raws/Raws_alon'
    outF='/Users/alonsinger/git/my-privacypolicy-thesis/Raws/parasplit_alon'
    filterred_outF='/Users/alonsinger/git/my-privacypolicy-thesis/Raws/filtered_alon'
    
    if not os.path.exists(outF):
        os.makedirs(outF)
    if not os.path.exists(filterred_outF):
        os.makedirs(filterred_outF)
    print ("start to iterate")
    # iterate over all files in dir
    for entry in scandir.scandir(rootDir):
        if entry.is_file():
            try:
                filename_w_ext = os.path.basename(entry.path)
                filename, file_extension = os.path.splitext(filename_w_ext)
                
                baseF=os.path.join(outF,filename)
                          
                with open(entry.path, 'r') as f:
                    all_file_text = f.read()
                    low_text = all_file_text.lower()
                    if not 'privacy' in low_text or 'function(' in low_text or 'catch(' in low_text or 'exception(' in low_text \
                        or '{' in low_text or 'personnelles' in low_text or 'voor' in low_text or 'servicios' in low_text \
                        or 'maggior' in low_text or 'posizione' in low_text or 'werden' in low_text: 
                        filteredF=os.path.join(filterred_outF,filename)
                        fw=open(filteredF+".txt","w")
                        fw.write(all_file_text)
                        fw.close()
                        continue
                             
                    all_file_text = clean_garbage(all_file_text)
                    ttt = TextTilingTokenizer()
                    tttr = ttt.tokenize(all_file_text)
                        
                    idn=0
                    
                    
                    finally_saved = False
                    for paragraph in tttr:
                        lines = paragraph.splitlines()
                        beg=0
                        end=-1
                        totLines=len(lines)
                        while(beg<totLines and len(lines[beg])<100):
                            beg+=1
                           
                        while(end>-totLines and len(lines[end])<100):
                            end-=1
         
                        relLines=lines[beg:end]
         
                        paragraph="" 
                        
                        for line in relLines:
                            paragraph+=(" "+line)
                             
                            if(len(line)<100):               
                                continue

                            if(len(paragraph)<100):               
                                continue
                            
                            
                            db_rows = []
                            db_row = [paragraph,baseF,idn,filename]
                            db_rows.append(db_row)
#                             db_utils.exec_command("INSERT INTO privacy_policy_paragraphs \
#                                                   (paragraph,filename,index,privacy_policy_id)\
#                                                   VALUES \
#                                                    (%s,%s,%s,%s)",db_rows)            
                            paragraph=""
                            idn+=1  
                            finally_saved = True
                            
                    if not finally_saved:
                        text_file.write("Not saved by us,{0}\n".format(paragraph))
                
            except Exception as e:
                print("not saved {0}".format(low_text))
                print("bypassed file:{0}".format(entry.name))
                text_file.write("Not saved by TextTiling,{0}\n".format(low_text))
  
    text_file.close()          

def clean_garbage(all_file_text):
    ret1 = all_file_text.replace('/\d\.\s+|[a-z]\)\s+|[A-Z]\.\s+|[IVX]+\.\s+/g', "")
    return re.sub(r'(\d+.\d?.?)+','',  ret1)        

#init_pp_table()  
#load_pp_html_to_db()  #this takes the url and load the HTML to table   


process_privacy_policy()   #this is for parsing the PP into clean  
#export_clean_privact_policy_to_folder() #from the DB to the folder, clean bullets
#db_utils.exec_command("CREATE TABLE privacy_policy_paragraphs (id serial not null primary key, \
#                                                        paragraph text, filename text,index numeric, privacy_policy_id numeric )")  
#split_pp_to_paragraphs()


