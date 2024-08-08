from flask import Flask, request, jsonify
import configparser
from ai.assistent import Assistent
from ai.gpt_flow import GPTFlow
from pprint import pprint
from ai.objects.project import GetProjectByID, GetProjectImagesByID
from ai.objects.supabase_init import supabase
import httpx

config = configparser.ConfigParser()
config.read('../config.ini')

app = Flask(__name__)

proxies = {"http://": config['openai']['proxy_addr'], "https://": config['openai']['proxy_addr']}
http_client = httpx.Client(proxies=proxies)
assistent = Assistent(config['openai']['api_key'], http_client)

@app.route('/create_report', methods=['POST'])
def test():
    data = request.json
    if not data or 'project_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    project_id = data['project_id']
    user_id = data['user_id']
    email = data['email']

    project_data = GetProjectByID.execute(project_id, user_id)
    project_images = GetProjectImagesByID.execute(project_id, user_id, email)

    gpt_flow = GPTFlow(project_data, project_images, assistent)

    gpt_flow.start()
    
    return jsonify({'response': 'ok'})

if __name__ == '__main__':
    app.run(port=5001)
