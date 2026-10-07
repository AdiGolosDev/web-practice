from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .auth import SignupForm
from .models import Book, Quote, BookOfTheMonth, Review, Story, Comment, Vote
import markdown
import random
from datetime import date

# Create your views here.
# logic that handles requests and responses goes here

RECENT_COUNT = 3
MAX_COMMENT_LENGTH = 2000


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
    score = review.vote_set.aggregate(total=Sum('value'))['total'] or 0
    return render(request, 'review.html', {'review': review, 'content_html': content_html, 'score': score,})


@login_required
def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    content_html = markdown.markdown(story.markdown_content)
    score = story.vote_set.aggregate(total=Sum('value'))['total'] or 0
    return render(request, 'story.html', {'story': story, 'content_html': content_html, 'score': score,})


@login_required
def add_comment(request, slug):
    review = get_object_or_404(Review, slug=slug)
    if request.method != 'POST':
        return HttpResponseForbidden()
    content = request.POST.get('content', '').strip()
    if not content or len(content) > MAX_COMMENT_LENGTH:
        return HttpResponseBadRequest('Comment must be between 1 and 2000 characters.')
    comment = Comment.objects.create(
        review=review,
        user=request.user,
        content=content,
    )
    return render(request, 'partials/comment.html', {'comment': comment})

@login_required
def add_story_comment(request, slug):
    story = get_object_or_404(Story, slug=slug)
    if request.method != 'POST':
        return HttpResponseForbidden()
    content = request.POST.get('content', '').strip()
    if not content or len(content) > MAX_COMMENT_LENGTH:
        return HttpResponseBadRequest('Comment must be between 1 and 2000 characters.')
    comment = Comment.objects.create(
        story=story,
        user=request.user,
        content=content,
    )
    return render(request, 'partials/comment.html', {'comment': comment})

@login_required
def vote_review(request, slug, direction):
    review = get_object_or_404(Review, slug=slug)
    if request.method != 'POST' or direction not in ('up', 'down'):
        return HttpResponseForbidden()
    value = 1 if direction == 'up' else -1
    Vote.objects.update_or_create(
        user=request.user, review=review,
        defaults={'value': value},
    )
    score = review.vote_set.aggregate(total=Sum('value'))['total'] or 0
    return render(request, 'partials/vote_widget.html', {
        'kind': 'review',
        'slug': review.slug,
        'score': score,
    })
 
 
@login_required
def vote_story(request, slug, direction):
    story = get_object_or_404(Story, slug=slug)
    if request.method != 'POST' or direction not in ('up', 'down'):
        return HttpResponseForbidden()
    value = 1 if direction == 'up' else -1
    Vote.objects.update_or_create(
        user=request.user, story=story,
        defaults={'value': value},
    )
    score = story.vote_set.aggregate(total=Sum('value'))['total'] or 0
    return render(request, 'partials/vote_widget.html', {
        'kind': 'story',
        'slug': story.slug,
        'score': score,
    })


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
