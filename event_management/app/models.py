from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.conf import settings 
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
    title = models.CharField(max_length=200)
    description = models.TextField()
    initial_date = models.DateTimeField(default= '9999-12-31 00:00:00')
    final_date = models.DateTimeField(default='9999-12-31 23:59:59')
    location = models.CharField(max_length=200)
    max_capacity = models.IntegerField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE, 
        related_name='eventos_criados',
        null=True,
        blank=True
    )
    event_type = models.CharField(max_length=20, choices=event_type_choices, default='Palestra')
    hours_event = models.TimeField(null=False, blank=True, default='00:00:00')
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='EventParticipant',
        through_fields=('event', 'participant'), 
        related_name='eventos_participados', 
        blank=True 
    )
    
    class Meta:
        db_table = 'event'
        ordering = ['initial_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
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
    type_user = models.CharField(max_length=20, choices=type_user_choices, default='Estudante')
    
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']
    
    objects = UserRegisterManager()
    
    class Meta:
        db_table = 'user_register'
        ordering = ['username']
        verbose_name = 'User Register'
        verbose_name_plural = 'User Registers'

    def __str__(self):
        return self.username
