from flask import Flask, jsonify
from season_scraper import fetch_season_data

app = Flask(__name__)


@app.route('/player/<first_name>/<last_name>/<year>/stats/season', methods=['GET'])
def get_season_stats(first_name, last_name, year):
    try:
        # Call the function to fetch data with the given parameters
        data = fetch_season_data(first_name, last_name, year)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
