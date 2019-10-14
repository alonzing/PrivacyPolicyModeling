# Privacy Policy Modeling

For front-end client instructions, please refer to [this](https://github.com/alonzing/PrivacyPolicyModeling/tree/master/ng-server) page.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* Python 2.7
* [GraphLab](https://turi.com/)
  **Please Note: A license is required, you can get an Academic license.**
* [PostgreSQL](https://www.postgresql.org/download/) -
   **Please Note: choose your password according to the password in this 
   [module](https://github.com/alonzing/PrivacyPolicyModeling/blob/master/src/server/utils/db/tools.py), or change it accordingly.**
   

### Installing
*The following steps can also be done via an IDE of your choice, this is a step-by-step Command Prompt guide.*

* Clone the project
```
git clone https://github.com/alonzing/PrivacyPolicyModeling.git
```

* Create a virtual environment
```
virutalenv venv
```

* Activate the virtual environment
```bash
On Linux:
source venv/bin/activate

On Windows:
venv\Scripts\activate
```

* Install the required packages
```
pip install -r requirements.txt
```

* Install GraphLab - **Replace your registered email address here/your product key here with your email address AND product key**
```
pip install --upgrade --no-cache-dir https://get.graphlab.com/GraphLab-Create/2.1/
your registered email address here/your product key here/GraphLab-Create-License.tar.gz
```

* Install GraphLab dependencies:
```
python -c "import graphlab; graphlab.get_dependencies()"
```

* Install NLTK stopwords
```python
python -m nltk.downloader stopwords
```

* Initialize the DB - **use this only once, unless a reset of the DB is required.**
```python
python src/server/utils/db/db_initialzer.py
```

## Test Run
### For detailed reference regarding the project structure refer to the Project Documentation.
1. Populate the DB with applications by running the crawler under ```src/server/crawler/main_crawler.py```
   Let it run for approx. 2-5 min to get some data.
   
   ##### Verifying the Results:
   - Query the DB, using ```pgAdmin4``` or some other tool.  
     - Verify that the applications table has data.

2. Run the pre-processing module under ```src/server/ml/pre_processing/pre_processing_executor.py```
   to split the privacy policies into paragraphs and perform some cleaning of the HTML.
   
   You can let it complete its run, or stop it midway, and run it again at a later time. (Will resume from the same point it stopped).
   ##### Verifying the Results:
   - Query the DB, using ```pgAdmin4``` or some other tool.
      - Verifty that the privacy_policy and privacy_policy_paragraphs tables have data.
   ##### OR
   - By running the debug http server under ```src/server/management_utils/debug_http_server.py```
     - Access ```localhost:8181``` to see the clean HTML.
     - Access ```localhost:8181/show_paragraphs_and_pp``` to see the split to paragraphs.
   

3. Run the model under ```src/server/ml/topic_modeling.py```
   ##### Verifying the Results:
   - Access ```src/server/ml/topic_modeling/my-privacypolicy-thesis/results100/results.html``` - these are the prediction results with        the predicted probability.
   - Query the DB using ```pgAdming``` or any other tool.
     - Verify that the table ```privacy_policy_paragraphs_prediction``` has data.
