import requests
import json
import datetime

# base_team_data_url = 'http://stats.nba.com/stats/teaminfocommon'
# payload_for_team_data = {"LeagueID": '00', "SeasonType": "Regular Season",
#                          "Season": "2015-16", "TeamId": None}

base_score_board_url = 'http://stats.nba.com/stats/scoreboardV2'
payload_for_board = {"LeagueID": '00', "DayOffset": "0", "gameDate": None}

headers = {'User-Agent': 'InOrOut/AppleWebKit (KHTML, like Gecko) Chrome'}


# def query_api(team_id):
#     payload_for_team_data["TeamId"] = team_id
#     results = requests.get(base_team_data_url, headers=headers,
#                            params=payload_for_team_data)
#     if results.status_code != 200:
#         print(results.text + '\n' + results.headers)
#         return json.dumps({'error': 'Failed to query data.'})
#     else:
#         return json.loads(results.text)


# def position_from_results(common_info):
#     ## Doom to break, but test for now
#     position = common_info['resultSets'][0]['rowSet'][0][11]
#     return position


def data_for_upcomings(mongo_client, team_data):
    today_date_as_int = int(datetime.date.today().strftime('%Y%m%d'))
    team_id = team_data['teamId']
    query = {"$and": [
            {"$or": [{"team_home_id": team_id}, {"team_visit_id": team_id}]},
            {"date_as_int": {"$gt": today_date_as_int - 1}}
            ]}

    print(query)
    games_left = mongo_client['nba_stats']['schedule'].find(query).count()

    return {"date": today_date_as_int, "games_left": games_left}


def score_board():
    payload_for_board['gameDate'] = datetime.date.today().strftime('%m/%d/%Y')

    results = requests.get(base_score_board_url, headers=headers,
                           params=payload_for_board)
    if results.status_code != 200:
        print(results.text + '\n' + results.headers)
        return json.dumps({'error': 'Failed to query data.'})
    else:
        team_position = manage_score_board_results(json.loads(results.text))
        return team_position


def manage_score_board_results(results):
    east_results = results['resultSets'][4]['rowSet']
    west_results = results['resultSets'][5]['rowSet']
    data = {}
    for pos, team in enumerate(east_results):
        data[team[0]] = {'name': team[5], 'currentPosition': pos + 1,
                         'conference': team[4], 'home_record': team[10],
                         'away_record': team[11]}

    for pos, team in enumerate(west_results):
        data[team[0]] = {'name': team[5], 'currentPosition': pos + 1,
                         'conference': team[4], 'home_record': team[10],
                         'away_record': team[11]}
    return data

#__END__
