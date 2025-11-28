from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from datetime import date, datetime
from django.conf import settings 
from django.db import models
import uuid

class Event(models.Model):
    event_type_choices = [
        ('Palestra', 'Palestra'),
        ('Workshop', 'Workshop'),
        ('Seminário', 'Seminário'),
        ('Curso', 'Curso'),
        ('Congresso', 'Congresso'),
        ('Simpósio', 'Simpósio'),
        ('Fórum', 'Fórum'),
        ('Mesa Redonda', 'Mesa Redonda'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    image = models.ImageField(
        upload_to='eventos/',
        verbose_name='Imagem do Evento',
        null=True,
        blank=True
    )
    initial_date = models.DateField(default= '9999-12-31', verbose_name="Data de Início")
    final_date = models.DateField(default='9999-12-31', verbose_name="Data Final")
    location = models.CharField(max_length=200, verbose_name="Local")
    max_capacity = models.IntegerField(verbose_name="Capacidade Máxima")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        related_name='created_events', # Relacionamento reverso para eventos criados pelo usuário.
        null=True,
        blank=True,
        verbose_name="Criador"
    )
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Mantém o evento se o professor for deletado (o campo será nulo).
        null=True,                   
        blank=True,                  
        verbose_name="Professor Responsável",
        related_name="instructed_events",
        
        limit_choices_to={'user_type': 'Professor'} # Limita as opções de escolha no admin/formulário.
    )
    event_type = models.CharField(max_length=20, choices=event_type_choices, default='Palestra', verbose_name="Tipo de Evento")
    event_start = models.TimeField(null=False, blank=True, verbose_name="Horario de Início") 
    event_end = models.TimeField(null=False, blank=True, verbose_name="Horario de Término")
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventParticipant', # Define que a relação M2M será gerenciada pelo modelo EventParticipant.
        through_fields=('event', 'participant'), 
        related_name='attended_events', # Relacionamento reverso para eventos que o usuário participa.
        blank=True,
        verbose_name="Participantes"
    )
    
    class Meta:
        db_table = 'event'
        ordering = ['initial_date']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
    
    def __str__(self):
        return self.title

    @property
    def calculated_duration_hours(self):
        start_datetime = datetime.combine(self.initial_date, self.event_start)
        final_datetime = datetime.combine(self.final_date, self.event_end)
        
        duration = final_datetime - start_datetime
        
        return round(duration.total_seconds() / 3600, 1) # Calcula a duração total em horas.
    
    @property
    def event_duration(self):
        """Calcula a duração total do evento como um timedelta ou formata como string."""
        start_datetime = datetime.combine(self.initial_date, self.event_start)
        final_datetime = datetime.combine(self.final_date, self.event_end)
        
        duration = final_datetime - start_datetime
        
        return duration # Retorna a duração como objeto timedelta.

    @property
    def formatted_duration(self):
        """Calcula e formata a duração total como 'HhMMmin' (ex: '25h30min')."""
        duration = self.event_duration # duration é um timedelta
        
        total_seconds = int(duration.total_seconds())
        
        # Calcula as horas totais (incluindo horas que ultrapassam 24)
        total_hours = total_seconds // 3600
        # Calcula os minutos restantes
        remaining_minutes = (total_seconds % 3600) // 60
        
        # Garante que minutos sejam sempre dois dígitos (ex: 5 -> '05')
        formatted_minutes = f"{remaining_minutes:02}" 
        
        return f"{total_hours}h{formatted_minutes}min"
    
    @property
    def current_participants_count(self):
        return self.participants.count() # Retorna a contagem atual de participantes.
    
    @property
    def is_full(self):
        return self.current_participants_count >= self.max_capacity # Verifica se a capacidade máxima foi atingida.


class EventParticipant(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        db_column='user_id' # Define o nome da coluna no banco de dados para a chave estrangeira.
    ) 
    
    class Meta:
        unique_together = ('event', 'participant') # Garante que um usuário só pode se inscrever uma vez por evento.


class EventRegister(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        db_table = 'EventRegister'
        ordering = ['name']
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class Certificate(models.Model):
    """Model to track certificates issued to event participants."""
    
    event = models.ForeignKey(
        'Event', 
        on_delete=models.CASCADE, 
        related_name='certificates', 
        verbose_name="Evento"
    )
    
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_certificates',
        verbose_name="Participante" 
    )
    
    issue_date = models.DateField(
        default=date.today, # Define a data de emissão como a data atual por padrão.
        verbose_name="Data de Emissão" 
    )
    
    verification_code = models.UUIDField(
        default=uuid.uuid4, # Gera um UUID (código único e universal) por padrão.
        unique=True, 
        editable=False, # Impede que o código seja alterado no admin.
        verbose_name="Código de Verificação" 
    )

    class Meta:
        db_table = 'certificate'
        verbose_name = "Certificado" 
        verbose_name_plural = "Certificados" 
        unique_together = ('event', 'participant') # Garante um único certificado por participante por evento.
        ordering = ['-issue_date']

    def __str__(self):
        return f"Certificate: {self.participant.username} for {self.event.title}"

    @property
    def full_name_participant(self):
        return self.participant.name # Acessa o campo 'name' do modelo de usuário relacionado.


class UserRegisterManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail deve ser configurado')
        email = self.normalize_email(email) # Normaliza o endereço de e-mail (ex: transforma em minúsculas).
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # Criptografa e define a senha.
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True) # Define como True para acesso ao admin.
        extra_fields.setdefault('is_superuser', True) # Define como True para permissões totais.
        return self.create_user(username, email, password, **extra_fields)


class UserRegister(AbstractBaseUser):
    type_user_choices = [
        ('Estudante', 'Estudante'),
        ('Professor', 'Professor'),
        ('Organizador', 'Organizador'),
    ]
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    institution = models.CharField(max_length=150, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=type_user_choices, default ='Estudante', verbose_name="Tipo de Usuário") 
    image = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    
    USERNAME_FIELD = 'username' # Define 'username' como o campo usado para login.
    REQUIRED_FIELDS = ['email', 'name'] # Define os campos obrigatórios na criação de usuário (além de USERNAME_FIELD e password).
    
    objects = UserRegisterManager() # Associa o Manager customizado ao modelo.
    
    class Meta:
        db_table = 'user_register'
        ordering = ['username']
        verbose_name = 'Registro de Usuário'
        verbose_name_plural = 'Registros de Usuário' 
        
    def __str__(self):
        return self.username

    def get_full_name(self): # Método padrão do Django para obter o nome completo.
        name = getattr(self, 'name', None)
        if name:
            return name
        first = getattr(self, 'first_name', '') or ''
        last = getattr(self, 'last_name', '') or ''
        full = f"{first} {last}".strip()
        if full:
            return full
        return getattr(self, 'username', '') or ''


class Auditoria(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Usuário" 
    )
    action = models.CharField(max_length=255, verbose_name="Ação") 
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora") # Define que a data/hora é definida automaticamente na criação.

    class Meta:
        db_table = 'auditoria'
        verbose_name = "Auditoria" 
        verbose_name_plural = "Auditorias" 
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"