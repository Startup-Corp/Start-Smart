import requests

base_url = 'http://127.0.0.1:5000'


def test_get_users():
    response = requests.get(f'{base_url}/all_users')
    assert response.status_code == 200


def test_get_projects():
    response = requests.get(f'{base_url}/get_projects')
    assert response.status_code == 200


def test_get_projects_page():
    data = {'name': 'Test User'}
    response = requests.post(f'{base_url}/projects_page', json=data)
    assert response.status_code == 200

def test_create_new_user():
    data = {'rate': 0, 'name': 'adfh', 'email': 'testsfgjsfgj@example.com'}
    response = requests.post(f'{base_url}/new_user', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Data saved successfully'


def test_delete_user():
    data = {'id': 7}  
    response = requests.post(f'{base_url}/del_user', json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'Data delete successfully'

if __name__ == '__main__':
    # test_get_users()
    # test_get_projects()
    #test_create_new_user()
    #test_delete_user()
    test_get_projects_page()