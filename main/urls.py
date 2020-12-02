"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from rest_framework import routers
from django.views.static import serve
from .views import ResetValues, Login, AddQuestion,EditAnswer,DeleteTutorial,EditTutorial, EditQuestion
from .views import OpenApi,Signup, AddFolder,ShareFile, Download_file, DeleteFile, ShowDevDrive, AppTour
from .views import DevDrive,AddCatTodo,Logout,ToDo, DeleteActivity, ActivityQuery, ShowActivity, CommentDisLike
from .views import AddActivity, Contact, About,EditProfile, SearchTutorial, OpenProfile, MainPage, ReviewQuestion
from .views import AddComment, DispTutorial,DispQuestion, AddTutorial, AddLikes, DisLike, AddAnswers, CommentLike
from .views import DeleteAnswer, DeleteQuestion,SearchQuestion, AcceptAnswer, ShowTutorials,CloseQuestion, Dashboard
from . import views
router = routers.DefaultRouter()
router.register(r'Questions', views.HeroViewSet)
router.register(r'Answers', views.AnswerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('Dashboard/', Dashboard, name='Dashboard'),
    path('main/', MainPage, name='main'),
    path('AskQuestion/', AddQuestion, name='AskQuestion'),
    path('ShowQuestion/<slug>/', DispQuestion, name='ShowQuestion'),
    path('AddLike/', AddLikes, name='AddLike'),
    path('AddDisLike/', DisLike, name='AddDisLike'),
    path('AddAnswer/<slug>', AddAnswers, name='AddAnswer'),
    path('DeleteAnswer/', DeleteAnswer, name='DeleteAnswer'),
    path('DeleteQuestion/<slug>/', DeleteQuestion, name='DeleteQuestion'),
    path('SearchQuestion/', SearchQuestion, name='SearchQuestion'),
    path('AcceptAnswer/', AcceptAnswer, name='AcceptAnswer'),
    path('AddTutorial/', AddTutorial, name='AddTutorial'),
    path('ShowTutorials/', ShowTutorials, name='ShowTutorials'),
    path('DispTutorial/<slug>/', DispTutorial, name='DispTutorial'),
    path('AddComment/<slug>', AddComment, name='AddComment'),
    path('SearchTutorial/', SearchTutorial, name='SearchTutorial'),
    path('OpenProfile/<user>/', OpenProfile, name='OpenProfile'),
    path('EditProfile/<ispass>/', EditProfile, name='EditProfile'),
    path('Logout/', Logout, name='Logout'),
    path('About/', About, name='About'),
    path('Contact/',Contact, name='Contact'),
    path('AddActivity/', AddActivity, name='AddActivity'),
    path('ShowActivity/',ShowActivity, name='ShowActivity'),
    path('ActivityQuery/', ActivityQuery, name='ActivityQuery'),
    path('DeleteActivity/', DeleteActivity, name='DeleteActivity'),
    path('ToDo/', ToDo, name='ToDo'),
    path('AddCatTodo/',AddCatTodo, name='AddCatTodo'),
    path('DevDrive/', DevDrive, name='DevDrive'),
    path('ShowDevDrive/',ShowDevDrive, name='ShowDevDrive'),
    path('DownloadFile/<pk>/',Download_file, name='DownloadFile'),
    path('DeleteFile/<pk>/',DeleteFile, name='DeleteFile'),
    path('AddFolder/',AddFolder, name='AddFolder'),
    path('ShareFile/<id>/',ShareFile, name='ShareFile'),
    path('RawData/', include(router.urls)),
    path('Api/', OpenApi, name='Api'),
    path('Signup/',Signup, name='Signup'),
    path('EditQuestion/<slug>/', EditQuestion, name='EditQuestion'),
    path('EditAnswer/<id>/', EditAnswer, name='EditAnswer'),
    path('DeleteTutorial/<id>/',DeleteTutorial, name='DeleteTutorial'),
    path('EditTutorial/<slug>/',EditTutorial, name='EditTutorial'),
    path('CloseQuestion/<slug>/',CloseQuestion, name='CloseQuestion'),
    path('AddCommentLike/', CommentLike, name='CommentLike'),
    path('AddCommentDisLike/', CommentDisLike, name='CommentDisLike'),
    path('AppTour/', AppTour, name='AppTour'),
    path('ReviewQuestion/', ReviewQuestion, name='ReviewQuestion'),
    path('ResetValues/', ResetValues, name='ResetValues'),

]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]