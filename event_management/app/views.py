from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Event, Certificate, EventParticipant, UserRegister, Auditoria
from .forms import RegisterForm, LoginForm, EventForm, ProfileForm
from datetime import datetime, time, timedelta # O 'time' não é mais usado aqui, mas pode deixar
from .utils import get_relative_path, salvar_imagem_em_pasta
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

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
            messages.info(request, 'Por favor, faça login para continuar.')
            messages.info(request, 'Um e-mail de boas-vindas foi enviado para o seu endereço de e-mail.')
            enviar_email(user)

            Auditoria.objects.create(
                user=user,
                action='Registro',
                timestamp=datetime.now(),
            )
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
def remove_event(request, pk):
    evento = get_object_or_404(Event, pk=pk)
    
    if evento.creator != request.user:
         messages.error(request, 'Você não tem permissão para deletar este evento.')
         return redirect('event_list')
         
    if request.method == 'POST':
        evento.delete()
        messages.success(request, f'O evento "{evento.title}" foi removido com sucesso.')
        return redirect('event_list')
    
    Auditoria.objects.create(
                user=request.user,
                action='Remover Evento',
                timestamp=datetime.now(),
            )
    return render(request, 'remove_event.html', {'evento': evento})


@login_required
def toggle_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user

    if request.method == 'POST':
        if user.user_type != 'organizer':
            messages.error(request, 'Você não tem permissão para inscrever ou desinscrever este evento.')
            return redirect('event_detail', pk=event.pk)
         
        if event.participants.filter(pk=user.pk).exists():
            event.participants.remove(user)
            messages.info(request, f'Você foi desinscrito do evento "{event.title}".')
        
        else:
            if event.is_full:
                 messages.error(request, f'O evento "{event.title}" está lotado (Capacidade Máxima: {event.max_capacity}).')
                 return redirect('event_detail', pk=event.pk)
                 
            event.participants.add(user)
            messages.success(request, f'Inscrição confirmada no evento "{event.title}"!')
            Auditoria.objects.create(
                user=request.user,
                action='Inscrição no Evento',
                timestamp=datetime.now(),
            )
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
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    Auditoria.objects.create(
        user=request.user,
        action='Adicionar Evento',
        timestamp=datetime.now(),
    )
    return render(request, 'add_event.html', {'form': form})


@login_required
def certificate_list(request):
    user = request.user
    
    participated_events = user.attended_events.all()
    
    events_data = []
    for event in participated_events:
        certificate_status = Certificate.objects.filter(event=event, participant=user).exists()
        

        event_data = event
        event_data.certificate_issued = certificate_status
        events_data.append(event_data)
        
    context = {
        'events_with_certificates': events_data,
        'participant': user
    }
    
    return render(request, 'certificate_list.html', context)

@login_required
def issue_certificate(request, event_id):

    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:

        messages.error(request, 'Evento não encontrado.')
        return redirect('event_list') 
        
    participant = request.user

    if not EventParticipant.objects.filter(event=event, participant=participant).exists():
        messages.error(request, f'Você não está registrado como participante do evento "{event.title}".')

        return redirect('event_detail', pk=event_id)
    
    try:
        certificate = Certificate.objects.get(event=event, participant=participant)
        created = False
        messages.info(request, 'Certificado já registrado. Visualizando registro...')

    except Certificate.DoesNotExist:
        certificate = Certificate.objects.create(event=event, participant=participant)
        created = True
        messages.success(request, 'Registro do certificado criado com sucesso. Preparando visualização...')

    except ValueError as e:
        if "badly formed hexadecimal UUID string" in str(e):
            
            Certificate.objects.filter(event=event, participant=participant).delete()
            messages.warning(request, f'Registro de certificado corrompido para "{event.title}" foi removido.')

            certificate = Certificate.objects.create(event=event, participant=participant)
            created = True
            messages.success(request, f'Novo certificado válido para "{event.title}" criado com sucesso.')
        else:
            messages.error(request, f'Erro inesperado ao acessar/criar o registro do certificado. Detalhe: {e}')
            return redirect('event_detail', pk=event_id)
    
    context = {
        'certificate': certificate,
        'event': event,
        'participant': participant
    }

    Auditoria.objects.create(
                user=request.user,
                action='Emitir Certificado',
                timestamp=datetime.now(),
            )
    return render(request, 'certificate_detail.html', context)


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            evento = form.save(commit=False)

            # Salva a imagem diretamente no campo do modelo
            if 'image' in request.FILES:
                evento.image = request.FILES['image']

            evento.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('event_detail', pk=evento.pk)
        else:
            messages.error(request, 'Erro ao atualizar o evento. Verifique os dados e tente novamente.')
    else:
        form = EventForm(instance=event)

    Auditoria.objects.create(
                user=request.user,
                action='Editar Evento',
                timestamp=datetime.now(),
            )
    return render(request, 'add_event.html', {'form': form, 'is_edit': True, 'event': event})


@login_required
def perfil(request):
    """
    Exibe a página de perfil do usuário logado.
    Tenta usar o próprio request.user (caso UserRegister seja o modelo de usuário)
    ou busca a instância em UserRegister por pk/username como fallback.
    """
    user = request.user
    profile = None
    try:
        # se o user já for instância de UserRegister
        if isinstance(user, UserRegister):
            profile = user
        else:
            # tenta localizar um UserRegister correspondente
            profile = UserRegister.objects.filter(pk=user.pk).first() or \
                      UserRegister.objects.filter(username=user.username).first()
    except Exception:
        profile = None

    return render(request, 'perfil.html', {'profile': profile})

@login_required
def perfil_edicao(request):
    """
    Edita o perfil do usuário logado.
    """
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('perfil')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = ProfileForm(instance=user)

    return render(request, 'perfil_edicao.html', {'form': form})

def auditorial(request):
    if not request.user.is_authenticated or request.user.user_type != 'Organizador':
        messages.error(request, 'Você não tem permissão para acessar o auditorial.')
        return redirect('home')

    logs = Auditoria.objects.all().order_by('-timestamp')

    context = {
        'logs': logs
    }

    return render(request, 'auditorial.html', context)

def enviar_email(user):
    base_url = "http://127.0.0.1:8000/" # Ou o seu domínio público
    link_para_site = f"{base_url}/login/"

    html_content = f"""
    <html>
    <body>
        <h2>Bem-vindo(a) ao Event Management!</h2>
        <h3>Agradecemos por se cadastrar. Clique na imagem ou no link abaixo para começar:</h3>

        <a href="{link_para_site}">
            <img src="https://i.ibb.co/27j1wVmK/logo.png" alt="logo" border="0" />
        </a>

        <p>Se a imagem não carregar, acesse: <a href="{link_para_site}">Clique Aqui para Começar</a></p>

        <p>Saudações!</p>
    </body>
    </html>
    """

    send_mail(
        subject="Saudação de boas vindas 👋",
        message="Seja bem vindo ao Event Management! (Para uma melhor visualização, ative o HTML em seu e-mail.)", # Versão texto simples (obrigatória)
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_content, # A versão HTML que inclui imagem e link
    )

    return HttpResponse("E-mail enviado com sucesso!")
