from flask import Flask, request, jsonify
from google.oauth2 import service_account
import requests

app = Flask(__name__)

# Путь к вашему файлу сервисного аккаунта
SERVICE_ACCOUNT_FILE = "C:/Users/salam/OneDrive/Desktop/islamvolga-11e09-5ebd84f347ee.json"
SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

# Создаем учетные данные
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Получаем токен доступа
access_token = credentials.token

# URL для отправки уведомлений
url = "https://fcm.googleapis.com/v1/projects/islamvolga-11e09/messages:send"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

@app.route('/send-notification', methods=['POST'])
def send_notification():
    # Получаем данные из запроса
    data = request.json
    title = data.get('title', 'Заголовок уведомления')
    body = data.get('body', 'Текст уведомления')

    # Формируем payload
    payload = {
        "message": {
            "topic": "all_users",  # Отправка уведомления на тему
            "notification": {
                "title": title,
                "body": body,
            },
        }
    }

    # Отправляем уведомление через FCM
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Уведомление отправлено!"}), 200
    else:
        return jsonify({"status": "error", "message": "Ошибка отправки уведомления!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
