from django.db import models
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'event'
        ordering = ['date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

class login(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'login'
        ordering = ['username']
        verbose_name = 'Login'
        verbose_name_plural = 'Logins'
    def __str__(self):
        return self.username
    
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    class Meta:
        db_table = 'registration'
        ordering = ['name']
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class register(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'register'
        ordering = ['username']
        verbose_name = 'Register'
        verbose_name_plural = 'Registers'

    def __str__(self):
        return self.username
