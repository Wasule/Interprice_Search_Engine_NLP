import pandas as pd
import numpy as np
import pdb; 

#Setting an path where current and imported module exists together.
import sys
from Search_v1_0 import search
import Data_Cleaning_Structured_v1_0 as DCS

med_data = DCS.med_data
products_data = DCS.products_data

def rank_2(sentence,dataset):
    """
    RULE Based Ranking.\n\n
    
    In this function, we rank our search results obtained using search function using a rule based method.\n
    The rules are:\n
        1. List the list of documents based on their presence score (or the value of function fraction_of_words()).\n
        2. Then break the ties (if any) using the sum of the frequencies of words from query in the document.\n
        3. Then finally break the ties (if any) using the sum of tfidfs of the words from query in the document.\n
        
    Input is a search query (string) and dataset name ('m' for medical data and 'p' for products data).\n
    Output is a list of ordered documents to be displayed to the user.
    """
    result=search(sentence,dataset)
    
    #extract metrics
    words=result[1]
    words_frequencies=result[2]
    words_tfidfs=result[3]
    presence_score=result[4]
    close_score=result[5]
    
    combined_metrics=[]
    
    for wf in words_frequencies.items():
        doc_id=wf[0]
        freq_metric=sum(wf[1]) #Metric 1
        for ps in presence_score:
            if ps[0]==doc_id:
                pres_metric=ps[1] #Metric 2
                break
        tfidf_metric=sum(words_tfidfs[doc_id]) #Metric 3
                
        combined_metrics.append([doc_id,pres_metric,freq_metric,tfidf_metric])
    
    #Lets now sort them according to the rules
    final_order=sorted(combined_metrics,key=lambda x: (-x[1], -x[2], -x[3]))
    final_order = return_original_data(final_order,dataset)
    return final_order


def return_original_data(ranked_data,dataset):
    # final_result = pd.DataFrame(columns=['ID1', 'ID2', 'Name', 'Composition', 'Manufacturer', 'Form', 'PackSize',
    #    'MRP', 'Subclass', 'Class'])
    final_index=[];
    if dataset=='m':
        data = med_data;
    elif dataset=='p':
        data = products_data
    for index, results in enumerate(ranked_data):
        # pdb.set_trace();
        
        final_index.append(results[0])
    
    Filter_df  = data[data.index.isin(final_index)]
    
    return Filter_df
    
    
    
    
s1="1969 Harley Davidson Ultimate Chopper"

if __name__ == "__main__":
    # Example usage when run directly; keep import-time free of side-effects
    s1 = "1969 Harley Davidson Ultimate Chopper"
    try:
        result = search(s1, 'p')
        ranked_result = rank_2(s1, 'm')
    except Exception as e:
        print('Example run failed:', e)
