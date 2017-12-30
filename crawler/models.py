from django.db import models

# Create your models here.

class UserOne(models.Model):
    name = models.CharField(max_length=100, null=False)
    screen_name = models.CharField(max_length=100, null=False, unique=True)
    user_ID = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return self.name + ' ' + str(self.user_ID)

class UserTwo(models.Model):
    name = models.CharField(max_length=100, null=False)
    screen_name = models.CharField(max_length=100, null=False, unique=True)
    user_ID = models.IntegerField(null=True, unique=True)

    followed_by = models.ManyToManyField(UserOne, related_name='follows', verbose_name='Followers')

    def __str__(self):
        return self.name + ' ' + str(self.user_ID)

class SportsKW(models.Model):
    count = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    user = models.ForeignKey(UserOne, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.name, self.count)

class Tweet(models.Model):
    text = models.TextField()
    user = models.ForeignKey(UserOne, on_delete=models.CASCADE)

    def __str__(self):
        return 'Tweets of {}'.format(self.user.name)