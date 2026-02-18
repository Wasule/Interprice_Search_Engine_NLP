import pandas as pd
import numpy as np
import pdb; 

from collections import Counter

#Setting an path where current and imported module exists together.
import sys
import os
# ensure current project directory is on path (no hardcoded Windows paths)
sys.path.append(os.path.dirname(__file__) or '.')

import Data_Cleaning_Structured_v1_0 as DCS
from nltk.tokenize import word_tokenize

worddic = "" #Global variable which will contain inverted index of a dataset.

def filter_search_terms(words):
    """
    This function only keeps the words in the search query (i.e., 'words' object) which are present in the index.\n
    Input is a list of words from the search query.\n
    Output is a list of relevant words.
    """
    real_words=[]
    for word in words:
        if word in list(worddic.keys()):
            real_words.append(word)
    return real_words

def n_terms_and_idfs(words):
    """
    This function is used to calculate:\n
        1. The number of times any word from the list 'words' is present in any document.\n
        2. The tfidf scores of each word from the list 'words' for every document.\n
    Input is a list of words (user search query).\n
    Output are two dict type objects.\n
    """
    enddic={}
    idfdic={}
    for word in words:
        for ind in worddic[word]:
            index=ind[0]
            amount=len(ind[1])
            idf_scores=ind[2]
            try:
                enddic[index].append(amount)
            except:
                enddic[index]=[]
                enddic[index].append(amount)
            try:
                idfdic[index].append(idf_scores)
            except:
                idfdic[index]=[]
                idfdic[index].append(idf_scores)
    return enddic, idfdic

def fraction_of_words(words):
    """
    This function determines the fraction of the words from the list 'words' present in the each document.\n
    Only those documents are displayed which have at least one word from object 'words' in it.\n
    Input is a list of words.\n
    Output is a sorted list type object.
    """
    combo=[]
    all_options={k: worddic.get(k,None) for k in words}
    # pdb.set_trace();
    for worddex in list(all_options.values()):
        for indexpos in worddex:
            combo.append(indexpos[0])
    combo_count=Counter(combo)
    for key in combo_count:
        combo_count[key]=combo_count[key]/len(words)
    combo_count=sorted(combo_count.items(), key= lambda x:x[1], reverse=True)
    for i in range(len(combo_count)):
        combo_count[i]=list(combo_count[i])
    return combo_count

# make metric for if words appear in same order as in search

def co_occurring_words_metric(words):
    """
    This function determines the number of pairs of words (from the list 'words') occuring one after another in order.\n\n
    For example:\n
    If the document is "asian exporters fear damage from us japan rift mounting trade friction between the us and japan has raised fears"\n
    Now consider that the search query is:\n
        1. "asian fear rift trade", then the value of this metric will be 0 as no pair of words occur one after another.\n
        2. "asian exporters damage us", then the value of this metric will be 1 as the pair of words "asian" and "exporters" occur together in the document.\n
        3. "exporters asian damage us", then the value of this metric will be 0 as even though the pair of words "asian" and "exporters" occur together, they do not occur in the same order.\n
        4. "asian exporters japan rift", then the value of this metric will be 2 as there are 2 pairs of words ["aisan","exporters"] and ["japan","rift"] which occur together in the document.\n
    Input and Output both are list type objects.
    """
    if len(words)>1:
        x=[]
        y=[]
        for recordlist in [worddic[z] for z in words]:
            for record in recordlist:
                x.append(record[0])
        for i in x:
            if x.count(i)>1:
                y.append(i)
        y=list(set(y))
    
        closedic={}
        for recordlist in [worddic[z] for z in words]:
            for record in recordlist:
                if record[0] in y:
                    index=record[0]
                    positions=record[1]
                    try:
                        closedic[index].append(positions)
                    except:
                        closedic[index]=[]
                        closedic[index].append(positions)
    
        fdic={}
        for index in y:
            csum=[]
            temp=0
            for poslist in closedic[index]:
                while temp>0:
                    secondlist=poslist
                    temp=0
                    csum.append([1 for i in firstlist if i+1 in secondlist])
                    fsum=[item for sublist in csum for item in sublist]
                    fdic[index]=sum(fsum)
                while temp==0:
                    firstlist=poslist
                    temp+=1
                    
        fdic=sorted(fdic.items(), key=lambda x: x[1], reverse=True)
        for i in range(len(fdic)):
            fdic[i]=list(fdic[i])
    
    else:
        fdic=0
    
    return fdic

def search(sentence,dataset):
    """
    This function returns multiple lists/dictionaries which are various metrics used for ranking of the documents.\n
    Input is a serach sentence (string) and dataset ('p' for products data and 'm' for medical data).\n
    Output is a tuple made of of 6 elements as follows:\n
        1. Sentence (string type object) which is our search query.\n
        2. List of relevent words for searching. (after cleaning, lemmatizing and stop words removal).\n
        3. Two dict type objects which are the output of the function n_terms_and_idfs().\n
        4. A list type object which is the output of the function fraction_of_words() And\n
        5. A list type object which is the output of the function co_occurring_words_metric().\n
    """
    try:
        global worddic
        if dataset=='m':
            worddic=np.load("med_index_1000.npy",allow_pickle=True).item()
            clean_sentence=DCS.clean_medical_text(sentence)
        elif dataset=='p':
            worddic=np.load("products_index.npy",allow_pickle=True).item()
            clean_sentence=DCS.clean_products_text(sentence)
        else:
            print("Error: Dataset not found")
            return
        
        words=word_tokenize(clean_sentence)
        words=[words] #Converting it into a list of list so that the functions from DCS can be directely used.
        words_pos=DCS.pos_tagger(words)
        words_pos=DCS.get_wordnet_pos(words_pos)
        words=DCS.lemmatized_list(words_pos)
        words=DCS.stop_words_removal(words)
        words=words[0] #Converting back to a single list.
        
        words=filter_search_terms(words)
        words_quantity, all_idfs=n_terms_and_idfs(words)
        
        words_presence=fraction_of_words(words)
        
        closeness_metric=co_occurring_words_metric(words)
        
        return(sentence, words, words_quantity, all_idfs, words_presence, closeness_metric)
        
    except Exception:
        # Return empty-but-typed structure to avoid callers breaking on import-time failures
        return ("", [], {}, {}, [], [])
    

###Main
# s1="Plymouth hemi Classic 1970 aloo CUDA studio and to"
# res1=search(sentence=s1, dataset='p')

# s2="ASTHAMON"
# res2=search(sentence=s2,dataset="m")

###Please note:
# The files Data_Cleaning_Structured_v1_0.py and Indexing_v1_0.py are required to be in same directory as this file.
# This directory's address needs to be mentioned in line 8 of this code.
# The output of Indexing_v1_0.py (i.e., the 2 pickle files) are uploaded in this code at lines 149 and 152 directly from the local machine by typing their addresses.


###To Do:
#The function to clean data needs to be merged into a single function in Data_Cleaning_Structured_v1_0.py and Search_v1_0.py file.
#Hence, we can eleminate the 2nd argument from the search() function.  