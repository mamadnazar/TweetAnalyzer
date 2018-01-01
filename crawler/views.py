from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
import json
import tweepy

from . import models

consumer_key = 'AJdeg3hr4BMeGITAve6yBEsGT'
consumer_secret = 'NqFSmrweF84yVHYckqkwdyS12Is5urRZ9JOsXJ08yGRaBDOQfz'
access_token = '942969496087814146-SkcAqlauIY8D9oMmHp3t6z2foqi2TFq'
access_secret = 'NC7nz5dIgENxkLtofyOIQO82coJ7U7Ewhv84rgeEaZzur'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

sports_keywords = ('sport', 'football', 'sports', 'box', 'спорт', 'футбол', 'spectator','extreme', 'friendly','competition', 'match', 'game', 'played', 'games', 'hockey', 'tennis', 'ball', 'training')
news_keywords = ('news', 'breaking', 'weather', 'новость', 'information', 'communicating', 'people', 'television', 'newspapers', 'mass', 'attention', 'opinions')
politics = ('president', 'administration', 'government', 'affairs', 'politics', 'country', 'political', 'influence', 'governing', 'organizations', 'sociopolitical')
education = ('education', 'college', 'university', 'students', 'school', 'training', 'degree', 'study', 'advanced', 'learning', 'methods', 'science', 'knowledge', 'tutor', 'teacher')
computers = ('', )

usersToAnalyze = ('ismetullah2', 'AhmadzaiMaher', 'ger_alt_j', 'acmilan', 'realDonaldTrump')

'''
def countKeywords():
    words = re.findall(r'\w+', tt.lower())
'''

def addToUserOneTable(user):
    try:
        uo = models.UserOne.objects.get(screen_name=user.screen_name)
    except models.UserOne.DoesNotExist:
        uo = models.UserOne(screen_name=user.screen_name, name=user.name, user_ID = user.id)
        uo.save()
    return uo

def addFollowsToUserTwoTable(user):
    for fid in api.friends_ids(user.screen_name):
        print('{} follows {}'.format(user.screen_name, api.get_user(id=fid).screen_name, fid))
        friend = api.get_user(id=fid)
        try:
            ut = models.UserTwo.objects.get(user_ID = fid)
            ut.followed_by.add(user)
        except models.UserTwo.DoesNotExist:
            ut = models.UserTwo(screen_name=friend.screen_name, name=friend.name, user_ID=friend.id)
            ut.save()
            ut.followed_by.add(user)
        getUserTweets(ut, friend)

def getUserTweets(userObject, user):
    tweetCount = user.statuses_count
    print('Getting {} tweets of {}'.format(tweetCount, userObject.screen_name))
    oldest = user.status.id
    contents = ''
    count = 0

    while True:
        tweets = api.user_timeline(id = user.id, count=200, max_id = oldest)
        if len(tweets) < 1:
            break
        count += len(tweets)
        oldest = tweets.max_id
        for tw in tweets:
            contents += tw.text + ' '
    print('{} tweets of {} were stored'.format(count, userObject.screen_name))

    userClass = userObject.__class__.__name__

    try:
        if userClass == 'UserOne':
            tweet = models.UserOneTweet.objects.get(user=userObject)
        else:
            tweet = models.UserTwoTweet.objects.get(user=userObject)
        tweet.text = contents
        tweet.save()
    except (models.UserOneTweet.DoesNotExist, models.UserTwoTweet.DoesNotExist):
        print('here 3')
        if userClass == 'UserOne':
            tweet = models.UserOneTweet(text=contents, user=userObject)
        else:
            tweet = models.UserTwoTweet(text=contents, user=userObject)
        tweet.save()

def index(request):
    for screenName in usersToAnalyze:
        thisUser = api.get_user(screenName)
        uo = addToUserOneTable(thisUser)
        print('Getting info of {}'.format(uo.screen_name))
        getUserTweets(uo, thisUser)
        addFollowsToUserTwoTable(uo)

    stri = ''
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        stri += tweet.text + '\n'
    return HttpResponse(stri)