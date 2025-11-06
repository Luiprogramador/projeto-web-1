# inicio/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Event, EventParticipant, UserRegister

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer simples para mostrar dados do organizador (criador do evento).
    """
    class Meta:
        model = UserRegister
        # Informações públicas do organizador
        fields = ['id', 'username', 'name', 'email', 'user_type']


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer para o Endpoint 3.1: Consulta de Eventos.
    """
    # Usa o serializer acima para mostrar detalhes do organizador (creator)
    creator = UserRegisterSerializer(read_only=True)
    
    # Renomeia 'title' para 'nome' no JSON de saída
    nome = serializers.CharField(source='title')
    data = serializers.DateField(source='initial_date')
    local = serializers.CharField(source='location')
    organizador_responsavel = serializers.CharField(source='creator.name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 
            'nome',       # 'title' no modelo
            'data',       # 'initial_date' no modelo
            'local',      # 'location' no modelo
            'organizador_responsavel', # 'creator.name' no modelo
            'creator'     # Objeto aninhado completo (opcional, mas útil)
        ]


class EventParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer para o Endpoint 3.2: Inscrição de Participantes.
    Baseado no seu modelo 'EventParticipant'.
    """
    
    # Pega o usuário logado (pelo token) e o define como participante
    participant = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = EventParticipant
        fields = ['id', 'event', 'participant'] # 'event' será o ID do evento

    def validate_event(self, event):
        """
        Validação: Verifica se o evento está lotado antes de permitir a inscrição.
        """
        if event.is_full:
            raise ValidationError(
                f'O evento "{event.title}" está lotado (Capacidade Máxima: {event.max_capacity}).'
            )
        return event

    def validate(self, data):
        """
        Validação: Verifica se o usuário já está inscrito.
        """
        event = data.get('event')
        participant = self.context['request'].user # Pega o usuário da requisição
        
        if EventParticipant.objects.filter(event=event, participant=participant).exists():
            raise ValidationError(f'Você já está inscrito no evento "{event.title}".')
            
        return data

    def create(self, validated_data):
        # A lógica de validação já foi executada
        return EventParticipant.objects.create(**validated_data)