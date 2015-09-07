from flask import Flask, render_template, request, redirect, url_for
from flask_esclient import ESClient
import requests
from elasticsearch import Elasticsearch
from datetime import datetime
from iron_celery import iron_cache_backend
import relevantarticles
import feedparser
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import TwitterSearchV2
import json
import pickle
import sys

app = Flask(__name__)


#Displaying Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    
    if request.method == "POST":
        twitter_handle = request.form['text']
        return render_template('persoNews.html', urlList=urlList)
    
    return render_template('index.html')
    

#Displaying news suggestions
@app.route('/persoNews', methods=['GET', 'POST'])
def personewspage():
    
    if request.method == "POST":
        twitter_handle = request.form['text']
    
    listOfTextFiles = ["BodyTexts.json"]
    
    es = Elasticsearch()
    
    es.indices.create(index='twf-index', ignore=400)
    i = 0
    for fileName in listOfTextFiles:
        with open(fileName) as bodytx:
            tweets = {}
            tweets = json.load(bodytx)
        for key in tweets.keys():
            doc = {
                'url' : key,
                'text' : tweets[key]
            }
            es.index(index = 'twf-index' , doc_type='tweet',id = i, body = doc)
            i = i+1
    es.indices.refresh(index='twf-index')

    comparetweet = TwitterSearchV2.userSearchbyName(twitter_handle)
    comparetweet1 = comparetweet.split()
    ct1 = ""
    for wc in range(500):
        ct1 = ct1 + " " + comparetweet1[wc]
    q2= {
    "size": 8,
    "query": {
    "match": {"text": ct1}
        }}
    resA = es.search(index='twf-index',body = q2)
    urlList = []
    for hit in resA['hits']['hits']:
        urlList.append("%(url)s" % hit["_source"])
    return render_template('persoNews.html', urlList=urlList)


#Displaying news suggestions for celebrities
@app.route('/persoNewsceleb', methods=['GET', 'POST'])
def persoNewsceleb():
    return render_template('persoNewsceleb.html', urlList=urlList)



if __name__=='__main__':
    app.run(debug=True)
