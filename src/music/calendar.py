from datetime import timedelta

from ..endpoint_requests import request_daily_kpop_calendar
from .search_youtube import search_youtube

async def get_daily_kpop_calendar(search_date):
    results = await request_daily_kpop_calendar(search_date)
    musics = extract_music_names(results)

    if not musics:
        return 'Sem lançamentos hoje!!'

    musics_with_urls = []

    for music in musics:
        try:
            video_url = await search_youtube(music)

            if video_url:
                musics_with_urls.append(f"{music}\n{video_url}")
            else:
                musics_with_urls.append(music)
        except Exception as e:
            print(f"Erro ao buscar URL para '{music}': {e}")
            musics_with_urls.append(music)
    
    daily_musics = '\n\n'.join(map(str, musics_with_urls))

    return daily_musics

async def get_weekly_kpop_calendar(search_start_date):
    weekly_musics = {}
    search_date = search_start_date
   
    for _ in range(7):
        results = await request_daily_kpop_calendar(search_date.strftime("%Y-%m-%d"))
        musics = extract_music_names(results)

        weekly_musics[search_date.strftime("%Y-%m-%d")] = musics

        search_date = search_date + timedelta(days=1)

    return weekly_musics   

def extract_music_names(results):
    music_names = []

    for page in results['results']:
        name_property = page['properties']['Name']['title']

        if name_property:
            title_text = ''.join(part['text']['content'] for part in name_property)
            music_names.append(title_text)

    return music_names