
import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from youtube import get_url, video_downloader, simplify_video_title, check_duration
from config import TOKEN


async def search_and_send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    
    try:
        if await check_duration(user_message):

            video_url = await get_url(user_message)
            video_title = await video_downloader(video_url)
            
            # Определяем путь к загруженному видео
            video_path = f"./downloads/video/{video_title}"
            
            # Ожидаем завершения загрузки
            while not os.path.exists(video_path):
                await asyncio.sleep(1)

            # Отправляем видео пользователю
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Вот ваше видео: {video_title}"
            )
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=open(video_path, 'rb'),
                supports_streaming=True
            )

            # Удаляем файл после отправки
            os.remove(video_path)
        else:
            await update.message.reply_text("Видео слишком длинное. Максимальная длина видео - 4 минуты")
        
    except Exception as e:
        print(f"Ошибка при поиске и отправке видео: {e}")
        await update.message.reply_text("Произошла ошибка при поиске и отправке видео.")


def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение."""
    update.message.reply_text("Привет! Отправьте мне сообщение с запросом видео.")


def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с описанием доступных команд."""
    update.message.reply_text("Вы можете использовать следующие команды:\n/start - начать взаимодействие с ботом\n/help - получить справку о командах")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, search_and_send_video))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print('Запуск бота...')
    asyncio.run(main())
    print('Бот остановлен.')

