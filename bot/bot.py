import asyncio
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from youtube import get_url, download_audio
from config import TOKEN
from database import authenticate_user, register_user, create_db, save_query_to_database, create_queries_table
from decorators import rate_limit

logged_in_users = {}


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in logged_in_users.values():
        await update.message.reply_text("Введи название песни, которую мы ищем.")
    else:
        await update.message.reply_text("Привет! Для начала работы отправьте команду /register <логин> <пароль> для регистрации, либо /login <логин> <пароль> для авторизации.")


async def register(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in logged_in_users.values():
        await update.message.reply_text("Вы уже залогинены и не можете зарегистрировать новый аккаунт.")
        return

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

    telegram_name = update.message.chat.username
    telegram_id = update.message.from_user.id

    if authenticate_user(username, password):
        await update.message.reply_text("Пользователь с таким логином уже существует.")
        return
    register_user(username, password, telegram_name, telegram_id)
    await update.message.reply_text("Регистрация прошла успешно.")


async def login(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in logged_in_users.values():
        await update.message.reply_text("Вы уже авторизованы. Чтобы войти в другой аккаунт, сначала разлогиньтесь с текущего.")
        return

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
        context.user_data['username'] = username
    else:
        await update.message.reply_text("Неверный логин или пароль.")


async def logout(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in logged_in_users.values():
        username_to_remove = None
        for username, chat_id in logged_in_users.items():
            if chat_id == user_id:
                username_to_remove = username
                break
        if username_to_remove:
            del logged_in_users[username_to_remove]
            del context.user_data['username']
            await update.message.reply_text("Вы успешно разлогинились.")
        else:
            await update.message.reply_text("Произошла ошибка при разлогинивании.")
    else:
        await update.message.reply_text("Вы не были авторизованы.")


@rate_limit(10)
async def send_video_and_audio(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in logged_in_users.values():
        await handle_authentication_required(update)
        return
    user_message = update.message.text
    try:
        url = await get_url(user_message)
        await update.message.reply_text(f"Ваша ссылка: {url}")
    except Exception as e:
        print(f"Ошибка при отправке ссылки: {e}")
        await update.message.reply_text("Произошла ошибка при поиске и отправке видео.")

    username = context.user_data.get('username')
    try:
        audio_path, _ = download_audio(url[0])
        if audio_path:
            await context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=open(audio_path, 'rb'),
            )
        else:
            print('Ошибка загрузки аудио')
    except Exception as e:
        await update.message.reply_text(f"Не удалось загрузить аудио")

    
    if username:
        user_id = user_id = update.effective_user.id
        query = update.message.text
        save_query_to_database(user_id, username, query)
    else:
        handle_authentication_required(update)


async def handle_authentication_required(update: Update) -> None:
    await update.message.reply_text("Для использования этой функции необходимо авторизоваться. Пожалуйста, войдите в систему с помощью /login или зарегистрируйтесь с помощью /register.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(CommandHandler("logout", logout))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, send_video_and_audio))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    # create_db()
    # create_queries_table()
    print('Запуск бота...')
    asyncio.run(main())
    print('Бот остановлен.')