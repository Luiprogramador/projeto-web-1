from django import forms
from .models import Event, EventRegister, UserRegister
from django.contrib.auth.forms import AuthenticationForm
<<<<<<< HEAD
from django.forms import ModelForm, SplitDateTimeWidget, DateInput, TimeInput, NumberInput
=======
from django.contrib.auth.hashers import make_password

>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
<<<<<<< HEAD
=======
# ...existing code...
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
    def save(self, commit=True):
        user = super().save(commit=False)
        # use set_password para manter a lógica do AbstractBaseUser
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
<<<<<<< HEAD
=======
# ...existing code...
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1


class EventForm(forms.ModelForm):
    initial_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        label="Data de Início" 
    )
    final_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        label="Data de Fim"
    )
    
    class Meta:
        model = Event
        fields = [
            'title', 
            'description', 
<<<<<<< HEAD
            'initial_date',
            'final_date',
            'location', 
            'max_capacity', 
            'event_type',
            'event_start',
            'event_end',
        ]
        widgets = {
            'initial_date': forms.SplitDateTimeWidget(
                date_attrs={'type': 'date'},
            ),
            'final_date': forms.SplitDateTimeWidget(
                date_attrs={'type': 'date'},
            ),
            'event_start': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'event_end': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'max_capacity': forms.NumberInput(
                attrs={'min': 1}
            ),
        }
        labels = {
            'title': 'Título do Evento',
            'description': 'Descrição do Evento',
            'initial_date': 'Data de Início',
            'final_date': 'Data de Fim',      
            'location': 'Local do Evento',
            'max_capacity': 'Capacidade Máxima',      
            'event_type': 'Tipo de Evento',          
            'event_start': 'Horário de Início',
            'event_end': 'Horário de Término',         
=======
            'initial_date',  # <-- Adicionado
            'final_date',    # <-- Adicionado
            'location', 
            'max_capacity', 
            'event_type',    # <-- Adicionado
            'hours_event'    # <-- Adicionado
        ]
        # 'creator' e 'participants' geralmente são gerenciados fora do formulário de criação (como no salvamento da view)
        
        labels = {
            'title': 'Título do Evento',
            'description': 'Descrição do Evento',
            'initial_date': 'Data e Hora de Início',
            'final_date': 'Data e Hora de Fim',      
            'location': 'Local do Evento',
            'max_capacity': 'Capacidade Máxima',      
            'event_type': 'Tipo de Evento',          
            'hours_event': 'Duração (Horas)',         
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
        }
        
        help_texts = {
            'title': 'Insira o título do evento.',
            'description': 'Insira uma breve descrição do evento.',
            'initial_date': 'Data e hora em que o evento começará.', 
            'final_date': 'Data e hora em que o evento terminará.',  
            'location': 'Insira o local onde o evento será realizado.',
            'max_capacity': 'O número máximo de participantes permitidos.', 
            'event_type': 'Selecione o tipo de evento.',                   
<<<<<<< HEAD
            'event_start': 'Horário de início do evento.',
            'event_end': 'Horário de término do evento.',
=======
            'hours_event': 'A duração total prevista para o evento (apenas horas:minutos:segundos).',
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
        }
        
        error_messages = {
            'title': {
                'max_length': 'O título é muito longo.',
                'required': 'O título é obrigatório.',
            },
            'description': {
                'required': 'A descrição é obrigatória.',
            },
            'initial_date': {
                'required': 'A data de início é obrigatória.',
                'invalid': 'Insira uma data e hora válidas para o início.',
            },
            'final_date': {
                'required': 'A data de fim é obrigatória.',
                'invalid': 'Insira uma data e hora válidas para o fim.',
            },
            'location': {
                'max_length': 'O local é muito longo.',
                'required': 'O local é obrigatório.',
            },
            'max_capacity': {
                'required': 'A capacidade máxima é obrigatória.',
                'invalid': 'Insira um número inteiro para a capacidade.',
            },
            'event_type': {
                'required': 'O tipo de evento é obrigatório.',
            },
<<<<<<< HEAD
            'event_start': {
                'invalid': 'Insira um formato de hora válido (HH:MM:SS).',
            },
            'event_end': {
=======
            'hours_event': {
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
                'invalid': 'Insira um formato de hora válido (HH:MM:SS).',
            },
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegister
        fields = ['event', 'name', 'email']
        labels = {
            'event': 'Event',
            'name': 'Your Name',
            'email': 'Your Email',
            
        }
        help_texts = {
            'event': 'Select the event you want to register for.',
            'name': 'Enter your full name.',
            'email': 'Enter your email address.',
        }
        error_messages = {
            'event': {
                'required': 'Event selection is required.',
            },
            'name': {
                'max_length': 'Name is too long.',
                'required': 'Name is required.',
            },
            'email': {
                'invalid': 'Enter a valid email address.',
                'required': 'Email is required.',
            },
        }


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        help_text='Obrigatório. Usado para comunicação e recuperação de conta.',
        # Exemplo de widget
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'})
    )
    
    password_confirm = forms.CharField(
        label='Confirmação de Senha',
        widget=forms.PasswordInput,
        help_text='Repita a senha para confirmação.'
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput
    )

    class Meta:

        model = UserRegister 
        
        fields = [
            'name', 
            'username', 
            'email', 
            'password',
            'phone', 
            'institution', 
<<<<<<< HEAD
            'user_type'
=======
            'type_user'
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
        ]
        
        labels = {
            'name': 'Nome Completo',
            'username': 'Nome de Usuário',
            'phone': 'Telefone',
            'institution': 'Instituição/Empresa',
<<<<<<< HEAD
            'user_type': 'Tipo de Usuário (Professor/Aluno)'
=======
            'type_user': 'Tipo de Usuário (Professor/Aluno)'
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
        }
        
        help_texts = {
            'username': 'Nome único que você usará para fazer login.',
            'phone': 'Opcional. Para contato de emergência ou recuperação de conta.',
            'institution': 'Opcional. Sua afiliação institucional/profissional.',
<<<<<<< HEAD
            'user_type': 'Marque se você for um Professor; desmarque para Aluno.'
=======
            'type_user': 'Marque se você for um Professor; desmarque para Aluno.'
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
        }
        
        error_messages = {
            'name': {
                'required': 'O nome completo é obrigatório para o registro.',
                'max_length': 'O nome não pode exceder 150 caracteres.',
            },
            'username': {
                'required': 'O nome de usuário é obrigatório.',
                'unique': 'Este nome de usuário já está em uso. Por favor, escolha outro.',
                'max_length': 'O nome de usuário não pode exceder 150 caracteres.',
            },
            'email': {
                'required': 'O e-mail é obrigatório.',
                'unique': 'Este e-mail já está cadastrado. Tente fazer login ou recuperar a senha.',
                'invalid': 'Insira um endereço de e-mail válido.',
            },
            'password': {
                'required': 'A senha é obrigatória.',
            },
            'phone': {
                'max_length': 'O telefone não pode exceder 20 caracteres.',
            },
            'institution': {
                'max_length': 'O nome da instituição não pode exceder 150 caracteres.',
            },
<<<<<<< HEAD
            'user_type': {
=======
            'type_user': {
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
                'required': 'O tipo de usuário (Professor/Aluno) é obrigatório.',
            }
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # use set_password para manter a lógica do AbstractBaseUser
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "As senhas não coincidem."
            )
<<<<<<< HEAD
        return cleaned_data
    
=======
        return cleaned_data
>>>>>>> 5a96fedf93e6b0de9087d57868d0edb4fd6311c1
