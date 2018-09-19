import tweets_video


tweets_video.consumer_key = "Enter the consumer key"
tweets_video.consumer_secret = "Enter the consumer secret"
tweets_video.access_key = "Enter the access key"
tweets_video.access_secret = "Enter the access secret"

#run 'export GOOGLE_APPLICATION_CREDENTIALS="your cloud vison json file"' in terminal

tweets_video.get_video("Enter the screen name")
