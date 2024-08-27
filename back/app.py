import os

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from objects.dbManager import DB_manager
from gotrue import errors
from objects.project import GetProjectsByUserID
from objects.project import GetProjectByID


from routes.auth import auth_api, login_is_required
from routes.user import user_api
from routes.projects import project_api

from objects.supabase_init import supabase
# from objects.dbManager import db

import configparser
import logging

logging.basicConfig(filename="app.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    filemode="w")

app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.register_blueprint(auth_api)
app.register_blueprint(user_api)
app.register_blueprint(project_api)

config = configparser.ConfigParser()
print(os.getcwd())
config.read('config.ini')
app.secret_key = config['flask']['secret_key']

# supabase_url = config['supabase']['url']
# supabase_key = config['supabase']['key']
db = DB_manager()

def setNickname():
    user_data = supabase.auth.get_user()
    nickname = user_data.user.user_metadata['name'] if user_data is not None else "Aboba"
    return nickname

def getProjects():
    user_id: str = supabase.auth.get_user().user.id
    projects_list = GetProjectsByUserID.execute(user_id)
    return projects_list

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

@app.route('/create_projects', endpoint='create_projects')
@login_is_required
def create_projects_page():
    nickname = setNickname()
    return render_template('createProject.html', nickname=nickname)


@app.route('/my_projects', methods=['GET'], endpoint='my_projects')
@login_is_required
def main_page():
    projects_list = getProjects()
    nickname = setNickname()
    return render_template('myProjects.html', projects=projects_list, nickname=nickname)

@app.route('/my_projects/<int:project_id>')
def project_detail(project_id):
    nickname = setNickname()
    user_id: str = supabase.auth.get_user().user.id
    project = GetProjectByID.execute(project_id, user_id)
    
    if not project:
        return "Проект не найден", 404
    
    return render_template('project.html', project=project, nickname=nickname)

# @app.route('/create_projects_none')
# def create_projects_none_page():
#     nickname = setNickname()
#     return render_template('createProjectNone.html', nickname=nickname)

if __name__ == '__main__':
    app.run()