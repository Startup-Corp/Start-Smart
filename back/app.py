from flask import Flask, request, jsonify
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

@app.route('/create_project', methods=['POST'])
def create_new_project():
    data = request.json

    name = data.get('name')
    description = data.get('description')
    logo = data.get('logo')

    response = supabase.table('Projects').select('id').eq('name', name).execute()

    if not response.data:
        insert_data_response = supabase.table('Projects').insert([{'name': name, 'description': description, 'logo': logo}]).execute()
        return jsonify(insert_data_response.data), 201
    else:
        return jsonify({'message': 'Project with this name already exists'}), 400

@app.route('/get_users', methods=['GET'])
def get_users():
    response = supabase.table('Users').select('*').execute()
    return jsonify(response.data), 200
    

@app.route('/get_all_projects', methods=['GET'])
def get_all_projects():
    response = supabase.table('Projects').select('*').execute()
    return jsonify(response.data), 200

@app.route('/get_projects', methods=['POST'])
def get_projects():
    data = request.json

    name = data.get('name')

    user_response = supabase.table('Users').select('id').eq('name', name).execute()
    if user_response.data:
        user_id = user_response.data[0]['id']
        users_projects_response = supabase.table('Users_projects').select('project_id').eq('user_id', user_id).execute()
        
        project_ids = [project['project_id'] for project in users_projects_response.data]

        projects_response = supabase.table('Projects').select('*').in_('id', project_ids).execute()
        print(projects_response.data)
        return jsonify(projects_response.data), 200
    else:
        return jsonify({'message': 'User name not exist'}), 400

@app.route('/new_user', methods=['POST'])
def create_new_user():
    data = request.json
    
    rate = data.get('rate')
    name = data.get('name')
    email = data.get('email')

    response = supabase.table('Users').insert([{'rate': rate, 'name': name, 'email': email}]).execute()

    return jsonify({'message': 'Data saved successfully'}), 200

@app.route('/del_user', methods=['POST'])
def delete_user():
    data = request.json
    
    id = data.get('id')

    response = supabase.table('Users').delete().eq('id', id).execute()
    return jsonify({'message': 'Data delete successfully'}), 200

if __name__ == '__main__':
    app.run()