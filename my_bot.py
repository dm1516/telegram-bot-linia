import requests
import time
import threading

# === Настройки ===
TOKEN = '8403421825:AAH9dpr4wUydrj3bCDsDpR21MunzPwh91d4'
API_URL = f'https://api.telegram.org/bot{TOKEN}/'
user_state = {}  # user_id: current_state

# === Утилиты ===
def send_message(chat_id, text, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    if reply_markup:
        payload['reply_markup'] = reply_markup
    requests.post(API_URL + 'sendMessage', json=payload)

def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(API_URL + 'getUpdates', params=params)
    return response.json()['result']

# === Основная логика ===
def handle_update(update):
    message = update.get('message')
    if not message:
        return

    chat_id = message['chat']['id']
    user_id = message['from']['id']
    text = message.get('text', '')

    state = user_state.get(user_id, 'start')

    if state == 'start':
        send_message(
            chat_id,
            "Привет! Я — бот проекта LINIA. Мы помогаем владельцам бизнеса выйти из операционки и построить систему, которая работает без перегруза. Скажи, что ближе к твоей ситуации?",
            reply_markup={
                "keyboard": [
                    ["Хочу навести порядок в бизнесе"],
                    ["Хочу пройти диагностику"],
                    ["Хочу начать с нуля"]
                ],
                "one_time_keyboard": True,
                "resize_keyboard": True
            }
        )
        user_state[user_id] = 'segment'

    elif state == 'segment':
        if text == "Хочу навести порядок в бизнесе":
            send_message(chat_id, "📘 Вот PDF с системными шагами: https://example.com/system")
        elif text == "Хочу пройти диагностику":
            send_message(chat_id, "📝 Пройди диагностику: https://example.com/diagnostic")
        elif text == "Хочу начать с нуля":
            send_message(chat_id, "🎥 Стартовое видео: https://example.com/start-from-zero")
        else:
            send_message(chat_id, "Пожалуйста, выбери один из вариантов выше 👆")
            return

        # Следующий шаг — CTA
        send_message(
            chat_id,
            "Хочешь перейти к следующему шагу?",
            reply_markup={
                "keyboard": [
                    ["Да, хочу результат!"],
                    ["Пока не готов(а)"]
                ],
                "one_time_keyboard": True,
                "resize_keyboard": True
            }
        )
        user_state[user_id] = 'cta'

        # Запускаем дожим через 24 часа
        threading.Thread(target=delayed_reminder, args=(chat_id,), daemon=True).start()

    elif state == 'cta':
        if "Да" in text:
            send_message(chat_id, "🚀 Отлично! Вот ссылка на участие: https://example.com/webinar")
        else:
            send_message(chat_id, "Хорошо! Напомню тебе чуть позже.")
        user_state[user_id] = 'done'

def delayed_reminder(chat_id):
    time.sleep(60 * 60 * 24)  # 24 часа
    send_message(chat_id, "Напоминаю — ты можешь всё ещё присоединиться к программе! 💡")

# === Главный цикл ===
def main():
    offset = None
    print("Бот запущен. Ожидаю сообщения...")
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                handle_update(update)
                offset = update['update_id'] + 1
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
