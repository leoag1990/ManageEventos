from django.urls import path
from .views import (
    RegistroUsuarioView, CustomLoginView, InscribirEventoView, CustomLogoutView, ListaEventosView, DetalleEventoView,
    CrearEventoView, MisEventosView
)

urlpatterns = [
    path('', ListaEventosView.as_view(), name='lista_cursos'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('curso/<int:pk>/', DetalleEventoView.as_view(), name='detalle_curso'),
    path('curso/crear/', CrearEventoView.as_view(), name='crear_cursos'),
    path('mis-cursos/', MisEventosView.as_view(), name='mis_cursos'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('curso/<int:pk>/inscribir/', InscribirEventoView.as_view(), name='inscribir_curso'),

]