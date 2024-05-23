
from youtubesearchpython.__future__ import *
from pytube import YouTube
import os


def download_audio(video_url):
    yt = YouTube(video_url)
    audio = yt.streams.filter(only_audio=True).first()
    audio_path = os.path.join('downloads', yt.title + ".mp3")
    audio_title = yt.title
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