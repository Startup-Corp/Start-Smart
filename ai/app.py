from flask import Flask, request, jsonify
import configparser
from ai.assistent import Assistent
from ai.gpt_flow import GPTFlow
from pprint import pprint
from ai.objects.project import GetProjectByID, GetProjectImagesByID
from ai.objects.supabase_init import supabase
from ai.tg.main import start_approval, run_dp
import httpx
import asyncio
import os
import threading

config = configparser.ConfigParser()
config.read('../config.ini')

app = Flask(__name__)

proxies = {"http://": config['openai']['proxy_addr'], "https://": config['openai']['proxy_addr']}
http_client = httpx.Client(proxies=proxies)
assistent = Assistent(config['openai']['api_key'])# , http_client

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def start_bot():
    loop.run_until_complete(run_dp())

threading.Thread(target=start_bot, daemon=True).start()

@app.route('/create_report', methods=['POST'])
def create_report():
    data = request.json
    if not data or 'project_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    project_id = data['project_id']
    user_id = data['user_id']
    email = data['email']

    project_data = GetProjectByID.execute(project_id, user_id)
    project_images = GetProjectImagesByID.execute(project_id, user_id, email)

    bucket_id = f'{email}_{str(user_id)[:5]}'
    gpt_flow = GPTFlow(project_data, project_images, assistent, bucket_id, project_id, True)

    gpt_flow.start()

    file_name = "report.md"
    file_path = os.path.abspath(file_name)

    # Вызов start_approval в текущем event loop
    asyncio.run_coroutine_threadsafe(start_approval('-1002244887628', file_path, project_id), loop)

    return jsonify({'response': 'ok'})

# async def main():
#     file_name = "report.md"
#     file_path = os.path.abspath(file_name)

#     await asyncio.gather(
#         run_dp(),
#         start_approval('-1002244887628', file_path, 32)
#     )

if __name__ == '__main__':
    app.run(port=5001)
    
