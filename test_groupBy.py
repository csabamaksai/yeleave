from datetime import date
from itertools import groupby

entries = [
    {'user_name': 'Maksai Csaba', 'date': date(2026, 5, 20), 'hours': 8, 'is_leave': False},
    {'user_name': 'Maksai Csaba', 'date': date(2026, 5, 21), 'hours': 8, 'is_leave': False},
]

entries.sort(key=lambda x: (x['user_name'], -x['date'].toordinal()))
grouped_entries = []

for user_name, group in groupby(entries, key=lambda x: x['user_name']):
    group_list = list(group)
    user_hours = sum(float(e['hours']) for e in group_list if not e['is_leave'])
    user_days = round(user_hours / 8, 2)
    grouped_entries.append({
        'user_name': user_name,
        'entries': group_list,
        'total_hours': user_hours,
        'total_days': user_days
    })

print(grouped_entries)

