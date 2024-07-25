from flask import Blueprint, jsonify, request, redirect, render_template
from gotrue import errors
from objects.supabase_init import supabase

auth_api = Blueprint('auth_api', __name__)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        res = supabase.auth.get_session()
        print(res)
        if res is None:
            return redirect('/')
        return function(*args, **kwargs)
    return wrapper


@auth_api.route('/registration')
def first_page():
    return render_template('registration.html')


@auth_api.route('/')
def authorization_page():
    return render_template('authorization.html')


@auth_api.route('/auth', methods=['POST'])
def auth():
    data = request.json
    email = data.get('email')
    password = data.get('passwordUser')

    try:
        data = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except errors.AuthApiError as ex:
        return jsonify({'message': 'User does not exist', 'error': ex}), 404
    except Exception as ex:
        return jsonify({'message': 'Unknown error', 'error': ex}), 500

    return jsonify({'message': 'Sing in success'}), 200


@auth_api.route('/new_user', methods=['POST'])
def create_new_user():
    data = request.json
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    try:
        response = supabase.auth.sign_up(
            credentials={
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "name": name,
                        "display_name": name
                    }
                },
            }
        )
    except errors.AuthApiError as ex:
        return jsonify({'message': 'User already exist', 'error': ex}), 500
    except Exception as ex:
        return jsonify({'message': 'Unknown error', 'error': ex}), 500

    return jsonify({'message': 'Sing up success'}), 200


@auth_api.route('/singout', methods=['GET'])
def sing_out():
    try:
        response = supabase.auth.sign_out()
    except errors.AuthApiError as ex:
        return jsonify({'message': 'User already exist', 'error': ex}), 500
    except Exception as ex:
        return jsonify({'message': 'Unknown error', 'error': ex}), 500

    return redirect('/')
