import telebot
import os
from youtube import search_and_convert_video, cleanup

# Настройки Telegram бота
bot = telebot.TeleBot('7087734459:AAHE1kURiluqCMZXtNNaFd6sJHudoegO6kw')

def send_audio(bot, chat_id, audio_path):
    with open(audio_path, 'rb') as audio_file:
        bot.send_audio(chat_id, audio_file)

def send_video(bot, chat_id, video_path):
    with open(video_path, 'rb') as video_file:
        bot.send_video(chat_id, video_file)

# Обработчик для команды /start/
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который поможет тебе найти видео на YouTube.")

# Обработчик для текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    video_path, audio_path = search_and_convert_video(message.text)
    if video_path and audio_path:
        send_video(bot, message.chat.id, video_path)
        send_audio(bot, message.chat.id, audio_path)
        cleanup(video_path, audio_path)
    else:
        bot.reply_to(message, "Извините, не удалось найти видео по вашему запросу.")

# Запуск бота
bot.polling()