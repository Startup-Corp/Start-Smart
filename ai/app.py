from flask import Flask, request, jsonify
import httpx
import configparser
import logging
from openai import OpenAI 
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('../config.ini')

# Использование правильного формата прокси URL
# proxies = {
#     'http://': 'socks5://92.51.36.153:9000',
#     'https://': 'socks5://92.51.36.153:9000',
# }
client = OpenAI(api_key=config['openai']['api_key'])
#openai_api_key = config['openai']['api_key']

# @app.route('/test', methods=['POST'])
# def test():
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {openai_api_key}',
#     }
#     data = {
#         'model': 'gpt-3.5-turbo',
#         'messages': [
#             {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#             {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#         ]
#     }
    
#     try:
#         logging.debug("Sending request to OpenAI API")
#         with httpx.Client(proxies=proxies) as client:
#             response = client.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
#             response.raise_for_status()
#             result = response.json()
#         logging.debug("Received response from OpenAI API")
#         return jsonify(result)
#     except httpx.RequestError as e:
#         logging.error(f"Request failed: {e}")
#         return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['POST'])
def test():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."}, # as promt
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."} # as request from user
            ]
    )
    print(response.choices[0].message)

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         data = request.json
#         user_prompt = data.get('system')
#         question = data.get('user')
#         if not user_prompt:
#             return jsonify({'error': 'No prompt provided'}), 400

#         response = openai.completions.create(
#             model="gpt-3.5-turbo",
#             #prompt=user_prompt
#             messages= [
#             {"role": "system", "content": user_prompt},
#             {"role": "user", "content": question}
#         ]
#         )

#         print(response.choices[0].message)

#         if response:
#             return jsonify({'response': response.choices[0].text.strip()}), 200
#         else:
#             return jsonify({'error': 'No response from AI'}), 500
#     except Exception as e:
#         logging.exception("Exception occurred during data processing")
#         return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run()
