from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import re
from calendar import monthrange
from datetime import date, datetime
from .models import TimeEntry
from projects.models import Project

def format_hours(decimal_hours):
    if not decimal_hours:
        return ""
    h = int(decimal_hours)
    m = int(round((float(decimal_hours) - h) * 60))
    if m == 0:
        return f"{h}ó"
    elif h == 0:
        return f"{m}p"
    return f"{h}ó {m}p"

def parse_hours(val_str):
    val = val_str.strip().lower()
    if not val:
        return 0.0
    
    # Próbáljuk "7ó 40p" / "8ó" formátumból
    m_match = re.match(r'^(\d+)\s*(?:ó|o|h)\s*(?:(\d+)\s*(?:p|m)?)?$', val)
    if m_match:
        h = int(m_match.group(1))
        m_val = int(m_match.group(2)) if m_match.group(2) else 0
        return h + (m_val / 60.0)
    
    # Ha "p" vagy "m" re végződik, pl. 40p
    m_only = re.match(r'^(\d+)\s*(?:p|m)$', val)
    if m_only:
        return int(m_only.group(1)) / 60.0

    val = val.replace(',', '.')
    if ':' in val:
        parts = val.split(':')
        h = float(parts[0]) if parts[0] else 0.0
        m_val = float(parts[1]) if len(parts) > 1 and parts[1] else 0.0
        return h + (m_val / 60.0)

    try:
        return float(val)
    except ValueError:
        return 0.0

def get_prev_and_next_month(year, month):
    if month == 1:
        prev_month_date = date(year - 1, 12, 1)
        next_month_date = date(year, 2, 1)
    elif month == 12:
        prev_month_date = date(year, 11, 1)
        next_month_date = date(year + 1, 1, 1)
    else:
        prev_month_date = date(year, month - 1, 1)
        next_month_date = date(year, month + 1, 1)
    return prev_month_date, next_month_date

@login_required
def timesheet_view(request):
    try:
        year = int(request.GET.get('year', date.today().year))
        month = int(request.GET.get('month', date.today().month))
    except ValueError:
        year, month = date.today().year, date.today().month

    current_date = date(year, month, 1)
    prev_month, next_month = get_prev_and_next_month(year, month)

    # Naptári napok kiszámítása az adott hónapban
    _, num_days = monthrange(year, month)
    days_in_month = []
    for day in range(1, num_days + 1):
        day_date = date(year, month, day)
        days_in_month.append({
            'date': day_date,
            'day': day,
            'is_weekend': day_date.weekday() >= 5, # 5=Sat, 6=Sun
            'weekday_name': day_date.strftime('%a')[:2] # Rövidített nap név, pl. Mo, Tu
        })

    # Felhasználóhoz rendelt projektek lekérdezése
    projects = request.user.assigned_projects.filter(is_active=True).select_related('client')
    
    # E havi mentett bejegyzések
    entries = TimeEntry.objects.filter(
        user=request.user,
        date__year=year,
        date__month=month
    )
    
    # Szótárat építünk a gyors kereséshez: (project_id, dátum_string) -> float hours
    entry_dict = {(e.project_id, str(e.date)): float(e.hours) for e in entries}

    # Sorok előkészítése a template-hez
    project_rows = []
    for project in projects:
        row_days = []
        for d in days_in_month:
            date_str = str(d['date'])
            hours_decimal = entry_dict.get((project.id, date_str), 0)
            hours_formatted = format_hours(hours_decimal) if hours_decimal > 0 else ''
            
            row_days.append({
                'date_str': date_str,
                'hours_formatted': hours_formatted,
                'hours_decimal': hours_decimal,
                'is_weekend': d['is_weekend']
            })
        project_rows.append({
            'project': project,
            'client_name': project.client.name,
            'days': row_days
        })

    return render(request, 'timesheet/index.html', {
        'current_date': current_date,
        'prev_month': prev_month,
        'next_month': next_month,
        'days_in_month': days_in_month,
        'project_rows': project_rows,
    })

@login_required
@require_POST
def save_time_entry(request):
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        entry_date_str = data.get('date')
        hours_str = data.get('hours')
        
        project = Project.objects.filter(id=project_id, assigned_users=request.user).first()
        if not project:
            return JsonResponse({'status': 'error', 'message': 'Project nem található vagy nincs rá jogosultságod.'}, status=403)

        entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
        
        parsed_hours = parse_hours(hours_str) if hours_str else 0.0
        
        if parsed_hours <= 0:
            # Törölni kell, ha üres vagy 0 (mert nem rögzítünk 0 órát)
            TimeEntry.objects.filter(user=request.user, project=project, date=entry_date).delete()
            return JsonResponse({'status': 'success', 'message': 'Törölve', 'formatted_hours': ''})

        hours = round(parsed_hours, 2)
        
        # Frissítjük vagy Létrehozzuk
        entry, created = TimeEntry.objects.update_or_create(
            user=request.user,
            project=project,
            date=entry_date,
            defaults={'hours': hours}
        )
        
        return JsonResponse({'status': 'success', 'formatted_hours': format_hours(entry.hours)})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


