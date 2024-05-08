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
    # if responce null insert
    # insert_data_response = supabase.table('Projects').insert([{'name': name, 'description': description, 'logo': logo}]).execute()

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

@app.route('/del_user', methods=['POST'])
def delete_user():
    data = request.json
    
    id = data.get('id')

    response = supabase.table('Users').delete().eq('id', id).execute()
    return jsonify({'message': 'Data delete successfully'}), 200

@app.route('/first')
def first_page():
    return render_template('index.html')

@app.route('/options')
def options_page():
    return render_template('options.html')

@app.route('/main_page')
def main_page():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run()