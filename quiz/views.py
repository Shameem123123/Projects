from django.shortcuts import render
from .models import Question

# Create your views here.

def quiz_view(request):
    questions = Question.objects.all()

    context = {
        'questions': questions
    }

    return render(request, 'quiz/quiz.html', context)
