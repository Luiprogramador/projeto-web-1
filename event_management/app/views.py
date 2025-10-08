from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 

from .models import Event
from .forms import RegisterForm, LoginForm, EventForm


def home(request):
    return render(request, 'index.html')
# Create your views here.


def base(request):
    return render(request, 'base.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            login(request, user) 
            
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request): 
    form = RegisterForm()
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save() 
            
            login(request, user)
            
            messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {user.username}.')
            
            return redirect('home') 
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os dados e tente novamente.')
    else:
        form = RegisterForm()
        
    return render(request, 'register.html', {'form': form})


def event_list(request):
    eventos = Event.objects.all()
    return render(request, 'event_list.html', {'eventos': eventos})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    context = {
        'event': event,
        'is_registered': request.user.is_authenticated and event.participants.filter(pk=request.user.pk).exists()
    }
    
    return render(request, 'event_detail.html', context)


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            
            evento.creator = request.user 
            
            evento.save() 
            
            messages.success(request, 'Evento adicionado com sucesso!')
            return redirect('event_list')
    else:
        form = EventForm()
        
    return render(request, 'add_event.html', {'form': form})


@login_required
def remove_event(request, pk):
    evento = get_object_or_404(Event, pk=pk)
    
    if evento.creator != request.user:
         messages.error(request, 'Você não tem permissão para deletar este evento.')
         return redirect('event_list')
         
    if request.method == 'POST':
        evento.delete()
        messages.success(request, f'O evento "{evento.title}" foi removido com sucesso.')
        return redirect('event_list')
        
    return render(request, 'remove_event.html', {'evento': evento})


@login_required
def toggle_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user

    if request.method == 'POST':
        
        if event.participants.filter(pk=user.pk).exists():
            event.participants.remove(user)
            messages.info(request, f'Você foi desinscrito do evento "{event.title}".')
        
        else:
            if event.is_full:
                 messages.error(request, f'O evento "{event.title}" está lotado (Capacidade Máxima: {event.max_capacity}).')
                 return redirect('event_detail', pk=event.pk)
                 
            event.participants.add(user)
            messages.success(request, f'Inscrição confirmada no evento "{event.title}"!')

    return redirect('event_detail', pk=event.pk)


@login_required
def event_subscribed(request):
    eventos = request.user.eventos_participados.all()
    
    context = {
        'eventos': eventos,
        'page_title': 'Meus Eventos Inscritos'
    }
    
    return render(request, 'event_subscribed.html', context)