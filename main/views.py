from django.http import HttpResponse, FileResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from random import randrange
from .MachineLearningAlgorithms.TrainAI import InitialLoad, RetrainModel
from .MachineLearningAlgorithms.Train_spam_ham_ai import Check_spam_ham

from .models import Questions,cedge_Teams, Likes,Badges_Master, AllLogin, Badges, DriveFolder,Reputation, \
     Notifications,MLdata, UserLastOpenedQuestions, DisLikes, Answers, Tutorials, Contacted, Activities, Drive, Tags, ToDo, TodoCategory, Comment_likes, Comment_DisLikes
import datetime
from django.contrib.auth import logout as django_logout
from django.db.models import F,Q
from .forms import BlogForm
from .CreateDataSet import CreateDS
import itertools
import pickle
#from TrainAI import get_index_from_id, get_index_from_title

import random
import string
import xlwt
import filetype
from rest_framework import viewsets
from .serializers import HeroSerializer,AnswerSerializer
from django.template.loader import render_to_string


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def Login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            AllLogin.objects.create(user=request.user)
            return HttpResponseRedirect('/Dashboard/')
        else:
           return render(request, 'index.html')
    else:
        uid = request.POST["uname"]
        password = request.POST["psw"]
        user = auth.authenticate(username=uid, password=password)

        if user is not None:
            auth.login(request, user)
            AllLogin.objects.create(user=request.user)
            return HttpResponseRedirect('/Dashboard/')
        else:
            messages.info(request, 'Invalid login details')
            return HttpResponseRedirect('/')

def Signup(request):
     if request.method == "GET":
         teams = cedge_Teams.objects.all()
         context={
             'teams':teams
         }
         return render(request, 'Signup.html',context)
     else:
         uname = request.POST['uname']
         fnames = request.POST['fnames']
         snames = request.POST['snames']
         cmail = request.POST['cmail']
         Password1 = request.POST['Password1']
         Password2 = request.POST['Password2']
         userexist = User.objects.filter(username=uname)
         password_is_good, pass_message = password_check(Password1)
         if Password1 != Password2:
             messages.info(request, 'Passwords not matching')
             return render(request, 'Signup.html')
         elif User.objects.filter(username=uname).exists():
             messages.info(request, 'User already exist')
             return render(request, 'Signup.html')
         elif User.objects.filter(email=cmail).exists():
             messages.info(request, 'email already exist')
             return render(request, 'Signup.html')
         elif password_is_good == False:
             messages.info(request, pass_message)
             return render(request, 'Signup.html')
         else:
             authuser = User.objects.create_user(username=uname, password=Password1, email=cmail, first_name=fnames, last_name=snames)
             authuser.save()
             messages.info(request, 'Registered succesfully!')
             return HttpResponseRedirect('/')

def Dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        if Badges.objects.filter(Badges_owner = request.user).exists():
            pass
        else:
            B = Badges(Badges_owner=request.user)
            B.save()
        if Reputation.objects.filter(Rep_owner=request.user).exists():
            pass
        else:
            R = Reputation(Rep_owner=request.user)
            R.save()
        data_added = False
        Rep = Reputation.objects.filter(Rep_owner=request.user)
        all_badges = Badges_Master.objects.all()
        for badg in all_badges:
            if data_added == False:
                if Rep[0].reputation_count >= badg.Rep_required:
                   data = Badges.objects.get(Badges_owner=request.user)
                   data.Badges_earned.add(badg)
        top_users = Reputation.objects.all().order_by('-reputation_count')
        users = User.objects.all()
        Login_dates, Question_dates, Tut_dates, Ans_dates = DashGraph(request.user)
        noti = Notifications.objects.filter(user=request.user)
        context = {
            'top_users':top_users,
            'all_users':users,
            'notifications':noti,
            'Login_dates': Login_dates,
            'Question_dates':Question_dates,
            'Tut_dates':Tut_dates,
            'Ans_dates':Ans_dates
        }
        return render(request, 'Dashboard.html', context)

def MainPage(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        questions_to_display = []
        noti = Notifications.objects.filter(user=request.user)
        questions = Questions.objects.all()
        range = randrange(1,4)
        if UserLastOpenedQuestions.objects.filter(user=request.user).exists():
            ml_data_point = UserLastOpenedQuestions.objects.filter(user=request.user)
            print(ml_data_point)
            if range == 1:
                ml_value = ml_data_point[0].index_1
            elif range == 2:
                ml_value = ml_data_point[0].index_2
            elif range == 3:
                ml_value = ml_data_point[0].index_3
            elif range == 4:
                ml_value = ml_data_point[0].index_4
            if ml_value == 0:
                ml_dp = 0
            else:
                ml_dp = MLdata.objects.filter(index=ml_value)
                print(ml_dp)
                ml_dp = ml_dp[0].ML_id
                print(ml_dp)
        else:
            ml_dp = 0
        question_ids = InitialLoad(ml_dp)
        for ids in question_ids:
            for questions_data in questions:
                if questions_data.id == ids:
                    questions_to_display.append(questions_data)
        context = {
            'questions':questions_to_display,
            'notofications':noti,
        }
        return render(request, 'Main.html', context)
    else:
        pass

def AddQuestion(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        form = BlogForm()
        context = {
            'form': form,
            'initload': True,
            'question_review_good': False
        }
        return render(request, 'AddQuestion.html', context)
    else:
        form = BlogForm(request.POST or None)
        title = request.POST["title"]
        tags_raw = request.POST["tags"]
        tags_reformated = ReformatTags(tags_raw)
        sluged = ''.join(e for e in title if e.isalnum())
        rand_string = create_ref_code()
        slugeded = sluged + rand_string
        if form.is_valid():
            content = form.cleaned_data.get('body')
        print("chandu here")
        ML_Result = ReviewQuestion(title,content,tags_raw)
        print(ML_Result)
        if ML_Result == 'SPAM':
            isclosed = True
        else:
            isclosed = False
        a = Questions(title = title, slug = slugeded, author = request.user, body = content, status = 1,isclosed=isclosed)
        a.save()
        for tags in tags_reformated:
            if Tags.objects.filter(tag=tags).exists():
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Questions.objects.get(title = title, slug = slugeded, author = request.user, body = content, status = 1)
                tagged.tags.add(saved_tag[0].id)
            else:
                t = Tags(tag = tags )
                t.save()
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Questions.objects.get(title=title, slug=slugeded, author=request.user, body=content, status=1)
                tagged.tags.add(saved_tag[0].id)
        if Reputation.objects.filter(Rep_owner=request.user).exists():
           Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') + 5)
        else:
            R = Reputation(Rep_owner=request.user, reputation_count = 5)
            R.save()
        qid = Questions.objects.filter(title=title, slug=slugeded, author=request.user)
        if UserLastOpenedQuestions.objects.filter(user=request.user).exists():
            UserLastOpenedQuestions.objects.filter(user=request.user).update(index_1 = qid[0].id)
        else:
            u = UserLastOpenedQuestions(user=request.user, index_1 = qid[0].id)
            u.save()
        dataset = CreateDS(qid[0].id)
        Train_the_ai = RetrainModel()
        if Train_the_ai == True:
            mldata = MLdata(ML_id =  dataset  , index = qid[0].id)
            mldata.save()
        return HttpResponseRedirect('/main/')

def EditQuestion(request, slug):
    edits_instance = Questions.objects.filter(slug=slug, author=request.user).first()
    if request.method == "GET":
       edits = Questions.objects.filter(slug=slug, author=request.user)
       form = BlogForm(instance=edits_instance)
       context={
           'edits':edits,
           'form': form
       }
       return render(request, 'EditQuestion.html', context)
    else:
        form = BlogForm(request.POST , instance=edits_instance)
        if form.is_valid():
            content = form.cleaned_data.get('body')
        title = request.POST["title"]
        tags_raw = request.POST["tags"]
        tags_reformated = ReformatTags(tags_raw)
        Questions.objects.filter(slug=slug, author=request.user).update(title = title, body = content)
        for tags in tags_reformated:
            if Tags.objects.filter(tag=tags).exists():
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Questions.objects.get(title = title, slug = slug, author = request.user, body = content, status = 1)
                tagged.tags.add(saved_tag[0].id)
            else:
                t = Tags(tag = tags )
                t.save()
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Questions.objects.get(title=title, slug=slug, author=request.user, body=content, status=1)
                tagged.tags.add(saved_tag[0].id)
        return HttpResponseRedirect('/ShowQuestion/%s/' % slug)

def DispQuestion(request, slug):
        if not request.user.is_authenticated:
               return render(request, 'index.html')
        if request.method == "GET":
            form = BlogForm()
            full_question = Questions.objects.filter(slug = slug)
            print(full_question)
            if UserLastOpenedQuestions.objects.filter(user=request.user).exists():
                UserLastOpenedQuestions.objects.filter(user=request.user).update(index_2=full_question[0].id)
            else:
                u = UserLastOpenedQuestions(user=request.user, index_2=full_question[0].id)
                u.save()
            Questions.objects.filter(slug = slug).update(views=F('views')+1)
            if Answers.objects.filter(question_slug = slug).exists():
                Answerss = Answers.objects.filter(question_slug = slug)
            else:
                Answerss = " "
            dislike_status = DisLikes.objects.filter(users=request.user, post_slug=slug).exists()
            like_status = Likes.objects.filter(users=request.user, post_slug=slug).exists()
            context = {
                'full_question': full_question,
                'Answers':Answerss,
                'like_status': like_status,
                'dislike_status':dislike_status,
                'form': form,
            }
            return render(request, 'ShowQuestion.html', context)

def AddLikes(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    slug=request.POST['post_id']
    tut=request.POST['istut']
    if Likes.objects.filter(post_slug = slug).exists():
        if Likes.objects.filter(users = request.user, post_slug = slug).exists():
           data = Likes.objects.get(post_slug=slug, users = request.user)
           data.users.remove(request.user)
           if tut == "T":
               Tutorials.objects.filter(slug=slug).update(claps=F('claps')-1)
           else:
               Questions.objects.filter(slug=slug).update(upvotes=F('upvotes')-1)
        else:
            data = Likes.objects.get(post_slug=slug)
            data.users.add(request.user)
            if tut == "T":
                Tutorials.objects.filter(slug=slug).update(claps=F('claps')+1)
            else:
                Questions.objects.filter(slug=slug).update(upvotes=F('upvotes')+1)
            if DisLikes.objects.filter(users=request.user, post_slug=slug).exists():
                Questions.objects.filter(slug=slug).update(downvotes=F('downvotes')-1)
                data = DisLikes.objects.get(post_slug=slug, users=request.user)
                data.users.remove(request.user)
    else:
        data = Likes(post_slug=slug)
        data.save()
        data.users.add(request.user)
        if DisLikes.objects.filter(users=request.user, post_slug=slug).exists():
            Questions.objects.filter(slug=slug).update(downvotes=F('downvotes') - 1)
            data = DisLikes.objects.get(post_slug=slug, users=request.user)
            data.users.remove(request.user)
        if tut == "T":
            Tutorials.objects.filter(slug=slug).update(claps=F('claps')+1)
        else:
            Questions.objects.filter(slug=slug).update(upvotes=F('upvotes')+1)
    if tut == "T":
        FullTutorial = Tutorials.objects.filter(slug=slug)
        clap_status = Likes.objects.filter(users=request.user, post_slug=slug).exists()
        context = {
            'FullTutorial': FullTutorial,
            'clap_status': clap_status
        }
        html = render_to_string('Ajax_powered/MarkHot.html', context, request=request)
        return JsonResponse({'form': html})
    else:
        full_question = Questions.objects.filter(slug=slug)
        if UserLastOpenedQuestions.objects.filter(user=request.user).exists():
            UserLastOpenedQuestions.objects.filter(user=request.user).update(index_3=full_question[0].id)
        else:
            u = UserLastOpenedQuestions(user=request.user, index_3=full_question[0].id)
            u.save()
        dislike_status = DisLikes.objects.filter(users=request.user, post_slug=slug).exists()
        like_status = Likes.objects.filter(users=request.user, post_slug=slug).exists()
        if Answers.objects.filter(question_slug=slug).exists():
            Answerss = Answers.objects.filter(question_slug=slug)
        else:
            Answerss = " "
        context = {
            'full_question': full_question,
            'like_status': like_status,
            'Answers': Answerss,
            'dislike_status': dislike_status
        }
        html = render_to_string('Ajax_powered/likesdislikes.html', context, request=request)
        return JsonResponse({'form':html})


def DisLike(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    slug = request.POST['post_id']
    if DisLikes.objects.filter(post_slug = slug).exists():
        if DisLikes.objects.filter(users = request.user, post_slug = slug).exists():
           data = DisLikes.objects.get(post_slug=slug, users = request.user)
           data.users.remove(request.user)
           Questions.objects.filter(slug=slug).update(downvotes=F('downvotes')-1)
        else:
            data = DisLikes.objects.get(post_slug=slug)
            data.users.add(request.user)
            Questions.objects.filter(slug=slug).update(downvotes=F('downvotes')+1)
            if Likes.objects.filter(users=request.user, post_slug=slug).exists():
                data = Likes.objects.get(post_slug=slug, users=request.user)
                data.users.remove(request.user)
                Questions.objects.filter(slug=slug).update(upvotes=F('upvotes')-1)
    else:
        data = DisLikes(post_slug=slug)
        data.save()
        data.users.add(request.user)
        if Likes.objects.filter(users=request.user, post_slug=slug).exists():
            data = Likes.objects.get(post_slug=slug, users=request.user)
            data.users.remove(request.user)
            Questions.objects.filter(slug=slug).update(upvotes=F('upvotes') - 1)
        Questions.objects.filter(slug=slug).update(downvotes=F('downvotes')+1)
    full_question = Questions.objects.filter(slug=slug)
    if Answers.objects.filter(question_slug=slug).exists():
        Answerss = Answers.objects.filter(question_slug=slug)
    else:
        Answerss = " "
    dislike_status = DisLikes.objects.filter(users=request.user, post_slug=slug).exists()
    like_status = Likes.objects.filter(users=request.user, post_slug=slug).exists()
    context = {
        'full_question': full_question,
        'like_status': like_status,
        'Answers': Answerss,
        'dislike_status': dislike_status
    }
    html = render_to_string('Ajax_powered/likesdislikes.html', context, request=request)
    return JsonResponse({'form': html})

def AddAnswers(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    form = BlogForm(request.POST or None)
    if form.is_valid():
        answer_body = form.cleaned_data.get('body')
    if len(answer_body) == 0 :
        return HttpResponseRedirect('/ShowQuestion/%s/' % slug)
    Answers_obj = Answers(author = request.user, question_slug = slug, body = answer_body, status = 1)
    Answers_obj.save()
    Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') + 2)
    Questions.objects.filter(slug=slug).update(answers=F('answers')+1)
    full_question = Questions.objects.filter(slug=slug)
    if UserLastOpenedQuestions.objects.filter(user=request.user).exists():
        UserLastOpenedQuestions.objects.filter(user=request.user).update(index_4=full_question[0].id)
    else:
        u = UserLastOpenedQuestions(user=request.user, index_4=full_question[0].id)
        u.save()
    return HttpResponseRedirect('/ShowQuestion/%s/' %slug)

def EditAnswer(request, id):
    edits_instance = Answers.objects.filter(question_slug=id, author=request.user).first()
    if request.method == "GET":
        edits = Answers.objects.filter(question_slug=id, author=request.user)
        form = BlogForm(instance=edits_instance)
        context = {
            'edits': edits,
            'form': form
        }
        return render(request, 'EditAnswer.html', context)
    else:
        form = BlogForm(request.POST , instance=edits_instance)
        if form.is_valid():
            content = form.cleaned_data.get('body')
        Answers.objects.filter(question_slug=id, author=request.user).update(body=content)
        return HttpResponseRedirect('/ShowQuestion/%s/' % id)

def DeleteAnswer(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    id = request.POST['id']
    pkid = int(id)
    slug =  request.POST['slug']
    tut = request.POST['tut']
    post = Answers.objects.get(question_slug=slug, id=pkid, author=request.user)
    post.delete()
    Questions.objects.filter(slug=slug).update(answers=F('answers')-1)
    Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') - 2)
    if tut  == "T":
        FullTutorial = Tutorials.objects.filter(slug=slug)
        if Answers.objects.filter(question_slug=slug).exists():
            comment = Answers.objects.filter(question_slug=slug)
        else:
            comment = " "
        #all_comment_likes = Comment_likes.objects.filter(comment = comment)
        #all_comment_dislikes = Comment_DisLikes.objects.filter(comment = comment)
        C_likes = Comment_likes.objects.filter(users=request.user)
        Liked_list = LikesFunction(C_likes, comment, request.user)
        c_dislikes = Comment_DisLikes.objects.filter(users=request.user)
        DisLiked_list = DislikesFunction(c_dislikes, comment, request.user)
        clap_status = Likes.objects.filter(users=request.user, post_slug=slug).exists()
        context = {
            'FullTutorial': FullTutorial,
            'comment': comment,
            'clap_status': clap_status,
            'Liked_list': Liked_list,
            'DisLiked_list': DisLiked_list,
        }
        html = render_to_string('Ajax_powered/Comments.html', context, request=request)
        return JsonResponse({'form': html})
    else:
        if Answers.objects.filter(question_slug=slug).exists():
            Answerss = Answers.objects.filter(question_slug=slug)
        else:
            Answerss = " "
        context = {
            'Answers': Answerss
        }
        html = render_to_string('Ajax_powered/AcceptAnswer.html', context, request=request)
        return JsonResponse({'form': html})

def DeleteQuestion(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if Answers.objects.filter(question_slug=slug).exists():
       return HttpResponseRedirect('/main/')
    else:
        Questions.objects.filter(slug = slug, author = request.user).delete()
        Answers.objects.filter(question_slug=slug, author = request.user).delete()
        Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') - 5)
        return HttpResponseRedirect('/main/')

def SearchQuestion(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    query = request.POST["query"]
    ques2 = []
    count = 0
    lookups = Q(title__icontains=query) | Q(body__icontains=query)
    ques1 = Questions.objects.filter(lookups).distinct()
    break_up_query = query.split(" ")
    break_up_query_cleaned = list(dict.fromkeys(break_up_query))
    spaces = ['']
    for query in list(break_up_query_cleaned):
        if query in spaces:
            break_up_query_cleaned.remove(query)
    break_up_query_cleaned = map(lambda x: x.upper(), break_up_query_cleaned)
    for tags in break_up_query_cleaned:
        if Tags.objects.filter(tag = tags).exists():
           count += 1
           query_id = Tags.objects.filter(tag = tags)
           ques = Questions.objects.filter(tags = query_id[0].id)
           ques1 = itertools.chain(ques1, ques)
    if count != 0:
        questions = itertools.chain(ques1, ques2)
    else:
        questions = ques1
    context = {
        'questions': questions
    }
    return render(request, 'Main.html', context)

def AcceptAnswer(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    slug = request.POST['post_id']
    qid = request.POST['qid']
    owner = Questions.objects.filter(slug=slug)
    if owner[0].author == request.user:
        Answers.objects.filter(question_slug = slug, id = qid).update(isanswer = True)
    Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') + 1)
    if Answers.objects.filter(question_slug=slug).exists():
        Answerss = Answers.objects.filter(question_slug=slug)
    else:
        Answerss = " "
    context = {
        'Answers': Answerss
    }
    html = render_to_string('Ajax_powered/AcceptAnswer.html', context, request=request)
    return JsonResponse({'form': html})

def AddTutorial(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        form = BlogForm()
        return render(request, 'AddTutorial.html', {'form':form})
    else:
        form = BlogForm(request.POST or None)
        title = request.POST["title"]
        tags_raw = request.POST["tags"]
        tags_reformated = ReformatTags(tags_raw)
        sluged = title.replace(' ', '-').lower()
        rand_string = create_ref_code()
        sluged = sluged + rand_string
        if form.is_valid():
            content = form.cleaned_data.get('body')
        a = Tutorials(title=title, slug=sluged, author=request.user, body=content, status=1)
        a.save()
        for tags in tags_reformated:
            if Tags.objects.filter(tag=tags).exists():
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Tutorials.objects.get(title = title, slug = sluged, author = request.user, body = content, status = 1)
                tagged.tags.add(saved_tag[0].id)
            else:
                t = Tags(tag = tags )
                t.save()
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Tutorials.objects.get(title=title, slug=sluged, author=request.user, body=content, status=1)
                tagged.tags.add(saved_tag[0].id)
        Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') + 10 )
        return HttpResponseRedirect('/ShowTutorials/')


def ShowTutorials(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    filters = request.POST.get('filter', False)
    if filters == False or filters == 1:
       tutorials = Tutorials.objects.all().order_by('-created_on')
    elif filters == 2:
        tutorials = Tutorials.objects.all().order_by('-views')
    elif filters == 3:
        tutorials = Tutorials.objects.all().order_by('-claps')
    else:
        tutorials = Tutorials.objects.all().order_by('-created_on')
    context = {
        'Tutorials':tutorials,
    }
    return render(request, 'ShowTutorials.html', context)

def DispTutorial(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    FullTutorial = Tutorials.objects.filter(slug=slug)
    Tutorials.objects.filter(slug=slug).update(views=F('views')+1)
    if Answers.objects.filter(question_slug = slug).exists():
        comment = Answers.objects.filter(question_slug = slug)
    else:
        comment = " "
    C_likes = Comment_likes.objects.filter(users=request.user)
    Liked_list = LikesFunction(C_likes, comment, request.user)
    c_dislikes = Comment_DisLikes.objects.filter(users=request.user)
    DisLiked_list = DislikesFunction(c_dislikes, comment, request.user)
    clap_status = Likes.objects.filter(users=request.user, post_slug=slug).exists()
    context = {
        'FullTutorial': FullTutorial,
        'comment':comment,
        'clap_status':clap_status,
        'Liked_list': Liked_list,
        'DisLiked_list':DisLiked_list,
    }
    return render(request, 'DispTutorial.html', context)

def AddComment(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    answer_body = request.POST['cktext']
    if len(answer_body) == 0 :
        return HttpResponseRedirect('/DispTutorial/%s/' % slug)
    Answers_obj = Answers(author = request.user, question_slug = slug, body = answer_body, status = 1)
    Answers_obj.save()
    Tutorials.objects.filter(slug=slug).update(answers=F('answers')+1)
    return HttpResponseRedirect('/DispTutorial/%s/' %slug)

def SearchTutorial(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    query = request.POST["query"]
    lookups = Q(title__icontains=query) | Q(body__icontains=query)
    ques2 = []
    count = 0
    ques1 = Tutorials.objects.filter(lookups).distinct()
    break_up_query = query.split(" ")
    break_up_query_cleaned = list(dict.fromkeys(break_up_query))
    spaces = ['']
    for query in list(break_up_query_cleaned):
        if query in spaces:
            break_up_query_cleaned.remove(query)
    break_up_query_cleaned = map(lambda x: x.upper(), break_up_query_cleaned)
    for tags in break_up_query_cleaned:
        if Tags.objects.filter(tag=tags).exists():
            count += 1
            query_id = Tags.objects.filter(tag=tags)
            ques = Tutorials.objects.filter(tags=query_id[0].id)
            ques1 = itertools.chain(ques1, ques)
    if count != 0:
        tutorials = itertools.chain(ques1, ques2)
    else:
        tutorials = ques1
    context = {
        'Tutorials': tutorials,
    }
    return render(request, 'ShowTutorials.html', context)

def OpenProfile(request, user):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        data = User.objects.get(username=user)
        if data == request.user:
            owner=True
        else:
            owner= False
        all_questions = Questions.objects.all()
        questions = Questions.objects.filter(author=data)
        tutorials = Tutorials.objects.filter(author=data)
        answered = Answers.objects.filter(author=data)
        reputation = Reputation.objects.filter(Rep_owner=data)
        percent = reputation[0].reputation_count / 3000
        percent = percent * 100
        badges = Badges.objects.filter(Badges_owner=data)
        context = {
            'all_questions':all_questions,
            'questions':questions,
            'tutorials':tutorials,
            'answered':answered,
            'user_data':data,
            'owner':owner,
            'percent':percent,
            'reputation':reputation,
            'badges':badges
        }
        return render(request, 'Profile.html', context)

def EditProfile(request, ispass):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        data = User.objects.get(username=request.user)
        teams = cedge_Teams.objects.all()
        context = {
            'user_data':data,
            'teams':teams
        }
        return render(request, 'EditProfile.html', context)
    else:
        if ispass == "Y":
            old_password = request.POST["old_password"]
            new_pw_one = request.POST["new_pw_one"]
            new_pw_two = request.POST["new_pw_two"]
            password_is_good, pass_message = password_check(new_pw_one)
            if new_pw_one != new_pw_two:
               messages.info(request, 'Passwords not matching')
               return HttpResponseRedirect('/EditProfile/n/')
            if password_is_good == False:
               messages.info(request, pass_message)
               return HttpResponseRedirect('/EditProfile/n/')

            user = auth.authenticate(username=request.user, password=old_password)
            if user is not None:
                u = User.objects.get(username=request.user)
                u.set_password(new_pw_two)
                u.save()
                messages.info(request, 'Password changed succesfully!')
                return HttpResponseRedirect('/EditProfile/n/')
            else:
                messages.info(request, 'Old password wrong!!!')
                return HttpResponseRedirect('/EditProfile/n/')
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        User.objects.filter(username=request.user).update(first_name=fname, last_name=lname)
        data = User.objects.get(username=request.user)
        return HttpResponseRedirect('/OpenProfile/%s/' %request.user )

def Logout(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    django_logout(request)
    return render(request, 'index.html')

def About(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method=="GET":
        total_questions = Questions.objects.all().count()
        total_answers = Answers.objects.all().count()
        total_upvotes = Likes.objects.all().count()
        total_downvotes = DisLikes.objects.all().count()
        total_tutorials = Tutorials.objects.all().count()
        total_users = User.objects.all().count()
        total_commentlikes = Comment_likes.objects.all().count()
        total_commentdislikes = Comment_DisLikes.objects.all().count()
        context = {
            'total_questions':total_questions,
            'total_answers':total_answers,
            'total_upvotes':total_upvotes,
            'total_downvotes': total_downvotes,
            'total_tutorials':total_tutorials,
            'total_users':total_users,
            'total_commentlikes':total_commentlikes,
            'total_commentdislikes':total_commentdislikes,
        }
        return render(request, 'About.html', context)

def Contact(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method=="GET":
        return render(request, 'Contact.html')
    else:
        f_name = request.POST["fnames"]
        s_name = request.POST["snames"]
        c_no = request.POST["cno"]
        comment = request.POST["comm"]
        data = Contacted(first_name=f_name, second_name=s_name, contact=c_no, comment=comment)
        data.save()
        return render(request, 'Contact.html')

def AddActivity(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method=="GET":
        return render(request, 'AddActivity.html')
    else:
        Issue = request.POST["issue"]
        Bank_name = request.POST["bankname"]
        Discription = request.POST["discp"]
        Asondate = request.POST["asondate"]
        Action = request.POST["act"]
        date = datetime.datetime.strptime(Asondate, '%b %d, %Y').strftime('%Y-%m-%d')
        a=Activities(author=request.user,Title=Issue,Bank_name=Bank_name,Description=Discription,Action=Action,created_on=date)
        a.save()
        messages.info(request, 'show')
        return render(request, 'AddActivity.html')

def ShowActivity(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method=="GET":
        activities = Activities.objects.filter(author=request.user)
        context={
            'activities':activities
        }
        return render(request, 'ShowActivity.html', context)

def ActivityQuery(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    from_date = datetime.datetime.strptime(request.POST["f_date"], '%b %d, %Y').strftime('%Y-%m-%d')
    to_date = datetime.datetime.strptime(request.POST["t_date"], '%b %d, %Y').strftime('%Y-%m-%d')
    if "Download" in request.POST:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Activity_data.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Activity')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Date', 'Ticket No./Task/Issue', 'Bank Name', 'Discription', 'Action/Remarks']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = Activities.objects.filter(author=request.user, created_on__lte=to_date, created_on__gte=from_date).values_list('created_on', 'Title', 'Bank_name', 'Description', 'Action')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response
    elif "Sendtotl" in request.POST:
        return HttpResponseRedirect('/ShowActivity/')

def DeleteActivity(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    id = request.POST['id']
    id=int(id)
    Activities.objects.filter(id=id,author=request.user).delete()
    activities = Activities.objects.filter(author=request.user)
    context = {
        'activities': activities
    }
    html = render_to_string('Ajax_powered/ShowActivityAjax.html', context, request=request)
    return JsonResponse({'form': html})

def ToDo(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method=="GET":
        return render (request,'TODO.html')
    else:
        todo = request.POST['task']
        cat = request.POST['catgory']
        a = ToDo(author=request.user,todo_title=todo,category=cat)
        a.save()
        return HttpResponseRedirect('/ToDo/')

def AddCatTodo(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    category = request.POST["task"]
    a = TodoCategory(author=request.user,cat_name=category)
    a.save()
    messages.info(request, 'Category Added')
    return HttpResponseRedirect('/ToDo/')


def DevDrive(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == "GET":
        users = User.objects.all()
        if DriveFolder.objects.filter(owner=request.user, folder="Default").exists():
           folders = DriveFolder.objects.filter(owner=request.user)
        else:
            d = DriveFolder(owner=request.user, folder="Default")
            d.save()
            folders = DriveFolder.objects.filter(owner=request.user)
        context = {
            'folders':folders,
            'users':users
        }
        return render(request, 'AddFiles.html', context)
    else:
        file = request.FILES["user_file"]
        title = request.POST["title"]
        discription = request.POST["disc"]
        folders = request.POST["folder"]
        shared_with = request.POST.getlist('sharenames')
        kind = filetype.guess(file)
        key = create_ref_code()
        message = str(request.user) + " has shared a file with you"
        if kind is None:
            d = Drive(owner=request.user, key = key, title=title, folder=folders,Description=discription, file=file, file_type='text-type',file_mime='text-mime')
            d.save()
        else:
            d = Drive(owner = request.user,key = key, folder=folders, title = title,Description = discription,file = file, file_type=kind.extension, file_mime=kind.mime)
            d.save()
        for share_users in shared_with:
            username = User.objects.get(id=share_users)
            SendNotfications(username, message)
            data = Drive.objects.get(key = key,owner = request.user, title = title )
            data.download_rights.add(share_users)
        messages.info(request, 'Done!')
        return HttpResponseRedirect('/DevDrive/')

def ShowDevDrive(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    users = User.objects.all()
    if request.method == "GET":
       files = Drive.objects.filter(Q(owner=request.user) | Q(download_rights = request.user))
       folders = DriveFolder.objects.filter(owner=request.user)
       context = {
           'folders':folders,
           'files':files,
           'result':"All",
           'users': users
       }
       return render(request, 'DevDriveContent.html', context)
    else:
        folder = request.POST['folder']
        if folder == "All":
            return HttpResponseRedirect('/ShowDevDrive/')
        elif folder == "Shared_with_me":
            files = Drive.objects.filter(Q(download_rights=request.user))
            folders = DriveFolder.objects.filter(owner=request.user)
            context = {
                'folders': folders,
                'files': files,
                'result': folder,
                'users': users
            }
            return render(request, 'DevDriveContent.html', context)
        else:
            files = Drive.objects.filter(owner=request.user, folder = folder)
            folders = DriveFolder.objects.filter(owner=request.user)
            context = {
                'folders': folders,
                'files': files,
                'result': folder,
                'users': users
            }
            return render(request, 'DevDriveContent.html', context)

def Download_file(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    obj = Drive.objects.get(id=pk)
    filename = obj.file.path
    response = FileResponse(open(filename, 'rb'))
    return response

def DeleteFile(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    Drive.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/ShowDevDrive/')

def AddFolder(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    folder_name = request.POST["folder"]
    a = DriveFolder(owner=request.user,folder=folder_name)
    a.save()
    return HttpResponseRedirect('/DevDrive/')

def ShareFile(request, id):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    shared_with = request.POST.getlist('sharenames')
    message = str(request.user) + " has shared a file with you"
    for share_users in shared_with:
        username = User.objects.get(id=share_users)
        SendNotfications(username, message)
        data = Drive.objects.get(id=id, owner=request.user)
        data.download_rights.add(share_users)
    messages.info(request, 'Shared!!')
    return HttpResponseRedirect('/ShowDevDrive/')

def SendNotfications(user, message):
    notifi = Notifications(user=user, message=message)
    notifi.save()

class HeroViewSet(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = HeroSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer

def OpenApi(request):
    return render(request, 'API.html')

def DeleteTutorial(request, id):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    pkid = int(id)
    slug = Tutorials.objects.filter(id=pkid, author=request.user)
    slug = slug[0].slug
    tutorial = Tutorials.objects.get(id=pkid, author=request.user)
    tutorial.delete()
    Reputation.objects.filter(Rep_owner=request.user).update(reputation_count=F('reputation_count') - 10)
    Answers.objects.filter(question_slug=slug, author=request.user).delete()
    return HttpResponseRedirect('/ShowTutorials/')

def EditTutorial(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    data = Tutorials.objects.filter(slug=slug, author=request.user).first()
    if request.method == "GET":
       edit_tut =  Tutorials.objects.filter(slug=slug, author=request.user)
       form = BlogForm(instance=data)
       context={
           'data':edit_tut,
           'form': form
       }
       return render(request, 'EditTutorial.html', context)
    else:
        form = BlogForm(request.POST , instance=data)
        title = request.POST["title"]
        tags_raw = request.POST["tags"]
        tags_reformated = ReformatTags(tags_raw)
        if form.is_valid():
            content = form.cleaned_data.get('body')
        Tutorials.objects.filter(slug=slug, author=request.user).update(title=title, body=content)
        for tags in tags_reformated:
            if Tags.objects.filter(tag=tags).exists():
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Tutorials.objects.get(title = title, slug = slug, author = request.user, body = content, status = 1)
                tagged.tags.add(saved_tag[0].id)
            else:
                t = Tags(tag = tags )
                t.save()
                saved_tag = Tags.objects.filter(tag=tags)
                tagged = Tutorials.objects.get(title=title, slug=slug, author=request.user, body=content, status=1)
                tagged.tags.add(saved_tag[0].id)
        return HttpResponseRedirect('/DispTutorial/%s/' % slug)

def CloseQuestion(request, slug):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    Questions.objects.filter(slug=slug).update(isclosed=True)
    return HttpResponseRedirect('/ShowQuestion/%s/' % slug)

def DashGraph(user):
    login_data_list = []
    ques_data_list=[]
    tut_data_list=[]
    ans_data_list=[]
    ques = Questions.objects.filter(author=user)
    tut = Tutorials.objects.filter(author=user)
    log = AllLogin.objects.filter(user=user)
    ans = Answers.objects.filter(author=user)
    for data in ques:
         ques_data_list.append(data.created_on)
    for data2 in tut:
        tut_data_list.append(data2.created_on)
    for data3 in log:
        login_data_list.append(data3.date)
    for data4 in ans:
        ans_data_list.append(data4.created_on)
    return login_data_list, ques_data_list, tut_data_list, ans_data_list

def CommentLike(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    Answer_id = request.POST['Ans_id']
    slug = request.POST['slug']
    Answer = Answers.objects.get(id=Answer_id)
    if Comment_likes.objects.filter(comment = Answer).exists():
        if Comment_likes.objects.filter(users = request.user, comment = Answer).exists():
           data = Comment_likes.objects.get(comment = Answer, users = request.user)
           data.users.remove(request.user)
           Answers.objects.filter(id=Answer_id).update(likes=F('likes')-1)
        else:
            data = Comment_likes.objects.get(comment = Answer)
            data.users.add(request.user)
            Answers.objects.filter(id=Answer_id).update(likes=F('likes')+1)
            if Comment_DisLikes.objects.filter(users=request.user, comment = Answer).exists():
                data = Comment_DisLikes.objects.get(comment = Answer, users=request.user)
                data.users.remove(request.user)
                Answers.objects.filter(id=Answer_id).update(dislikes=F('dislikes')-1)
    else:
        data = Comment_likes(comment = Answer)
        data.save()
        data.users.add(request.user)
        if Comment_DisLikes.objects.filter(users=request.user, comment = Answer).exists():
            data = Comment_DisLikes.objects.get(comment = Answer, users=request.user)
            data.users.remove(request.user)
            Answers.objects.filter(id=Answer_id).update(dislikes=F('dislikes') - 1)
        Answers.objects.filter(id=Answer_id).update(likes=F('likes')+1)

    if Answers.objects.filter(question_slug=slug).exists():
        comment = Answers.objects.filter(question_slug=slug)
    else:
        comment = " "
    C_likes = Comment_likes.objects.filter(users=request.user)
    Liked_list = LikesFunction(C_likes, comment, request.user)
    c_dislikes = Comment_DisLikes.objects.filter(users=request.user)
    DisLiked_list = DislikesFunction(c_dislikes, comment, request.user)
    FullTutorial = Tutorials.objects.filter(slug=slug)
    context = {
        'FullTutorial': FullTutorial,
        'comment': comment,
        'Comment_Likes': C_likes,
        'Liked_list':Liked_list,
        'DisLiked_list':DisLiked_list,

    }
    html = render_to_string('Ajax_powered/comments.html', context, request=request)
    return JsonResponse({'form': html})


def CommentDisLike(request):
        if not request.user.is_authenticated:
            return render(request, 'index.html')
        Answer_id = request.POST['Ans_id']
        slug = request.POST['slug']
        Answer = Answers.objects.get(id=Answer_id)
        if Comment_DisLikes.objects.filter(comment=Answer).exists():
            if Comment_DisLikes.objects.filter(users=request.user, comment=Answer).exists():
                data = Comment_DisLikes.objects.get(comment=Answer, users=request.user)
                data.users.remove(request.user)
                Answers.objects.filter(id=Answer_id).update(dislikes=F('dislikes')-1)
            else:
                data = Comment_DisLikes.objects.get(comment=Answer)
                data.users.add(request.user)
                Answers.objects.filter(id=Answer_id).update(dislikes=F('dislikes')+1)
                if Comment_likes.objects.filter(users=request.user, comment=Answer).exists():
                    data = Comment_likes.objects.get(comment=Answer, users=request.user)
                    data.users.remove(request.user)
                    Answers.objects.filter(id=Answer_id).update(likes=F('likes')-1)
        else:
            data = Comment_DisLikes(comment=Answer)
            data.save()
            data.users.add(request.user)
            if Comment_likes.objects.filter(users=request.user, comment=Answer).exists():
                data = Comment_likes.objects.get(comment=Answer, users=request.user)
                data.users.remove(request.user)
                Answers.objects.filter(id=Answer_id).update(likes=F('likes') - 1)
            Answers.objects.filter(id=Answer_id).update(dislikes=F('dislikes')+1)

        if Answers.objects.filter(question_slug=slug).exists():
            comment = Answers.objects.filter(question_slug=slug)
        else:
            comment = " "
        C_likes = Comment_likes.objects.filter(users=request.user)
        c_dislikes = Comment_DisLikes.objects.filter(users=request.user)
        DisLiked_list = DislikesFunction(c_dislikes, comment, request.user)
        Liked_list = LikesFunction(C_likes, comment, request.user)
        FullTutorial = Tutorials.objects.filter(slug=slug)
        context = {
            'FullTutorial': FullTutorial,
            'comment': comment,
            'Comment_Likes': C_likes,
            'Liked_list': Liked_list,
            'DisLiked_list':DisLiked_list,

        }
        html = render_to_string('Ajax_powered/comments.html', context, request=request)
        return JsonResponse({'form': html})

def LikesFunction(likes, comments, user):
    liked_list = []
    for comm in comments:
        for lik in likes:
            if lik.comment == comm:
                if user in lik.users.all():
                   liked_list.append(lik.comment)
    return liked_list

def DislikesFunction(dislikes, comments, user):
    disliked_list = []
    for comm in comments:
        for dis in dislikes:
            if dis.comment == comm:
                if user in dis.users.all():
                   disliked_list.append(dis.comment)
    return disliked_list

def AppTour(request):
    badges = Badges_Master.objects.all()
    context = {
        'badges':badges,
    }
    return render(request, 'AppTour.html', context)


def ReformatTags(raw_tags):
    tags_split = raw_tags.split(",")
    tags_reformatted = list(dict.fromkeys(tags_split))
    spaces = ['']
    for tag in list(tags_reformatted):
        if tag in spaces:
            tags_reformatted.remove(tag)
    tags_reformatted = map(lambda x: x.upper(), tags_reformatted)
    return tags_reformatted


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True
    message = 'JAI SHREE RAM'

    if len(passwd) < 6:
        message = 'length should be at least 6'
        val = False

    if len(passwd) > 20:
        message = 'length should be not be greater than 8'
        val = False

    if not any(char.isdigit() for char in passwd):
        message = 'Password should have at least one numeral'
        val = False

    if not any(char.isupper() for char in passwd):
        message = 'Password should have at least one uppercase letter'
        val = False

    if not any(char.islower() for char in passwd):
        message = 'Password should have at least one lowercase letter'
        val = False

    if not any(char in SpecialSym for char in passwd):
        message = 'Password should have at least one of the symbols $@#'
        val = False
    return val, message

def ReviewQuestion(title,content,tags):
    ml_result_title = Check_spam_ham(title)
    ml_result_content = Check_spam_ham(content)
    if ml_result_title == 'HAM' and ml_result_content == 'HAM':
        return 'HAM'
    else:
        return 'SPAM'

def ResetValues(request):
    context = {
        'initload': True,
        'question_review_good': False,
    }
    html = render_to_string('Ajax_powered/ButtonsAddQ.html', context, request=request)
    return JsonResponse({'form': html}, safe=False)