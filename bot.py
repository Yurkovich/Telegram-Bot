import telebot
from youtube import search_video
from database import add_query

# Настройки Telegram бота
bot = telebot.TeleBot('7087734459:AAHE1kURiluqCMZXtNNaFd6sJHudoegO6kw')

# Обработчик для команды /start/
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который поможет тебе найти видео на YouTube.")

# Обработчик для текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    search_video(bot, message)
    add_query(message.text)
    
# Запуск бота
bot.polling()