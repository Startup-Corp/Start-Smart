import requests
import json

base_url = 'http://127.0.0.1:5000'

def test_response():
    headers = {'Content-Type': 'application/json'}

    data = {
        "project_id": 32,
        "user_id": 'e7d852b6-4ebc-4bbc-b141-a2e672948184',
        "email": 'info@mail.com'
    }

    response = requests.post(f'{base_url}/create_report', headers=headers, data=json.dumps(data))
    print(response.json())

if __name__ == '__main__':
    test_response()
