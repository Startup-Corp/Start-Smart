from flask import Flask, render_template, request, jsonify
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

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()
    print(data)
    name = data['name']
    phoneNumber = data['phone']
    nameProj = data['project']

    # Сохранение данных в базе данных на Supabase
    response = supabase.table('testForCheck').insert([{'name': name, 'phoneNumber': phoneNumber, 'nameProj': nameProj}]).execute()

    # if response['status_code'] == 201:
    return jsonify({'message': 'Data saved successfully'}), 200
    # else:
    #     return jsonify({'message': 'Error occurred while saving data'}), 500


@app.route('/first')
def first_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()