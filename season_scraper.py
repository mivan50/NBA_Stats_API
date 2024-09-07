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

    headers = [th.getText() for th in table.find('thead').find_all('th')][:len(table.find('thead').find_all('th'))-1]

    data = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        if len(cells) - 1 == len(headers):
            cell_data = [cell.getText() for cell in cells][:len(cells) - 1]
            data.append(cell_data)

    df = pd.DataFrame(data, columns=headers)

    return df.to_dict(orient='records')


def get_season_leaders(p_r_a, rs_or_p):

    if rs_or_p == "playoffs":
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_season_p.html'
    else:
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_season.html'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', {'id': 'stats_NBA'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.getText() for cell in cells][1:]
        # Remove trailing '*' from names
        if row_data:
            row_data = [item.rstrip('*') for item in row_data]
        data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df.to_dict(orient='records')


def get_career_leaders(p_r_a, rs_or_p):
    if rs_or_p == "playoffs":
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_career_p.html'
    else:
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_career.html'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', {'id': 'nba'})
    rows = table.find_all('tr')

    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    # Extract row data while ensuring only rows with the correct number of columns are processed
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) - 1 == len(headers):
            row_data = [cell.getText() for cell in cells][1:]
            row_data[0] = row_data[0].strip().rstrip('*')
            data.append(row_data)

    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df.to_dict(orient='records')


def get_team_roster_year(team, year):
    url = f'https://www.basketball-reference.com/teams/{team}/{year}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', {'id': 'roster'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.getText() for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    df['Player'] = df['Player'].str.replace(r'\s*\(TW\)', '', regex=True)
    df['Birth'] = df['Birth'].str.strip().str[-2:]

    return df.to_dict(orient='records')
