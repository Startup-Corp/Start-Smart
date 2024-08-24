import requests
import json

base_url = 'http://127.0.0.1:5001'

def test_response():
    headers = {'Content-Type': 'application/json'}

    data = {
        "project_id": 27    ,
        "user_id": 'a51b6fff-4412-4369-bca8-93aa013c858b',
        "email": '234@gmail.com'
    }

    response = requests.post(f'{base_url}/create_report', headers=headers, data=json.dumps(data))
    print(response.json())

if __name__ == '__main__':
    test_response()
