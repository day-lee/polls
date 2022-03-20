from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/suggest-choice/', views.ChoiceCreateView.as_view(), name='new-choice'),
    path('<int:pk>/comment', views.AddCommentView.as_view(), name='add_comment'),
]
#question_id
