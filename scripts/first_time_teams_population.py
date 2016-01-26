#!/usr/local/bin/python

import os
import sys
import json
from pymongo import MongoClient


''' Create Initial Connection '''
client = MongoClient('localhost', 27017)

db = client['nba_stats']

''' Read Teams JSON to variable '''

teams_data_file = open(os.path.join(sys.path[0], "teams_data.json"), "r")
data_as_json = json.load(teams_data_file)


'''enrich with unique identifier and populate if not already present'''
print "Current Teams in dataset: " + str(db.teams.count())
if db.teams.count() == 0:
    for team in data_as_json:
        team["_id"] = team["abbreviation"]
        print db.teams.insert(team)

# __end__
