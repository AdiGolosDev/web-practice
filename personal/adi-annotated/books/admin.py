from django import forms
from django.contrib import admin
from .models import Book, Review, Story

# Register your models here.
# where I should register models(book, review),
#  so they show up and are manageable in the /admin/ panel

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


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "year_read", "difficulty", "rating", "is_reviewed")
    search_fields = ("title", "author")
    list_filter = ("genre", "is_classic", "is_reviewed")


@admin.register(Review)
class ReviewAdmin(MarkdownUploadAdminMixin, admin.ModelAdmin):
    list_display = ("title", "book", "published", "date_written")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Story)
class StoryAdmin(MarkdownUploadAdminMixin, admin.ModelAdmin):
    list_display = ("title", "published", "date_written")
    prepopulated_fields = {"slug": ("title",)}