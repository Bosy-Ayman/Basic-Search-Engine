#Import the necessary modules:
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import *
from nltk.stem.porter import *
import pandas as pd
import re # used to clean the data
#to display the full text on the notebook without truncation
pd.set_option('display.max_colwidth', 150)

import pyterrier as pt
if not pt.started():
  pt.init()

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

df = pd.read_csv('corona.csv')
df.head()

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
pd_indexer = pt.DFIndexer("F:/CSAI/2nd year/Spring/Data Retrieval and Information Retreival/IR_Project/pd_index1")
indexref = pd_indexer.index(df["OriginalTweet"], df["docno"])

index = pt.IndexFactory.of(indexref)


word_to_documents = {}

inv = index.getInvertedIndex()
meta = index.getMetaIndex()

for kv in index.getLexicon():
    term = kv.getKey()
    pointer = index.getLexicon()[term]
    doc_ids = []
    for posting in inv.getPostings(pointer):
        docno = meta.getItem("docno", posting.getId())
        doc_ids.append(docno)

    word_to_documents[term] = doc_ids

# for term, doc_ids in word_to_documents.items():
#     print("%s -> %s (%d occurrences)" % (term, doc_ids, len(doc_ids)))
