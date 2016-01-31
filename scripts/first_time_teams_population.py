#!/usr/local/bin/python

import os
import sys
import json
from pymongo import MongoClient
from datetime import datetime


''' Create Initial Connection '''
client = MongoClient('localhost', 27017)

db = client['nba_stats']

''' Read Teams JSON to variable '''

teams_data_file = open(os.path.join(sys.path[0], "teams_data.json"), "r")
data_as_json = json.load(teams_data_file)
team_to_id_mapping = {}


'''enrich with unique identifier and populate if not already present'''
print("Current Teams in dataset: " + str(db.teams.count()))
do_insert = True if db.teams.count() == 0 else False
for team in data_as_json:
    team["_id"] = team["abbreviation"]
    team_to_id_mapping[team["abbreviation"]] = team["teamId"]
    db.teams.insert(team) if do_insert else None

'''Populate the full session schedule'''
schedule = open(os.path.join(sys.path[0], "game_schedule_2015-1016.json"), "r")
schedule_as_json = json.load(schedule)

for index, game in enumerate(schedule_as_json):
    game['team_visit_id'] = team_to_id_mapping[game['team_visit']]
    game['team_home_id'] = team_to_id_mapping[game['team_home']]
    game["_id"] = index
    date = datetime.strptime(game["date"], '%m/%d/%Y')
    game["date_as_int"] = int(date.strftime('%Y%m%d'))
    db.schedule.insert(game)

# __end__
