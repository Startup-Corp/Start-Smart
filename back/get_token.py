import requests

url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

payload='scope=GIGACHAT_API_PERS'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': '513a1915-924e-4dcc-b80d-0af4d8786e25',
  'Authorization': 'Basic <NTEzYTE5MTUtOTI0ZS00ZGNjLWI4MGQtMGFmNGQ4Nzg2ZTI1OmQ0N2Q3MDIyLTM3YmQtNGY2Yi04NDAzLWM4NWI1MTA3ZTgxMA==>'# <> 
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)