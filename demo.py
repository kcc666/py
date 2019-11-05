import requests
import json
import socket


r = requests.get("http://106.15.53.80:56789/vpsType.json")
r_text = r.text
# print(r_text)

a = json.loads(r_text)
cpn = socket.gethostname()
print()
for i in a:
    if i["computerName"] == cpn:
        return  i["type"]