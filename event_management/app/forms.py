from django import forms
from .models import Event, EventRegister, UserRegister
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class EventForm(forms.ModelForm):   
    class Meta:
        model = Event
        fields = [
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
        ]
        
        widgets = {
            # Campos de data
            'initial_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': datetime.date.today().strftime('%d-%m-%Y')
                }
            ),
            'final_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            # Campos de hora
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
            # Outros campos
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

    def clean(self):
        cleaned = super().clean()
        inicial = cleaned.get('initial_date')
        final = cleaned.get('final_date')
        hoje = datetime.date.today()

        if inicial and inicial < hoje:
            raise forms.ValidationError("A data inicial não pode ser anterior a hoje.")

        if inicial and final and final < inicial:
            raise forms.ValidationError("A data final não pode ser anterior à data inicial.")

        return cleaned

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
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'})
    )
    
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '(99) 99999-9999', 'data-mask': '(00) 00000-0000'}))

    password_confirm = forms.CharField(
        label='Confirmação de Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Djgh@1234'}),
        help_text='Repita a senha para confirmação.',
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Djgh@1234'})
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
            'user_type'
        ]
        
        labels = {
            'name': 'Nome Completo',
            'username': 'Nome de Usuário',
            'phone': 'Telefone',
            'institution': 'Instituição/Empresa',
            'user_type': 'Tipo de Usuário (Professor/Aluno)'
        }
        
        help_texts = {
            'username': 'Nome único que você usará para fazer login.',
            'phone': 'Opcional. Para contato de emergência ou recuperação de conta.',
            'institution': 'Opcional. Sua afiliação institucional/profissional.',
            'user_type': 'Marque se você for um Professor; desmarque para Aluno.'
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        username = cleaned_data.get('username')

        # Limpa erros anteriores deste formulário (se houver)
        # (Django já lida com isso, mas mantemos para clareza)
        
        # Verifica confirmação
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")

        # Regras de força da senha (cada uma gera erro no campo 'password')
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
            if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
                self.add_error('password', "A senha deve conter pelo menos um caractere especial.")
            if ' ' in password:
                self.add_error('password', "A senha não pode conter espaços.")
            if password.lower() in ['senha', '12345678', 'qwerty', 'abcdefg']:
                self.add_error('password', "A senha é muito comum. Por favor, escolha uma senha mais forte.")
            if username and username.lower() in password.lower():
                self.add_error('password', "A senha não pode conter o nome de usuário.")

        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'phone',
            'institution',
            'image',
            'user_type',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
