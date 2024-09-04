import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_player_season_stats(first_name, last_name, year):
    # Build the player URL component
    first_letter = last_name[0].lower()
    player_code = last_name[:5].lower() + first_name[:2].lower() + "01"

    # Construct the full URL
    url = f'https://www.basketball-reference.com/players/{first_letter}/{player_code}/gamelog/{year}/'

    # Fetch and parse the page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', {'id': 'pgl_basic'})
    rows = table.find_all('tr')

    headers = [th.getText().strip() for th in table.find('thead').find_all('th')[1:]]
    headers[4] = "Loc"
    headers[6] = "Out"

    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == len(headers):
            data.append([cell.getText().strip() for cell in cells])

    df = pd.DataFrame(data, columns=headers)

    # Convert DataFrame to JSON format
    return df.to_dict(orient='records')


def get_player_career_stats(first_name, last_name):
    first_letter = last_name[0].lower()
    player_code = last_name[:5].lower() + first_name[:2].lower() + "01"

    url = f'https://www.basketball-reference.com/players/{first_letter}/{player_code}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', {'id': 'per_game'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    headers = [th.getText() for th in table.find('thead').find_all('th')][:30]

    data = []
    for row in rows:
        cells = row.find_all('td')
        season_year = row.find('th').getText()
        cell_data = [season_year] + [cell.getText() for cell in cells][:29]
        data.append(cell_data)

    df = pd.DataFrame(data, columns=headers)

    return df.to_dict(orient='records')