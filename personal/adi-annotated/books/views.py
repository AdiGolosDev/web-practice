from django.shortcuts import render, get_object_or_404
from .models import Review, Story
import markdown

# Create your views here.
# logic that handles requests and responses goes here

def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)
    content_html = markdown.markdown(review.markdown_content)
    return render(request, 'review.html', {'review': review, 'content_html': content_html})

def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    content_html = markdown.markdown(story.markdown_content)
    return render(request, 'story_detail.html', {'story': story, 'content_html': content_html})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
