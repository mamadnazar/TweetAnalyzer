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

usersToAnalyze = ('ismetullah2', 'AhmadzaiMaher', 'ger_alt_j', 'acmilan', 'realDonaldTrump')

def addToUserOneTable(user):
    try:
        uo = models.UserOne.objects.get(screen_name=user.screen_name)
    except models.UserOne.DoesNotExist:
        uo = models.UserOne(screen_name=user.screen_name, name=user.name, user_ID = user.id)
        uo.save()
    return uo

def addFollowsToUserTwoTable(user):
    for fid in api.friends_ids(user.screen_name):
        print('{} follows {}...'.format(user.screen_name, fid))
        try:
            ut = models.UserTwo.objects.get(user_ID = fid)
            ut.followed_by.add(user)
        except models.UserTwo.DoesNotExist:
            friend = api.get_user(id=fid)
            ut = models.UserTwo(screen_name=friend.screen_name, name=friend.name, user_ID=friend.id)
            ut.save()
            ut.followed_by.add(user)

def getUserTweets(userO, user):
    tweetCount = user.statuses_count
    print('Getting {} tweets of {}'.format(tweetCount, userO.screen_name))
    oldest = user.status.id
    contents = ''
    count = 0

    while True:
        tweets = api.user_timeline(id = user.id, count=200, max_id = oldest)
        if len(tweets) < 1:
            break
        count += len(tweets)
        oldest = tweets.max_id
        for tweet in tweets:
            contents += tweet.text + ' '
    print('{} tweets of {} were stored'.format(count, userO.screen_name))

    try:
        tweet = models.Tweet.objects.get(user=userO)
        tweet.text = contents
        tweet.save()
    except models.Tweet.DoesNotExist:
        tweet = models.Tweet(text=contents, user = userO)
        tweet.save()

def index(request):
    for screenName in usersToAnalyze:
        thisUser = api.get_user(screenName)
        uo = addToUserOneTable(thisUser)
        print(uo.screen_name)
        addFollowsToUserTwoTable(uo)
        # if uo.screen_name == 'Ismetullah2' or uo.screen_name == 'ger_alt_j':
        getUserTweets(uo, thisUser)

    stri = ''
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        stri += tweet.text + '\n'
    return HttpResponse(stri)