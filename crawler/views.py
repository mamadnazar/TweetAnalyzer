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
        uo = models.UserOne.objects.get(screenName=user.screen_name)
    except models.UserOne.DoesNotExist:
        uo = models.UserOne(screenName=user.screen_name, name=user.name, userId = user.id)
        uo.save()

def index(request):
    for username in usersToAnalyze:
        thisUser = api.get_user(username)
        addToUserOneTable(thisUser)

    stri = ''
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        stri += tweet.text + '\n'
    return HttpResponse(stri)