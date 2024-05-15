import telebot
from youtube import search_video
from database import add_query

# Настройки Telegram бота
bot = telebot.TeleBot('7087734459:AAHE1kURiluqCMZXtNNaFd6sJHudoegO6kw')

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который поможет тебе найти видео на YouTube.")

# Обработчик для текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    video_path = search_video(message.text)
    if video_path:
        add_query(message.chat.id, message.text)  # Изменили эту строку
        send_video(bot, message.chat.id, video_path)
    else:
        bot.reply_to(message, "К сожалению, не удалось найти видео по вашему запросу.")

# Функция для отправки видеофайла пользователю
def send_video(bot, chat_id, video_path):
    with open(video_path, 'rb') as video_file:
        bot.send_video(chat_id, video_file)

# Запуск бота
bot.polling()