from django.contrib import admin
from .models import UserOne, UserTwo, UserOneTweet, UserTwoTweet, UserOneHit, UserTwoHit

# Register your models here.

class FollowInline(admin.TabularInline):
    model = UserTwo.followed_by.through
    extra = 0

class UserOneAdmin(admin.ModelAdmin):
    model = UserOne
    list_display = ('name', 'screen_name', 'user_ID')
    inlines = (FollowInline, )

class UserTwoAdmin(admin.ModelAdmin):
    model = UserTwo
    list_display = ('name', 'screen_name', 'user_ID')
    inlines = (FollowInline,)
    exclude = ('followed_by', )


admin.site.register(UserOne, UserOneAdmin)
admin.site.register(UserTwo, UserTwoAdmin)
admin.site.register(UserOneTweet)
admin.site.register(UserTwoTweet)
admin.site.register(UserOneHit)
admin.site.register(UserTwoHit)