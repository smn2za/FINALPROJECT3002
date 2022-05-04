# import stuff
import tweepy
import time
from credentials import *
from urllib import request
file_name = 'lastseen.txt'

# connect
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# set API
api = tweepy.API(auth)

# set id so we don't reply to our own tweets
bot_id = int(api.verify_credentials().id_str)

# fetch new tweets that mention bot and not the same one over and over
mention_id = 1

# configure quote grabbing from API -- using same code from discord bot

# use urllib to connect to webpage
html_content = request.urlopen('https://api.quotable.io/random')
html = str(html_content.read())

# find where quote starts, author starts, and ends
quote_finder = html.find("content")
author_finder = html.find("author")
endpoint = html.find("authorSlug")
# "authorslug" comes immediately after so it serves as an endpoint

# index and print values at those indices and take out unnecessary words/characters
full_quote = str(html[quote_finder + 9:author_finder - 2:])
author = str(html[author_finder + 9:endpoint - 3])

# set up help message
help_message = "To receive a quote, tweet me with the word quote"

# set up actual quote reply
quote_message = full_quote + " - " + author


# get last ID replied to
def read_last_seen(file_name):
    file_read = open(file_name, 'r')
    last_seen_id = file_read.read().strip()
    file_read.close()
    return last_seen_id


# overwrite last ID replied to
def store_last_seen(file_name, last_seen_id):
    file_write = open(file_name, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


# reply function
def reply():
    tweets = api.mentions_timeline()
    for tweet in tweets:
        # help message
        if 'quotebot3002' and 'help' in tweet.text:
            api.update_status('@' + tweet.user.screen_name + " " + help_message)
            print("Helped " + str(tweet.id))
        # quote message
        if 'quotebot3002' and 'quote' in tweet.text:
            api.update_status('@' + tweet.user.screen_name + " " + quote_message)
            print("Gave" + str(tweet.id) + " a quote!")
        store_last_seen(file_name, tweet.id)
        api.create_favorite(tweet.id)  # like tweet with mention


# run bot
while True:
    reply()
    time.sleep(15)
