from .forms import UserRegisterForm, LoginForm, EventForm, ProfileForm,OrganizerUserCreationForm
from .models import Event, Certificate, EventParticipant, UserRegister, Auditoria
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.urls import reverse        

def home(request):
    eventos = Event.objects.all() # Busca todos os eventos cadastrados.
    return render(request, 'event/event_list.html', {'eventos': eventos})


def base(request):
    return render(request, 'base.html')

# ------------- USER-------------
def login_view(request):
    if request.user.is_authenticated: # Redireciona usuários já logados para a página inicial.
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) # Inicializa o formulário com dados do POST.
        if form.is_valid():
            user = form.get_user()

            login(request, user) # Faz o login do usuário na sessão.
            
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request) # Desloga o usuário da sessão.
    return redirect('home')


def user_register_view(request): 
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save() # Cria e salva o novo usuário no banco de dados.
            
            messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {user.username}.')
            messages.info(request, 'Por favor, faça login para continuar.')
            messages.info(request, 'Um e-mail de boas-vindas foi enviado para o seu endereço de e-mail.')
            enviar_email(user) # Chama a função para enviar e-mail de boas-vindas.

            Auditoria.objects.create(
                user=user,
                action=f'Registro do(a) {user.username}',
                timestamp=datetime.now(),
            )
            return redirect('home') 
        else:
            messages.error(request, 'Erro ao criar a conta. Verifique os dados e tente novamente.')
    else:
        form = UserRegisterForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def organizer_add_user(request):
    # 1. Segurança: Só Organizador pode acessar
    if request.user.user_type != 'Organizador':
        messages.error(request, "Apenas organizadores podem cadastrar usuários manualmente.")
        return redirect('home') # ou para onde você preferir

    if request.method == 'POST':
        form = OrganizerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Usuário {form.cleaned_data['username']} criado com sucesso!")
            Auditoria.objects.create(
                user=request.user,
                action=f'Registro do {form.cleaned_data["username"]} pelo(a) Organizador(a) {request.user.username}',
                timestamp=datetime.now(),
            )
            return redirect('organizer_add_user') # Recarrega a página limpa para adicionar outro
    else:
        form = OrganizerUserCreationForm()

    return render(request, 'organizer_add_user.html', {'form': form})

# ------------- PROFILE -------------
@login_required # Garante que apenas usuários logados acessem esta view.
def profile(request):
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
                        UserRegister.objects.filter(username=user.username).first() # Lógica de fallback para garantir que a instância correta do modelo de perfil seja obtida.
    except Exception:
        profile = None

    return render(request, 'profile/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    """
    Edita o perfil do usuário logado.
    """
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user) # Popula o formulário com dados POST e a instância atual do usuário.
        if form.is_valid():
            form.save() # Salva as alterações no perfil do usuário.
            messages.success(request, "Perfil atualizado com sucesso.")
            Auditoria.objects.create(
                user=request.user,
                action=f'Editar Perfil {user.username}',
                timestamp=datetime.now(),
            )
            return redirect('profile')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = ProfileForm(instance=user) # Inicializa o formulário com os dados atuais do usuário (para GET).

    return render(request, 'profile/profile_edit.html', {'form': form})

# ------------- EVENT -------------
def event_list(request):
    eventos = Event.objects.all()
    return render(request, 'event/event_list.html', {'eventos': eventos})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk) # Busca o evento ou retorna 404.
    
    context = {
        'event': event,
        'is_registered': request.user.is_authenticated and event.participants.filter(pk=request.user.pk).exists() # Verifica se o usuário logado está inscrito no evento.
    }
    
    return render(request, 'event/event_detail.html', context)

@login_required
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False) # Não salva imediatamente.
            event.creator = request.user # Associa o evento ao usuário criador (logado).
            event.save() # Salva o evento após adicionar o criador.
            Auditoria.objects.create(
                user=request.user,
                action=f'Adicionar Evento {event.title}',
                timestamp=datetime.now(),
            )
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event/event_add.html', {'form': form})

@login_required
def remove_event(request, pk):
    evento = get_object_or_404(Event, pk=pk)
    
    if evento.creator != request.user: # Verifica se o usuário logado é o criador do evento.
           messages.error(request, 'Você não tem permissão para deletar este evento.')
           return redirect('event_list')
           
    if request.method == 'POST': # A deleção só ocorre após a confirmação (POST).
        evento.delete() # Deleta o objeto Evento.
        messages.success(request, f'O evento "{evento.title}" foi removido com sucesso.')
        Auditoria.objects.create(
                user=request.user,
                action=f'Remover Evento {evento.title}',
                timestamp=datetime.now(),
            )
        return redirect('event_list')
    
    return render(request, 'event/event_remove.html', {'evento': evento})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event) # Inicializa o formulário com a instância existente (para edição).
        if form.is_valid():
            evento = form.save(commit=False)

            # Salva a imagem diretamente no campo do modelo
            if 'image' in request.FILES:
                evento.image = request.FILES['image'] # Atualiza o campo de imagem se um novo arquivo for enviado.

            evento.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            Auditoria.objects.create(
                user=request.user,
                action=f'Editar Evento {evento.title}',
                timestamp=datetime.now(),
            )
            return redirect('event_detail', pk=evento.pk)
        else:
            messages.error(request, 'Erro ao atualizar o evento. Verifique os dados e tente novamente.')
    else:
        form = EventForm(instance=event) # Preenche o formulário com os dados atuais do evento (para GET).

    return render(request, 'event/event_add.html', {'form': form, 'is_edit': True, 'event': event})

@login_required
def event_final(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # Verifica permissão
    if request.user != event.creator:
        messages.error(request, 'Você não tem permissão.')
        return redirect('event_detail', pk=pk)

    if request.method == 'POST': 
        
        # Verifica se já não estava finalizado
        if not event.event_finalized: 
            event.event_finalized = True 
            event.save()
            
            # Auditoria
            Auditoria.objects.create(
                user=request.user,
                action=f'Finalizar Evento {event.title}',
                timestamp=datetime.now(),
            )

            count_emails = 0
            
            # Loop pelos participantes
            for participant in event.participants.all():
                
                # --- AQUI ESTÁ A CORREÇÃO DA DATA ---
                certificate, created = Certificate.objects.get_or_create(
                    event=event, 
                    participant=participant,
                    defaults={
                        # Aqui definimos que a data do certificado será a data final do evento
                        'issue_date': event.final_date 
                    }
                )
                
                # Opcional: Se o certificado já existia mas estava sem data (antigo), atualiza:
                if not created and not certificate.issue_date:
                    certificate.issue_date = event.final_date
                    certificate.save()

                # Envia o e-mail
                enviar_email_certificado(participant, event)
                Auditoria.objects.create(
                    user=request.user,
                    action=f'Emitir certificado {participant.username}',
                    timestamp=datetime.now(),
                )
                count_emails += 1
            
            messages.success(request, f'Evento finalizado! {count_emails} certificados gerados e enviados.')
        else:
            messages.warning(request, 'Este evento já estava finalizado.')

    return redirect('event_detail', pk=event.pk)

# ------------- EVENT SUBSCRIBE -------------
@login_required
def event_subscribe(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user

    if request.method == 'POST':
        if user.user_type == 'organizer':
            messages.error(request, 'Você não tem permissão para inscrever ou desinscrever este evento.')
            return redirect('event_detail', pk=event.pk)

        # Se o usuário já está inscrito
        if event.participants.filter(pk=user.pk).exists():
            event.participants.remove(user)
            messages.info(request, f'Você foi desinscrito do evento "{event.title}".')

        else:
            # Se o evento estiver lotado
            if event.is_full:
                messages.error(request, f'O evento "{event.title}" está lotado (Capacidade Máx: {event.max_capacity}).')
                return redirect('event_detail', pk=event.pk)

            event.participants.add(user)
            messages.success(request, f'Inscrição confirmada no evento "{event.title}"!')
            Auditoria.objects.create(
                user=request.user,
                action=f'Inscrição no Evento {event.title} pelo(a) {user.username}',
                timestamp=datetime.now(),
            )

    return redirect('event_detail', pk=event.pk)

@login_required
def event_subscribed_list(request):
    eventos = request.user.attended_events.all() # Acessa a lista de eventos nos quais o usuário está inscrito
    
    context = {
        'eventos': eventos,
        'page_title': 'Meus Eventos Inscritos'
    }
    return render(request, 'event/event_subscribed.html', context)

# ------------- CERTIFICATE -------------
@login_required
def certificate_list(request):
    user = request.user
    
    participated_events = user.attended_events.all()
    
    events_data = []
    for event in participated_events:
        certificate_status = Certificate.objects.filter(event=event, participant=user).exists() # Verifica se o certificado para o evento e usuário existe.
        
        event_data = event
        event_data.certificate_issued = certificate_status # Adiciona dinamicamente um atributo à instância do evento (não salva no DB).
        events_data.append(event_data)
        
    context = {
        'events_with_certificates': events_data,
        'participant': user
    }
    
    return render(request, 'certificate/certificate_list.html', context)

@login_required
def issue_certificate(request, event_id):
    try:
        # Verifica se o evento existe
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:

        messages.error(request, 'Evento não encontrado.')
        return redirect('event_list') 
        
    participant = request.user
    
    # Verifica se o usuário está registrado como participante do evento
    if not EventParticipant.objects.filter(event=event, participant=participant).exists():
        messages.error(request, f'Você não está registrado como participante do evento "{event.title}".')

        return redirect('event_detail', pk=event_id)
    
    try:
        # Cria um novo certificado ou recupera o existente
        certificate = Certificate.objects.get(event=event, participant=participant) # Tenta recuperar o certificado existente.
        messages.info(request, 'Certificado já registrado. Visualizando registro...')
        Auditoria.objects.create(
                user=request.user,
                action=f'Emitir certificado {participant.username}',
                timestamp=datetime.now(),
            )
        
    # Caso o certificado não exista, cria um novo
    except Certificate.DoesNotExist:
        certificate = Certificate.objects.create(event=event, participant=participant) # Cria um novo registro de certificado.
        messages.success(request, 'Registro do certificado criado com sucesso. Preparando visualização...')
        Auditoria.objects.create(
                user=request.user,
                action=f'Emitir certificado {participant.username}',
                timestamp=datetime.now(),
            )
    
    # Tratamento de Erro de Dados Corrompidos
    except ValueError as e:
        if "badly formed hexadecimal UUID string" in str(e):
            
            Certificate.objects.filter(event=event, participant=participant).delete() # Deleta o registro corrompido.
            messages.warning(request, f'Registro de certificado corrompido para "{event.title}" foi removido.')

            certificate = Certificate.objects.create(event=event, participant=participant) # Cria um novo certificado válido.
            messages.success(request, f'Novo certificado válido para "{event.title}" criado com sucesso.')
        else:
            messages.error(request, f'Erro inesperado ao acessar/criar o registro do certificado. Detalhe: {e}')
            return redirect('event_detail', pk=event_id)
        
    
    
    context = {
        'certificate': certificate,
        'event': event,
        'participant': participant
    }
    return render(request, 'certificate/certificate_detail.html', context)

# ------------- AUDITORIAL -------------        # Importe o seu model de Auditoria

def auditorial(request):
    if not request.user.is_authenticated or getattr(request.user, 'user_type', '') != 'Organizador':
        messages.error(request, 'Você não tem permissão para acessar o auditorial.')
        return redirect('home')

    logs = Auditoria.objects.all().order_by('-timestamp')

    # --- Lógica do Filtro ---
    user_id = request.GET.get('user')
    action_query = request.GET.get('action')

    if user_id:
        logs = logs.filter(user__id=user_id)

    if action_query:
        # icontains continua sendo necessário pois a ação no banco pode ser uma frase longa
        # Ex: Se selecionar "Editar", ele acha "Editar perfil de fulano"
        logs = logs.filter(action__icontains=action_query)

    # --- Dados para os Menus ---
    users = UserRegister.objects.all().order_by('username')
    
    # Lista exata das palavras-chave que você usa nos "if/elif" do seu HTML
    action_options = [
        'Adicionar', 
        'Editar', 
        'Remover', 
        'Emitir', 
        'Registro', 
        'Inscrição', 
        'Finalizar'
    ]

    context = {
        'logs': logs,
        'users': users,
        'action_options': action_options  # Enviamos a lista para o template
    }

    return render(request, 'auditorial.html', context)

# ------------- EMAIL -------------
def enviar_email(user):
    base_url = "http://127.0.0.1:8000/" # URL base do projeto (local).
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

    # 
    send_mail( # Função do Django para enviar e-mail.
        subject="Saudação de boas vindas 👋",
        message="Seja bem vindo ao Event Management! (Para uma melhor visualização, ative o HTML em seu e-mail.)",
        from_email=None,
        recipient_list=[user.email], # Envia para o e-mail do usuário recém-criado.
        fail_silently=False,
        html_message=html_content, # Envia o conteúdo HTML formatado.
    )

    return HttpResponse("E-mail enviado com sucesso!")

def enviar_email_certificado(user, event):
    # Cria o link para o certificado
    relative_link = reverse('issue_certificate', args=[event.pk])
    full_link = f"http://127.0.0.1:8000{relative_link}" # Mude o domínio em produção

    subject = f"Certificado Disponível: {event.title}"
    message = f"Olá {user.username}, seu certificado do evento {event.title} está pronto. Acesse: {full_link}"
    
    html_content = f"""
    <html>
        <body>
            <h2>Olá, {user.username}!</h2>
            <p>O evento <strong>"{event.title}"</strong> foi finalizado com sucesso.</p>
            <p>Seu certificado já está disponível para download.</p>
            <br>
            <a href="{full_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Baixar Certificado
            </a>
            <p>Ou acesse: {full_link}</p>
        </body>
    </html>
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=None, # Usa o padrão do settings
        recipient_list=[user.email],
        fail_silently=True, # Se falhar um, não trava o site
        html_message=html_content
    )


@login_required
def event_participants(request, pk):
    event = get_object_or_404(Event, pk=pk)
    participants = event.participants.all()
    
    # Verificação de segurança: Só o criador pode ver a lista
    if request.user != event.creator and request.user not in participants:
        return HttpResponseForbidden("Você não tem permissão para ver esta lista.")
    
    context = {
        'event': event,
        'participants': participants
    }
    return render(request, 'event/event_participants.html', context)

def exemplo(request):
    return render(request, 'exemplo.html')