from flask import Flask, request, jsonify
import openai
import configparser
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('../config.ini')

openai.api_key = config['openai']['api_key']

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        user_prompt = data.get('prompt')

        if not user_prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_prompt,
            max_tokens=150
        )

        if response:
            return jsonify({'response': response.choices[0].text.strip()}), 200
        else:
            return jsonify({'error': 'No response from AI'}), 500
    except Exception as e:
        logging.exception("Exception occurred during data processing")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
