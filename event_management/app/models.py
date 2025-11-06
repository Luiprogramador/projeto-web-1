from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.conf import settings 
import uuid
from datetime import date, datetime

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
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    image = models.ImageField(upload_to='eventos/', blank=True, null=True)
    initial_date = models.DateField(default= '9999-12-31', verbose_name="Data de Início")
    final_date = models.DateField(default='9999-12-31', verbose_name="Data Final")
    location = models.CharField(max_length=200, verbose_name="Local")
    max_capacity = models.IntegerField(verbose_name="Capacidade Máxima")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        related_name='created_events',
        null=True,
        blank=True,
        verbose_name="Criador"
    )
    event_type = models.CharField(max_length=20, choices=event_type_choices, default='Palestra', verbose_name="Tipo de Evento")
    event_start = models.TimeField(null=False, blank=True, verbose_name="Horario de Início") 
    event_end = models.TimeField(null=False, blank=True, verbose_name="Horario de Término")
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventParticipant',
        through_fields=('event', 'participant'), 
        related_name='attended_events',
        blank=True,
        verbose_name="Participantes"
    )
    
    class Meta:
        db_table = 'event'
        ordering = ['initial_date']
        verbose_name = 'Evento' # Português
        verbose_name_plural = 'Eventos' # Português
    
    def __str__(self):
        return self.title

    @property
    def calculated_duration_hours(self):
        # 1. Combina Data de Início e Hora de Início
        start_datetime = datetime.combine(self.initial_date, self.event_start)
        # 2. Combina Data Final e Hora de Término
        final_datetime = datetime.combine(self.final_date, self.event_end)
        
        # 3. Calcula a diferença (timedelta)
        duration = final_datetime - start_datetime
        
        return round(duration.total_seconds() / 3600, 1)

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
    
    event = models.ForeignKey(
        'Event', 
        on_delete=models.CASCADE, 
        related_name='certificates', 
        verbose_name="Evento" # Português
    )
    
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_certificates',
        verbose_name="Participante" # Português
    )
    
    issue_date = models.DateField( # Nome do campo em Inglês
        default=date.today, 
        verbose_name="Data de Emissão" # Português
    )
    
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
        verbose_name = 'Registro de Usuário'
        verbose_name_plural = 'Registros de Usuário' 
        
    def __str__(self):
        return self.username


