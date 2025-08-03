from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = '8403421825:AAH9dpr4wUydrj3bCDsDpR21MunzPwh91d4'  # ← вставь токен бота
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# Простая база пользователей (в памяти)
user_segments = {}

# Кнопки для выбора сегментации
def get_main_menu():
    return {
        "keyboard": [
            [{"text": "Хочу навести порядок в бизнесе"}],
            [{"text": "Хочу пройти диагностику"}],
            [{"text": "Хочу начать с нуля"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }

# Обработка входящих сообщений
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        # Обработка /start
        if text == '/start':
            msg = (
                "Привет! Я — бот проекта LINIA. "
                "Мы помогаем владельцам бизнеса выйти из операционки и построить систему, которая работает без перегруза.\n\n"
                "С чего ты хочешь начать?"
            )
            send_message(chat_id, msg, reply_markup=get_main_menu())

        # Сегментация по кнопке
        elif text == "Хочу навести порядок в бизнесе":
            user_segments[chat_id] = 'оптимизация'
            send_message(chat_id, "Отлично! Вот короткое видео о том, как выстроить систему управления 👇")
            send_message(chat_id, "https://youtu.be/dQw4w9WgXcQ")  # Замени на своё видео
            send_message(chat_id, "Хочешь пойти глубже? Запишись на диагностику:", 
                         reply_markup={"keyboard": [[{"text": "Записаться"}]], "resize_keyboard": True})

        elif text == "Хочу пройти диагностику":
            user_segments[chat_id] = 'диагностика'
            send_message(chat_id, "Вот короткий PDF-гайд, как проходит диагностика:")
            send_message(chat_id, "https://example.com/diagnostic.pdf")  # Замени на свой файл
            send_message(chat_id, "Готов пройти прямо сейчас?", 
                         reply_markup={"keyboard": [[{"text": "Записаться"}]], "resize_keyboard": True})

        elif text == "Хочу начать с нуля":
            user_segments[chat_id] = 'стартап'
            send_message(chat_id, "Класс! Вот первый бесплатный урок по запуску проекта с нуля:")
            send_message(chat_id, "https://example.com/start-course")  # Замени на свой курс

        elif text == "Записаться":
            send_message(chat_id, "Вот ссылка на запись 📅:\nhttps://example.com/booking")

        else:
            send_message(chat_id, "Не понял тебя. Выбери действие из меню 👇", reply_markup=get_main_menu())

    return {'ok': True}

# Упрощённая функция отправки сообщений
def send_message(chat_id, text, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    if reply_markup:
        payload['reply_markup'] = reply_markup
    requests.post(URL, json=payload)

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
