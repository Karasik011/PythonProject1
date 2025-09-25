import aiohttp
import requests
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import tracemalloc
tracemalloc.start()
from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS


Table = []
async def request(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
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
    match_type = match_stats['info']['gameMode']
    stats = {'Id': Id_match,'Champion': champion_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists, 'KDA': kda,
             'Position': team_position, 'Win Status': win_status, 'Type': match_type}
    return stats


async def main(summoner_name, tag_name, count):
    async with aiohttp.ClientSession() as session:
        data = await request(session, SUMMONER_INFO.format(summoner_name, tag_name))
        puu_id = data['puuid']
        match_id = await request(session, MATCH_HISTORY.format(puu_id, count))
        dicts = [match_data(session, match_id, puu_id) for match_id in match_id]
        outcome = await asyncio.gather(*dicts)
        result = [i for i in outcome if i]
        for a in result:
            Table.append(a)
        return result


asyncio.run(main('Karasik4', 'EUW', 70))
DataTable = pd.DataFrame(Table)
print(DataTable)
#MatchData = pd.DataFrame(newTable)
#MatchData.head()



#Хочу выводить КДА на дистанции 100 игр с помощью гистограмы и высчитать среднее KDA

#plt.bar(MatchData['Position'],MatchData['KDA'])
#plt.show()




