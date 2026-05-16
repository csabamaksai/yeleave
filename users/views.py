from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserForm

User = get_user_model()

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        # We can list everyone, and indicate inactive.
        return User.objects.all().order_by('-is_active', 'last_name', 'first_name')

class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request, "Új dolgozó sikeresen hozzáadva.")
        return super().form_valid(form)

class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request, "Dolgozó adatai sikeresen frissítve.")
        return super().form_valid(form)

class UserDeleteView(StaffRequiredMixin, TemplateView):
    template_name = 'users/user_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        user_to_delete = get_object_or_404(User, pk=self.kwargs['pk'])
        
        # Admin megakadályozása, hogy önmagát törölje
        if user_to_delete == request.user:
            messages.error(request, "Saját magadat nem deaktiválhatod!")
            return redirect('users:update', pk=user_to_delete.pk)
        
        user_to_delete.is_active = False
        user_to_delete.save()
        messages.success(request, f"{user_to_delete.username} fiókja deaktiválva lett.")
        return redirect('users:list')

