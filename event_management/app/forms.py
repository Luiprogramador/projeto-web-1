from django import forms
from .models import login, Event, Registration, register

class LoginForm(forms.ModelForm):
    class Meta:
        model = login
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Username',
            'password': 'Password',
        }
        help_texts = {
            'username': 'Enter your username.',
            'password': 'Enter your password.',
        }
        error_messages = {
            'username': {
                'max_length': 'Username is too long.',
                'required': 'Username is required.',
            },
            'password': {
                'max_length': 'Password is too long.',
                'required': 'Password is required.',
            },
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
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

class RegisterForm(forms.ModelForm):
    class Meta:
        model = register
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }