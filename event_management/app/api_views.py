from .serializers import EventSerializer, EventParticipantSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import Event, EventParticipant, UserRegister
from rest_framework import generics

# View para listar todos os eventos (herda de ListAPIView do DRF)
class EventListAPIView(generics.ListAPIView):
    """
    Endpoint para listar todos os eventos.
    """
    
    # Define o conjunto de consultas que a view deve retornar
    queryset = Event.objects.all().select_related('creator') 
    serializer_class = EventSerializer # Define qual serializador será usado para formatar os dados
    
    # Define que apenas usuários autenticados podem acessar este endpoint
    permission_classes = [IsAuthenticated] 
    
    # Define a classe de limitação de taxa a ser aplicada
    throttle_classes = [UserRateThrottle] 
    
    # Define o escopo de limitação de taxa
    throttle_scope = 'eventos' 

# View para um usuário se inscrever em um evento
class EventSubscriptionCreateAPIView(generics.CreateAPIView):
    """
    Endpoint para um usuário se inscrever em um evento.
    """
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    
    # Define que apenas usuários autenticados podem criar inscrições
    permission_classes = [IsAuthenticated and UserRegister.user_type != "Organizador"] 
    throttle_classes = [UserRateThrottle]
    
    # Define o escopo de limitação de taxa para inscrições
    throttle_scope = 'inscricoes'