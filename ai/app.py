from flask import Flask, request, jsonify
import configparser
from assistent import Assistent
from pprint import pprint

config = configparser.ConfigParser()
config.read('../config.ini')

app = Flask(__name__)

assistent = Assistent(config['openai']['api_key'])

@app.route('/test', methods=['POST'])
def test():
    data = request.json
    pprint(data)
    if not data or 'messages' not in data:
        return jsonify({"error": "Invalid input"}), 400

    messages = data['messages']

    result = assistent.create_request(messages)
    
    return jsonify({'response': result})

if __name__ == '__main__':
    app.run()
