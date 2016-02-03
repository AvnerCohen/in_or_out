
import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from pymongo import MongoClient

from models import nba_api
from models import memoizer

app = Flask(__name__)

client = MongoClient('localhost', 27017)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.before_request
def print_route():
    print(request.url_rule)


@app.route('/')
def teams():
    teams = client['nba_stats']['teams'].find()
    team_with_positions = nba_api.score_board()
    memoizer.team_data_dict['teams'] = teams
    memoizer.team_data_dict['team_with_positions'] = team_with_positions

    return render_template('teams.html', teams=teams,
                           team_with_positions=team_with_positions)


@app.route('/in_or_out.json')
def in_or_out():
    team_arg = request.args.get('team')
    team = client['nba_stats']['teams'].find_one({"_id": team_arg})
    query_results = nba_api.data_for_upcomings(client, [team])

    return jsonify(query_results[team_arg])


@app.route('/upcoming_games_for_teams.json')
def upcoming_games_for_teams():
    teams_arg = request.args.get('teams').split(',')
    teams_data = client['nba_stats']['teams'].find({"_id": {"$in": teams_arg}})

    upcoming_games = nba_api.data_for_upcomings(client, teams_data)
    return jsonify(upcoming_games)


@app.context_processor
def helper_methods():
    def image_for_team(name):
        image_name = 'cha_hornets' if name == 'CHA' else name
        return '//i.cdn.turner.com/nba/nba/.element/img/1.0/logos/teamlogos_80x64/' + image_name.lower() + '.gif'

    return dict(image_for_team=image_for_team)


if __name__ == '__main__':
    app.run(debug=True)

# __END__
