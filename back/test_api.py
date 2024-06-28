import requests

base_url = 'http://127.0.0.1:5000'

def insert():
    data = {
        "UserId": 3,
        "photos": [
            {"url": "http://example.com/photo1.jpg", "description": "Description for photo 1"},
            {"url": "http://example.com/photo2.jpg", "description": "Description for photo 2"}
        ],
        "context_info": "Some context information",
        "target_metric": "Target metric data",
        "inverse_metric": "Inverse metric data"
    }

    response = requests.post(f'{base_url}/input_data', json=data)
    #print(response.status_code, response.json())
    assert response.status_code == 201

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

if __name__ == '__main__':
    insert()
    #test_create_new_user()
    #test_delete_user()