
import requests
import json
from datetime import datetime, timedelta
import memoizer

base_score_board_url = 'http://stats.nba.com/stats/scoreboardV2'
payload_for_board = {'LeagueID': '00', 'DayOffset': '0', 'gameDate': None}

headers = {'User-Agent': 'InOrOut/AppleWebKit (KHTML, like Gecko) Chrome'}


def data_for_upcomings(mongo_client, teams_data):
    today_date_as_int = int((datetime.now() - timedelta(days=2)).strftime('%Y%m%d'))
    results = {}
    for team_data in teams_data:
        team_id = team_data['teamId']
        query = {'$and': [
                {'$or': [{'team_home_id': team_id}, {'team_visit_id': team_id}]},
                {'date_as_int': {'$gt': today_date_as_int - 1}}
                ]}

        games_left = mongo_client['nba_stats']['schedule'].find(query).sort('date_as_int', 1)
        total_strength_score = 0
        this_team_pos = memoizer.team_data_dict['team_with_positions'][team_id]['currentPosition']
        stats = []
        game_dates = []
        game_dates_as_int = []
        vs_whom = []
        wins = 0
        for index, game in enumerate(games_left):
            other_side_id = game['team_home_id'] if game['team_visit_id'] == team_data['teamId'] else game['team_visit_id']
            other_side = memoizer.team_data_dict['team_with_positions'][other_side_id]
            total_strength_score += other_side['currentPosition']
            game_dates.append(game['date'])
            game_dates_as_int.append(game['date_as_int'])

            if this_team_pos > other_side['currentPosition']:
                wins = wins - 1
                state_for_game = wins
            elif this_team_pos <= other_side['currentPosition']:
                wins = wins + 3
                state_for_game = wins
            else:
                state_for_game = wins

            stats.append(state_for_game)
            vs_whom.append(other_side['name'])

        results[team_data['_id']] = {'date': today_date_as_int, 'games_left': games_left.count(),
                                     'total_strength_score': total_strength_score,
                                     'game_dates_as_int': '|'.join(map(str, game_dates_as_int)),
                                     'game_dates': "|".join(game_dates), 'stats': '|'.join(map(str, stats)),
                                     'vs_whom': "|".join(vs_whom),
                                     'name': team_data['teamName']}

    return results


def score_board():
    payload_for_board['gameDate'] = datetime.today().strftime('%m/%d/%Y')

    results = requests.get(base_score_board_url, headers=headers,
                           params=payload_for_board)
    if results.status_code != 200:
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
