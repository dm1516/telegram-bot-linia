from flask import Flask, request
import requests
import os

TOKEN = '8403421825:AAH9dpr4wUydrj3bCDsDpR21MunzPwh91d4'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        
        reply = f"Ты написал: {text}"
        
        requests.post(URL, json={'chat_id': chat_id, 'text': reply})

    return {'ok': True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
