from pytube import Search, YouTube
import os


def search_and_download_music(query: str) -> str: 
    result_search = Search(query) 
    if len(result_search.results) > 0: 
        url = f'https://www.youtube.com/watch?v={result_search.results[0].video_id}' 
        yt = YouTube(url)
        output_path = f'downloads'
        try:
            os.mkdir(output_path)
        except:
            pass
        finally:
            video = yt.streams.filter(only_audio=True).first() 
            downloaded_file = video.download(output_path=output_path) 
            base, ext = os.path.splitext(downloaded_file) 
            new_file = base + '.mp3' 
            os.rename(downloaded_file, new_file)
            return new_file