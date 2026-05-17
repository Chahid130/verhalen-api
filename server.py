from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

@app.route('/verhaal', methods=['POST'])
def maak_verhaal():
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 2000)
    if not prompt:
        return jsonify({'error': 'Geen prompt'}), 400
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={'Content-Type': 'application/json', 'anthropic-version': '2023-06-01', 'x-api-key': ANTHROPIC_API_KEY},
        json={'model': 'claude-opus-4-5', 'max_tokens': max_tokens, 'messages': [{'role': 'user', 'content': prompt}]}
    )
    if response.status_code == 200:
        tekst = response.json()['content'][0]['text']
        return jsonify({'tekst': tekst})
    else:
        return jsonify({'error': 'API fout'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
