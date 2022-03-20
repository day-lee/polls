from django import forms
from .models import Choice, Question, SuggestedChoice, Comment


class SuggestChoiceForm(forms.ModelForm):
    class Meta:
        model = SuggestedChoice
        #fields = '__all__'
        fields = ('choice_text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')
