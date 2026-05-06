from django.shortcuts import render, redirect
from .models import Question, Choice


def start_quiz(request):

    request.session['score'] = 0

    return redirect('question', index=0)


def question_view(request, index):

    questions = list(Question.objects.all())

    total_questions = len(questions)

    if index >= total_questions:
        return redirect('result')

    question = questions[index]

    if request.method == 'POST':

        selected_choice = request.POST.get('choice')

        if selected_choice:

            choice = Choice.objects.get(id=selected_choice)

            if choice.is_correct:
                request.session['score'] += 1

        return redirect('question', index=index + 1)

    context = {
        'question': question,
        'index': index + 1,
        'total': total_questions
    }

    return render(request, 'quiz/question.html', context)


def result_view(request):

    score = request.session.get('score', 0)

    total_questions = Question.objects.count()

    context = {
        'score': score,
        'total': total_questions
    }

    return render(request, 'quiz/result.html', context)