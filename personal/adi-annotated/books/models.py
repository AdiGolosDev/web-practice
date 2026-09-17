from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
        return self.title


# Book keeps track of books read
class Book(models.Model):
    class Genre(models.TextChoices):
        FICTION = 'fiction', 'Fiction'
        NON_FICTION = 'non_fiction', 'Non-Fiction'

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=20, choices=Genre.choices)
    is_classic = models.BooleanField(default=False)
    year_published = models.IntegerField()
    year_read = models.IntegerField()
    month_read = models.IntegerField()
    page_count = models.IntegerField()
    difficulty = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
