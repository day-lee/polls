from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:pk>/suggest-choice/', views.ChoiceCreateView.as_view(), name='new-choice'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('like/<int:pk>', views.LikeView, name='like_question'),

    #path('<int:pk>/approve-choice/', views.ApprovedChoiceUpdateView.as_view(), name='approve_choice'),

]
