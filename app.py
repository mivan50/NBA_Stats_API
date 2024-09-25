from flask import Flask, jsonify
from web_scraper_functions import *

app = Flask(__name__)


@app.route('/player/<first_name>/<last_name>/<year>/stats/season', methods=['GET'])
def get_season_stats(first_name, last_name, year):
    try:
        # Call the function to fetch season stats
        data = get_player_season_stats(first_name, last_name, year)
        if data is None:
            return jsonify({'error': 'Player not found or invalid URL'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/player/<first_name>/<last_name>/stats/career', methods=['GET'])
def get_career_stats(first_name, last_name):
    try:
        # Call the function to fetch career stats
        data = get_player_career_stats(first_name, last_name)
        if data is None:
            return jsonify({'error': 'Player not found or invalid URL'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<pra>/<rs_p>/leaders/career', methods=['GET'])
def get_career_pra_leaders(pra, rs_p):
    try:
        # Call the function to fetch career leaders
        data = get_career_leaders(pra, rs_p)
        if data is None:
            return jsonify({'error': 'Leaders not found or invalid URL'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<pra>/<rs_p>/leaders/season', methods=['GET'])
def get_season_pra_leaders(pra, rs_p):
    try:
        # Call the function to fetch season leaders
        data = get_season_leaders(pra, rs_p)
        if data is None:
            return jsonify({'error': 'Leaders not found or invalid URL'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<team>/<year>/roster', methods=['GET'])
def get_team_roster(team, year):
    try:
        # Call the function to fetch team roster
        data = get_team_roster_year(team, year)
        if data is None:
            return jsonify({'error': 'Team not found or invalid URL'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/NBA/<year>/draft', methods=['GET'])
def get_nba_draft(year):
    try:
        # Call the function to fetch NBA draft data
        data = get_nba_draft_year(year)
        if data is None:
            return jsonify({'error': 'Draft data not found or invalid URL'}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
