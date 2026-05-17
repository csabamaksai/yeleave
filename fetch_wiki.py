import urllib.request
import json
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://hu.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Kateg%C3%B3ria:Magyarorsz%C3%A1g_telep%C3%BCl%C3%A9sei&cmlimit=5000&format=json"
cities = set()

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, context=ctx)
data = json.loads(response.read().decode('utf-8'))

for member in data['query']['categorymembers']:
    title = member['title']
    title = re.sub(r' \(.*?\)', '', title) # kiszedni a zárójeles részeket
    if not title.startswith('Kategória:') and not title.startswith('Sablon:'):
        cities.add(title)

# Továbbá a kategóriában lehetnek alkategóriák, de nem bonyolítjuk, 
# inkább letöltünk egy nyílt listát.
