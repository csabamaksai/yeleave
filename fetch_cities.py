import urllib.request
import json
import csv

url = "https://raw.githubusercontent.com/koleszar/hungarian-zip-codes/master/zip_codes.json"
try:
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))
    cities = sorted(list(set([d['city'] for d in data])))
    with open('clients/hungarian_cities.py', 'w', encoding='utf-8') as f:
        f.write("HUNGARIAN_CITIES = [\n")
        for city in cities:
            f.write(f"    '{city}',\n")
        f.write("]\n")
    print(f"Sikeresen letöltve {len(cities)} település.")
except Exception as e:
    print(f"Hiba JSON letöltésnél: {e}")
    # Próbáljuk CSV-ből (ha az előző repo nem élne)
    url_csv = "https://raw.githubusercontent.com/bcserna/iranyitoszamok/master/iranyitoszamok.csv"
    req = urllib.request.urlopen(url_csv)
    reader = csv.reader(req.read().decode('utf-8').splitlines(), delimiter=';')
    next(reader) # skip header
    cities = sorted(list(set([row[1].strip() for row in reader if len(row) > 1])))
    with open('clients/hungarian_cities.py', 'w', encoding='utf-8') as f:
        f.write("HUNGARIAN_CITIES = [\n")
        for city in cities:
            f.write(f"    '{city}',\n")
        f.write("]\n")
    print(f"Sikeresen letöltve {len(cities)} település CSV-ből.")
