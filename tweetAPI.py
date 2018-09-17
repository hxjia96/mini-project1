#!/usr/bin/env python
# encoding: utf-8
#Author - Prateek Mehta


import tweepy #https://github.com/tweepy/tweepy
import json
import urllib.request
#import os


#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
#    os.mkdir('pic')
    alltweets = []
#    mediaurls = []
    n = 1
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    for tweet in alltweets:
        entities = tweet._json['entities']
        if 'media' not in entities:
            continue
        else:
            media = entities['media']
            mediaurl = media[0]['media_url']
#            mediaurls.append(mediaurl)
            picpath = 'pic/image' + str(n) + '.jpg'
            urllib.request.urlretrieve(mediaurl, picpath)
            n = n + 1
        

if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@Ibra_official")
