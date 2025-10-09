from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.conf import settings 
import uuid
from datetime import date

# Create your models here.

class EventParticipant(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        db_column='user_id'
    ) 
    
    class Meta:
        unique_together = ('event', 'participant')


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
    title = models.CharField(max_length=200, verbose_name="Título") # Adicionado verbose_name
    description = models.TextField(verbose_name="Descrição") # Adicionado verbose_name
    initial_date = models.DateTimeField(default= '9999-12-31 00:00:00', verbose_name="Data de Início") # Adicionado verbose_name
    final_date = models.DateTimeField(default='9999-12-31 23:59:59', verbose_name="Data Final") # Adicionado verbose_name
    location = models.CharField(max_length=200, verbose_name="Local") # Adicionado verbose_name
    max_capacity = models.IntegerField(verbose_name="Capacidade Máxima") # Adicionado verbose_name
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        related_name='created_events', # Renomeado para Inglês
        null=True,
        blank=True,
        verbose_name="Criador" # Adicionado verbose_name
    )
    event_type = models.CharField(max_length=20, choices=event_type_choices, default='Palestra', verbose_name="Tipo de Evento") # Adicionado verbose_name
    # hours_event é misturado. Mude para event_duration ou similar.
    event_duration = models.TimeField(null=False, blank=True, default='00:00:00', verbose_name="Carga Horária") # Renomeado para Inglês e verbose_name em Português
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventParticipant',
        through_fields=('event', 'participant'), 
        related_name='attended_events', # Renomeado para Inglês
        blank=True,
        verbose_name="Participantes" # Adicionado verbose_name
    )
    
    class Meta:
        db_table = 'event'
        ordering = ['initial_date']
        verbose_name = 'Evento' # Português
        verbose_name_plural = 'Eventos' # Português
    
    def __str__(self):
        return self.title

    @property
    def current_participants_count(self):
        return self.participants.count()
    
    @property
    def is_full(self):
        return self.current_participants_count >= self.max_capacity

 
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
    
    # Links to the Event.
    event = models.ForeignKey(
        'Event', 
        on_delete=models.CASCADE, 
        related_name='certificates', 
        verbose_name="Evento" # Português
    )
    
    # Links to the User (Participant).
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_certificates',
        verbose_name="Participante" # Português
    )
    
    # Date the certificate was issued.
    issue_date = models.DateField( # Nome do campo em Inglês
        default=date.today, 
        verbose_name="Data de Emissão" # Português
    )
    
    # Unique and immutable UUID for verification.
    verification_code = models.UUIDField( # Nome do campo em Inglês
        default=uuid.uuid4, 
        unique=True, 
        editable=False, 
        verbose_name="Código de Verificação" # Português
    )

    class Meta:
        db_table = 'certificate'
        verbose_name = "Certificado" # Português
        verbose_name_plural = "Certificados" # Português
        # Ensure a participant only gets one certificate per event.
        unique_together = ('event', 'participant') 
        ordering = ['-issue_date']

    def __str__(self):
        return f"Certificate: {self.participant.username} for {self.event.title}"

    @property
    def full_name_participant(self): # Nome do método em Inglês
        return self.participant.name

class UserRegisterManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail deve ser configurado')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
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
    user_type = models.CharField(max_length=20, choices=type_user_choices, default='Estudante', verbose_name="Tipo de Usuário") 
    
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']
    
    objects = UserRegisterManager()
    
    class Meta:
        db_table = 'user_register'
        ordering = ['username']
        verbose_name = 'Registro de Usuário' # Português
        verbose_name_plural = 'Registros de Usuário' # Português
    def __str__(self):
        return self.username
