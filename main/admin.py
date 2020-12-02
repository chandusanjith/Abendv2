from django.contrib import admin
from .models import Tags,UserLastOpenedQuestions,MLdata,cedge_Teams, Badges_Master, Comment_likes, Badges, Reputation, Questions,DriveFolder,Notifications, DisLikes, Likes, Answers, Drive,Tutorials, Contacted, Activities, TodoCategory, ToDo


admin.site.register(Tags)
admin.site.register(UserLastOpenedQuestions)
admin.site.register(MLdata)
admin.site.register(Questions)
admin.site.register(Likes)
admin.site.register(DisLikes)
admin.site.register(Answers)
admin.site.register(Tutorials)
admin.site.register(Contacted)
admin.site.register(Activities)
admin.site.register(TodoCategory)
admin.site.register(ToDo)
admin.site.register(Drive)
admin.site.register(DriveFolder)
admin.site.register(Notifications)
admin.site.register(Badges_Master)
admin.site.register(Reputation)
admin.site.register(Badges)
admin.site.register(cedge_Teams)
admin.site.register(Comment_likes)