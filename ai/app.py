from flask import Flask, request, jsonify
import configparser
# from assistent import Assistent
from pprint import pprint
from ai.objects.project import GetProjectByID, GetProjectImagesByID
from ai.objects.supabase_init import supabase

config = configparser.ConfigParser()
config.read('../config.ini')

app = Flask(__name__)

# assistent = Assistent(config['openai']['api_key'])

@app.route('/create_report', methods=['GET'])
def test():
    data = request.json
    if not data or 'project_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    project_id = data['project_id']
    user_id = data['user_id']
    username = data['username']

    project_data = GetProjectByID.execute(project_id, user_id)
    project_images = GetProjectImagesByID.execute(project_id, user_id, username)

    

    pprint(project_data)

    # result = assistent.create_request(messages)
    
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(port=5001)
