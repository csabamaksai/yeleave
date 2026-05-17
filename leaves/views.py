from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import datetime

from .models import Leave
from .forms import LeaveForm
from timesheet.models import TimeEntry

class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'leaves/leave_list.html'
    context_object_name = 'leaves'

    def get_queryset(self):
        year = self.request.GET.get('year', datetime.date.today().year)
        try:
            year = int(year)
        except ValueError:
            year = datetime.date.today().year
        return Leave.objects.filter(user=self.request.user, start_date__year=year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get('year', datetime.date.today().year)
        try:
            year = int(year)
        except ValueError:
            year = datetime.date.today().year
            
        context['current_year'] = year
        context['prev_year'] = year - 1
        context['next_year'] = year + 1
        
        # Opcionálisan: összes kivett nap számítása (nagyon faék egyszerűséggel, ahol start és end közti napok száma van)
        # Bonyolultabb esetben munkanapokat kéne számolni, de egyelőre simán sumoljuk
        total_days = 0
        for leave in context['leaves']:
            # Használjuk a modell get_working_days() metódusát a tényleges munkanapok számításához
            total_days += leave.get_working_days()
        context['total_days'] = total_days

        return context


class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leaves:list')

    def get_initial(self):
        initial = super().get_initial()
        today = datetime.date.today().strftime('%Y-%m-%d')
        initial['start_date'] = today
        initial['end_date'] = today
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Ha 'force_save' érkezett, töröljük a TS rekordokat
        if self.request.POST.get('force_save') == 'true':
            TimeEntry.objects.filter(
                user=self.request.user,
                date__gte=form.instance.start_date,
                date__lte=form.instance.end_date
            ).delete()
            messages.warning(self.request, _('A szabadság mentve, a rajta lévő korábbi munkaidő bejegyzések törlésre kerültek.'))
        else:
            messages.success(self.request, _('A szabadság sikeresen létrehozva.'))
            
        return response


class LeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leaves:list')

    def get_queryset(self):
        return Leave.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Ha 'force_save' érkezett, töröljük a TS rekordokat
        if self.request.POST.get('force_save') == 'true':
            TimeEntry.objects.filter(
                user=self.request.user,
                date__gte=form.instance.start_date,
                date__lte=form.instance.end_date
            ).delete()
            messages.warning(self.request, _('A szabadság módosítva, a rajta lévő korábbi munkaidő bejegyzések törlésre kerültek.'))
        else:
            messages.success(self.request, _('A szabadság sikeresen frissítve.'))
            
        return response


class LeaveDeleteView(LoginRequiredMixin, DeleteView):
    model = Leave
    template_name = 'leaves/leave_confirm_delete.html'
    success_url = reverse_lazy('leaves:list')

    def get_queryset(self):
        return Leave.objects.filter(user=self.request.user)
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, _('A szabadság bejegyzést töröltük.'))
        return super().delete(request, *args, **kwargs)


@login_required
def api_check_ts_collision(request):
    start_str = request.GET.get('start_date')
    end_str = request.GET.get('end_date')
    
    if not start_str or not end_str:
        return JsonResponse({'collision': False})
        
    try:
        start_date = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'collision': False})
        
    count = TimeEntry.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).count()
    
    return JsonResponse({
        'collision': count > 0,
        'count': count
    })
