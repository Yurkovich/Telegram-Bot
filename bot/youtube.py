import asyncio
from youtubesearchpython.__future__ import *
from pytube import YouTube
import re
import os
from moviepy.editor import VideoFileClip

# async def check_duration(user_request: str):
#     try:
#         videosSearch = VideosSearch(
#             user_request, limit=1, language='ru', region='RU')
#         videosResult = await videosSearch.next()
#         video_duration = videosResult["result"][0]["duration"]
#         print(video_duration, type(video_duration))
#         len_video_duration = len(video_duration)
#         if len_video_duration <= 4:
#             splited = video_duration.split(':')
#             seconds = int(splited[0]) * 60 + int(splited[1])
#             if seconds > 240:
#                 return False
#             else:
#                 return True
#         else:
#             return False
#     except Exception as e:
#         print(f"Ошибка при проверке продолжительности видео: {e}")
#         return False

def download_audio(video_url):
    # Создаем объект YouTube и загружаем видео
    yt = YouTube(video_url)
    audio = yt.streams.filter(only_audio=True).first()

    # Задаем путь для сохранения видео
    audio_path = os.path.join('downloads', yt.title + ".mp3")
    audio_title = yt.title

    # Скачиваем аудио на сервер
    audio.download(output_path='downloads', filename=audio_title + ".mp3")
    return audio_path, audio_title

async def get_url(user_request: str):
    try:
        videosSearch = VideosSearch(
            user_request, limit=1, language='ru', region='RU')
        videosResult = await videosSearch.next()

        video_url = videosResult["result"][0]["id"]
        video_title = videosResult["result"][0]["title"]
        result_url = f'https://www.youtube.com/watch?v={video_url}'

        return result_url, video_title
    except Exception as e:
        print(f"Ошибка при получении URL видео: {e}")
        return None


# async def download_audio_from_video(video_url: str, output_path: str) -> str:
#     try:
#         yt = YouTube(video_url)
#         audio_stream = yt.streams.filter(only_audio=True).first()
#         if not os.path.exists(output_path):
#             os.makedirs(output_path)
#         audio_file_path = os.path.join(output_path, f"audio.{audio_stream.subtype}")
#         audio_stream.download(output_path=output_path, filename="audio")
#         return audio_file_path
#     except Exception as e:
#         print(f"Ошибка загрузки аудио: {e}")
#         return None
    
# async def download_video(video_url: str, output_path: str) -> str:
#     try:
#         yt = YouTube(video_url)
#         video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
#         if video_stream is None:
#             raise ValueError("Видеопоток не найден.")
#         if not os.path.exists(output_path):
#             os.makedirs(output_path)
#         video_file_path = os.path.join(output_path, f"{yt.title}.mp4")
#         video_stream.download(output_path=output_path, filename=yt.title)
#         return video_file_path
#     except Exception as e:
#         print(f"Ошибка загрузки видео: {e}")
#         return None

# def convert_video_to_mp3(video_file_path: str) -> str:
#     try:
#         video_clip = VideoFileClip(video_file_path)
#         audio_file_path = video_file_path.replace(".mp4", ".mp3")
#         video_clip.audio.write_audiofile(audio_file_path)
#         video_clip.close()
#         return audio_file_path
#     except Exception as e:
#         print(f"Ошибка конвертации видео: {e}")
#         return None
    
# async def video_downloader(video_url, max_retries=3, retry_interval=10):
#     for i in range(max_retries):
#         try:
#             my_video = YouTube(video_url)
#             stream = my_video.streams.get_by_resolution('720p')
#             video_title = simplify_video_title(my_video.title)
#             video_title = f"{video_title}.mp4"
#             stream.download(output_path='./downloads/video', filename=video_title)
#             return video_title
#         except Exception as e:
#             print(f"Ошибка при загрузке видео: {e}")
#             if i < max_retries - 1:
#                 print(f"Повторная попытка через {retry_interval} секунд...")
#                 await asyncio.sleep(retry_interval)
#             else:
#                 print("Превышено количество попыток. Загрузка видео не удалась.")
#                 return None

def simplify_video_title(video_title):
    return re.sub(r'[^\w\s]', '', video_title)

