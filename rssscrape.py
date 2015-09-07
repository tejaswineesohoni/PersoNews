import feedparser
import iron_celery
from celery import Celery
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=4)

#Fetch news links from RSS Feeds
def getrssfeed():

    d = feedparser.parse ('http://www.huffingtonpost.com/feeds/news.xml')
    rssfeed = []
    for post in d.entries:
        rssfeed.append(post.link)
    return rssfeed

def main():
    getrssfeed()

main()


