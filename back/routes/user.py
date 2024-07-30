from flask import Blueprint, jsonify, request, redirect, render_template
from gotrue import errors
from objects.supabase_init import supabase
import logging

user_api = Blueprint('user_api', __name__)


@user_api.route('/user_info', methods=['POST'])
def get_user_info():
    user_data = supabase.auth.get_user()
    if user_data is None:
        return jsonify({'message': 'User not auth'}), 500
    
    data = {
        'username': user_data.user.user_metadata['name']
    }
    return jsonify({'message': 'Ok', 'data': {'user_data': data}}), 200
