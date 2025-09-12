import requests
import pandas as pd
import asyncio
import matplotlib.pyplot as plt

from constants import SUMMONER_INFO, MATCH_HISTORY, MATCH_STATS
def main():
    summoner_name = 'KaRasIK4'
    tag_name = 'EUW'
    response = requests.get(SUMMONER_INFO.format(summoner_name, tag_name))
    if response.status_code == 200:
        data = response.json()
        puu_id = data['puuid']
        match_history_response = requests.get(MATCH_HISTORY.format(puu_id))
        if match_history_response.status_code == 200:
            matches = match_history_response.json()
            games = []
            for i in matches:
                match_info_response = requests.get(MATCH_STATS.format(i))
                if match_info_response.status_code == 200:
                    match_data = match_info_response.json()
                    if match_data['info']['gameMode'] == 'CLASSIC':
                        participants = match_data['metadata']['participants']
                        player_index = participants.index(puu_id)
                        player_info = match_data['info']['participants'][player_index]
                        champion_name = player_info['championName']
                        kills = player_info['kills']
                        deaths = player_info['deaths']
                        assists = player_info['assists']
                        if deaths != 0:
                            kda = (kills + assists) // deaths
                        else:
                            kda = kills + assists
                        team_position = player_info['teamPosition']
                        if player_info['win'] is True:
                            win_status = 'Win'
                        else:
                            win_status = 'Loss'
                        match_type = match_data['info']['gameMode']
                        stats = {'Champion': champion_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists,'KDA': kda, 'Position': team_position, 'Win/Lose': win_status, 'Type': match_type}
                        games.append(stats)
                        print(stats)
                    else:
                        print('Фан режим')
            game_data = pd.DataFrame(games)
            print(game_data.head())
            plt.hist(game_data['Kills'], bins=30)
            plt.show()




main()