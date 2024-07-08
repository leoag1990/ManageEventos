from . import views
from django.urls import path
from .views import (
    RegistroUsuarioView, CustomLoginView, CustomLogoutView, ListaEventosView, DetalleEventoView,
    CrearEventoView, MisEventosView, FiltrarInscritoView, InscribirCursoView
)

urlpatterns = [
    path('', ListaEventosView.as_view(), name='lista_eventos'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('evento/<int:pk>/', DetalleEventoView.as_view(), name='detalle_evento'),
    path('evento/crear/', CrearEventoView.as_view(), name='crear_eventos'),
    path('mis-eventos/', MisEventosView.as_view(), name='mis_eventos'),
    path('eventos-inscritos/', FiltrarInscritoView.as_view(), name='eventos_inscritos'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('evento/<int:pk>/inscribir/', InscribirCursoView.as_view(), name='inscribir_evento'),
]
