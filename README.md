# Event Manager - Sistema de Gerenciamento de Eventos

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)

## 📋 Sobre o Projeto

O **Event Management** é um sistema de gerenciamento de eventos desenvolvido em Django. A aplicação permite criar, organizar e gerenciar eventos de forma simples e eficiente.

## Preview do site
um preview da página inicial do projeto

<img width="1919" height="1018" alt="Captura de tela 2025-10-09 205124" src="https://github.com/user-attachments/assets/5915ac25-276c-4bcc-92bd-19a78e871cb8" />

## ✨ Funcionalidades

### 🎯 Para Organizadores
- **Criação e edição de eventos** com informações básicas
- **Gestão de participantes** e inscrições
- **Visualização** de eventos criados
- **Controle básico** de informações do evento

### 👥 Para Participantes
- **Visualização** de eventos disponíveis
- **Sistema de inscrição** em eventos
- **Área do participante** com eventos confirmados
- **Cancelamento** de inscrição

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django 4.2+
- **Frontend:** HTML5, CSS3
- **Banco de Dados:** SQLite
- **Autenticação:** Sistema de autenticação do Django

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 📥 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/event-manager.git
cd event-manager
```

2. **Instale as dependências do Django**
```bash
pip install Django
```

3. **Execute as migrações**
```bash
python manage.py migrate
```

4. **Crie um superusuário(Opicional)**
```bash
python manage.py createsuperuser
```

5. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

O projeto estará disponível em `http://localhost:8000`

## 🗂️ Estrutura do Projeto

```
event_management/
├── app/            # App principal de eventos
├── event_management/    # Configurações do projeto
└── staticfiles/           # Arquivos estáticos 
```

## 📊 Modelos Principais

### Event
- `id` - Id do evento
- `title` - Título do evento
- `description` - Descrição do evento
- `location` - Local do evento
- `max_capacity` - capacidade máxima do evento
- `created_id` - Id do organizador do evento
- `inicial_date` - Data de início do evento
- `final_date` - Data final do evento
- `event_end` - Hora final do evento
- `event_start` - Hora inicial do evento
  
### User
- `id` - Id do usuário
- `name` - Nome real do usuário
- `username` - Apelido do usuário
- `email` - Email do usuário
- `password` - Senha do usuário
- `phone` - Telefone do usuário
- `institution` - Instituição de ensino do usuário
- `last_login` - Hora do último acesso
- `user_type` - Tipo do usuário('estudante', 'professor', 'organizador'

  
## 🔧 Funcionalidades Implementadas

### Páginas Principais
- **Página inicial**: Lista de eventos disponíveis
- **Login/Registro**: Sistema de autenticação
- **Criar evento**: Formulário para criação de novos eventos
- **Meus eventos**: Eventos criados pelo usuário logado
- **Minhas inscrições**: Eventos onde o usuário está inscrito

### Fluxo do Usuário
1. **Cadastro/Login** no sistema
2. **Visualizar** eventos disponíveis na página inicial
3. **Criar** eventos (se organizador)
4. **Inscrever-se** em eventos de interesse
5. **Gerenciar** próprios eventos e inscrições

## 🧪 Comandos Úteis

### Criar migrações
```bash
python manage.py makemigrations
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Desenvolvedores

- **Lui Mendes** - [luiprogramador@gmail.com](mailto:luiprogramador@gmail.com)
- **Alejandro Reyes** - [alejandro.reyesd.dev@gmail.com](mailto:alejandro.reyes.dev@gmail.com)

---

**Event Management** - Gerencie seus eventos de forma simples! 🎉
