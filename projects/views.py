from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.utils.dateparse import parse_date

from .models import Project
from .forms import ProjectForm
from timesheet.models import TimeEntry

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (getattr(user, 'is_company_admin', False) or user.is_staff or user.is_superuser)

class ProjectListView(StaffRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_active=True).select_related('client')

class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        messages.success(self.request, _("Új projekt sikeresen hozzáadva."))
        return super().form_valid(form)

class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        messages.success(self.request, _("Projekt adatai sikeresen frissítve."))
        return super().form_valid(form)

class ProjectDeleteView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return render(request, 'projects/project_confirm_delete.html', {'target_project': project})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        project.is_active = False
        project.save()
        messages.success(request, _("A(z) '%(name)s' projekt sikeresen lezárva.") % {'name': project.name})
        return redirect('projects:list')
