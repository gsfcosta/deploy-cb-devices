#!/usr/bin/python3
from time import timezone
import time
import requests,json,sys,os
from dateutil import parser
from datetime import datetime, timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Proxy Bypass
os.environ['http_proxy'] = 'http://127.0.0.1:3128'
os.environ['https_proxy'] = 'http://127.0.0.1:3128'
#Carrega Variaveis
cb_api_id           = os.environ["API_ID"]
cb_api_secret_key   = os.environ["API_SECRET_KEY"]
cb_url              = "https://defense-prod05.conferdeploy.net/appservices/v6/orgs/<token>"
#Verifica devices
headers = {
    'content-type': "application/json",
    'X-AUTH-TOKEN': cb_api_secret_key + "/" + cb_api_id,
}
criteria = {
    "criteria": {
        "status": ["ALL"],
        },
    "rows": 10000
    }
x = requests.post(cb_url + "/devices/_search", headers=headers, json=criteria, verify=False)
response = json.loads(x.content)
# found = (response['num_found'])
response = (response['results'])
z = 0
for alert in response:
    ####################
    
    # <GET IF INCIDENT EXISTS> #
    count = 0
    ####################  
    if count == 0:
        try:
            # Abrir incidente
            impact="MultipleUsers"
            urgency="NoDisruption"
            data = datetime.now() - timedelta(days=5)
            dataold = f"{data.isoformat()[:-3]}Z"
            dt = (alert["last_contact_time"])
            if dt < dataold:
                dt = parser.parse(alert["last_contact_time"])
                data = str(dt.date())
                tempo = str(dt.time().strftime("%H:%M:%S"))
                try:
                    device = alert["name"]
                    splited = device_name.split("\\")
                    splited = splited[1]
                    device_name = splited.lower()
                except:
                    device = alert["name"]
                    device_name = device.lower()
                alert_id = str(alert["id"])
                policy_id = alert["policy_id"]
                z = z + 1
        except BaseException as e:
            log = str(datetime.now()) + "  ERROR : Erro ao abrir incidente - " + str(e)
            print(log)
    else:
        continue
log = str(datetime.now()) + "  INFO : " + str(z) + " incidentes abertos"
print(log)