from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Client
from .forms import ClientForm
from .hungarian_cities import HUNGARIAN_CITIES

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class ClientListView(StaffRequiredMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.filter(is_active=True)

class ClientCreateView(StaffRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = HUNGARIAN_CITIES
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Új ügyfél sikeresen hozzáadva."))
        return super().form_valid(form)

class ClientUpdateView(StaffRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = HUNGARIAN_CITIES
        return context

    def form_valid(self, form):
        messages.success(self.request, _("Ügyfél adatai sikeresen frissítve."))
        return super().form_valid(form)

class ClientDeleteView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return render(request, 'clients/client_confirm_delete.html', {'target_client': client})

    def post(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        client.is_active = False
        client.save()
        
        # Kapcsolódó aktív projektek deaktiválása
        for project in client.projects.filter(is_active=True):
            project.is_active = False
            project.save()
            
        messages.success(request, _("%(name)s ügyfél és a hozzá tartozó projektek deaktiválva lettek.") % {'name': client.name})
        return redirect('clients:list')
