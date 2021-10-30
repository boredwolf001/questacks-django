from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models
from crispy_forms.helper import FormHelper
from taggit.forms import *


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    website = forms.URLField(
        max_length=200, help_text="input page URL", initial='http://')

    class Meta:
        fields = ('bio', "website", 'github', 'profile_img', )
        model = models.Profile


class QuestionForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'question', 'tag')
        model = models.Question


class AnswerForm(forms.ModelForm):
    class Meta:
        fields = ('answer_text', )
        model = models.Answer

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # self.helper.form_method = 'post'  # this line sets your form's method to post
        self.helper.form_tag = False  # this line sets the form action
