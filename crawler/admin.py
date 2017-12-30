from django.contrib import admin
from .models import UserOne, UserTwo, SportsKW

# Register your models here.

class UserOneAdmin(admin.ModelAdmin):
    model = UserOne
    list_display = ('name', 'screenName', 'userId')

class UserTwoAdmin(admin.ModelAdmin):
    model = UserTwo
    list_display = ('name', 'screenName', 'userId')

admin.site.register(UserOne, UserOneAdmin)
admin.site.register(UserTwo, UserTwoAdmin)
admin.site.register(SportsKW)