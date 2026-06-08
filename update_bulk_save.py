import re
import json

filepath = 'timesheet/views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

old_func_pattern = re.compile(r'def bulk_save_time_entries.*?except Exception as e:', re.DOTALL)

new_func = """def bulk_save_time_entries(request):
    try:
        data = json.loads(request.body)
        days = data.get('days', [])
        
        updated_count = 0
        deleted_count = 0
        leave_updated = 0
        leave_deleted = 0
        
        for day_obj in days:
            entry_date_str = day_obj.get('date')
            is_leave = day_obj.get('is_leave', False)
            task_desc = day_obj.get('task', '')
            entries = day_obj.get('entries', [])
            
            entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()

            if is_leave:
                # Töröljük a TimeEntry-ket ha voltak
                del_time = TimeEntry.objects.filter(user=request.user, date=entry_date).delete()
                if del_time[0]:
                    deleted_count += del_time[0]
                
                # Ha nem volt még erre a napra szabadság, próbáljuk meg létrehozni
                exists = Leave.objects.filter(user=request.user, start_date__lte=entry_date, end_date__gte=entry_date).exists()
                if not exists:
                    try:
                        Leave.objects.create(
                            user=request.user,
                            start_date=entry_date,
                            end_date=entry_date,
                            leave_type='PTO',
                            notes=task_desc
                        )
                        leave_updated += 1
                    except Exception as exc:
                        # Akkor futhat ide, ha hétvégére esne (a modell clean() dobna exceptiont)
                        pass
            else:
                # Nincs szabadság, törölni kell a napi szabadságot ha pontosan egyezik.
                del_leave = Leave.objects.filter(user=request.user, start_date=entry_date, end_date=entry_date).delete()
                if del_leave[0]: 
                    leave_deleted += del_leave[0]
                
                for row_entry in entries:
                    project_id = row_entry.get('project_id')
                    hours_str = row_entry.get('hours')
                    
                    project = Project.objects.filter(id=project_id, assigned_users=request.user).first()
                    if not project:
                        continue
                        
                    parsed_hours = parse_hours(hours_str) if hours_str else 0.0
                    
                    if parsed_hours <= 0:
                        # Törölni kell, ha 0
                        deleted = TimeEntry.objects.filter(user=request.user, project=project, date=entry_date).delete()
                        if deleted[0] > 0:
                            deleted_count += deleted[0]
                    else:
                        hours = round(parsed_hours, 2)
                        obj, created = TimeEntry.objects.update_or_create(
                            user=request.user,
                            project=project,
                            date=entry_date,
                            defaults={'hours': hours, 'description': task_desc}
                        )
                        updated_count += 1
                        
        return JsonResponse({'status': 'success', 'message': f'Sikeresen beküldve: {updated_count} TS és {leave_updated} Szabadság mentve.'})
    except Exception as e:"""

new_text = old_func_pattern.sub(new_func, text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated timesheet/views.py successfully.")
