from flask import Flask, jsonify
from season_scraper import *

app = Flask(__name__)


@app.route('/player/<first_name>/<last_name>/<year>/stats/season', methods=['GET'])
def get_season_stats(first_name, last_name, year):
    try:
        # Call the function to fetch season stats
        data = get_player_season_stats(first_name, last_name, year)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/player/<first_name>/<last_name>/stats/career', methods=['GET'])
def get_career_stats(first_name, last_name):
    try:
        # Call the function to fetch career stats
        data = get_player_career_stats(first_name, last_name)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<pra>/<rs_p>/leaders/career', methods=['GET'])
def get_career_pra_leaders(pra, rs_p):
    try:
        # Call the function to fetch career stats
        data = get_career_leaders(pra, rs_p)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<pra>/<rs_p>/leaders/season', methods=['GET'])
def get_season_pra_leaders(pra, rs_p):
    try:
        # Call the function to fetch career stats
        data = get_season_leaders(pra, rs_p)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<team>/<year>/roster', methods=['GET'])
def get_team_roster(team, year):
    try:
        # Call the function to fetch career stats
        data = get_team_roster_year(team, year)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
