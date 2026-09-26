from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .auth import SignupForm
from .models import Book, Quote, BookOfTheMonth, Review, Story
import markdown
import random
from datetime import date

# Create your views here.
# logic that handles requests and responses goes here

# How many items the "recent stories" / "recent reviews" cards show.
RECENT_COUNT = 5


def get_quote_of_the_day():
    quotes = list(Quote.objects.all())
    if not quotes:
        return None
    rng = random.Random(date.today().toordinal())
    return rng.choice(quotes)


def latest_published(model):
    """Newest published items of `model` (Story or Review), padded with
    None up to RECENT_COUNT so the template always gets a full-length list."""
    items = list(
        model.objects.filter(published=True).order_by('-date_written')[:RECENT_COUNT]
    )
    return items + [None] * (RECENT_COUNT - len(items))


def index(request):
    return render(request, 'index.html', {
        'recent_stories': latest_published(Story),
        'recent_reviews': latest_published(Review),
        'quote': get_quote_of_the_day(),
        'book_of_month': BookOfTheMonth.objects.first(),
    })

@login_required
def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)
    content_html = markdown.markdown(review.markdown_content)
    return render(request, 'review.html', {'review': review, 'content_html': content_html})

@login_required
def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    content_html = markdown.markdown(story.markdown_content)
    return render(request, 'story.html', {'story': story, 'content_html': content_html})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)      # was UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()                  # was UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

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