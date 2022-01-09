import emoji
import tweepy
from os import environ
from random import randint
import requests

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

user = api.get_user(screen_name='bot_trolley')

def make_problem():
    page = requests.get('https://raw.githubusercontent.com/homomorfismo/trolley_problem_bot/main/twemojis.txt')
    twemojis = page.text.split('\n')
    n = len(twemojis)
    emoji1 = twemojis.pop(randint(0,n))[:-1]
    emoji2 = twemojis[randint(0,n-1)][:-1]
    pretweet = """
    Who do you want to save?
    🔁 for {0}
    :heart: for {1}

    🌲      🌲🌲        🌲
    _____{0}_____________🚂___
    _____{1}_______/ 
    🌲          🌲      🌲🌲

    """.format(emoji1, emoji2)
    return emoji.emojize(pretweet, use_aliases=True)

def action():
    TL = user.timeline()
    if len(TL) > 0:
        tweet = user.timeline()[0]
        if 'Who' in tweet.text:
            solve_problem(tweet)
        else:
            new_problem = make_problem()
            api.update_status(new_problem)
    else:
        new_problem = make_problem()
        api.update_status(new_problem)

def solve_problem(tweet):    
    tweet = user.timeline(tweet_mode = 'extended')[0]
    splitted = tweet.full_text.split()
    emoji1 = splitted[8]
    emoji2 = splitted[11]
    if tweet.retweet_count >= tweet.favorite_count:
        tweets = ["""

        🌲      🌲🌲        🌲
_____{0}_____________🚂___
_____{1}_______/ 
🌲          🌲      🌲🌲

        """.format(emoji1, emoji2),
        """
        🌲      🌲🌲        🌲
_____{0}_🚂_______________
_____{1}_______/ 
🌲          🌲      🌲🌲
        """.format(emoji1, emoji2),
        """
        🌲      🌲🌲        🌲
_🚂______________________
_____{1}_______/ 
🌲          🌲      🌲🌲
        """.format(emoji1, emoji2)]
        t1 = api.update_status(status=tweets[0])
        t2 = api.update_status(status=tweets[1], 
                                 in_reply_to_status_id=t1.id, 
                                 auto_populate_reply_metadata=True)
        t2 = api.update_status(status=tweets[2], 
                                 in_reply_to_status_id=t2.id, 
                                 auto_populate_reply_metadata=True)
    else:
        tweets = ["""

        🌲      🌲🌲        🌲
_____{0}_____________🚂___
_____{1}_______/ 
🌲          🌲      🌲🌲

        """.format(emoji1, emoji2),
        """
        🌲      🌲🌲        🌲
_____{0}__________________
_____{1}___🚂__/ 
🌲          🌲      🌲🌲
        """.format(emoji1, emoji2),
        """
        🌲      🌲🌲        🌲
_____{0}__________________
_🚂__x_________/  
🌲          🌲      🌲🌲
        """.format(emoji1, emoji2)]
        t1 = api.update_status(status=tweets[0])
        t2 = api.update_status(status=tweets[1], 
                                 in_reply_to_status_id=t1.id, 
                                 auto_populate_reply_metadata=True)
        t2 = api.update_status(status=tweets[2], 
                                 in_reply_to_status_id=t2.id, 
                                 auto_populate_reply_metadata=True)