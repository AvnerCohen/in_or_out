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
    return render_template('teams.html', teams=teams)


@app.route('/in_or_out.json')
def in_or_out():
    team_arg = request.args.get('team')
    team = client['nba_stats']['teams'].find_one({"_id": team_arg})
    print team_arg
    team_id = team['teamId']
    results = nba_api.query_api(team_id)
    current_position = nba_api.position_from_results(results)
    return jsonify(currentPosition=current_position)

if __name__ == '__main__':
    app.run(debug=True)

# __END__
