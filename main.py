from itertools import repeat
import time
import aiohttp
import os
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import tracemalloc
import sqlite3
from aiolimiter import AsyncLimiter
from numpy.ma.core import append
from pandas.core.interchange.dataframe_protocol import DataFrame

tracemalloc.start()
from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS

database = sqlite3.connect('database.db')
cursor = database.cursor()

rate_limit_sec = AsyncLimiter(20, 1)
rate_limit_min = AsyncLimiter(100, 120)
Table = []
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
                return await request(session, url)
            else:
                print(f'Mistake:{response.status}')
                return None


async def match_data(session, match_id, puuid):
    match_stats = await request(session, MATCH_STATS.format(match_id))
    if not match_stats:
        return None
    if match_stats['info']['gameMode'] != 'CLASSIC':
        return None
    participants = match_stats['metadata']['participants']
    player_index = participants.index(puuid)
    player_info = match_stats['info']['participants'][player_index]
    champion_name = player_info['championName']
    Id_match = match_id
    kills = player_info['kills']
    deaths = player_info['deaths']
    assists = player_info['assists']
    kda = (kills + assists) / deaths if deaths > 0 else (kills + assists)
    team_position = player_info['teamPosition']
    win_status = 'Win' if player_info['win'] else 'Lose'
    #match_type = match_stats['info']['gameMode']
    stats = {'Match_Id': Id_match,'Champion': champion_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists, 'KDA': kda,
             'Position': team_position, 'Win_Status': win_status}
    return stats


async def main(summoner_name, tag_name, count):
    async with aiohttp.ClientSession() as session:
        data = await request(session, SUMMONER_INFO.format(summoner_name, tag_name))
        puu_id = data['puuid']
        match_id = await request(session, MATCH_HISTORY.format(puu_id, count))
        dicts = [match_data(session, match_id, puu_id) for match_id in match_id]
        for i in range (0, len(dicts), 10):
            data_slice = dicts[i:i+10]
            outcome = await asyncio.gather(*data_slice)
            result = [r for r in outcome if r]
            for a in result:
                Table.append(a)
            await asyncio.sleep(1)
        return result


asyncio.run(main('Karasik4', 'EUW', 70))
DataTable = pd.DataFrame(Table)
print(DataTable)



DataTable.to_sql(name = 'games', con=database, if_exists='replace', index=False)
database.commit()
database.close()
#game_count = datatable.groupby(['Position'])['Id'].count()
#print(game_count)
#kda_by_pos = datatable.groupby(['Position'])['KDA'].mean()
#print(kda_by_pos)
#plt.bar(kda_by_pos.index, kda_by_pos.values)
#plt.show()

#def KDA(kda, position):
    #avg_kda = int(sum(kda) / len(kda))
    #plt.bar(position, avg_kda)
    #plt.show()

#KDA(DataTable['KDA'], DataTable['Position'])
#Хочу выводить КДА на дистанции 100 игр с помощью гистограмы и высчитать среднее KDA




