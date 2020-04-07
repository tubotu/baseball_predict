import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time
from tqdm import tqdm

BASE_URL = 'http://npb.jp'
DETAIL_URL = 'box.html'
DETAIL_URL_2 = '/games/'
YEARS = ["2016","2017"]
DETAIL_URL_3 = '/schedule_'
MONTHS = ["03", "04", "05", "06", "07", "08", "09", "10"]
DETAIL_URL_4 = '_detail.html'

def make_soup(url: str):
  """
  Get soup object from the specified url.
  """
  sleep_time = 3
  time.sleep(sleep_time)
  res = requests.get(url)
  soup = BeautifulSoup(res.content, 'html.parser')
  return soup


def get_game_url(soup):
  a_list = soup.find("div", id="schedule_detail").find_all("a")
  url_list = [BASE_URL + a.get("href") + DETAIL_URL for a in a_list if a.find("div", class_="cancel") is None]
  return url_list


def soup_to_dataframe(url, soup, path):
  """
  """
  result_dict = {}
  game_tit = soup.find("div", class_="game_tit")
  result_dict["url"] = url
  result_dict["date"] = game_tit.find("time").text
  home_team = soup.find("tr", class_="bottom")
  result_dict["home_team"] = home_team.find("span").text
  away_team = soup.find("tr", class_="top")
  result_dict["away_team"] = away_team.find("span").text
  result_dict["place"] = game_tit.find("span", class_="place").text
  result_dict["runs"] = home_team.find("td", class_="total-1").text
  result_dict["away_runs"] = away_team.find("td", class_="total-1").text
  result_dict["home_victory"] = 1 if result_dict["runs"] > result_dict["away_runs"] else 0
  result_dict["home_hits"] = home_team.find_all("td", class_="total-2")[0].text
  result_dict["away_hits"] = away_team.find_all("td", class_="total-2")[0].text
  result_dict["home_errors"] = home_team.find_all("td", class_="total-2")[1].text
  result_dict["away_errors"] = away_team.find_all("td", class_="total-2")[1].text
  result_dict["game_info"] = soup.find("div", class_="line-score").find("p", class_="game_info").text.replace('\n','')
  for home_or_away in ['home_', 'away_']:
    if home_or_away == 'home_':
      batter_all_result = soup.find_all("div", class_="scroll_wrapper table_score table_batter")[1].find("tbody").find_all("tr")
    else:
      batter_all_result = soup.find_all("div", class_="scroll_wrapper table_score table_batter")[0].find("tbody").find_all("tr")
    batters_columns_list = [
      ['batter1_name', 'batter1_url', 'batter1_at_bat', 'batter1_hit', 'batter1_two_hit', 'batter1_three_hit', 'batter1_homerun'
      , 'batter1_rbi', 'batter1_steal', 'batter1_strikeout', 'batter1_four_balls', 'batter1_dead_ball', 'batter1_position']
      , ['batter2_name', 'batter2_url', 'batter2_at_bat', 'batter2_hit', 'batter2_two_hit', 'batter2_three_hit', 'batter2_homerun'
      , 'batter2_rbi', 'batter2_steal', 'batter2_strikeout', 'batter2_four_balls', 'batter2_dead_ball', 'batter2_position']
      , ['batter3_name', 'batter3_url', 'batter3_at_bat', 'batter3_hit', 'batter3_two_hit', 'batter3_three_hit', 'batter3_homerun'
      , 'batter3_rbi', 'batter3_steal', 'batter3_strikeout', 'batter3_four_balls', 'batter3_dead_ball', 'batter3_position']
      , ['batter4_name', 'batter4_url', 'batter4_at_bat', 'batter4_hit', 'batter4_two_hit', 'batter4_three_hit', 'batter4_homerun'
      , 'batter4_rbi', 'batter4_steal', 'batter4_strikeout', 'batter4_four_balls', 'batter4_dead_ball', 'batter4_position']
      , ['batter5_name', 'batter5_url', 'batter5_at_bat', 'batter5_hit', 'batter5_two_hit', 'batter5_three_hit', 'batter5_homerun'
      , 'batter5_rbi', 'batter5_steal', 'batter5_strikeout', 'batter5_four_balls', 'batter5_dead_ball', 'batter5_position']
      , ['batter6_name', 'batter6_url', 'batter6_at_bat', 'batter6_hit', 'batter6_two_hit', 'batter6_three_hit', 'batter6_homerun'
      , 'batter6_rbi', 'batter6_steal', 'batter6_strikeout', 'batter6_four_balls', 'batter6_dead_ball', 'batter6_position']
      , ['batter7_name', 'batter7_url', 'batter7_at_bat', 'batter7_hit', 'batter7_two_hit', 'batter7_three_hit', 'batter7_homerun'
      , 'batter7_rbi', 'batter7_steal', 'batter7_strikeout', 'batter7_four_balls', 'batter7_dead_ball', 'batter7_position']
      , ['batter8_name', 'batter8_url', 'batter8_at_bat', 'batter8_hit', 'batter8_two_hit', 'batter8_three_hit', 'batter8_homerun'
      , 'batter8_rbi', 'batter8_steal', 'batter8_strikeout', 'batter8_four_balls', 'batter8_dead_ball', 'batter8_position']
      , ['batter9_name', 'batter9_url', 'batter9_at_bat', 'batter9_hit', 'batter9_two_hit', 'batter9_three_hit', 'batter9_homerun'
      , 'batter9_rbi', 'batter9_steal', 'batter9_strikeout', 'batter9_four_balls', 'batter9_dead_ball', 'batter9_position']
    ]
    batter_1_9_result = []
    batter_others_result = []
    for batter_result in batter_all_result:
      td_list = batter_result.find_all("td")
      if re.match('\d',td_list[0].text):
        batter_1_9_result.append(batter_result)
      else:
        batter_others_result.append(batter_result)

    atbat_aggregate_word_list = ["２", "３", "本", "三　振", "四　球", "死　球"]
    for batter_result, batter_columns in zip(batter_1_9_result, batters_columns_list):
      td_list = batter_result.find_all("td")
      result_dict[home_or_away + batter_columns[0]] = td_list[2].text
      result_dict[home_or_away + batter_columns[1]] = 'http://npb.jp' + td_list[2].a.get("href")
      result_dict[home_or_away + batter_columns[2]] = td_list[3].text
      result_dict[home_or_away + batter_columns[3]] = td_list[5].text
      atbat_aggregate_list = [batter_columns[4], batter_columns[5], batter_columns[6], batter_columns[9], batter_columns[10], batter_columns[11]]
      for atbat_aggregate in atbat_aggregate_list:
        result_dict[home_or_away + atbat_aggregate] = 0
      for atbat_detail in td_list[8:]:
        for atbat_aggregate, atbat_aggregate_word in zip(atbat_aggregate_list, atbat_aggregate_word_list):
          if re.search(atbat_aggregate_word, atbat_detail.text):
            result_dict[home_or_away + atbat_aggregate] += 1
      result_dict[home_or_away + batter_columns[7]] = td_list[6].text
      result_dict[home_or_away + batter_columns[8]] = td_list[7].text
      result_dict[home_or_away + batter_columns[12]] = td_list[1].text.replace('(','').replace(')','')
    
    atbat_aggregate_list = ['other_batters_at_bat', 'other_batters_hit', 'other_batters_steal', 'other_batters_strikeout']
    atbat_aggregate_list2 = ['other_batters_two_hit', 'other_batters_three_hit', 'other_batters_homerun'
    , 'other_batters_strikeout', 'other_batters_four_balls', 'other_batters_dead_ball']
    for atbat_aggregate in atbat_aggregate_list + atbat_aggregate_list2:
      result_dict[home_or_away + atbat_aggregate] = 0
    for batter_result in batter_others_result:
      td_list = batter_result.find_all("td")
      result_dict[home_or_away + atbat_aggregate_list[0]] += int(td_list[3].text)
      result_dict[home_or_away + atbat_aggregate_list[1]] += int(td_list[5].text)
      result_dict[home_or_away + atbat_aggregate_list[2]] += int(td_list[6].text)
      result_dict[home_or_away + atbat_aggregate_list[3]] += int(td_list[7].text)
      for atbat_detail in td_list[8:]:
        for atbat_aggregate, atbat_aggregate_word in zip(atbat_aggregate_list2, atbat_aggregate_word_list):
          if re.search(atbat_aggregate_word, atbat_detail.text):
            result_dict[home_or_away + atbat_aggregate] += 1

    if home_or_away == 'home_':
      pitcher_all_result = soup.find_all("div", class_="scroll_wrapper table_score table_pitcher")[1].find("tbody").find_all("tr")
    else:
      pitcher_all_result = soup.find_all("div", class_="scroll_wrapper table_score table_pitcher")[0].find("tbody").find_all("tr")
    starting_pitcher_result_list = pitcher_all_result[0].find_all("td")
    result_dict[home_or_away + "st_name"] = starting_pitcher_result_list[1].text
    result_dict[home_or_away + "st_url"] = 'http://npb.jp' + starting_pitcher_result_list[1].a.get("href")
    
    st_columns = ['st_pitches', 'st_batters', 'st_times', 'st_times_decimal', 'st_hits', 'st_homerun', 'st_four_balls'
    , 'st_dead_ball', 'st_strikeout', 'st_wild_pitches', 'st_boke', 'st_runs', 'st_responsible_runs']
    for st_column, starting_pitcher_result in zip(st_columns, starting_pitcher_result_list[2:]):
      if(st_column == 'st_times'):
        tr = starting_pitcher_result.find("tr")
        result_dict[home_or_away + st_column] = tr.find("th").text + tr.find("td").text
        continue 
      if(st_column == 'st_times_decimal'):
        continue
      result_dict[home_or_away + st_column] = starting_pitcher_result.text
    
    re_columns = ['re_pitches', 're_batters', 're_times', 're_times_decimal', 're_hits', 're_homerun', 're_four_balls'
    , 're_dead_ball', 're_strikeout', 're_wild_pitches', 're_boke', 're_runs', 're_responsible_runs']
    result_dict[home_or_away + 're_pitchers'] = len(pitcher_all_result[2::2])
    for re_column in re_columns:
      result_dict[home_or_away + re_column] = 0
    for relief_pitchers_result in pitcher_all_result[2::2]:
      relief_pitcher_result_list = relief_pitchers_result.find_all("td")
      for re_column, relief_pitcher_result in zip(re_columns, relief_pitcher_result_list[2:]):
        if(re_column == 're_times'):
          tr = relief_pitcher_result.find("tr")
          result_dict[home_or_away + re_column] = tr.find("th").text + tr.find("td").text
          continue 
        if(re_column == 're_times_decimal'):
          continue
        result_dict[home_or_away + re_column] += int(relief_pitcher_result.text)
  result_df = pd.DataFrame(result_dict.values(), index=result_dict.keys()).T
  if os.path.exists(path):
    result_df.to_csv(path, mode='a', index=False, header=None)
  else:
    result_df.to_csv(path, mode='a', index=False)
  
for year in YEARS:
  CSV_NAME = './game_result_' + year + '.csv'
  for month in MONTHS:
    print(month+"月")
    url_list = get_game_url(make_soup(BASE_URL + DETAIL_URL_2 + year + DETAIL_URL_3 + month + DETAIL_URL_4))
    for url in tqdm(url_list):
      soup_to_dataframe(url, make_soup(url), CSV_NAME)
