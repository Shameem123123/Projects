from django.shortcuts import render, redirect
from .models import Question, Choice


def start_quiz(request):

    request.session['score'] = 0

    # Randomize questions ONCE
    question_ids = list(
        Question.objects.order_by('?').values_list('id', flat=True)
    )

    request.session['question_ids'] = question_ids

    return redirect('question', index=0)


def question_view(request, index):

    question_ids = request.session.get('question_ids', [])

    total_questions = len(question_ids)

    # Quiz finished
    if index >= total_questions:
        return redirect('result')

    question_id = question_ids[index]

    question = Question.objects.get(id=question_id)

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

    total_questions = len(
        request.session.get('question_ids', [])
    )

    context = {
        'score': score,
        'total': total_questions
    }

    return render(request, 'quiz/result.html', context)