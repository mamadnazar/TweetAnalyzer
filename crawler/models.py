from django.db import models

# Create your models here.

class UserOne(models.Model):
    name = models.CharField(max_length=100, null=False)
    screenName = models.CharField(max_length=100, null=False, unique=True)
    userId = models.IntegerField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.name + ' ' + str(self.userId)

class UserTwo(models.Model):
    name = models.CharField(max_length=100, null=False)
    screenName = models.CharField(max_length=100, null=False, unique=True)
    userId = models.IntegerField(max_length=100, null=True, unique=True)

    followedBy = models.ManyToManyField('UserOne', related_name='follows')

    def __str__(self):
        return self.name + ' ' + str(self.userId)

class SportsKW(models.Model):
    count = models.IntegerField(default=0)
    name = models.CharField(max_length=100)

    user = models.ForeignKey(UserOne, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.name, self.count)