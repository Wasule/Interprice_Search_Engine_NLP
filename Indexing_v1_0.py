import pandas as pd
import numpy as np

#Setting an path where current and imported module exists together.
import sys
sys.path.append('D:\Personal_DS_Docs\Live Project 2\Codes\FlackCode')

#Importing data
import Data_Cleaning_Structured_v1_0 as DCS

all_med_data=DCS.all_med_data
all_products_data=DCS.all_products_data

import math

def all_unique_words(doclist):
    """
    Returns all unique words from the input list.\n
    Input is a list of documents.\n
    Output is a list of all unique words in the input list.    
    """
    flatten=[words for doc in doclist for words in doc]
    words_unique=list(set(flatten))
    return words_unique

def tf(word,doc):
    """
    Term frequency for a 'word' in 'doc' document.\n
    Input is a word (string type object) and a document (list type object).\n
    Output is the term frequency (numeric type object).
    """
    return doc.count(word)/len(doc)

def n_containing(word,doclist):
    """
    Number of documents in 'doclist' with at least 1 occurance of the word 'word' in it.\n
    Input is a word (string type object) and a list of documents (list type object).\n
    Output is a numeric type object.
    """
    return sum(1 for doc in doclist if word in doc)

def idf(word,doclist):
    """
    Returns Inverse Document Frequency of a word in a list of documents.\n
    Using the formula used by TfidfTransformer when smooth=True.\n
    idf = log(N+1/n+1)+1 \n
    Where,\n
    N = number of documents in doclist.\n
    n = number of documents in doclist with at least 1 occurance of word 'word'.\n\n
    Input is word (string type object) and a list of documents (list type object).\n
    Output is smoothened idf value (numeric type object.
    """
    idf = 1 + math.log((len(doclist)+1)/(n_containing(word,doclist)+1))
    return idf

def tfidf(word,doc,doclist):
    """
    Returns Term Frequency - Inverse Document Frequency of a word in a document within a list of documents.
    """
    return tf(word,doc)*idf(word,doclist)

def indexer(doclist):
    """
    It returns an inverted index of doclist.\n 
    Inverted because in this case a unique word takes up a unique row instead of a unique document taking up a unique row.\n 
    It calculates and stores 3 key elements for any word in a row:\n
        1. The document index in which the word in located.\n
        2. The position(s) of that word in particular document.\n
        3. Tfidf value for the word in a particular document which is in a particular document list.\n\n
        
    Input is a list of documents (list type object).\n
    Output is an inverted index (dict type object).
    """
    worddic={}
    words_unique=all_unique_words(doclist)
    for doc in doclist:
        for word in words_unique:
            if word in doc:
                word=str(word)
                index=doclist.index(doc)
                positions=list(np.where(np.array(doclist[index])==word)[0])
                tfidf_value=tfidf(word,doc,doclist)
                try:
                    worddic[word].append([index,positions,tfidf_value])
                except:
                    worddic[word]=[]
                    worddic[word].append([index,positions,tfidf_value])
    return worddic

###Main

#Medical data
med_index=indexer(all_med_data)
np.save('D:/Personal_DS_Docs/Live Project 2/Codes/FlackCode/med_index_1000.npy',med_index) #Saving as pickle file

#Products data
products_index=indexer(all_products_data)
np.save('D:/Personal_DS_Docs/Live Project 2/Codes/FlackCode/products_index.npy',products_index) #Saving as pickle file


###FootNotes:
#The medical index is only based on 1000 records (It needs to be changed in future).
#The indices are stores as pickle file to avoid recalculating them. The will be used in future.








