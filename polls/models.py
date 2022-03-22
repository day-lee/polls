import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Q


class QuestionManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            lookup = (Q(question_text__icontains=query))
            qs = qs.filter(lookup).distinct()
        return qs

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date      = models.DateTimeField("date published")
    is_closed     = models.BooleanField(default=False)
    closed_at     = models.DateField(default=datetime.date.today, auto_now=False, auto_now_add=False)

    objects       = QuestionManager()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)




class ChoiceManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            lookup =  (Q(choice_text__icontains=query))
            qs = qs.filter(lookup).distinct()
        return qs


class Choice(models.Model):
    question     = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text  = models.CharField(max_length=200)
    votes        = models.IntegerField(default=0)
    
    objects      = ChoiceManager()

    def __str__(self):
        return self.choice_text


class SuggestedChoice(models.Model):
    question       = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text    = models.CharField(max_length=200)
    is_approved    = models.BooleanField(default=False)
    created_date   = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.question) + ' | ' + str(self.choice_text)


class Comment(models.Model):
    question       = models.ForeignKey(Question, related_name="comment", on_delete=models.CASCADE) # related_name="comment",
    author         = models.CharField(max_length=20)
    body           = models.TextField(max_length=300)
    created_date  = models.DateTimeField(auto_now_add=True)
    #author can become user but not yet, self FK for replying comments

    def __str__(self):
        return str(self.question)
