import urllib.request
import json
import ssl
import os

def update_cities():
    url = "https://raw.githubusercontent.com/koleszar/hungarian-zip-codes/master/zip_codes.json"
    
    # SSL hiba elkerülése macOS limitációk miatt
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print("Településlista letöltése...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        
        cities = set()
        for item in data:
            city = item.get('city', '').strip()
            if not city:
                continue
            
            # Különböző kerületek helyett csak egy összegző "Budapest"
            if "Budapest" in city:
                cities.add("Budapest")
            else:
                cities.add(city)
        
        sorted_cities = sorted(list(cities))
        
        # Fájl kiírása a clients mappába
        output_file = os.path.join(os.path.dirname(__file__), 'hungarian_cities.py')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("HUNGARIAN_CITIES = [\n")
            for c in sorted_cities:
                f.write(f'    "{c}",\n')
            f.write("]\n")
            
        print(f"Sikeresen frissítve lett a lista {len(sorted_cities)} településsel!")
        
    except Exception as e:
        print(f"Hiba történt a letöltés során: {e}")

if __name__ == '__main__':
    update_cities()
