# inicio/urls.py
from django.urls import path
from . import views
urlpatterns = [
path('', views.home, name='home'),
# outras rotas podem ser adicionadas aqui
path('base/', views.base, name='base'),
path('event/', views.event_list, name='event_list'),
path('event/new/', views.add_event, name='add_event'),
path('event/<int:pk>/remove/', views.remove_event, name='remove_event'),
path('evento/<int:pk>/toggle_registration/', views.toggle_registration, name='toggle_registration'),
path('meus-event_subscribed/subscribed/', views.event_subscribed, name='event_subscribed'),
path('evento/<int:pk>/', views.event_detail, name='event_detail'), 
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'), 
path('register/', views.register_view, name='register'),
]