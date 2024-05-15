import telebot
from youtube import search_video

# Настройки Telegram бота
bot = telebot.TeleBot('7087734459:AAHE1kURiluqCMZXtNNaFd6sJHudoegO6kw')

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который поможет тебе найти видео на YouTube.")

# Обработчик для текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    video_title, video_url = search_video(message.text)
    if video_title and video_url:
        bot.send_message(message.chat.id, f"Найдено видео: {video_title}\n{video_url}")
    else:
        bot.send_message(message.chat.id, "Видео не найдено.")

# Запуск бота
bot.polling()