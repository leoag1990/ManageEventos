from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from eventos.forms import RegistroUsuarioForm, EventoForm
from eventos.models import Evento, Inscrito


class RegistroUsuarioView(CreateView):
    form_class = RegistroUsuarioForm
    template_name = 'registro/registro.html'
    success_url = reverse_lazy('lista_eventos')

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
    success_url = reverse_lazy('lista_eventos')

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

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class DetalleEventoView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'evento'


class InscribirCursoView(LoginRequiredMixin, DetailView):
    model = Inscrito

    def get(self, request, *args, **kwargs):
        id_evento = Evento.objects.get(id=kwargs['pk'])
        Inscrito.objects.create(evento=id_evento, usuario=request.user)
        return redirect('lista_eventos')


class CrearEventoView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/eventos_form.html'
    context_object_name = 'evento'
    success_url = reverse_lazy('lista_eventos')

    def form_valid(self, form):
        formulario = form.save(commit=False)
        formulario.usuario_creador = self.request.user
        formulario.save()
        response = super().form_valid(form)
        messages.success(self.request, 'El curso se ha creado correctamente.')
        return response


class MisEventosView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/nuevos_eventos.html'
    context_object_name = 'eventos'

    def get_queryset(self):
        return self.request.user.evento_creado.all()


class FiltrarInscritoView(LoginRequiredMixin, DetailView):
    model = Inscrito
    template_name = 'eventos/eventos_inscritos.html'
    context_object_name = 'inscrito'

    def get_queryset(self):
        inscrito = self.request.user.usuario_id.all()
        return Evento.objects.filter(evento=inscrito.evento)


def mostrar_asistentes(request, id_evento):
    evento = get_object_or_404(Evento, id=id_evento)
    asistentes = evento.evento_id.all()  # trae los asistentes con en el evento con id que se pasa por get
    return render(request, 'eventos/mostrar_asistentes.html', {'event': evento, 'attendees': asistentes})