import os
from flask import Flask, request, render_template, jsonify, send_from_directory
from pymongo import MongoClient

from models import nba_api

app = Flask(__name__)

client = MongoClient('localhost', 27017)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def teams():
    teams = client['nba_stats']['teams'].find()
    team_with_positions = nba_api.score_board()
    return render_template('teams.html', teams=teams, team_with_positions=team_with_positions)


@app.route('/in_or_out.json')
def in_or_out():
    team_arg = request.args.get('team')
    team = client['nba_stats']['teams'].find_one({"_id": team_arg})
    team_id = team['teamId']
    query_results = nba_api.query_api(team_id)
    if not query_results.get('error', False):
        current_position = nba_api.position_from_results(query_results)
        query_results = {"currentPosition": current_position}

    return jsonify(query_results)


@app.context_processor
def helper_methods():
    def image_for_team(name):
        image_name = 'cha_hornets' if name == 'CHA' else name
        return '//i.cdn.turner.com/nba/nba/.element/img/1.0/logos/teamlogos_80x64/' + image_name.lower() + '.gif'

    return dict(image_for_team=image_for_team)


if __name__ == '__main__':
    app.run(debug=True)

# __END__
