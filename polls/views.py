import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework import viewsets
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from itertools import chain

from utils.url import restify

from .models import Choice, Question, SuggestedChoice, Comment
from .serializers import QuestionSerializer
from .forms import SuggestChoiceForm, CommentForm, ApprovedChoiceForm

"""original listview"""
# class IndexView(generic.ListView):
#     template_name = "polls/index.html"
#     context_object_name = "latest_question_list"
#     allow_empty = False
#     queryset = Question.objects.filter(is_closed=False)
#
#     # def get_queryset(self):
#     #     """Return the last five published questions."""
#     #     response = requests.get(restify("/polls/"))
#     #     questions = response.json()
#     #     return questions[:5]

class IndexView(generic.ListView):
    template_name = "polls/indexview.html"
    count = 0
    allow_empty = False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')

        return context

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = Question.objects.filter(is_closed=False)

        if query:
            if len(query) > 1:
                question_results = Question.objects.search(query)
                choice_results = Choice.objects.search(query)

                queryset_chain = chain(
                                question_results,
                                choice_results
                )
                qs = sorted(queryset_chain,
                            key=lambda instance: instance.pk,
                            reverse=True)
                self.count = len(qs)
                return qs
            else:
                messages.error(self.request, 'Please type more than two characters')
        return object_list



class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


def LikeView(request, pk):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))
    #template button "name" is question_id
    question.likes.add(request.user)
    return HttpResponseRedirect(reverse('detail', args=[str(pk]))


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
        #selected_choice.votes += 1
        selected_choice.votes = F('votes')+1
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
        # form.instance.question_id = self.kwargs['question_id']
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


# FIX NEEDED
# class ApprovedChoiceUpdateView(generic.UpdateView):
#     model = SuggestedChoice
#     template_name =  "polls/approve_choice.html"
#     form_class = ApprovedChoiceForm
#
#
#     def form_valid(self, form):
#         form.instance.question_id = self.kwargs['pk']
#         return super().form_valid(form)
#
#
#     def get_success_url(self):
#         return reverse_lazy('polls:detail', kwargs={'pk': self.kwargs['pk']})


# API
# ===


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
