from googlesearch import search
import requests
from bs4 import BeautifulSoup

def search_video(query):
    # Выполняем поиск запроса в Google
    search_results = search(query + " site:youtube.com", num=5, stop=5, pause=2)
    
    # Перебираем результаты поиска
    for url in search_results:
        # Извлекаем только URL-адреса YouTube
        if "youtube.com" in url:
            # Получаем HTML-страницу видео
            html_content = requests.get(url).text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Находим заголовок и URL видео
            video_title = soup.find("meta", itemprop="name")["content"]
            video_url = url
            
            # Возвращаем заголовок и URL первого найденного видео
            return video_title, video_url
    
    # Если не найдено ни одного видео на YouTube
    return None, None