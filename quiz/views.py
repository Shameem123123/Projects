from django.shortcuts import render, redirect
from .models import Question, Choice


def home_view(request):
    return render(request, 'quiz/home.html')


def start_quiz(request):

    request.session['score'] = 0

    request.session['answers'] = {}

    question_ids = list(
        Question.objects.order_by('?').values_list('id', flat=True)
    )

    request.session['question_ids'] = question_ids

    return redirect('question', index=0)


def question_view(request, index):

    question_ids = request.session.get('question_ids', [])

    total_questions = len(question_ids)

    if index >= total_questions:
        return redirect('result')

    question_id = question_ids[index]

    question = Question.objects.get(id=question_id)

    if request.method == 'POST':

        selected_choice = request.POST.get('choice')

        answers = request.session.get('answers', {})

        if selected_choice:

            answers[str(question.id)] = int(selected_choice)

            choice = Choice.objects.get(id=selected_choice)

            if choice.is_correct:
                request.session['score'] += 1

        request.session['answers'] = answers

        return redirect('question', index=index + 1)

    context = {
        'question': question,
        'index': index + 1,
        'total': total_questions
    }

    return render(request, 'quiz/question.html', context)


def result_view(request):

    score = request.session.get('score', 0)

    question_ids = request.session.get('question_ids', [])

    answers = request.session.get('answers', {})

    review_data = []

    for question_id in question_ids:

        question = Question.objects.get(id=question_id)

        choices = question.choice_set.all()

        selected_choice_id = answers.get(str(question.id))

        correct_choice = choices.get(is_correct=True)

        review_data.append({
            'question': question,
            'choices': choices,
            'selected_choice_id': selected_choice_id,
            'correct_choice_id': correct_choice.id
        })

    context = {
        'score': score,
        'total': len(question_ids),
        'review_data': review_data
    }

    return render(request, 'quiz/result.html', context)