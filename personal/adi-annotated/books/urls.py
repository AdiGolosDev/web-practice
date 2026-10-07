from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/<slug:slug>/', views.review_detail, name='review_detail'),
    path('stories/<slug:slug>/', views.story_detail, name='story_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('api/books/', views.books_api, name='book_api'),
    path('reviews/<slug:slug>/vote/<str:direction>/', views.vote_review, name='vote_review'),
    path('stories/<slug:slug>/vote/<str:direction>/', views.vote_story, name='vote_story'),
    path('reviews/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('stories/<slug:slug>/comment/', views.add_story_comment, name='add_story_comment'),
]
