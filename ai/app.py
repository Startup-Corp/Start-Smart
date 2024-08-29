from flask import Flask, request, jsonify
import configparser
from assistent import Assistent
from gpt_flow import GPTFlow
from objects.project import GetProjectByID, GetProjectImagesByID, UpdateProjectStatus
from bot import start_approval
import httpx
import asyncio
import os
import threading

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

proxies = {"http://": config['openai']['proxy_addr'], "https://": config['openai']['proxy_addr']}
http_client = httpx.Client(proxies=proxies)
assistent = Assistent(config['openai']['api_key'], http_client)# , http_client

loop = asyncio.new_event_loop()
def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=run_loop, args=(loop,), daemon=True).start()

@app.route('/create_report', methods=['POST'])
def create_report():
    data = request.json
    if not data or 'project_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    project_id = data['project_id']
    user_id = data['user_id']
    email = data['email']

    UpdateProjectStatus.execute(project_id, 'AI')

    project_data = GetProjectByID.execute(project_id, user_id)
    project_images = GetProjectImagesByID.execute(project_id, user_id, email)

    bucket_id = f'{email}_{str(user_id)[:5]}'
    gpt_flow = GPTFlow(project_data, project_images, assistent, bucket_id, project_id, is_dev=True)

    gpt_flow.start()

    file_data = gpt_flow.get_result()
    # Используем run_in_executor для выполнения асинхронной задачи в отдельном потоке
    future = asyncio.run_coroutine_threadsafe(
        start_approval(file_data, project_id, user_id, bucket_id, email), 
        loop
    )
    
    future.result()
    return jsonify({'response': 'ok'})

if __name__ == '__main__':
    app.run(port=5001)