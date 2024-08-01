from flask import Flask, request, jsonify, render_template, session
from objects.dbManager import DB_manager
from gotrue import errors
from routes.auth import auth_api, login_is_required
from routes.user import user_api
from objects.supabase_init import supabase
import configparser
import logging

logging.basicConfig(filename="app.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    filemode="w")

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.register_blueprint(auth_api)
app.register_blueprint(user_api)

config = configparser.ConfigParser()
config.read('../config.ini')

app.secret_key = config['flask']['secret_key']
db = DB_manager(config['supabase']['url'], config['supabase']['key'])

def main():
    pass

@app.route('/set_nickname', methods = ['POST'])
def set_nickname():
    data_id = request.get_json()
    # print(data)
    
    # id = data.get('id')
    
    user_nickname_response = db.select(table="Users", columns="name" ,criteria={"id": data_id})
    
    nickname = user_nickname_response.data[0].get('name') if user_nickname_response.data else None

    session['nickname'] = nickname
    return "Nickname has been set in session."

@app.route('/projects', methods=['POST'])
def projects():
    data = request.json

    id = data.get('id')

    #user_response = supabase.table('Users').select('id').eq('name', name).execute()
    # if user_response.data:
    #user_id = user_response.data[0]['id']
    # users_projects_response = supabase.table('Projects').select('id').eq('owner_id', id).execute()
    users_projects_response = db.select(table="Projects", columns="id", criteria={"owner_id": id})


    # убрать name и искать по id
    project_ids = [project['id'] for project in users_projects_response.data]

    # projects_response = supabase.table('Projects').select('*').in_('id', project_ids).execute()
    projects_response = db.select(table="Projects", columns="*", criteria={"id": project_ids})

    session['projects'] = projects_response.data
    
    return jsonify(projects_response.data), 200
    # else:
    #     return jsonify({'message': 'User name not exist'}), 400
    
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

    # response = supabase.table('Requests').insert(new_request).execute()
    response = db.insert(table="Requests", data=new_request)
    return jsonify({'message': 'Data inserted successfully'}), 201

@app.route('/del_user', methods=['POST'])
def delete_user():
    data = request.json
    
    id = data.get('id')

    # response = supabase.table('Users').delete().eq('id', id).execute()
    response = db.delete(table="Users", criteria={'id': id})
    return jsonify({'message': 'Data delete successfully'}), 200


@app.route('/settings', endpoint='settings')
@login_is_required
def options_page():
    nickname = session.get('nickname', [])
    return render_template('settings.html', nickname=nickname)

@app.route('/create_projects', endpoint='create_projects')
@login_is_required
def create_projects_page():
    nickname = session.get('nickname', [])
    return render_template('createProject.html', nickname=nickname)

@app.route('/my_projects', methods=['GET'], endpoint='my_projects')
@login_is_required
def main_page():
    projects = session.get('projects', [])
    nickname = 'Loading...'
    # user_data = supabase.auth.get_user()  # Это второй способ
    # nickname = user_data.user.user_metadata['name']  # Это второй способ
    return render_template('myProjects.html', projects=projects, nickname=nickname)

@app.route('/create_projects_none')
def create_projects_none_page():
    return render_template('createProjectNone.html')

if __name__ == '__main__':
    app.run()