import asyncio
import re
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from youtube import get_url, video_downloader, simplify_video_title, check_duration
from config import TOKEN
from auth.bot_auth import authenticate_user
from auth.bot_registration import register_user
from auth.database import create_db
import time
from functools import wraps

logged_in_users = {}

def rate_limit(seconds):
    def decorator(func):
        last_called = 0

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal last_called
            current_time = time.time()
            if current_time - last_called < seconds:
                await args[0].message.reply_text("Пожалуйста, подождите некоторое время перед отправкой нового запроса.")
                return
            last_called = current_time
            return await func(*args, **kwargs)
        return wrapper
    return decorator

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in logged_in_users.values():
        await update.message.reply_text("Введи название песни, которую мы ищем.")
    else:
        await update.message.reply_text("Привет! Для начала работы отправьте команду /register <логин> <пароль> для регистрации, либо /login <логин> <пароль> для авторизации.")

async def register(update: Update, context: CallbackContext) -> None:
    message = update.message.text.split()
    if len(message) != 3:
        await update.message.reply_text("Используйте команду /register <логин> <пароль>")
        return
    username = message[1]
    password = message[2]
    if len(username) < 7:
        await update.message.reply_text("Минимальная длина логина - 7 символов.")
        return
    if len(password) < 8:
        await update.message.reply_text("Минимальная длина пароля - 8 символов.")
        return
    if not re.match(r'^[A-Za-z0-9_]+$', username) or not re.match(r'^[A-Za-z0-9_]+$', password):
        await update.message.reply_text("Логин и пароль могут содержать только буквы латинского алфавита, цифры и символ подчеркивания.")
        return
    if username.startswith('_'):
        await update.message.reply_text("Логин не должен начинаться с символа подчеркивания.")
        return
    telegram_name = await update.message.chat.username
    telegram_id = await update.message.from_user.id
    if authenticate_user(username, password):
        await update.message.reply_text("Пользователь с таким логином уже существует.")
        return
    register_user(username, password, telegram_name, telegram_id)
    await update.message.reply_text("Регистрация прошла успешно.")

async def login(update: Update, context: CallbackContext) -> None:
    message = update.message.text.split()
    if len(message) != 3:
        await update.message.reply_text("Используйте команду /login <логин> <пароль>")
        return
    username = message[1]
    password = message[2]
    for logged_user_username in logged_in_users:
        if logged_user_username == username:
            await update.message.reply_text("Вы уже авторизованы.")
            return
    if authenticate_user(username, password):
        logged_in_users[username] = update.message.chat_id
        await update.message.reply_text("Авторизация прошла успешно.")
    else:
        await update.message.reply_text("Неверный логин или пароль.")

async def logout(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in logged_in_users.values():
        for username, logged_user_id in logged_in_users.items():
            if logged_user_id == user_id:
                del logged_in_users[username]
                await update.message.reply_text("Вы разлогинены.")
                return
    else:
        await update.message.reply_text("Вы не были авторизованы.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Вы можете использовать следующие команды:\n/start - начать взаимодействие с ботом\n/help - получить справку о командах")

@rate_limit(10)
async def search_and_send_video(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in logged_in_users.values():
        await handle_authentication_required(update)
        return
    user_message = update.message.text
    try:
        if await check_duration(user_message):
            video_url = await get_video_url(user_message)
            video_title = await download_video(video_url)
            video_path = f"./downloads/video/{video_title}"
            await wait_for_download(video_path)
            await send_video(update, context, video_title, video_path)
            remove_video(video_path)
        else:
            await handle_long_video(update)
    except Exception as e:
        print(f"Ошибка при поиске и отправке видео: {e}")
        await handle_error(update)

async def handle_authentication_required(update: Update) -> None:
    await update.message.reply_text("Для использования этой функции необходимо авторизоваться. Пожалуйста, войдите в систему с помощью /login или зарегистрируйтесь с помощью /register.")

async def get_video_url(user_message: str) -> str:
    return await get_url(user_message)

async def download_video(video_url: str) -> str:
    return await video_downloader(video_url)

async def wait_for_download(video_path: str) -> None:
    while not os.path.exists(video_path):
        await asyncio.sleep(1)

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_title: str, video_path: str) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Вот ваше видео: {video_title}"
    )
    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=open(video_path, 'rb'),
        supports_streaming=True
    )

def remove_video(video_path: str) -> None:
    os.remove(video_path)

async def handle_long_video(update: Update) -> None:
    await update.message.reply_text("Видео слишком длинное. Максимальная длина видео - 4 минуты")

async def handle_error(update: Update) -> None:
    await update.message.reply_text("Произошла ошибка при поиске и отправке видео.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("logout", logout))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, search_and_send_video))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    create_db()
    print('Запуск бота...')
    asyncio.run(main())
    print('Бот остановлен.')
