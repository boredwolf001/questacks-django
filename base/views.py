from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as log_in, logout as log_out, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import ProfileForm, QuestionForm, AnswerForm
from . import models

from django import template

register = template.Library()

def filter_read_items(value, arg):
      value.filter(read=arg)


register.filter('readitems', filter_read_items)

import markdown


def home(request):
      latest_questions = models.Question.objects.all().order_by('-created_at', '-updated_at')[:20]

      return render(request, 'pages/home.html', {'questions': latest_questions})


def all_questions(request):
      questions = models.Question.objects.all().order_by('created_at', 'updated_at')

      return render(request, 'questacks/all_questions.html', {'questions': questions})



def login(request):
      if request.user.is_authenticated:
            return redirect('base:profile')

      if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                  log_in(request, user)
                  return redirect('base:profile', user.id)
            else:
                  return redirect('base:login')

      return render(request, 'registration/login.html')


@login_required(login_url='base:login')
def profile(request, id):
      profile = get_object_or_404(User, pk=id)

      return render(request, 'registration/profile.html', {'profile': profile})

def register(request):
    if request.user.is_authenticated:
        return redirect('base:profile')

    if request.method == 'POST':
      uform = UserCreationForm(request.POST)
      pform = ProfileForm(request.POST, request.FILES)
      
      if uform.is_valid() and pform.is_valid():
            user = uform.save()
            inbox = models.Inbox(user=user)
            inbox.save()

            profile = pform.save(commit=False)
            profile.user = user
            profile.save()
            
            return redirect('base:login')
      
      else:
            return render(request, 'registration/register.html', {'uform': uform, 'pform': pform, 'errors': ['Form not valid']})

    uform = UserCreationForm()
    pform = ProfileForm()
    return render(request, 'registration/register.html', {'uform': uform, 'pform': pform})

def logout(request):
      log_out(request)

      return redirect('base:login')


# Questacks stuff
def add_question(request):
      if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                  question = form.save(commit=False)
                  question.user = request.user
                  tags = form.cleaned_data['tag']

                  question.save()
                  for tag in tags:
                        question.tag.add(tag)
                  question.save()

                  return redirect('base:home')
            else:
                return render(request, 'questacks/ask_question.html', {'form': form, 'errors': ['Form not valid']})

      form = QuestionForm()

      return render(request, 'questacks/ask_question.html', {'form': form})


def view_question(request, id):
      question = get_object_or_404(models.Question, pk=id)
      question.views += 1
      question.save()
      html_question = markdown.markdown(question.question)


      answer_form = AnswerForm()

      return render(request, 'questacks/view_question.html', {'question': question, 'question_body': html_question, 'form': answer_form})

def new_answer(request, question_id):
      question = get_object_or_404(models.Question, pk=question_id)
      new_answer = models.Answer.objects.create(user=request.user, question=question, answer_text=request.POST['answer_text'])

      new_inbox_msg = models.InboxItem(inbox=question.user.inbox, target_question=question, inbox_type='Answer', message=new_answer.answer_text)
      
      try:
            new_answer.save()
            new_inbox_msg.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
      except Exception as e:
            print('Error:', e)
            return HttpResponse(status=500)

def tagged_questions(request, tag):
      questions = models.Question.objects.filter(tag__name__in=[tag])

      return render(request, 'questacks/tagged.html', {'questions': questions})


def inbox(request):
      user_inbox = get_object_or_404(models.Inbox, user=request.user)
      inbox_items = user_inbox.inboxitem_set.all().order_by('-created_at')
      for item in inbox_items:
            item.read = True
            item.save()

      return render(request, 'questacks/inbox.html', {'inbox_items': inbox_items})