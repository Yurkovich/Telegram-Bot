from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import requests
import html

# Ключ для доступа к YouTube API
YOUTUBE_API_KEY = 'AIzaSyBhBYbEPhAChoCBhizv6JtuonUzuh1X80w'

# Функция для поиска видео на YouTube
def search_video(bot, message):
    query = message.text
    try:
        video_id, video_title = get_video_info(query)
        video_path = download_video(video_id, video_title)
        send_video(bot, message.chat.id, video_path)
        audio_path = convert_to_audio(video_path, video_title)
        send_audio(bot, message.chat.id, audio_path)
        cleanup(video_path, audio_path)
        bot.send_message(message.chat.id, "Видео и аудио успешно скачаны!")
    except Exception as e:
        print(f"Ошибка при загрузке видео: {e}")
        bot.reply_to(message, "Произошла ошибка при загрузке видео. Попробуйте еще раз позже.")

# Функция для получения информации о видео
def get_video_info(query):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    video_id = data['items'][0]['id']['videoId']
    video_title = html.unescape(data['items'][0]['snippet']['title'])  # Декодируем HTML-символы
    return video_id, video_title

# Функция для загрузки видео
def download_video(video_id, video_title):
    video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    video_stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_path = f'downloads/{video_title}.mp4'
    video_stream.download(output_path='downloads', filename=f'{video_title}.mp4')
    return video_path

# Функция для отправки видеофайла пользователю
def send_video(bot, chat_id, video_path):
    bot.send_video(chat_id, open(video_path, 'rb'))

# Функция для конвертации видео в аудио
def convert_to_audio(video_path, video_title):
    audio_path = f'downloads/{video_title}.mp3'
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path

# Функция для отправки аудиофайла пользователю
def send_audio(bot, chat_id, audio_path):
    bot.send_audio(chat_id, open(audio_path, 'rb'))

# Функция для удаления временных файлов
def cleanup(video_path, audio_path):
    os.remove(video_path)
    os.remove(audio_path)