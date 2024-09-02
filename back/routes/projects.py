from flask import Blueprint, jsonify, request, redirect, render_template, send_file
from gotrue import errors
from objects.supabase_init import supabase
from objects.project import AddProject, GetProjectsByUserID, GetProjectByID, GetProjectImagesByID
from objects.user import GetBalanceByUserId, GetLastProjId, DecUserBalanceByUserId
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
    
    ai_balance, ex_balance = GetBalanceByUserId.execute(owner_id)
    if ai_balance is None and ex_balance is None:
        print('balance not found')
        return jsonify({'message': 'Balance not found'}), 501
    else:
        if (tariff == 2 and ex_balance > 0) or (tariff == 1 and ai_balance > 0):
            pr_id = AddProject(
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

            headers = {'Content-Type': 'application/json'}
            data = {
                "project_id": pr_id,
                "user_id": owner_id,
                "email": email
            }

            try:
                DecUserBalanceByUserId.execute(owner_id, tariff)
            except Exception as ex:
                logging.error(f'dec balance. u_id: {owner_id}, tariff: {tariff}')
                return jsonify({'message': ex}), 500

            try:
                response = requests.post(f'http://127.0.0.1:5002/create_report', headers=headers, data=json.dumps(data))
            except Exception as ex:
                logging.error(f'Request to GPT. pr_id: {pr_id}, ex: {ex}')
                return jsonify({'message': ex}), 500
        else:
            print('problems')
            return jsonify({'message': "Balance 0"}), 502


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
