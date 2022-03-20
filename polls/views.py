import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets
from django.contrib import messages

# from utils.url import restify

from .models import Choice, Question, SuggestedChoice, Comment
from .serializers import QuestionSerializer
from .forms import SuggestChoiceForm, CommentForm


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    allow_empty = False
    queryset = Question.objects.filter(is_closed=False)

    """
    this is not a perfect solution as problem will arise again when
    I try to apply pagination and filter once again.
    """
    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     response = requests.get(restify("/questions/"))
    #     questions = response.json()
    #     return questions[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

from django.urls import reverse_lazy

class ChoiceCreateView(generic.CreateView):
    model = SuggestedChoice
    template_name =  "polls/suggestedchoice_form.html"
    form_class = SuggestChoiceForm


    def is_limit_reached(self):
        return SuggestedChoice.objects.all().count() >= 3


    def post(self, request, *args, **kwargs):
        if self.is_limit_reached():
            print('limit over')
            messages.info(request, 'Warning: You have reached the limit for the number of suggestions you can create at this time.')
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('polls:detail', kwargs={'pk': self.kwargs['pk']})


class AddCommentView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'polls/add_comment.html'
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('polls:detail', kwargs={'pk': self.kwargs['pk']})

# API
# ===


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer