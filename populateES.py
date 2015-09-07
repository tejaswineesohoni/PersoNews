import json
from datetime import datetime
from elasticsearch import Elasticsearch
import TwitterSearchV2
import json
import pickle
import sys
from flask import Flask
from pyelasticsearch import ElasticSearch


#Fill ElasticSearch database with Tweets indexed by the news links
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


if __name__ == '__main__':
    main()
