#run 'export GOOGLE_APPLICATION_CREDENTIALS="your cloud vison json file"' in terminal
import tweets_video

# enter the twiiter keys needed to make the video
consumer_key = input("Please enter your consumer key:")
consumer_secret = input("Please enter the consumer secret:")
access_key = input("Please enter the access key:")
access_secret = input("Please enter the access secret:")

#enter the screen name and check if @ is missing
name = input("Please enter the twitter to fetch(remember to include the @):")
while '@' not in name:
    print("Oops, you forgot the @ symbol")
    name = input("Please try again:")
else:
    screen_name = name

#enter the number of tweets want to fetch and check if it's smaller than 200    
num = input("Please enter the number of tweets you want(the current version only supports numbers under 200):")
while int(num) > 200:
    print("I'm sorry, this version currently can't support that many tweets, the current maximum number is 200")
    num = input("Please try again:")
else:
    tweets_video.tweet_num = num

#pass the keys into tweets_video
tweets_video.consumer_key = consumer_key
tweets_video.consumer_secret = consumer_secret
tweets_video.access_key = access_key
tweets_video.access_secret = access_secret

#execute the get_video program
tweets_video.get_video(screen_name)
