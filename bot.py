
import asyncio
import logging
import os
import sys
from telegram import InputFile, InputMediaVideo
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from youtube import search_and_download, get_url


TOKEN = "7198719536:AAHxIiuXTtN9wwFJj1EiLa0LBIzOFWk5jD0"

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_path = r'.\downloads\video\SID×RAM - RAMSING.mp4'
    if os.path.isfile(video_path) and os.access(video_path, os.R_OK):
        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_file,
                supports_streaming=True
            )
    else:
        await update.message.reply_text("Видеофайл не найден или недоступен для чтения")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hola!")
    await send_video(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print('Start bot . . .')
    asyncio.run(main())
    print('Stopped bot . . .')
