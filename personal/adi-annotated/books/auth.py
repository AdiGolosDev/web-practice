import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ComplexityValidator:
    """Requires at least one uppercase letter, one lowercase letter, one
    digit, and one symbol. Minimum length is handled separately by
    Django's built-in MinimumLengthValidator. Referenced from settings.py
    as 'books.auth.ComplexityValidator'."""

    def validate(self, password, user=None):
        missing = []
        if not re.search(r'[A-Z]', password):
            missing.append('an uppercase letter')
        if not re.search(r'[a-z]', password):
            missing.append('a lowercase letter')
        if not re.search(r'[0-9]', password):
            missing.append('a number')
        if not re.search(r'[^A-Za-z0-9]', password):
            missing.append('a symbol')
        if missing:
            raise ValidationError(
                'Password must include ' + ', '.join(missing) + '.',
                code='password_no_complexity',
            )

    def get_help_text(self):
        return 'Your password must include an uppercase letter, a lowercase letter, a number, and a symbol.'


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    field_order = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email