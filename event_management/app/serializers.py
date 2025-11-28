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
        fields = ['id', 'username', 'name', 'email', 'user_type']


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer para o Endpoint 3.1: Consulta de Eventos.
    """
    creator = UserRegisterSerializer(read_only=True) # Usa o serializer de UserRegister para aninhar os detalhes do criador.
    
    nome = serializers.CharField(source='title') # Mapeia o campo 'title' do modelo para o nome 'nome' na API.
    data = serializers.DateField(source='initial_date') # Mapeia 'initial_date' para 'data'.
    local = serializers.CharField(source='location') # Mapeia 'location' para 'local'.
    organizador_responsavel = serializers.CharField(source='creator.name', read_only=True) # Acessa o campo 'name' do objeto 'creator' (relacionamento).

    class Meta:
        model = Event
        fields = [
            'id', 
            'nome',
            'data',
            'local',
            'organizador_responsavel',
            'creator'
        ]


class EventParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer para o Endpoint 3.2: Inscrição de Participantes.
    Baseado no seu modelo 'EventParticipant'.
    """
    
    participant = serializers.HiddenField(
        default=serializers.CurrentUserDefault() # Define automaticamente o participante como o usuário logado (requer autenticação).
    )
    
    class Meta:
        model = EventParticipant
        fields = ['id', 'event', 'participant']

    def validate_event(self, event):
        """
        Validação: Verifica se o evento está lotado antes de permitir a inscrição.
        """
        if event.is_full: # Acessa a propriedade `is_full` do objeto Event.
            raise ValidationError(
                f'O evento "{event.title}" está lotado (Capacidade Máxima: {event.max_capacity}).'
            )
        return event

    def validate(self, data):
        """
        Validação: Verifica se o usuário já está inscrito.
        """
        event = data.get('event')
        participant = self.context['request'].user # Obtém o usuário logado a partir do contexto da requisição.
        
        if EventParticipant.objects.filter(event=event, participant=participant).exists(): # Verifica a existência de um registro EventParticipant.
            raise ValidationError(f'Você já está inscrito no evento "{event.title}".')
            
        return data

    def create(self, validated_data):
        return EventParticipant.objects.create(**validated_data) # Cria o registro de inscrição.