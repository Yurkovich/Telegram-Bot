import os
from pytube import YouTube
from googlesearch import search
from moviepy.editor import VideoFileClip

def get_video_info(query):
    # Используем Google поиск для получения URL первого видео
    search_results = search(query + " site:youtube.com", num=1, stop=1)

    # Получаем URL первого видео
    video_url = next(search_results, None)
    if video_url:
        return video_url
    else:
        return None

def download_video(video_url):
    # Создаем объект YouTube и загружаем видео
    yt = YouTube(video_url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    # Задаем путь для сохранения видео
    save_path = os.path.join('downloads', yt.title + ".mp4")

    # Скачиваем видео на сервер
    video.download(output_path='downloads', filename=yt.title + ".mp4")

    return save_path

def convert_to_audio(video_path, video_title):
    audio_path = f'downloads/{video_title}.mp3'
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()
    return audio_path

# Функция для удаления временных файлов
def cleanup(video_path, audio_path):
    os.remove(video_path)
    os.remove(audio_path)

def search_and_convert_video(query):
    # Получаем URL видео
    video_url = get_video_info(query)
    if video_url:
        # Скачиваем видео на сервер
        video_path = download_video(video_url)
        audio_path = convert_to_audio(video_path, os.path.splitext(os.path.basename(video_path))[0])
        return video_path, audio_path
    else:
        return None, None