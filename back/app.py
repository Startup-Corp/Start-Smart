from flask import Flask, request, jsonify
import supabase
from supabase import create_client, Client
import configparser 

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('./config.ini')

supabaseURL = config['supabase']['supabaseURL']
supabaseKey = config['supabase']['supabaseKey']


supabase: Client = create_client(supabaseURL, supabaseKey)


def main():
    pass
    
@app.route('/get_users', methods=['GET'])
def get_users():
    response = supabase.table('Users').select('*').execute()
    return jsonify(response.data), 200
    

@app.route('/get_projects', methods=['GET'])
def get_projects():
    response = supabase.table('Projects').select('*').execute()
    return jsonify(response.data), 200

@app.route('/new_user', methods=['POST'])
def create_new_user():
    data = request.json
    
    rate = data.get('rate')
    name = data.get('name')
    email = data.get('email')

    response = supabase.table('Users').insert([{'rate': rate, 'name': name, 'email': email}]).execute()

    return jsonify({'message': 'Data saved successfully'}), 200

@app.route('/projects_page', methods=['POST']) 
def get_projects_page(): 
    data = request.json 
 
    name = data['name'] 
 
    subresponse_id = supabase.table('Users').select('*').eq('name', name).execute() 
    id = subresponse_id.data[0]['id'] 
 
    subresponse_proj_id = supabase.table('Users_projects').select('project_id').eq('user_id', id).execute() 
    project_id = subresponse_proj_id.data[0]['project_id'] 
     
    response = supabase.table('Projects').select('*').eq('id', project_id).execute() 
     
    return jsonify(response.data), 200

@app.route('/del_user', methods=['POST'])
def delete_user():
    data = request.json
    
    id = data.get('id')

    response = supabase.table('Users').delete().eq('id', id).execute()
    return jsonify({'message': 'Data delete successfully'}), 200

if __name__ == '__main__':
    app.run()