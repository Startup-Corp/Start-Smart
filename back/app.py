from flask import Flask, render_template, request, jsonify
import supabase
from supabase import create_client, Client
import configparser 

app = Flask(__name__, template_folder='../templates', static_folder='../static')

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

######################################################### Это сделал я на время, чтобы проверить
# @app.route('/add_user', methods=['POST'])
# def add_users():
#     data = request.json

#     password = data.get('passwordUser')
#     name = data.get('nameUser')
#     email = data.get('mailUser')
    
#     print(password, name, email)

#     response = supabase.table('Users').insert([{'password': password, 'name': name, 'email': email}]).execute()
#     return jsonify({'message': 'Data delete successfully'}), 200


# @app.route('/get_user', methods=['POST'])
# def get_user():
#     data = request.json

#     email = data.get('mailUser')
#     password = data.get('passwordUser')
    
#     response = supabase.table('Users').select('*').eq('email', email).eq('password', password).execute()
        
#     if response.data:
#         print(f"User found: {response.data}")
#         return jsonify({'message': 'User found', 'user': response.data}), 200
#     else:
#         print("User not found")
#         return jsonify({'message': 'User not found'}), 404
########################################################### 

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