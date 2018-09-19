#!/usr/bin/env python
# encoding: utf-8
#Author - Prateek Mehta


import tweepy #https://github.com/tweepy/tweepy
import json
import urllib.request
import os
import PIL
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

picpaths = []
piclabel = []


#Twitter API credentials

global consumer_key
global consumer_secret
global access_key
global access_secret

#def vision_path(visionpath):
#    os.system('export GOOGLE_APPLICATION_CREDENTIALS=' + '"' + str(visionpath) + '"')
    

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
            picpaths.append(picpath)
            urllib.request.urlretrieve(mediaurl, picpath)
            n = n + 1

def make_video():
    os.system("ffmpeg -framerate 24 -r 1 -i /home/ece-student/pic/image%d.jpg output.mp4")        

def get_label():
    client = vision.ImageAnnotatorClient()
    for imagepath in picpaths:
        file_name = os.path.join(
            os.path.dirname(__file__),
            imagepath)

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        
        description = ''
        for label in labels:
            description = description + '<' + label.description + '>'
            
# add label to image        

        
        imageFile = imagepath
        im = Image.open(imageFile)
        width = im.size[0]
        
        font = ImageFont.truetype('LiberationSans-Regular.ttf', int(width/50))        
    
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), description, (255, 0, 0),font = font)    
        draw = ImageDraw.Draw(im)                          

        im.save(imagepath)


def get_video(screen_name):
    get_all_tweets(screen_name)
    get_label()
    make_video()
    
    


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@Ibra_official")
#    get_all_tweets("@BU_Tweets")
    get_label()
    make_video()
