# PersoNews
Personalized News Aggregator Using Twitter

persoNews is a collection of Python codes and HTML pages running on Flask. This
application was previously deployed on Heroku­Cedar stack, but we have taken it down
because Heroku is charging the addons used in this application.

persoNews uses ElasticSearch that acts as a search engine in the background, which will
return results based on similarity.

Installation of Components:

Python
We used Python 2.7 for this project. Python 2.7 can be installed from Python installer package
from here: (‘https://www.python.org/download/releases/2.7/’)

Python modules used for this project:
Elasticsearch
Flask
Pyelasticsearch
Feedparser

All the modules can be installed using
pip install <modulename>
from your command prompt.

Flask
Flask is used to integrate the python codes and the html pages of this application.

ElasticSearch
Installation package for ElasticSearch is available from this site:
(‘http://www.elasticsearch.org/download/’).

To start ElasticSearch from your local machine, go to the ElasticSearch local folder and type
./elasticsearch –f
from your command prompt.

Getting started:
1. Copy the application folder to your local flask app directory
2. Run TwitterSearchV2.py to get the list of users that tweets a particular news links from
RSS feeds and the body of their most recent 100 tweets.
3. Run relevantarticles.py to populate the data inside ElasticSearch.
4. Run routes.py to start the application.
5. You can now access persoNews from this page (‘http://localhost:5000’).
