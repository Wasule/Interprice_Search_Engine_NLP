# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 18:55:05 2020

@author: pswatipali
"""

from flask import Flask, request, jsonify, render_template, Response,redirect,url_for
from Ranking_v1_final import *
import json
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    choices = ['Please Select A Dataset','Medical Data','Products Data']
    state={'choice': "Please Select A Dataset"};
    return render_template("home.html",choices=choices, state=state)

@app.route("/searchResult",methods=['POST'])
def searchResult():
    """ Get the entered values  """
    sQuery = request.form.get("search_val")
    sType = request.form.get("dataset_type")
    choices = ['Please Select A Dataset','Medical Data','Products Data']
    state = {'choice': sType}
    tableData=[];
    productsTable=[];
    
    if(sType == 'Medical Data'):
        d_type='m'
        """ get the search results from ranking algorithm  """
        ranked_result=rank_2(sQuery,d_type)
        """ Adding Serail number to Dataframe  """
        ranked_result['serial_number'] = np.arange(1,(len(ranked_result) + 1))
        """ Converting Dataframe to JSON  """
        jsonResult  = ranked_result.to_json(orient="table")
        parsed = json.loads(jsonResult)
        tableData = parsed['data']
    elif(sType == 'Products Data'):
        d_type='p'
        """ get the search results from ranking algorithm  """
        ranked_result=rank_2(sQuery,d_type)
        """ Adding Serail number to Dataframe  """
        ranked_result['serial_number'] = np.arange(1,(len(ranked_result) + 1))
        """ Converting Dataframe to JSON  """
        jsonResult  = ranked_result.to_json(orient="table")
        parsed = json.loads(jsonResult)
        productsTable = parsed['data']  
    """ Passing the results to View for binding Data to Tables  """
    return render_template("result.html",choices=choices, state=state,resultsTable = tableData,productsTable=productsTable,queryValue=sQuery)

if __name__ == "__main__":
    # Bind to 0.0.0.0 so the server is reachable from the host/environment
    app.run(host='0.0.0.0', port=5000, debug=True)

