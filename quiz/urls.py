from django.urls import path
from . import views

urlpatterns = [
 path('', views.start_quiz, name='start_quiz'),
    path('question/<int:index>/', views.question_view, name='question'),
    path('result/', views.result_view, name='result'),
    
]