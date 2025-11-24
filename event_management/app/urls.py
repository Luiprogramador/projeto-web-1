# inicio/urls.py
from rest_framework.authtoken import views as authtoken_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import api_views
from . import views

urlpatterns = [
path('', views.home, name='home'),
path('base/', views.base, name='base'),

# event urls
path('event/', views.event_list, name='event_list'),
path('event/new/', views.add_event, name='add_event'),
path('event/<int:pk>/remove/', views.remove_event, name='remove_event'),
path('evento/<int:pk>/toggle_registration/', views.toggle_registration, name='toggle_registration'),
path('meus-event_subscribed/subscribed/', views.event_subscribed, name='event_subscribed'),
path('evento/<int:pk>/', views.event_detail, name='event_detail'), 
path('event/<int:event_id>/certificate/', views.issue_certificate, name='issue_certificate'), 
path('eventos/editar/<int:pk>/', views.event_edit, name='event_edit'),

# certificates urls
path('certificates/', views.certificate_list, name='certificate_list'),

# user urls
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'), 
path('register/', views.register_view, name='register'),
path('perfil/', views.perfil, name='perfil'),
path('perfil/editar/', views.perfil_edicao, name='perfil_edicao'),

# auditorial urls
path('auditorial/', views.auditorial, name='auditorial'),

# api urls
path('api/token-auth/', authtoken_views.obtain_auth_token, name='api_token_auth'),
path('api/eventos/', api_views.EventListAPIView.as_view(), name='api_event_list'),
path('api/inscricoes/', api_views.EventSubscriptionCreateAPIView.as_view(), name='api_subscription_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)