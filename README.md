# Privacy Policy Modeling

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
*The following steps can also be done via an IDE of your choice, this a step-by-step via CMD.*

* Clone the project
```
git clone https://github.com/alonzing/PrivacyPolicyModeling.git
```

* Create a virtual enviornment
```
virutalenv venv
```

* Activate the virtual enviornment
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

* Install NLTK stopwords
```python
python -m nltk.downloader stopwords
```

* Initialize the DB - use this only once, unless a reset of the DB is required.
```python
python src/server/utils/db/db_initialzer.py
```
