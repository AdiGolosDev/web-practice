from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book, Review, Story
import markdown

# Create your views here.
# logic that handles requests and responses goes here

def index(request):
    return render(request, 'index.html')

def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)
    content_html = markdown.markdown(review.markdown_content)
    return render(request, 'review.html', {'review': review, 'content_html': content_html})

def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    content_html = markdown.markdown(story.markdown_content)
    return render(request, 'story.html', {'story': story, 'content_html': content_html})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def books_api(request):
    books = Book.objects.all()
    data = []
    for book in books:
        review = getattr(book, 'review', None)
        has_review = review is not None and review.published
        data.append({
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'language': book.language.name if book.language else None,
            'description': book.description,
            'year_published': book.year_published,
            'date_read': book.date_read.isoformat() if book.date_read else None,
            'page_count': book.page_count,
            'difficulty': book.difficulty,
            'rating': book.rating,
            'has_review': has_review,
            'review_slug': review.slug if has_review else None,
        })
    return JsonResponse(data, safe=False)
