from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.template import Context

import tweepy
from collections import Counter

import re

from . import models

consumer_key = 'AJdeg3hr4BMeGITAve6yBEsGT'
consumer_secret = 'NqFSmrweF84yVHYckqkwdyS12Is5urRZ9JOsXJ08yGRaBDOQfz'
access_token = '942969496087814146-SkcAqlauIY8D9oMmHp3t6z2foqi2TFq'
access_secret = 'NC7nz5dIgENxkLtofyOIQO82coJ7U7Ewhv84rgeEaZzur'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

themes = {
    'sport': (
        'sport', 'football', 'sports', 'box', 'спорт', 'футбол', 'spectator', 'extreme', 'friendly', 'competition',
        'match', 'game', 'played', 'games', 'hockey', 'tennis', 'ball', 'training'),
    'news': (
        'news', 'breaking', 'weather', 'новость', 'information', 'communicating', 'people', 'television', 'newspapers',
        'mass',
        'attention', 'opinions'),
    'politics': (
        'president', 'administration', 'government', 'affairs', 'politics', 'country', 'political', 'influence',
        'governing',
        'organizations', 'sociopolitical'),
    'education': (
        'education', 'college', 'university', 'students', 'school', 'training', 'degree', 'study', 'advanced',
        'learning',
        'methods', 'science', 'knowledge', 'tutor', 'teacher'),
    'computers': (
        'browsers', 'byte', 'server', 'architecture', 'computer', 'system', 'bit', 'device', 'disc', 'network',
        'protocol', 'interface', 'operating', 'bitcoin', 'development', 'software', 'hardware', 'programming', 'python',
        'android',
        'ios')
}
KWTHEMES = {'sport': 0, 'news': 0, 'politics': 0, 'education': 0, 'computers': 0}

usersToAnalyze = ('ismetullah2', 'AhmadzaiMaher', 'ger_alt_j', 'acmilan', 'realDonaldTrump')

def countKeywords(userObject):
    print('Analyzing keywords of user {}'.format(userObject.screen_name))
    userClass = userObject.__class__.__name__
    try:
        if userClass == 'UserOne':
            userTweets = models.UserOneTweet.objects.get(user=userObject)
        else:
            userTweets = models.UserTwoTweet.objects.get(user=userObject)

        words = re.findall(r'\w+', userTweets.text)
        wordCounts = Counter(words)
        hits = dict(KWTHEMES)
        for kw, kwlist in themes.items():
            for kword in kwlist:
                hits[kw] += wordCounts[kword]
        try:
            if userClass == 'UserOne':
                userObjectHits = models.UserOneHit.objects.get(user=userObject)
                models.UserOneHit.objects.filter(user=userObject).update(**hits)
            else:
                userObjectHits = models.UserTwoHit.objects.get(user=userObject)
                models.UserTwoHit.objects.filter(user=userObject).update(**hits)

        except (models.UserTwoHit.DoesNotExist, models.UserOneHit.DoesNotExist):
            if userClass == 'UserOne':
                userObjectHits = models.UserOneHit(user=userObject, sport=hits['sport'], news=hits['news'], politics=hits['politics'],
                                        education=hits['education'], computers=hits['computers'])
                userObjectHits.save()
            else:
                userObjectHits = models.UserTwoHit(user=userObject, sport=hits['sport'], news=hits['news'],
                                                   politics=hits['politics'],
                                                   education=hits['education'], computers=hits['computers'])
                userObjectHits.save()

    except (models.UserOneTweet.DoesNotExist, models.UserTwoTweet.DoesNotExist):
        print('User {} has no tweets'.format(userObject.screen_name))
        return HttpResponse('User {} has no sufficient data to analyze'.format(userObject.screen_name))


def addToUserOneTable(user):
    try:
        uo = models.UserOne.objects.get(screen_name=user.screen_name)
    except models.UserOne.DoesNotExist:
        uo = models.UserOne(screen_name=user.screen_name, name=user.name, user_ID=user.id)
        uo.save()
    return uo


def addFollowsToUserTwoTable(user):
    friendIDS = api.friends_ids(user.screen_name)
    if len(friendIDS) == 0:
        return False
    for fid in friendIDS:
        print('{} follows {}'.format(user.screen_name, api.get_user(id=fid).screen_name, fid))
        friend = api.get_user(id=fid)
        try:
            ut = models.UserTwo.objects.get(user_ID=fid)
            ut.followed_by.add(user)
        except models.UserTwo.DoesNotExist:
            ut = models.UserTwo(screen_name=friend.screen_name, name=friend.name, user_ID=friend.id)
            ut.save()
            ut.followed_by.add(user)
        getUserTweets(ut, friend)


def getUserTweets(userObject, user):
    tweetCount = user.statuses_count
    if tweetCount == 0:
        return False
    print('Getting {} tweets of {}'.format(tweetCount, userObject.screen_name))
    oldest = user.status.id
    contents = ''
    count = 0

    while True:
        tweets = api.user_timeline(id=user.id, count=200, max_id=oldest)
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
        if userClass == 'UserOne':
            tweet = models.UserOneTweet(text=contents, user=userObject)
        else:
            tweet = models.UserTwoTweet(text=contents, user=userObject)
        tweet.save()

    if userClass == 'UserTwo':
        countKeywords(userObject)

def updateDB(request):
    for screenName in usersToAnalyze:
        thisUser = api.get_user(screenName)
        uo = addToUserOneTable(thisUser)
        print('Getting info of {}'.format(uo.screen_name))
        getUserTweets(uo, thisUser)
        addFollowsToUserTwoTable(uo)
        countKeywords(uo)

def index(request):
    content = {}
    uoqs = models.UserOne.objects.all()

    for uo in uoqs:
        print('In index: {}'.format(uo.screen_name))
        try:
            uohitInstance = models.UserOneHit.objects.get(user = uo)
            uohits = model_to_dict(uohitInstance, fields=('sport', 'news', 'politics', 'education', 'computers'))
        except models.UserOneHit.DoesNotExist:
            print('No hit data for {}'.format(uo.screen_name))
            uohits = {}
        content[uo.screen_name] = uohits
        content[uo.screen_name]['linkedUsers'] = dict(KWTHEMES)
        print(KWTHEMES)

        utInstances = models.UserTwo.objects.filter(followed_by=uo)
        for utIn in utInstances:
            print('Following {}'.format(utIn.screen_name))
            try:
                utIn = models.UserTwoHit.objects.get(user=utIn)
                utHits = model_to_dict(utIn, fields=('sport', 'news', 'politics', 'education', 'computers'))
                for k, v in utHits.items():
                    content[uo.screen_name]['linkedUsers'][k] += v
            except models.UserTwoHit.DoesNotExist:
                # print('No hit data for {}'.format(utIn.screen_name))
                pass

    print(content)
    return render(request, 'crawler/report.html', {'report': content})
