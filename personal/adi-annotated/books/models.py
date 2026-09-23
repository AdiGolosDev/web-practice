from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import date

# Create your models here.
# this is where data structures go apparently
# books, reviews, stories, comments, votes classes in my case I think


# Contact keeps track of emails someone sent to me via the website form
class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


# Language keeps track of languages I've read books in
class Language(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Book keeps track of books read
class Book(models.Model):
    class Genre(models.TextChoices):
        FICTION = 'fiction', 'Fiction'
        NON_FICTION = 'non_fiction', 'Non-Fiction'

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, null=True, blank=True, related_name='books')
    description = models.TextField(blank=True)
    year_published = models.IntegerField()
    date_read = models.DateField(null=True, blank=True)
    page_count = models.IntegerField()
    difficulty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Quote keeps track of quotes from books I like
class Quote(models.Model):
    quote_english = models.TextField()
    author = models.CharField(max_length=128)
    original_language = models.CharField(max_length=64, blank=True)
    original_quote = models.TextField(blank=True)

    def __str__(self):
        return f"{self.author}: {self.quote_english[:50]}"


class BookOfTheMonth(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, blank=True)
    short_description = models.TextField()
    featured_date = models.DateField(default=date.today)
    cover_override_url = models.URLField(
        blank=True,
        help_text="Optional - paste a direct image URL here to override the automatic Open Library cover"
    )

    class Meta:
        ordering = ["-featured_date"]

    def __str__(self):
        return f"{self.book.title} — {self.featured_date}"

    @property
    def cover_url(self):
        if self.cover_override_url:
            return self.cover_override_url
        if self.isbn:
            return f"https://covers.openlibrary.org/b/isbn/{self.isbn}-L.jpg?default=false"
        return None


# keeps track of reviews written / links to book 1-to-1
class Review(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    markdown_content = models.TextField()
    date_written = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# keeps track of stories written
class Story(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    markdown_content = models.TextField()
    date_written = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Stories"

    def __str__(self):
        return self.title


# user comments on reviews/stories
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, null=True, blank=True, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.content[:32]}"


# upvotes/downvotes on stories/reviews
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, null=True, blank=True, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, null=True, blank=True, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ('user', 'review', 'story')


@receiver(post_save, sender=Review)
def sync_book_is_reviewed_save(sender, instance, **kwargs):
    instance.book.is_reviewed = instance.published
    instance.book.save(update_fields=['is_reviewed'])

@receiver(post_delete, sender=Review)
def sync_book_is_reviewed_delete(sender, instance, **kwargs):
    try:
        instance.book.is_reviewed = False
        instance.book.save(update_fields=['is_reviewed'])
    except Book.DoesNotExist:
        pass