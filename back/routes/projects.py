from flask import Blueprint, jsonify, request, redirect, render_template, send_file
from gotrue import errors
from objects.supabase_init import supabase
from objects.project import AddProject, GetProjectsByUserID, GetProjectByID, GetProjectImagesByID
from objects.user import GetBalanceByUserId, GetLastProjId
import requests
import json
import logging

project_api = Blueprint('project_api', __name__)


@project_api.route('/new_project', methods=['POST'])
def new_project():
    user_info = supabase.auth.get_user()
    
    files = request.files

    files_list = [files[file] for file in files]

    form_data = request.form

    owner_id: str = user_info.user.id
    email: str = user_info.user.user_metadata['email']
    title: str = form_data['nameProject'] or 'Test title'
    description: str = form_data['descriptionProject'] or 'Test desc'
    funnel_desc: str = form_data['descriptionFunnels'] or 'Test funnel'
    img_desc: str = form_data['img_description'] or 'img desc'
    metric_title: str = form_data['nameMetrics'] or 'metric'
    metric_desc: str = form_data['descriptionMetrics'] or 'desc metric'
    metric_target: str = form_data['targetValueMetric'] or 'target'
    extra_data: str = form_data['additionalData'] or 'add data'
    tariff: int = 1
    files: list = files_list

    headers = {'Content-Type': 'application/json'}
    data = {
            "project_id": GetLastProjId.execute(owner_id),
            "user_id": owner_id,
            "email": email
        }
    
    user_id = user_info.user.id
    print(data)
    print(f'{user_id} and type {type(user_id)}')
    print(user_id == '02e46b95-b31f-43bf-81b2-02357ff83d8d')
    ai_balance, ex_balance = GetBalanceByUserId.execute(user_id)
    if ai_balance is None and ex_balance is None:
        print('balance not found')
    else:
        if (tariff == 2 and ex_balance > 0) or (tariff == 1 and ai_balance > 0):
            AddProject(
                email,
                owner_id,
                title,
                description,
                funnel_desc,
                img_desc,
                metric_title,
                metric_desc,
                metric_target,
                extra_data,
                tariff,
                files
            ).execute()

            response = requests.post(f'http://127.0.0.1:5001/create_report', headers=headers, data=json.dumps(data))
        else:
            print('problems')

    return jsonify({'message': 'Ok'}), 200


@project_api.route('/projects', methods=['POST'])
def projects_list():
    user_id: str = supabase.auth.get_user().user.id
    projects_list = GetProjectsByUserID.execute(user_id)
    return jsonify({'message': 'Ok', 'data': projects_list}), 200


@project_api.route('/project_data', methods=['GET'])
def get_project_data():
    data = request.json

    project_id = data['project_id']
    user_info = supabase.auth.get_user()
    user_id: str = user_info.user.id
    email: str = user_info.user.user_metadata['email']

    project_data = GetProjectByID.execute(project_id, user_id, email)

    return jsonify({'message': 'Ok', 'data': project_data}), 200


@project_api.route('/project_images', methods=['POST'])
def get_project_images():
    data = request.json

    project_id = data['project_id']
    user_info = supabase.auth.get_user()
    user_id: str = user_info.user.id
    email: str = user_info.user.user_metadata['email']

    images_data = GetProjectImagesByID.execute(project_id, user_id, email)
    print(images_data)

    return send_file(
        images_data,
        mimetype='application/zip',
        as_attachment=True,
        download_name='files.zip'
    )
