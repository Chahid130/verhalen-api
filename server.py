from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

SAFETY_SYSTEM_PROMPT = """You are a creative storytelling AI for the app "Written By You". You generate fiction stories based on user prompts.

CONTENT SAFETY RULES (strictly enforced):
- NEVER generate sexually explicit content, graphic nudity, or pornographic descriptions
- NEVER generate detailed graphic violence, gore, or torture
- NEVER generate content sexualizing or harming minors under any circumstance
- NEVER generate instructions for real-world harm, weapons, drugs, or illegal activities
- NEVER generate hate speech, slurs, or content targeting protected groups
- Romance is allowed but must remain tasteful (kissing, emotional intimacy) - no explicit sexual scenes
- Violence in adventure/fantasy is allowed but kept non-graphic (no detailed gore)
- Horror/suspense is allowed but avoid extreme disturbing imagery

If a user requests content that violates these rules, politely refuse and offer an alternative story direction. Stay in character as a helpful storyteller.

Generate engaging, creative fiction appropriate for a general audience (teens and adults)."""

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
        json={
            'model': 'claude-sonnet-4-6',
            'max_tokens': max_tokens,
            'system': SAFETY_SYSTEM_PROMPT,
            'messages': [{'role': 'user', 'content': prompt}]
        },
        timeout=300
    )
    if response.status_code == 200:
        tekst = response.json()['content'][0]['text']
        return jsonify({'tekst': tekst})
    else:
        print(f"API ERROR {response.status_code}: {response.text}", flush=True)
        return jsonify({'error': 'API fout', 'status': response.status_code, 'detail': response.text}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
