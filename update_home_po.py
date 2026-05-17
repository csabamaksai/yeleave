po_file = 'locale/en/LC_MESSAGES/django.po'

with open(po_file, 'r', encoding='utf-8') as f:
    content = f.read()

content += '\n\nmsgid "Üdvözlünk a"\nmsgstr "Welcome to the"\n\nmsgid "rendszerben!"\nmsgstr "system!"\n'

with open(po_file, 'w', encoding='utf-8') as f:
    f.write(content)
