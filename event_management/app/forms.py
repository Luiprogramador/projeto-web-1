from django import forms
from .models import Event, Registration
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'max_capacity']
        labels = {
            'title': 'Event Title',
            'description': 'Event Description',
            'date': 'Event Date and Time',
            'location': 'Event Location',
        }
        help_texts = {
            'title': 'Enter the title of the event.',
            'description': 'Enter a brief description of the event.',
            'date': 'Select the date and time of the event.',
            'location': 'Enter the location of the event.',
        }
        error_messages = {
            'title': {
                'max_length': 'Title is too long.',
                'required': 'Title is required.',
            },
            'description': {
                'required': 'Description is required.',
            },
            'date': {
                'invalid': 'Enter a valid date and time.',
                'required': 'Date and time are required.',
            },
            'location': {
                'max_length': 'Location is too long.',
                'required': 'Location is required.',
            },
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['event', 'name', 'email']
        labels = {
            'event': 'Event',
            'name': 'Your Name',
            'email': 'Your Email',
        }
        help_texts = {
            'event': 'Select the event you want to register for.',
            'name': 'Enter your full name.',
            'email': 'Enter your email address.',
        }
        error_messages = {
            'event': {
                'required': 'Event selection is required.',
            },
            'name': {
                'max_length': 'Name is too long.',
                'required': 'Name is required.',
            },
            'email': {
                'invalid': 'Enter a valid email address.',
                'required': 'Email is required.',
            },
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        help_text='Obrigatório. Usado para comunicação e recuperação de conta.'
    )

    class Meta:
        model = User
        fields = ('username', 'email')