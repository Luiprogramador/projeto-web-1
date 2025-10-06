from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm, EventForm, RegistrationForm
def index(request):
    return render(request, 'index.html')
# Create your views here.

def base(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'login.html')

def register(request): 
    return render(request, 'register.html')