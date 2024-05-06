from flask import Flask, jsonify, render_template ,request
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from sqlite3 import Error
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import *
from nltk.stem.porter import *
import pandas as pd
import re 
import os
from datetime import datetime

#pd.set_option('display.max_colwidth', 150)

import pyterrier as pt
if not pt.started():
  pt.init()

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

#----------------------------- beginning of the code ------------------------------------

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

df = pd.read_csv("corona.csv")
connection = create_connection('data.db')
df.to_sql('corona_data', connection, if_exists='replace')
connection.close()

db_url = 'sqlite:///data.db'
engine = create_engine(db_url, echo=True)

app = Flask(__name__)

# Initialize Porter stemmer
stemmer = PorterStemmer()

def Stem_text(text):
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    # print (tokens)
    return ' '.join(stemmed_tokens)

def clean(text):
   text = re.sub(r"[\.\,\#_\|\:\?\?\/\=\@]", " ", text) # remove special characters
   text = re.sub(r'\t', ' ', text) # remove tabs
   text = re.sub(r'\n', ' ', text) # remove line jump
   text = re.sub(r"\s+", " ", text) # remove extra white space
   text = text.strip()
   return text

def remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words] #Lower is used to normalize al the words make them in lower case
    # print('Tokens are:',tokens,'\n')
    return ' '.join(filtered_tokens)

#we need to process the query also as we did for documents
def preprocess(sentence):
  sentence = clean(sentence)
  sentence = remove_stopwords(sentence)
  sentence = Stem_text(sentence)
  return sentence


res = df['OriginalTweet'].apply(preprocess)
df['docno'] = df["ScreenName"].astype(str)

index_path = "F:/CSAI/2nd year/Spring/Data Retrieval and Information Retreival/IR_Project/pd_index1"

# Check if the index already exists
if not os.path.exists(index_path):
    # Create the index if it doesn't exist
    pd_indexer = pt.DFIndexer(index_path)
    indexref = pd_indexer.index(df["OriginalTweet"], df["docno"])
else:
    # Load the existing index
    indexref = pt.IndexRef.of(index_path)

index = pt.IndexFactory.of(indexref)

tfidf = pt.BatchRetrieve(index, wmodel="TF_IDF")

@app.route('/search', methods=["POST"])
def search():
    start_time = datetime.now()  
    
    # Get the search query from the request
    query = request.form.get('query')
    preprocessed_query = preprocess(query)
    
    results = tfidf.transform(preprocessed_query)
    
    end_time = datetime.now()
    search_duration = end_time - start_time
    
    # Convert the results dataframe to a list of dictionaries
    results_list = results.to_dict('records')
    
    # Retrieve the original tweets corresponding to the docno
    original_tweets = df[df["docno"].isin([result["docno"] for result in results_list])]["OriginalTweet"].tolist()
    
    # Combine the results and original tweets
    for i, result in enumerate(results_list):
        result["original_tweet"] = original_tweets[i]
    
    search_duration_formatted = "{:.2f} secs".format(search_duration.total_seconds())
    
    # Render the search results in the HTML template along with the search duration
    return render_template('search.html', results=results_list, search_duration=search_duration_formatted)

@app.route('/')
def index():
    return render_template('search.html')
if __name__ == '__main__':
    app.run(debug=True, port=3001)