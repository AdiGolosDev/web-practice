from django import forms
from django.contrib import admin
from .models import Language, Book, Quote, BookOfTheMonth, Review, Story
from datetime import date

# Register your models here.
# where I should register models(book, review),
#  so they show up and are manageable in the /admin/ panel

class MonthYearField(forms.DateField):
    """A DateField whose widget is native year-month picker (no day option). Python's strptime fills in day=1 automatically when the format string only specifies year and month."""
    widget = forms.DateInput(attrs={'type': 'month'})
    input_formats = ['%Y-%m']

    def prepare_value(self, value):
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m')
        return value


class BookAdminForm(forms.ModelForm):
    date_read = MonthYearField(label='Month read', required=False)

    class Meta:
        model = Book
        fields = '__all__'


class MarkdownUploadForm(forms.ModelForm):
    """
    Adds an extra, non-model field that lets you upload a .md file.
    If a file is uploaded, its text will overwrite markdown_content on save.
    """
    markdown_file = forms.FileField(
        required=False,
        help_text="Upload a .md file to fill in the content below (overrides typed text)."
    )

    class Meta:
        fields = "__all__"
        widgets = {
            "markdown_content": forms.Textarea(attrs={"rows": 20, "cols": 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # markdown_content can be blank in the form now, since it might
        # get filled in from the uploaded file instead of being typed.
        self.fields["markdown_content"].required = False


class MarkdownUploadAdminMixin:
    """Shared save_model logic: pull uploaded .md file content into markdown_content."""
    form = MarkdownUploadForm

    def save_model(self, request, obj, form, change):
        uploaded_file = form.cleaned_data.get("markdown_file")
        if uploaded_file:
            content_bytes = uploaded_file.read()
            obj.markdown_content = content_bytes.decode("utf-8")
        super().save_model(request, obj, form, change)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ("title", "genre", "language", "date_read", "difficulty", "rating", "is_reviewed")
    search_fields = ("title", "author")
    list_filter = ("genre", "language", "is_reviewed")
    readonly_fields = ("is_reviewed",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("author", "quote_english", "original_language", "short_original_quote")
    search_fields = ("author", "quote_english")

    def short_original_quote(self, obj):
        return (obj.original_quote[:40] + "…") if len(obj.original_quote) > 40 else obj.original_quote
    short_original_quote.short_description = "Original quote"


@admin.register(BookOfTheMonth)
class BookOfTheMonthAdmin(admin.ModelAdmin):
    list_display = ("book", "featured_date")
    autocomplete_fields = ["book"]


@admin.register(Review)
class ReviewAdmin(MarkdownUploadAdminMixin, admin.ModelAdmin):
    list_display = ("title", "book", "published", "date_written")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Story)
class StoryAdmin(MarkdownUploadAdminMixin, admin.ModelAdmin):
    list_display = ("title", "published", "date_written")
    prepopulated_fields = {"slug": ("title",)}
