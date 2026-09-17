from django.urls import path
from . import views

urlpatterns = [
    path('reviews/<slug:slug>/', views.review_detail, name='review_detail'),
    path('stories/<slug:slug>/', views.story_detail, name='story_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
