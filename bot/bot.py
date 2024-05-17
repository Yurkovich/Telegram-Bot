
import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from youtube import get_url, video_downloader, simplify_video_title, check_duration
from config import TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    await update.message.reply_text("Привет! Отправьте мне сообщение с запросом видео.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с описанием доступных команд."""
    await update.message.reply_text("Вы можете использовать следующие команды:\n/start - начать взаимодействие с ботом\n/help - получить справку о командах")

async def search_and_send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, search_and_send_video))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print('Запуск бота...')
    asyncio.run(main())
    print('Бот остановлен.')

