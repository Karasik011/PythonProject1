from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS
import aiohttp
import asyncio


async def fetch_json(session, url):
    """Універсальна функція для GET-запитів"""
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        return None


async def parse_match(session, match_id, puu_id):
    """Парсить один матч і повертає статистику гравця"""
    match_data = await fetch_json(session, MATCH_STATS.format(match_id))
    if not match_data:
        return None

    if match_data['info']['gameMode'] != 'CLASSIC':
        return None  # ігноруємо фан режими

    participants = match_data['metadata']['participants']
    player_index = participants.index(puu_id)
    player_info = match_data['info']['participants'][player_index]

    kills, deaths, assists = player_info['kills'], player_info['deaths'], player_info['assists']
    kda = (kills + assists) / deaths if deaths else kills + assists

    return {
        'Champion': player_info['championName'],
        'Kills': kills,
        'Deaths': deaths,
        'Assists': assists,
        'KDA': round(kda, 2),
        'Position': player_info['teamPosition'],
        'Win Status': 'Win' if player_info['win'] else 'Loss',
        'Type': match_data['info']['gameMode']
    }


async def main(summoner_name, tag_name, count):
    async with aiohttp.ClientSession() as session:
        # Отримуємо puu_id
        data = await fetch_json(session, SUMMONER_INFO.format(summoner_name, tag_name))
        if not data:
            print("Summoner not found")
            return None
        puu_id = data['puuid']

        # Отримуємо історію матчів
        matches = await fetch_json(session, MATCH_HISTORY.format(puu_id, count))
        if not matches:
            print("No match history")
            return None

        # Паралельний збір статистики по матчах
        tasks = [parse_match(session, match_id, puu_id) for match_id in matches]
        results = await asyncio.gather(*tasks)

        # Фільтруємо None (фан-режими чи помилки)
        games = [res for res in results if res]

        # Вивід результатів
        for g in games:
            print(g)

        return games

# Запуск
asyncio.run(main("KaRasIK4", "EUW", 20))