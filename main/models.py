from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Tags(models.Model):
    tag = models.CharField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

class Questions(models.Model):

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_posts')
    updated_on = models.DateTimeField(auto_now=True)
    body = RichTextUploadingField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.ManyToManyField(Tags, related_name='tag_question_master')
    views = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    isanswered = models.BooleanField(default=False)
    isclosed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answers(models.Model):
      author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_posts')
      question_slug = models.SlugField(max_length=200)
      updated_on = models.DateTimeField(auto_now=True)
      body = RichTextUploadingField(blank=True, null=True)
      created_on = models.DateTimeField(auto_now_add=True)
      status = models.IntegerField(choices=STATUS, default=0)
      isanswer = models.BooleanField(default=False)
      likes = models.IntegerField(default=0)
      dislikes = models.IntegerField(default=0)

      def __str__(self):
          return self.body



class Likes(models.Model):
    users = models.ManyToManyField(User, related_name='likes_master')
    post_slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_slug


class DisLikes(models.Model):
    users = models.ManyToManyField(User, related_name='Dislikes_master')
    post_slug = models.SlugField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_slug

class Tutorials(models.Model):

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Tutorials_posts')
    updated_on = models.DateTimeField(auto_now=True)
    body = RichTextUploadingField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.ManyToManyField(Tags, related_name='tag_tutorial_master')
    views = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    claps = models.IntegerField(default=0)
    isanswered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Contact(models.Model):

    first_name = models.TextField()
    second_name = models.TextField()
    contact = models.TextField()
    comment = models.TextField()

    def __str__(self):
        return self.fname

class Contacted(models.Model):

    first_name = models.TextField()
    second_name = models.TextField()
    contact = models.TextField()
    comment = models.TextField()

    def __str__(self):
        return self.first_name + self.second_name

class Activities(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Activities_posts')
    Title = models.CharField(max_length=200,default=" ")
    Bank_name = models.CharField(max_length=200,default=" ")
    Description = models.CharField(max_length=200,default=" ")
    Action = models.CharField(max_length=200,default=" ")
    created_on = models.DateField()
    Sent_status = models.BooleanField(default=False)

    def __str__(self):
        return self.author + self.Title + self.Bank_name

class TodoCategory(models.Model):
    cat_name =  models.CharField(max_length=200,default=" ")
    created_on = models.DateField(auto_now_add=True)



class ToDo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ToDo_posts')
    todo_title = models.CharField(max_length=200,default=" ")
    created_on = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=200,default=" ")


class DriveFolder(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Drivefolder_owner')
    folder = models.CharField(max_length=200,default=" ")
    created_on = models.DateField(auto_now_add=True)

class Drive(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Drive_owner')
    download_rights = models.ManyToManyField(User, related_name='drie_download_rights')
    key = models.CharField(max_length=200,default=" ")
    title = models.CharField(max_length=200,default=" ")
    file = models.FileField(blank=True, null=True)
    Description = models.CharField(max_length=200, default=" ")
    folder = models.CharField(max_length=200, default=" ")
    Uploaded_on = models.DateField(auto_now_add=True)
    file_type = models.CharField(max_length=200, default=" ")
    file_mime = models.CharField(max_length=200, default=" ")

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Notifi_user')
    message = models.CharField(max_length=200,default=" ")
    viewed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

class Reputation(models.Model):
    Rep_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Reputation_user')
    reputation_count = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now_add=True)

class Badges_Master(models.Model):
     Badge_name = models.CharField(default="", max_length=200)
     Rep_required = models.IntegerField(default=0)

     def __str__(self):
         return self.Badge_name


class Badges(models.Model):
      Badges_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Badges_user')
      Badges_earned = models.ManyToManyField(Badges_Master, related_name='Badges_users')
      updated_on = models.DateTimeField(auto_now_add=True)

class AllLogin(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='AllLogin_user')
    date= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.date)

class cedge_Teams(models.Model):
    Team_name = models.CharField(default="", max_length=200)
    added_on = models.DateTimeField(auto_now_add= True)

class Comment_likes(models.Model):
    users = models.ManyToManyField(User, related_name='likes_master_comment')
    comment = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='Answer_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment_DisLikes(models.Model):
    users = models.ManyToManyField(User, related_name='Dislikes_master_comment')
    comment = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='Answer_Dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MLdata(models.Model):
    ML_id = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ML_id) + ': ' + str(self.index)

class UserLastOpenedQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_opened')
    index_1 = models.IntegerField(default=0)
    index_2 = models.IntegerField(default=0)
    index_3 = models.IntegerField(default=0)
    index_4 = models.IntegerField(default=0)
    index_5 = models.IntegerField(default=0)
    index_6 = models.IntegerField(default=0)