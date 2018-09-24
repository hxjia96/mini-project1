#run 'export GOOGLE_APPLICATION_CREDENTIALS="your cloud vison json file"' in terminal
import tweets_video

consumer_key = input("Enter your consumer key:")
consumer_secret = input("Enter the consumer secret")
access_key = input("Enter the access key")
access_secret = input("Enter the access secret")
screen_name = input("Enter the screen name:")

tweets_video.consumer_key = consumer_key
tweets_video.consumer_secret = consumer_secret
tweets_video.access_key = access_key
tweets_video.access_secret = access_secret


tweets_video.get_video(screen_name)
