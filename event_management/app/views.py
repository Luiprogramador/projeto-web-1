from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
<<<<<<< HEAD
from .models import Event, Certificate, EventParticipant 
from .forms import RegisterForm, LoginForm, EventForm
from datetime import datetime, time, timedelta
=======
from .models import Event
from .forms import RegisterForm, LoginForm, EventForm
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1

def home(request):
    eventos = Event.objects.all()
    return render(request, 'event_list.html', {'eventos': eventos})
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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save() 
            
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
<<<<<<< HEAD
    if request.user.user_type != 'Organizador': 
=======
    if request.user.type_user != 'Organizador':
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
        messages.error(request, 'Apenas usuários do tipo Organizador têm permissão para criar eventos.')
        return redirect('event_list')
        
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            
            evento = form.save(commit=False)
            
            evento.creator = request.user 
            
            try:
                evento.save() 
                form.save_m2m() 
            
                messages.success(request, 'Evento adicionado com sucesso!')
                return redirect('event_list')
            
            except Exception as e:
                 messages.error(request, f'Erro ao salvar o evento. Detalhe: {e}')
                 return render(request, 'add_event.html', {'form': form})
            
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
    eventos = request.user.attended_events.all()
    
    context = {
        'eventos': eventos,
        'page_title': 'Meus Eventos Inscritos'
    }
    
    return render(request, 'event_subscribed.html', context)


@login_required
def add_event(request):
    # VERIFICAÇÃO DE PERMISSÃO: Usa o campo 'user_type'
    if request.user.user_type != 'Organizador':
        # Mensagem de erro em Português
        messages.error(request, 'Apenas usuários do tipo Organizador têm permissão para criar eventos.')
        return redirect('event_list')
        
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            
            # --- Lógica de Cálculo da Duração (Novo) ---
            start_date = evento.initial_date
            end_date = evento.final_date
            
            # O cálculo retorna um objeto timedelta
            duration_timedelta = end_date - start_date

            # Se a duração for negativa ou nula, você pode adicionar uma mensagem de erro:
            if duration_timedelta <= timedelta(minutes=0):
                messages.error(request, 'A Data e Hora de Início deve ser anterior à Data e Hora de Fim.')
                return render(request, 'add_event.html', {'form': form})
            
            # Converte o timedelta (duração) para um objeto time para salvar no campo TimeField (event_duration)
            # Obs: Isso só funciona corretamente para eventos menores que 24 horas.
            # Se o evento for maior que 24h, você precisará armazenar a duração em um campo IntegerField (minutos)
            
            # Cálculo para TimeField (máximo 23:59:59)
            total_seconds = int(duration_timedelta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            
            # Garante que o valor não ultrapasse o limite do TimeField (23:59:59)
            # Se for maior que 24h, você pode decidir armazenar 23:59:59 ou emitir erro.
            if hours >= 24:
                 # Exemplo: Armazenar a duração total em minutos em um campo IntegerField no modelo, em vez de TimeField.
                 # Ou, como um TimeField não suporta mais de 24h, você define um limite:
                 hours = 23
                 minutes = 59
                 
            evento.event_duration = time(hours, minutes)
            # --------------------------------------------

            evento.creator = request.user 
            
            try:
                evento.save() 
                form.save_m2m() 
            
                messages.success(request, 'Evento adicionado com sucesso!')
                return redirect('event_list')
            
            except Exception as e:
                # Mensagem de erro em Português
                messages.error(request, f'Erro ao salvar o evento. Detalhe: {e}')
                return render(request, 'add_event.html', {'form': form})
            
    else:
        form = EventForm()
        
    return render(request, 'add_event.html', {'form': form})

@login_required
def certificate_list(request):
    user = request.user
    
    # 1. Recuperar todos os eventos nos quais o usuário participou.
    # O related_name que definimos é 'attended_events'.
    participated_events = user.attended_events.all()
    
    # 2. Verificar se o certificado já existe para cada evento
    events_data = []
    for event in participated_events:
        # Tenta encontrar um registro de certificado para o evento e o usuário atual
        certificate_status = Certificate.objects.filter(event=event, participant=user).exists()
        
        # Cria um objeto simples para passar ao template, adicionando o status
        event_data = event
        event_data.certificate_issued = certificate_status
        events_data.append(event_data)
        
    context = {
        # Passa a lista de eventos, já marcada com o status do certificado
        'events_with_certificates': events_data,
        'participant': user
    }
    
    # Renderiza o template de lista
    return render(request, 'certificate_list.html', context)

@login_required
def issue_certificate(request, event_id): # Nome da função em Inglês
    # 1. Obter o Evento
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        # Mensagem de erro em Português
        messages.error(request, 'Evento não encontrado.')
        return redirect('event_list') 
        
    participant = request.user
    
    # 2. Verificar se o usuário é um participante registrado do evento
    # Usa o modelo EventParticipant
    if not EventParticipant.objects.filter(event=event, participant=participant).exists():
        # Mensagem de erro em Português
        messages.error(request, f'Você não está registrado como participante do evento "{event.title}".')
        # Supondo que você tenha uma URL para o detalhe do evento
        return redirect('detalhe_evento', event_id=event_id)
    
    # 3. Criar ou Obter o registro do Certificate
    try:
        # Usa o modelo Certificate e os nomes dos campos em Inglês
        certificate, created = Certificate.objects.get_or_create(
            event=event,
            participant=participant
            # issue_date e verification_code são gerados por padrão
        )
        
        if created:
            # Mensagem em Português
            messages.success(request, 'Registro do certificado criado com sucesso. Preparando visualização...')
        else:
            # Mensagem em Português
            messages.info(request, 'Certificado já registrado. Visualizando registro...')

    except Exception as e:
        # Mensagem de erro em Português
        messages.error(request, f'Erro ao acessar/criar o registro do certificado. Detalhe: {e}')
        return redirect('detalhe_evento', event_id=event_id)
    
    # --- 4. Preparar contexto e retornar o template ---
    
    # Nomes das variáveis do contexto em Inglês
    context = {
        'certificate': certificate,
        'event': event,
        'participant': participant
    }
    
    # Nome do template em Inglês
    return render(request, 'certificate_detail.html', context)
