from django.urls import path
from . import views

urlpatterns = [
    path('quiz/list', views.quiz_list, name='quiz_list'),
    path('quiz/list/category/<int:category_id>/', views.quiz_list, name='quiz_list_category'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('quiz/history/', views.quiz_history, name='quiz_history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('quiz/ranking/', views.quiz_ranking, name='quiz_ranking'),
]
