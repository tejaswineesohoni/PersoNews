import oauth2
import time
import urllib2
import json
import rssscrape

#Get links from RSS Feed
def getLinks():
  data = rssscrape.getrssfeed()
  return data


#Call Twitter API and fetch tweets
def callTwitter(urlIn,otherParams,callType):
  CONSUMER_KEY = "DYqLbCBFr8ZpKPWJafizum7rm"
  CONSUMER_SECRET = "wAvH3UQxOgmGIgsM8rb5iVVMtNcudKnvFvu6rDmX5UGhV2WbPN"
  TOKEN_KEY = "633952001-HLjRHaATnDcYJSd0aBaQ8iig4Wq8Mr2eje3sdQhz"
  TOKEN_SECRET = "hPRimnhMKYKJwpHpEcYoUHkqGlwcN6N7ySbwJuX8mtjNT"
  url = urlIn
  reqParams = {
  "oauth_version": "1.0",
  "oauth_nonce": oauth2.generate_nonce(),
  "oauth_timestamp": int(time.time())
  }
  params = dict(reqParams.items() + otherParams.items()) 
  consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
  token = oauth2.Token(key=TOKEN_KEY, secret=TOKEN_SECRET)
  params["oauth_consumer_key"] = consumer.key
  params["oauth_token"] = token.key    
  req = oauth2.Request(method=callType, url=url, parameters=params)
  signature_method = oauth2.SignatureMethod_HMAC_SHA1()
  req.sign_request(signature_method, consumer, token)
  headers = req.to_header()
  url = req.to_url()
  response = urllib2.Request(url)
  data = json.load(urllib2.urlopen(response))
  return data


#Search Twitter for tweets which contain the links we have 
def urlSearch(urlIn):
  SEARCH_API = "https://api.twitter.com/1.1/search/tweets.json"
  tweeters = []
  params = {}
  params["q"] = urlIn
  params["result_type"] = "recent"
  params["count"] = 5
  dataOut = callTwitter(SEARCH_API,params,"GET")
  for tweet in range(len(dataOut["statuses"])):
      tweeters.append(dataOut["statuses"][tweet]["user"]["id"])
  return tweeters


#Search Twitter for users who have tweeted out the news links we have
def userSearch(tweeter):
  USER_API = "https://api.twitter.com/1.1/statuses/user_timeline.json"
  body_list = []
  params = {}
  params["user_id"] = tweeter
  params["count"] = 100
  params["include_rts"] = "true"
  dataOut = callTwitter(USER_API,params,"GET")
  for tweet in range(len(dataOut)):
    body_list.append(dataOut[tweet]["text"])
  return "".join(body_list)


#Search Twitter for users by their Twitter handle
def userSearchbyName(tweeter):
  USER_API = "https://api.twitter.com/1.1/statuses/user_timeline.json"
  body_list = []
  params = {}
  params["screen_name"] = tweeter
  params["count"] = 100
  params["include_rts"] = "true"
  dataOut = callTwitter(USER_API,params,"GET")
  print dataOut[0]["user"]["screen_name"]
  for tweet in range(len(dataOut)):
    body_list.append(dataOut[tweet]["text"])
  return "".join(body_list)
  

#Fetch Tweets of the users tweeting out the news links
def twitterSearch():
  bodyText = {}
  RATE_API = "https://api.twitter.com/1.1/application/rate_limit_status.json"
  
  urlLinks = getLinks()
  for i in range(len(urlLinks)):
    print "\n" + str(urlLinks[i])
    bodyText[urlLinks[i]] = ""
    tweetingUsers = []
    tweetingUsers = urlSearch(urlLinks[i])
    print "Users Tweeting This Article:"
    for j in range(len(tweetingUsers)):
      userBody = userSearch(tweetingUsers[j])
      bodyText[urlLinks[i]] = bodyText[urlLinks[i]] + userBody  
  outputFile = "BodyTexts.json"
  with open(outputFile, "w") as outfile:
		  json.dump(bodyText, outfile, indent=4)
  listOfTextFiles = [outputFile]

  return listOfTextFiles


def main():
  twitterSearch()
  
    
if __name__ == '__main__':
  main()
