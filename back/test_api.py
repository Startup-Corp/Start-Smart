import requests

base_url = 'http://127.0.0.1:5000'

def test_insert():
    data = {
        'UserId': 3,
        'photos': [
            {'url': 'http://example.com/photo1.jpg', 'description': 'Description for photo 1'},
            {'url': 'http://example.com/photo2.jpg', 'description': 'Description for photo 2'}
        ],
        'context_info': 'Some context information',
        'target_metric': 'Target metric data',
        'inverse_metric': 'Inverse metric data'
    }

    response = requests.post(f'{base_url}/input_data', json=data)
    #print(response.status_code, response.json())
    assert response.status_code == 201

def test_auth():
    data = {'email': 'test124@example.com', 'password': 'hashedpassword()(321985u)'}
    response = requests.post(f'{base_url}/auth', json=data)

    if response.status_code == 200:
        print('Password:', response.json().get('password'))
    elif response.status_code == 404:
        print('Message:', response.json().get('message'))
    else:
        print('Error:', response.json().get('error'))

def test_create_new_user():
    data = { 'name': 'name1', 'email': 'test124@example.com', 'password': 'hashedpassword()(321985u)'}
    response = requests.post(f'{base_url}/new_user', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Data saved successfully'

def test_delete_user():
    data = {'id': 2}  
    response = requests.post(f'{base_url}/del_user', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Data delete successfully'

def test_projects():
    data = {'id': '8'}
    response = requests.post(f'{base_url}/projects', json=data)
    if response.status_code == 200:
        print('Projects:', response.json())
    elif response.status_code == 400:
        print('Message:', response.json().get('message'))
    else:
        print('Error:', response.json())

if __name__ == '__main__':
    #test_insert()
    #test_create_new_user()
    #test_delete_user()
    test_projects()