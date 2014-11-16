import urllib2
import json
from google.appengine.api import urlfetch

def httpget(url):
    try:
        urlfetch.set_default_fetch_deadline(60)
        result = urllib2.urlopen(url)
        return result
    except urllib2.URLError, e:
        handleError(e)

def get_feed(appid):
    return json.load(httpget("https://itunes.apple.com/gb/rss/customerreviews/id=" + str(appid) + "/sortBy=mostRecent/json"))

def get_apps(config):
    return json.load(httpget("https://s3-eu-west-1.amazonaws.com/appreviewconfig/" + config + ".json"))["apps"]

