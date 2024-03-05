import telebot
import requests
from io import BytesIO # Класс для работы с байтовыми потоками
from PIL import Image # Библиотека для работы с изображениями

bot = telebot.TeleBot('API-TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, отправь мне ссылку на сайт и я покажу тебе, как выглядит страница сайта, не заводя тебя на сам сайт.')

# Обрабатываем текстовые сообщения, которые содержат ссылки формата https://...
@bot.message_handler(regexp='https?://')
def screenshot(message):
    url = message.text
    # Наш API ключ, берем с сайта screenshotmachine.com
    api_key = 'API-KEY'
    # Отправляем запрос к сайту, который делает скриншоты сайтов
    response = requests.get(f'https://api.screenshotmachine.com?key={api_key}&url={url}&dimension=1024x768&format=png')
    if response.status_code == 200:
        # Создаем объект изображения из байтового потока
        image = Image.open(BytesIO(response.content))
        # Сохраняем изображение во временный файл
        image.save('screenshot.png')
        # Открываем файл и отправляем его пользователю
        with open('screenshot.png', 'rb') as file:
            bot.send_photo(message.chat.id, file, caption=f'Вот скриншот страницы {url}')
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не смог сделать скриншот. Попробуйте другую ссылку.')

bot.polling()