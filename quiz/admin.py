from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizHistory, QuizRating

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 5

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'is_correct')
    list_filter = ['question__quiz']

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'quiz', 'points')
    list_filter = ['quiz']

class QuizHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'scores', 'completed_at')
    list_filter = ['user', 'quiz']

class QuizRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'rating')
    list_filter = ['user', 'quiz']

admin.site.register(Category)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(QuizHistory, QuizHistoryAdmin)
admin.site.register(QuizRating, QuizRatingAdmin)
