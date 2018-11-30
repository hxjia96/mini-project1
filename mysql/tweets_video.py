#!/usr/bin/env python
# encoding: utf-8
# Copyright 2018 Haoxuan Jia hxjia@bu.edu

import pymysql
import tweepy #https://github.com/tweepy/tweepy
import json
import urllib.request
import os
import io 
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# global list to hold the url got from tweepy and description got from clould vision
picpaths = []
piclabel = []
#des = {}


global username

#Twitter API credentials
global consumer_key
global consumer_secret
global access_key
global access_secret
    
db = pymysql.connect("localhost","root","123456","miniproject3")
 
cursor = db.cursor()
  
sql = """CREATE TABLE IF NOT EXISTS information1 (
         USERNAME  CHAR(20) NOT NULL,
         TWITTER  CHAR(20),
         TWEET_NUM INT,
         PICTURE_NUM INT,
         DESCRIPTION TEXT,
         COUNT TEXT )""" 

cursor.execute(sql)
 
db.close()

post = {}
#post['description'] = []
#des = {}
post['count'] = {}

def get_all_tweets(screen_name, tweet_num):
    print("downloading the images..")    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #detect if there is a internet problem or if the screen_name is wrong    
    try:
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name, count=tweet_num)
    except:
        print("Twitter is not responding, you might have entered a wrong twitter name or there's a problem with your internet")
        os._exit(0)
    
    #create a fold to keep the images
    if not os.path.exists('pic'):
        os.mkdir('pic')
    
    #a list to keep all the tweet information
    alltweets = []

    
    n = 1
        
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #get the url of images and save them as image1.jpg, image2.jpg, ...
    for tweet in alltweets:
        entities = tweet._json['entities']
        if 'media' not in entities:
            continue
        else:
            media = entities['media']
            mediaurl = media[0]['media_url']
            picpath = 'pic/image' + str(n) + '.jpg'
            picpaths.append(picpath)
            urllib.request.urlretrieve(mediaurl, picpath)
            n = n + 1
    post['picture num'] = n - 1
    
def make_video():
    # use FFMPEG to create a video out of images in pic folder
    print("generating the video..")
    os.system("ffmpeg -framerate 24 -r 1 -i ./pic/image%d.jpg -s 1080*1080 output.mp4")        

def get_label():
    #get labels information of the images from google cloud vision
    print("labeling the images..")
    client = vision.ImageAnnotatorClient()
    for imagepath in picpaths:
        file_name = os.path.join(
            os.path.dirname(__file__),
            imagepath)
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)

        #detect if there is a problem with the internet        
        try:
            response = client.label_detection(image=image)
            labels = response.label_annotations
        except:
            print("Google Vision is not responding, there might be a problem with your internet")
            os._exit(0)
        
        # get the description from the label information and put them three in a row
        descriptions = []
        raw_description = []
        description= ''        
        num = 0
        row = 0
        for label in labels:
            raw_description.append(label.description)
            description = description + '<' + label.description + '>'
            num = num + 1
            if num%3 == 0 or label == labels[-1]:
                descriptions.append(description)
                description = ''
                row = row + 1
#        for rdes in raw_description:
#            des.setdefault(rdes, 0)
#            if rdes in des:
#                des[rdes] = des[rdes] + 1
        for rdes in raw_description:
            post['count'].setdefault(rdes, 0)
            if rdes in post['count']:
                post['count'][rdes] = post['count'][rdes] + 1
                
#        post['description'] = des
#        imagename = imagepath.replace('pic/', '')
#        post[imagename.replace('.jpg', '')] = raw_description
        
        #add description to each of the images
        imageFile = imagepath
        im = Image.open(imageFile)        
        font = ImageFont.truetype('LiberationSans-Regular.ttf', 24)            
        draw = ImageDraw.Draw(im)
        for i in range(row):            
            draw.text((0, 30*i), descriptions[i], (255, 0, 0),font = font)    
        draw = ImageDraw.Draw(im)                          
        im.save(imagepath)

# the whole process of making a video from images from tweets
def get_video(screen_name):
    post['username'] = username
    post['tweet num'] = tweet_num
    post['screen_name'] = screen_name
#    post['date'] = datetime.datetime.now()
    get_all_tweets(screen_name, tweet_num)
    get_label()
    description =[]
    times = []
    for i in post['count']:
        description.append(i)
        times.append(str(post['count'][i]))
    description_str = ','.join(description)
    a = description_str
    times_str = ','.join(times)
#    print(description_str)
#    print(times_str)
    make_video()
    db = pymysql.connect("localhost","root","123456","miniproject3")
 
    cursor = db.cursor()
 
#cursor.execute("DROP TABLE IF EXISTS employee")
 
    sql = "INSERT INTO information1 (USERNAME, TWITTER, TWEET_NUM, PICTURE_NUM, DESCRIPTION, COUNT) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (post['username'], post['screen_name'], post['tweet num'], post['picture num'], description_str, times_str)
    cursor.execute(sql, val)

    db.commit() 
    db.close()
    
    print("the video is ready, have a look at it")
    
    
#runing directly from this file    
if __name__ == '__main__':
    get_video("@Ibra_official")

