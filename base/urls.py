from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [

    # General stuff
    path('', views.home, name='home'),
    path('questions', views.all_questions, name='all_questions'),
    path('questions/submit', views.add_question, name='ask_question'),
    path('questions/<int:id>', views.view_question, name='view_question'),
    path('questions/tagged/<str:tag>', views.tagged_questions, name='tagged'),
    path('questions/<int:question_id>/answer/submit',
         views.new_answer, name='new_answer'),
    path('inbox', views.inbox, name='inbox'),

    # Auth stuff
    path('auth/register', views.register, name='register'),
    path('auth/login', views.login, name='login'),
    path('users/<int:id>', views.profile, name='profile'),
    path('auth/logout', views.logout, name='logout'),
]
