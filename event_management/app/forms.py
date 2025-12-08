from django.contrib.auth.forms import AuthenticationForm
from .models import Event, EventRegister, UserRegister
from django.contrib.auth import get_user_model
from django import forms
import datetime

User = get_user_model() # Obtém o modelo de usuário ativo configurado no Django

# Formulário de login personalizado que herda do formulário de autenticação padrão do Django
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Formulário para criação ou edição de um Evento
class EventForm(forms.ModelForm):  
    class Meta:
        model = Event # Define o modelo associado
        fields = [ # Define os campos do modelo que serão usados no formulário
            'title',
            'description',
            'initial_date',
            'final_date',
            'event_start',
            'event_end',
            'location',
            'max_capacity',
            'image',
            'event_type',
            'professor',
        ]
        
        widgets = { # Configuração de widgets HTML para campos específicos
            'initial_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    # Define a data mínima permitida como a data de hoje
                    'min': datetime.date.today().strftime('%d-%m-%Y')
                }
            ),
            'final_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'event_start': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'event_end': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o título do evento'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite a descrição do evento'
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o local do evento'
                }
            ),
            'max_capacity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1'
                }
            ),
            'event_type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file'
                }
            ),
        }

    # Sobrescreve o método clean para adicionar validações personalizadas
    def clean(self):
        cleaned = super().clean()
        inicial = cleaned.get('initial_date')
        final = cleaned.get('final_date')
        hoje = datetime.date.today()

        # Valida se a data inicial não é anterior à data de hoje
        if inicial and inicial < hoje:
            raise forms.ValidationError("A data inicial não pode ser anterior a hoje.")

        # Valida se a data final não é anterior à data inicial
        if inicial and final and final < inicial:
            raise forms.ValidationError("A data final não pode ser anterior à data inicial.")

        return cleaned

# Formulário para registro em um Evento
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegister # Define o modelo de registro de evento
        fields = ['event', 'name', 'email']
        labels = { # Rótulos personalizados para os campos
            'event': 'Event',
            'name': 'Your Name',
            'email': 'Your Email',
            
        }
        help_texts = { # Textos de ajuda para os campos
            'event': 'Select the event you want to register for.',
            'name': 'Enter your full name.',
            'email': 'Enter your email address.',
        }
        error_messages = { # Mensagens de erro personalizadas por campo
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

# Formulário de registro de novo Usuário
class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField( # Redefine o campo email com configurações específicas
        label='E-mail',
        required=True,
        help_text='Obrigatório. Usado para comunicação e recuperação de conta.',
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'})
    )
    
    # Define o campo phone com um widget de entrada de texto e máscara de dados para o formato de telefone
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '(99) 99999-9999', 'data-mask': '(00) 00000-0000'}))

    # Campo extra para confirmação de senha, que não está no modelo UserRegister
    password_confirm = forms.CharField(
        label='Confirmação de Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Djgh@1234'}),
        help_text='Repita a senha para confirmação.',
    )
    
    # Redefine o campo password com um widget PasswordInput
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Djgh@1234'})
    )

    class Meta:

        model = UserRegister # Modelo de usuário personalizado
        
        fields = [ # Campos do formulário
            'name', 
            'username', 
            'email', 
            'password',
            'phone', 
            'institution', 
            'user_type'
        ]
        
        labels = { # Rótulos personalizados
            'name': 'Nome Completo',
            'username': 'Nome de Usuário',
            'phone': 'Telefone',
            'institution': 'Instituição/Empresa',
            'user_type': 'Tipo de Usuário (Professor/Aluno)'
        }
        
        help_texts = { # Textos de ajuda
            'username': 'Nome único que você usará para fazer login.',
            'phone': 'Opcional. Para contato de emergência ou recuperação de conta.',
            'institution': 'Opcional. Sua afiliação institucional/profissional.',
            'user_type': 'Marque se você for um Professor; desmarque para Aluno.'
        }
        
        error_messages = { # Mensagens de erro personalizadas
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
                'help_text': 'A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.'
            },
            'phone': {
                'max_length': 'O telefone não pode exceder 20 caracteres.',
            },
            'institution': {
                'max_length': 'O nome da instituição não pode exceder 150 caracteres.',
            },
            'user_type': {
                'required': 'O tipo de usuário (Professor/Aluno) é obrigatório.',
            }
        }
    
    # Sobrescreve o save para aplicar hash na senha antes de salvar o usuário
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Aplica hash na senha
        if commit:
            user.save()
        return user
    
    # Método clean para validação do formulário, incluindo validações de senha
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        username = cleaned_data.get('username')

        # Verifica se as senhas coincidem
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")

        # Adiciona várias regras de validação de força da senha
        if password:
            if len(password) < 8:
                self.add_error('password', "A senha deve ter pelo menos 8 caracteres.")
            if not any(char.isdigit() for char in password):
                self.add_error('password', "A senha deve conter pelo menos um número.")
            if not any(char.isalpha() for char in password):
                self.add_error('password', "A senha deve conter pelo menos uma letra.")
            if password.islower():
                self.add_error('password', "A senha deve conter pelo menos uma letra maiúscula.")
            if password.isupper():
                self.add_error('password', "A senha deve conter pelo menos uma letra minúscula.")
            
            # Verifica se há pelo menos um caractere especial
            if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
                self.add_error('password', "A senha deve conter pelo menos um caractere especial.")
            if ' ' in password:
                self.add_error('password', "A senha não pode conter espaços.")
            
            # Verifica senhas comuns/fracas
            if password.lower() in ['senha', '12345678', 'qwerty', 'abcdefg']:
                self.add_error('password', "A senha é muito comum. Por favor, escolha uma senha mais forte.")
            
            # Verifica se a senha contém o nome de usuário
            if username and username.lower() in password.lower():
                self.add_error('password', "A senha não pode conter o nome de usuário.")

        return cleaned_data

class OrganizerUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Senha Inicial', widget=forms.PasswordInput)
    
    class Meta:
        model = UserRegister
        fields = ['name', 'username', 'email', 'password', 'phone', 'institution', 'user_type']
        labels = {
            'name': 'Nome Completo',
            'username': 'Usuário (Login)',
            'institution': 'Instituição',
            'user_type': 'Tipo de Usuário',
            'phone': 'Telefone'
        }
        widgets = {
            'phone': forms.TextInput(attrs={'data-mask': '(00) 00000-0000', 'placeholder': '(99) 99999-9999'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Formulário para edição do perfil do usuário
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User # Utiliza o modelo de usuário ativo
        fields = [ # Campos permitidos para edição no perfil
            'name',
            'email',
            'phone',
            'institution',
            'image',
            'user_type',
        ]
        widgets = { # Configuração de widgets de formulário com classes CSS
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': '(99) 99999-9999', 'data-mask': '(00) 00000-0000'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }