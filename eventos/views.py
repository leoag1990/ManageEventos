from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from eventos.forms import RegistroUsuarioForm, EventoForm
from eventos.models import Evento, Inscrito


class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'registro/registro.html'
    success_url = reverse_lazy('lista_cursos')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Se ha registrado exitosamente")
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'registro/login.html'
    success_url = reverse_lazy('lista_cursos')

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrecto. Vuelva a ingresar')
        return super().form_invalid(form)


class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        response = redirect('login')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class ListaEventosView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/nuevos_eventos.html'

    context_object_name = 'eventos'

    def get_queryset(self):
        return self.request.user.evento_creado.all()


class DetalleEventoView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'evento'


class FiltrarInscritoView(LoginRequiredMixin, DetailView):
    model = Inscrito
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'inscrito'


class InscribirEventoView(LoginRequiredMixin, DetailView):
    model = Inscrito

    def get(self, request, *args, **kwargs):
        evento = self.get_object()
        if request.user not in evento.usuario.all():
            evento.usuario.add(request.user)
            messages.success(request, f'Éxito al inscribirse en {evento.nombre}')
        else:
            messages.error(request, 'No se pudo realizar la inscripción. Ya está inscrito.')
        return redirect('detalle_evento', pk=evento.pk)


class CrearEventoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/eventos_form.html'
    success_url = reverse_lazy('nuevos_eventos')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'El curso se ha creado correctamente.')
        return response


class MisEventosView(LoginRequiredMixin, ListView):
    model = Inscrito
    template_name = 'eventos/nuevos_eventos.html'
    context_object_name = 'evento'

    def get_queryset(self):
        return Inscrito.objects.filter.all()
