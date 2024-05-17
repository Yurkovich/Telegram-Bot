from youtubesearchpython.__future__ import *
import asyncio
import json
import os
from pytube import YouTube

raw_request = 'https://www.youtube.com/watch?v='


async def get_url(user_request: str):
    videosSearch = VideosSearch(
        user_request, limit=1, language='ru', region='RU')
    videosResult = await videosSearch.next()

    video_url = videosResult["result"][0]["id"]
    video_title = videosResult["result"][0]["title"]
    result_url = raw_request + video_url

    return result_url

async def video_downloader(video_url):
    my_video = YouTube(video_url)
    
    await my_video.streams.get_highest_resolution().download(
        output_path='./downloads/video')
    return my_video.title


async def search_and_download(user_request: str):
    videosSearch = VideosSearch(
        user_request, limit=1, language='ru', region='RU')
    videosResult = await videosSearch.next()

    video_url = videosResult["result"][0]["id"]
    video_title = videosResult["result"][0]["title"]
    result_url = raw_request + video_url

    try:
        # Добавляем аннотацию async перед объявлением метода video_downloader()
        await video_downloader(result_url)
    except:
        print('Видео имеет ограничение по возрасту')
        return
    




# async def main():
#     # Вызываем функцию search_and_download с аргументом
#     await search_and_download("SID RAM RAMSING")

# if __name__ == '__main__':
#     asyncio.run(main())
    

# async def write_json(data, filename):
#     data = json.dumps(data)
#     data = json.loads(str(data))
#     with open(filename, 'w', encoding='utf-8') as file:
#         await json.dump(data, file, indent=4, ensure_ascii=False)