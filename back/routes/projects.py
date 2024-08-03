from flask import Blueprint, jsonify, request, redirect, render_template
from gotrue import errors
from objects.supabase_init import supabase
from objects.project import AddProject
import logging

project_api = Blueprint('project_api', __name__)


@project_api.route('/new_project', methods=['POST'])
def new_project():
    files = request.files

    files_list = [files[file] for file in files]

    form_data = request.form


    owner_id: str = supabase.auth.get_user().user.id
    username: str = 'aboba'
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

    AddProject(
        username,
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

    # file.save(file.filename)
    # print(files_list)

    # print(files)
    # print(request.form)
    # print(request.form['descriptionMetrics'])

    # print(data)
    return jsonify({'message': 'Ok', 'data': {'user_data': 'data'}}), 200