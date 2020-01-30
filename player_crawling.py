import pandas as pd
import os
#from .utils import make_soup
from tqdm import tqdm
import time
import requests
from bs4 import BeautifulSoup
csv_names = ["game_result_2016.csv", "game_result_2017.csv", "game_result_2018.csv", "game_result_2019.csv"]
url_columns = ["batter1_url", "batter2_url", "batter3_url" , "batter4_url" , "batter5_url" 
, "batter6_url" , "batter7_url" , "batter8_url" , "batter9_url" , "st_url"]
path = './personal_achivements2.csv'

def make_soup(url: str):
    """
    Get soup object from the specified url.
    """
    sleep_time = 3
    time.sleep(sleep_time)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup

url_set = set()
for csv_name in csv_names:
    csv_df = pd.read_csv(csv_name)
    for url_column in url_columns:
        url_list = csv_df[url_column].values.tolist()
        url_set = url_set | set(url_list)

years_list = list(range(2010,2020))

dict_common_column_list = ["position", "pitching_and_batting", "height_and_weight", "birthday", "career", "draft"]
dict_batter_column_list = ["team_","match_", "plate_appearance_", "at_bat_", "run_", "hit_", "two_hit_", "three_hit_"
, "homerun_", "total_base_", "rbi_", "steal_", "steal_death_", "sacrifice_bunt_", "sacrifice_fly_"
, "four_balls_", "dead_ball_", "strikeout_", "double_play_", "batting_ave_", "slugging_ave_", "on_base_ave_"]
dict_pitcher_column_list = ["pitching_appearance_", "win_", "lose_", "save_", "hold_", "hold_point_"
, "complete_game_", "shutout_", "no_four_balls_", "win_rate_", "batter_", "time_", "time_decimal_", "give_up_hit_"
, "give_up_home_run_", "give_four_balls_", "give_dead_ball_", "get_strikeout_", "wild_pitch_", "boke_"
, "give_run_", "give_responsible_run_", "earned_run_ave_"]
for url in tqdm(url_set):
    result_dict = {}
    soup = make_soup(url)
    result_dict['url'] = url
    result_dict['name'] = soup.find("li", id="pc_v_name").text.replace(" ","").replace("\r","").replace("\n","")
    for dict_name in dict_common_column_list:
        result_dict[dict_name] = "-"
    td_common_soup_list = soup.find("section", id="pc_bio").find_all("td")
    for dict_name, td in zip(dict_common_column_list[len(dict_common_column_list)-len(td_common_soup_list):], td_common_soup_list):
        result_dict[dict_name] = td.text.replace(" ","").replace("\r","").replace("\n","")
        if result_dict[dict_name] == "":
            result_dict[dict_name] = "-"
    for year in years_list:
        for dict_name in dict_batter_column_list + dict_pitcher_column_list:
            if dict_name == "time_decimal_":
                continue
            result_dict[dict_name+str(year)] = "-"
    batter_table_id_name = "tablefix_b"
    pitcher_table_id_name = "tablefix_p"
    batter_soup = soup.find("table", id=batter_table_id_name)
    pitcher_soup = soup.find("table", id=pitcher_table_id_name)
    if batter_soup:
        tr_batter_soup_list = batter_soup.find_all("tr", class_="registerStats") 
        for tr in tr_batter_soup_list:
            tr_year = tr.find("td", class_="year").text.replace(" ","").replace("\r","").replace("\n","")
            if not int(tr_year) in years_list:
                continue
            td_all = tr.find_all("td")
            result_dict[dict_batter_column_list[0]+tr_year] = td_all[1].text.replace("　","")
            for dict_name, td in zip(dict_batter_column_list[1:], td_all[2:]):
                result_dict[dict_name+tr_year] = td.text
    if pitcher_soup:
        tr_pitcher_soup_list = pitcher_soup.find_all("tr", class_="registerStats")
        for tr in tr_pitcher_soup_list:
            tr_year = tr.find("td", class_="year").text.replace(" ","").replace("\r","").replace("\n","")         
            if not int(tr_year) in years_list:
                continue
            td_all = tr.find_all("td")
            for dict_name, td in zip(dict_pitcher_column_list, td_all[2:]):
                if dict_name == "time_decimal_":
                    continue
                result_dict[dict_name+tr_year] = td.text.replace(" ","").replace("\r","").replace("\n","")
    print(result_dict)
    result_df = pd.DataFrame(result_dict.values(), index=result_dict.keys()).T
    if os.path.exists(path):
        result_df.to_csv(path, mode='a', index=False, header=None)
    else:
        result_df.to_csv(path, mode='a', index=False)

        
        
        
