
import aiohttp
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import tracemalloc
import sqlite3
from aiolimiter import AsyncLimiter
tracemalloc.start()
from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS

database = sqlite3.connect('database.db')
cursor = database.cursor()



rate_limit_sec = AsyncLimiter(20, 1)
rate_limit_min = AsyncLimiter(100, 120)
queue_type = {400: 'Normal', 420: 'SoloQ', 440: 'Flex', 700: 'Clash'}
async def request(session, url):
    async with rate_limit_sec, rate_limit_min:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 429:
                print('Waiting')
                Retry_time = int(response.headers.get('Retry-After'))
                print(f'Time to retry: {Retry_time}')
                await asyncio.sleep(Retry_time)
                return request(session, url)
            else:
                print(f'Mistake:{response.status}')
                return None


async def match_data(session, match_id, puuid):
    match_stats = await request(session, MATCH_STATS.format(match_id))
    if not match_stats:
        return None
    if match_stats['info']['gameMode'] != 'CLASSIC':
        return None
    if match_stats["info"]["queueId"] not in [400,700,420, 440]:
        return None
    type = match_stats["info"]["queueId"]
    mode_name =queue_type.get(type)
    participants = match_stats['metadata']['participants']
    player_index = participants.index(puuid)
    player_info = match_stats['info']['participants'][player_index]
    champion_name = player_info['championName']
    id_match = match_id
    kills = player_info['kills']
    deaths = player_info['deaths']
    assists = player_info['assists']
    kda = (kills + assists) / deaths if deaths > 0 else (kills + assists)
    team_position = player_info['teamPosition']
    win_status = 'Win' if player_info['win'] else 'Lose'
    stats = {'Match_Id': id_match,'Champion': champion_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists, 'KDA': kda,
             'Position': team_position, 'Win_Status': win_status,'Mode': mode_name}
    return stats


async def get_info(summoner_name, tag_name, count, mode):
    mode = mode.lower()
    mode_type = {'soloq': [420],'normal': [400],'clash': [700],'all': [400, 420, 440, 700], 'flex' : [440]}
    queue_filter = mode_type.get(mode, mode_type['all'])
    print(queue_filter)
    table = []
    async with aiohttp.ClientSession() as session:
        data = await request(session, SUMMONER_INFO.format(summoner_name, tag_name))
        puu_id = data['puuid']
        match_ids = await request(session, MATCH_HISTORY.format(puu_id, count))
        dicts = [match_data(session, match_id, puu_id) for match_id in match_ids]
        for i in range (0, len(dicts), 10):
            data_slice = dicts[i:i+10]
            outcome = await asyncio.gather(*data_slice)
            clear_result = [r for r in outcome if r and r['Mode'] in [queue_type[q] for q in queue_filter]]
            table.extend(clear_result)
            await asyncio.sleep(1)
        result = pd.DataFrame(table)
        return result
asyncio.run(get_info('Karasik4','EUW',5,'SoloQ'))



async def plot_create(x_label, y_label, title):
    plt.plot(x_label, y_label, marker='o', label=title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)





