from django.db import models

# Create your models here.

class UserOne(models.Model):
    name = models.CharField(max_length=100, null=False)
    screen_name = models.CharField(max_length=100, null=False, unique=True)
    user_ID = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.screen_name)


class UserTwo(models.Model):
    name = models.CharField(max_length=100, null=False)
    screen_name = models.CharField(max_length=100, null=False, unique=True)
    user_ID = models.IntegerField(null=True, unique=True)

    followed_by = models.ManyToManyField(UserOne, related_name='follows', verbose_name='Followers')

    def __str__(self):
        return '{} {}'.format(self.name, self.screen_name)

class UserOneTweet(models.Model):
    user = models.ForeignKey(UserOne, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return 'Tweets of {}'.format(self.user.name)


class UserTwoTweet(models.Model):
    user = models.ForeignKey(UserTwo, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return 'Tweets of {}'.format(self.user.name)

class UserOneHit(models.Model):
    user = models.ForeignKey(UserOne, on_delete=models.CASCADE)

    sport = models.IntegerField(default=0)
    news = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    education = models.IntegerField(default=0)
    computers = models.IntegerField(default=0)

    def __str__(self):
        return 'Hit counter of {}'.format(self.user)

class UserTwoHit(models.Model):
    user = models.ForeignKey(UserTwo, on_delete=models.CASCADE)

    sport = models.IntegerField(default=0)
    news = models.IntegerField(default=0)
    politics = models.IntegerField(default=0)
    education = models.IntegerField(default=0)
    computers = models.IntegerField(default=0)

    def __str__(self):
        return 'Hit counter of {}'.format(self.user)