import json
from datetime import datetime
from elasticsearch import Elasticsearch
import TwitterSearchV2
import json
import pickle
import sys
from flask import Flask
from pyelasticsearch import ElasticSearch


#Find the most relevant articles by matching documents in ElasticSearch
def findRelavantArticles():
    
  es = Elasticsearch()
  comparetweet = TwitterSearchV2.userSearchbyName("drubix_cube")
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
  return urlList


#Fill ElasticSearch database with Tweets indexed by news links
def fillElasticSearch():
    
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

  
def main():
  fillElasticSearch()
  findRelavantArticles()

   
if __name__ == '__main__':
    main()
