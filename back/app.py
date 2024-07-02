from flask import Flask, request, jsonify, render_template
import supabase
from supabase import create_client, Client
import configparser 

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('../config.ini')

supabaseURL = config['supabase']['supabaseURL']
supabaseKey = config['supabase']['supabaseKey']


supabase: Client = create_client(supabaseURL, supabaseKey)


def main():
    pass


@app.route('/projects', methods=['POST'])
def projects():
    data = request.json

    name = data.get('name')

    user_response = supabase.table('Users').select('id').eq('name', name).execute()
    if user_response.data:
        user_id = user_response.data[0]['id']
        users_projects_response = supabase.table('Projects').select('id').eq('owner_id', user_id).execute()

        project_ids = [project['id'] for project in users_projects_response.data]

        projects_response = supabase.table('Projects').select('*').in_('id', project_ids).execute()
        print(projects_response.data)
        return jsonify(projects_response.data), 200
    else:
        return jsonify({'message': 'User name not exist'}), 400
    
@app.route('/input_data', methods=['POST'])
def input_data():
    data = request.json

    user_id = data.get('UserId')
    photos = data.get('photos')
    context_info = data.get('context_info')
    target_metric = data.get('target_metric')
    inverse_metric = data.get('inverse_metric')

    new_request = {
        'UserId': user_id,
        'photos': photos,
        'context_info': context_info,
        'target_metric': target_metric,
        'inverse_metric': inverse_metric
    }

    response = supabase.table('Requests').insert(new_request).execute()
    
    return jsonify({'message': 'Data inserted successfully'}), 201

@app.route('/new_user', methods=['POST'])
def create_new_user():
    data = request.json
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    response = supabase.table('Users').insert([{'name': name, 'email': email, 'password': password}]).execute()

    return jsonify({'message': 'Data saved successfully'}), 200

@app.route('/del_user', methods=['POST'])
def delete_user():
    data = request.json
    
    id = data.get('id')

    response = supabase.table('Users').delete().eq('id', id).execute()
    return jsonify({'message': 'Data delete successfully'}), 200

@app.route('/auth', methods=['POST'])
def auth():
    data  = request.json
    email = data.get('email')

    try:
        response = supabase.table('Users').select('password').eq('email', email).execute()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    if response.data:
        return jsonify({'password': response.data[0]['password']})
    else:
        return jsonify({'message': 'User does not exist'}), 404

@app.route('/')
def authorization_page():
    return render_template('authorization.html')

@app.route('/registration')
def first_page():
    return render_template('registration.html')

@app.route('/settings')
def options_page():
    return render_template('settings.html')

@app.route('/create_projects')
def create_projects_page():
    return render_template('createProject.html')

@app.route('/my_projects')
def main_page():
    return render_template('myProjects.html')

@app.route('/create_projects_none')
def create_projects_none_page():
    return render_template('createProjectNone.html')

if __name__ == '__main__':
    app.run()