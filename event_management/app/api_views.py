# inicio/api_views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

# Importa de seus arquivos existentes
from .models import Event, EventParticipant
from .serializers import EventSerializer, EventParticipantSerializer

# 3.1. Consulta de Eventos
class EventListAPIView(generics.ListAPIView):
    """
    Endpoint para listar todos os eventos.
    """
    queryset = Event.objects.all().select_related('creator')
    serializer_class = EventSerializer
    
    # Permissão e Throttling (já definidos globalmente, mas bom ser explícito)
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle] 
    
    # Conecta esta view ao escopo 'eventos' (20/dia) do settings.py
    throttle_scope = 'eventos'

# 3.2. Inscrição de Participantes
class EventSubscriptionCreateAPIView(generics.CreateAPIView):
    """
    Endpoint para um usuário se inscrever em um evento.
    """
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    
    # Permissão e Throttling
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    # Conecta esta view ao escopo 'inscricoes' (50/dia) do settings.py
    throttle_scope = 'inscricoes'
    
    # O Serializer (EventParticipantSerializer) já cuida de:
    # 1. Pegar o usuário logado (CurrentUserDefault)
    # 2. Validar se o evento está lotado (validate_event)
    # 3. Validar se o usuário já está inscrito (validate)