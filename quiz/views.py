from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Category, Question, Choice, QuizHistory, QuizRating
from .forms import QuizRatingForm
from django.utils import timezone
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@login_required    
def quiz_list(request, category_id=None):
    quizzes = Quiz.objects.all()
    categories = Category.objects.all()

    if category_id is not None:
        quizzes = quizzes.filter(category=category_id)
        print("asdf")

    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes, 'categories': categories})

@login_required        
def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    user = request.user

    quiz_history = QuizHistory.objects.filter(user=user, quiz=quiz, completed_at__isnull=True).first()

    if quiz_history is None:
        quiz_history = QuizHistory.objects.create(user=user, quiz=quiz, scores=0, current_question_number=0)

    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        selected_choice = get_object_or_404(Choice, pk=choice_id)
        feedback = ''

        if selected_choice.is_correct:
            question_points = questions[quiz_history.current_question_number].points
            quiz_history.scores = quiz_history.scores + question_points
            quiz_history.save()
            feedback = 'Correct'
        else:
            feedback = 'Incorrect'

        quiz_history.current_question_number = quiz_history.current_question_number + 1
        quiz_history.save()

        next_question_number = quiz_history.current_question_number
        if next_question_number >= questions.count():
            quiz_history.completed_at = timezone.now()
            quiz_history.save()
            
            message = render_to_string("quiz/quiz_result_mail.html", { 'user' : user, 'quiz' : quiz, 'total_questions' : questions.count(), 'quiz_history' : quiz_history })
            send_email = EmailMultiAlternatives("Quiz Result Mail", '', to=[user.email])
            send_email.attach_alternative(message, "text/html")
            send_email.send()
        
        current_question_number = quiz_history.current_question_number - 1
        current_question = questions[current_question_number]
        
        return render(request, 'quiz/quiz.html', {
            'quiz': quiz,
            'current_question': current_question,
            'current_question_number': current_question_number + 1,
            'total_questions': questions.count(),
            'feedback': feedback,
        })
    else:
        current_question_number = quiz_history.current_question_number
        current_question = questions[current_question_number]

        return render(request, 'quiz/quiz.html', {
            'quiz': quiz,
            'current_question': current_question,
            'current_question_number': current_question_number + 1,
            'total_questions': questions.count(),
        })
        
@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_history = QuizHistory.objects.filter(user=request.user, quiz=quiz).last()
    final_score = quiz_history.scores if quiz_history else 0

    if request.method == 'POST':
        form = QuizRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            QuizRating.objects.create(user=request.user, quiz=quiz, rating=rating)
            return redirect('quiz_ranking')
    else:
        form = QuizRatingForm()

    return render(request, 'quiz/quiz_result.html', {'quiz': quiz, 'final_score': final_score, 'rating_form': form})

@login_required
def quiz_ranking(request):
    ranked_quizzes = Quiz.objects.annotate(avg_rating=Avg('quizrating__rating')).order_by('-avg_rating')
    return render(request, 'quiz/quiz_ranking.html', {'ranked_quizzes': ranked_quizzes})

@login_required
def quiz_history(request):
    user_history = QuizHistory.objects.filter(user=request.user, completed_at__isnull=False).order_by('-completed_at')
    return render(request, 'quiz/quiz_history.html', {'user_history': user_history})

@login_required
def leaderboard(request):
    top_scores = QuizHistory.objects.filter(completed_at__isnull=False).order_by('-scores')[:10]
    return render(request, 'quiz/leaderboard.html', {'top_scores': top_scores})