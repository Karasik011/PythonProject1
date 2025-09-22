import aiohttp
import requests
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import tracemalloc
tracemalloc.start()
from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS

async def request(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return print(f'Mistake:{response.status}')

newTable = []
async def main(summoner_name, tag_name):
    async with aiohttp.ClientSession() as session:
        data = await request(session, SUMMONER_INFO.format(summoner_name, tag_name))
        puu_id = data['puuid']
        matches = await request(session, MATCH_HISTORY.format(puu_id))
        for i in matches:
                async with session.get(MATCH_STATS.format(i)) as match_info_response:
                    if match_info_response.status == 200:
                        match_data = await match_info_response.json()
                    if match_data['info']['gameMode'] == 'CLASSIC':
                        participants = match_data['metadata']['participants']
                        player_index = participants.index(puu_id)
                        player_info = match_data['info']['participants'][player_index]
                        champion_name = player_info['championName']
                        kills = player_info['kills']
                        deaths = player_info['deaths']
                        assists = player_info['assists']
                        kda = (kills + assists) / deaths if deaths > 0 else kda == kills + assists
                        team_position = player_info['teamPosition']
                        win_status = 'Win' if player_info['win'] else 'Lose'
                        match_type = match_data['info']['gameMode']
                        stats = {'Champion': champion_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists,'KDA': kda, 'Position': team_position, 'Win Status': win_status, 'Type': match_type}
                        newTable.append(stats)
                        print(stats)
                        continue

asyncio.run(main('Karasik4', 'EUW'))
MatchData = pd.DataFrame(newTable)
MatchData.head()



asyncio.run(main('Karasik4', 'EUW'))
#Хочу выводить КДА на дистанции 100 игр с помощью гистограмы и высчитать среднее KDA

plt.bar(MatchData['Position'],MatchData['KDA'].mean())

plt.show()




