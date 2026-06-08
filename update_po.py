import re

po_file = 'locale/en/LC_MESSAGES/django.po'

with open(po_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

translations = {
    'Partner szerkesztése': 'Edit Client',
    'Új partner': 'New Client',
    'Projekt szerkesztése': 'Edit Project',
    'Új projekt': 'New Project',
    'Lekérdező': 'Reporter',
    'Normál felhasználó': 'User',
    'Lekérdező (Könyvelő/Asszisztens)': 'Reporter (Accountant/Assistant)',
    'Adminisztrátor': 'Administrator',
    'Jogosultság': 'Role',
    'Felhasználói jogosultság': 'User Role',
    'Riportok': 'Reports',
    'Riportok (Fejlesztés alatt)': 'Reports (Under Development)',
    'Ez az oldal a jövőben különféle lekérdezési és riportálási lehetőségeket fog biztosítani a könyvelők és asszisztensek számára (például Timesheet-ek összesítése, szabadság statisztikák).': 'This page will provide various querying and reporting options for accountants and assistants in the future (e.g., timesheet summaries, leave statistics).'
}

for i, line in enumerate(lines):
    if line.startswith('msgid '):
        msgid = line.replace('msgid "', '').replace('"\n', '')
        if msgid in translations:
            if i + 1 < len(lines) and lines[i+1].startswith('msgstr ""'):
                lines[i+1] = f'msgstr "{translations[msgid]}"\n'

with open(po_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
