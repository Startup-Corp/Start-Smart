from flask import Blueprint, jsonify, request, redirect, render_template
from gotrue import errors
from objects.supabase_init import supabase
import logging

project_api = Blueprint('project_api', __name__)


@project_api.route('/new_project', methods=['POST'])
def new_project():
    data = request.json
    files = request.files

    print(files)

    print(data)
    return jsonify({'message': 'Ok', 'data': {'user_data': data}}), 200
