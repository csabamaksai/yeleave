import re

filepath = 'timesheet/views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

find = """                    if parsed_hours <= 0:
                        # Törölni kell, ha 0
                        deleted = TimeEntry.objects.filter(user=request.user, project=project, date=entry_date).delete()"""
                        
repl = """                    if parsed_hours > project.max_daily_hours:
                        return JsonResponse({
                            'status': 'error', 
                            'message': f'A(z) {project.name} projektre maximum napi {project.max_daily_hours} óra könyvelhető, de te ennyit írtál be: {hours_str}'
                        }, status=400)

                    if parsed_hours <= 0:
                        # Törölni kell, ha 0
                        deleted = TimeEntry.objects.filter(user=request.user, project=project, date=entry_date).delete()"""

new_text = text.replace(find, repl)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated validation successfully.")
