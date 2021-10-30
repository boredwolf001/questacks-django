from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(null=True, max_length=100)
    github = models.CharField(null=True, max_length=100)
    website = models.URLField(max_length=200, null=True)
    profile_img = models.ImageField(
        upload_to='profile_pics', default='default_profile.png')

    def __str__(self):
        return self.user.username


class Question(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=75)
    views = models.IntegerField(default=0)
    tag = TaggableManager()
    question = RichTextField()

    def __str__(self):
        return self.title


class Answer(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    answer_text = RichTextField()

    def __str__(self):
        return self.answer_text


class Inbox(TimeStampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + 's Inbox'


class InboxItem(TimeStampMixin):
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE)
    inbox_type = models.CharField(null=True, max_length=50)
    read = models.BooleanField(default=False, null=True)
    target_question = models.OneToOneField(
        Question, on_delete=models.CASCADE, null=True, max_length=200)
    message = models.CharField(null=True, max_length=300)

    def __str__(self):
        return self.question_title
