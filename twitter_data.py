#  Author:  Cheryl Dugas

# twitter_data.py searches Twitter for tweets matching a search term,
#      up to a maximun number

######  user must supply authentication keys where indicated

# to run from terminal window: 
#        python3  twitter_data.py   --search_term  mysearch   --search_max  mymaxresults 
# where:  mysearch is the term the user wants to search for;  default = music
#   and:  mymaxresults is the maximum number of resulta;  default = 30

# other options used in the search:  lang = "en"  (English language tweets)
#  and  result_type = "popular"  (asks for most popular rather than most recent tweets)

# The program uses the TextBlob sentiment property to analyze the tweet for:
#  polarity (range -1 to 1)  and  
#  subjectivity (range 0 to 1 where 0 is objective and 1 is subjective)

# The program creates a .csv output file with a line for each tweet
#    including tweet data items and the sentiment information

from textblob import TextBlob	# needed to analyze text for sentiment
import argparse    				# for parsing the arguments in the command line
import csv						# for creating output .csv file
import tweepy					# Python twitter API package
import unidecode				# for processing text fields in the search results

### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = "put key here"
CONSUMER_KEY_SECRET = "put secret here"
ACCESS_TOKEN = "put key here"
ACCESS_TOKEN_SECRET = "put secret here"

# AUTHENTICATION (OAuth)
authenticate = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(authenticate)

# Get the input arguments - search_term and search_max
parser = argparse.ArgumentParser(description='Twitter Search')
parser.add_argument("--search_term", action='store', dest='search_term', default="music")
parser.add_argument("--search_max", action='store', dest='search_max', default=30)
args = parser.parse_args()

search_term = args.search_term
search_max = int(args.search_max)

# create a .csv file to hold the results, and write the header line
csvFile = open('twitter_results.csv','w')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["username","userid","created", "text", "retweets", "followers",
    "friends","polarity","subjectivity"])

# do the twitter search
for tweet in tweepy.Cursor(api.search, q = search_term, lang = "en", 
		result_type = "popular").items(search_max):
		
    created = tweet.created_at				# date created
    text = tweet.text						# text of the tweet
    text = unidecode.unidecode(text) 
    retweets = tweet.retweet_count			# number of retweets
    username  = tweet.user.name            	# user name
    userid  = tweet.user.id              	# userid
    followers = tweet.user.followers_count 	# number of user followers
    friends = tweet.user.friends_count      # number of user friends
    
	# use TextBlob to determine polarity and subjectivity of tweet
    text_blob = TextBlob(text)
    polarity = text_blob.polarity
    subjectivity = text_blob.subjectivity
    
	# write tweet info to .csv tile
    csvWriter.writerow([username, userid, created, text, retweets, followers, 
    	friends, polarity, subjectivity])


csvFile.close()
