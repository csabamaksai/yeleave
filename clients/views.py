from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
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
        messages.success(self.request, "Új ügyfél sikeresen hozzáadva.")
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
        messages.success(self.request, "Ügyfél adatai sikeresen frissítve.")
        return super().form_valid(form)
