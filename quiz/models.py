from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    has_time_limit = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "quizzes"
        
    def average_rating(self):
        ratings = self.quizrating_set.values_list('rating', flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return 0


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    points = models.IntegerField(default=1)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.choice_text} (Question: {self.question.question_text})'
    
class QuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    scores = models.IntegerField(default=0)
    current_question_number = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "quiz histories"

class QuizRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]
    
    rating = models.IntegerField(choices=RATING_CHOICES)