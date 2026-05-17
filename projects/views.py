from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.dateparse import parse_date

from .models import Project
from .forms import ProjectForm
from timesheet.models import TimeEntry

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

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
        messages.success(self.request, "Új projekt sikeresen hozzáadva.")
        return super().form_valid(form)

class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        messages.success(self.request, "Projekt adatai sikeresen frissítve.")
        return super().form_valid(form)

class ProjectCloseView(StaffRequiredMixin, View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        end_date_str = request.POST.get('end_date')
        
        if not end_date_str:
            messages.error(request, "A lezárás dátuma kötelező!")
            return redirect('projects:list')
            
        end_date = parse_date(end_date_str)
        if not end_date:
            messages.error(request, "Érvénytelen dátum formátum!")
            return redirect('projects:list')
            
        # Ellenőrizzük, hogy van-e időkódolás a lezárás után
        future_entries = TimeEntry.objects.filter(project=project, date__gt=end_date)
        if future_entries.exists():
            messages.error(request, f"Nem zárhatod le a projektet {end_date} dátummal, mert van a projektnek későbbi jelenléti ív bejegyzése!")
            return redirect('projects:list')
            
        project.end_date = end_date
        project.is_active = False
        project.save()
        
        messages.success(request, f"A '{project.name}' projekt sikeresen lezárva ({end_date}).")
        return redirect('projects:list')
