import aiohttp
import requests
import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import tracemalloc
tracemalloc.start()
from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS
async def main(summoner_name, tag_name):
    newTable = []
    async with aiohttp.ClientSession() as session:
        async with session.get(SUMMONER_INFO.format(summoner_name, tag_name)) as response:
            if response.status == 200:
                data = await response.json()
                puu_id = data['puuid']
        async with session.get(MATCH_HISTORY.format(puu_id)) as id_response:
                if id_response.status == 200:
                    matches = await id_response.json()
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
                        if deaths != 0:
                            kda = (kills + assists) / deaths
                        else:
                            kda = kills + assists
                        team_position = player_info['teamPosition']
                        if player_info['win'] is True:
                            win_status = 'Win'
                        else:
                            win_status = 'Loss'
                        match_type = match_data['info']['gameMode']
                        stats = {'Champion': champion_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists,'KDA': kda, 'Position': team_position, 'Win Status': win_status, 'Type': match_type}
                        newTable.append(stats)
                        MatchData = pd.DataFrame(newTable)
                        print(stats)
                        continue
        print(MatchData.head())




asyncio.run(main('Karasik4', 'EUW'))
#Хочу выводить КДА на дистанции 20 игр с помощью гистограмы и высчитать среднее KDA
#def kda(summoner_name, tag):
    #id = requests.get(SUMMONER_INFO.format(summoner_name, tag))
    #if id.status_code == 200:
        #data = id.json()
        #puu_id = data['puuid']




