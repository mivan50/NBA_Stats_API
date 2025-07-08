import httpx
from bs4 import BeautifulSoup
import pandas as pd

def get_html(url):
    headers = {
        "user-agent": "Mozilla/5.0"
    }

    with httpx.Client(headers=headers, follow_redirects=True) as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.text
        return None


def get_player_season_stats(first_name, last_name, year):
    first_letter = last_name[0].lower()
    player_code = last_name[:5].lower() + first_name[:2].lower() + "01"
    url = f'https://www.basketball-reference.com/players/{first_letter}/{player_code}/gamelog/{year}/'

    html = get_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'player_game_log_reg'})
    if table is None:
        return None

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
    return df.to_dict(orient='records')

def get_player_career_stats(first_name, last_name):
    first_letter = last_name[0].lower()
    player_code = last_name[:5].lower() + first_name[:2].lower() + "01"
    url = f'https://www.basketball-reference.com/players/{first_letter}/{player_code}.html'

    html = get_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'per_game_stats'})
    if table is None:
        return None

    rows = table.find('tbody').find_all('tr')
    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    data = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        row_data = [cell.getText() for cell in cells][1:]
        if len(row_data) == len(headers):
            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    return df.to_dict(orient='records')

def get_season_leaders(p_r_a, rs_or_p):
    if rs_or_p == "playoffs":
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_season_p.html'
    else:
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_season.html'

    html = get_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats_NBA'})
    if table is None:
        return None

    rows = table.find('tbody').find_all('tr')
    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.getText() for cell in cells][1:]
        if row_data:
            row_data = [item.rstrip('*') for item in row_data]
            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    return df.to_dict(orient='records')

def get_career_leaders(p_r_a, rs_or_p):
    if rs_or_p == "playoffs":
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_career_p.html'
    else:
        url = f'https://www.basketball-reference.com/leaders/{p_r_a}_per_g_career.html'

    html = get_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'nba'})
    if table is None:
        return None

    rows = table.find_all('tr')
    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) - 1 == len(headers):
            row_data = [cell.getText() for cell in cells][1:]
            row_data[0] = row_data[0].strip().rstrip('*')
            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    return df.to_dict(orient='records')

def get_team_roster_year(team, year):
    url = f'https://www.basketball-reference.com/teams/{team}/{year}.html'

    html = get_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'roster'})
    if table is None:
        return None

    rows = table.find('tbody').find_all('tr')
    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]

    data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.getText().strip() for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    df['Player'] = df['Player'].str.replace(r'\s*\(TW\)', '', regex=True)
    df['Birth'] = df['Birth'].str.strip().str[-2:]

    return df.to_dict(orient='records')

def get_nba_draft_year(year):
    url = f'https://www.basketball-reference.com/draft/NBA_{year}.html'

    html = get_html(url)
    if html is None:
        return None

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'stats'})
    if table is None:
        return None

    rows = table.find('tbody').find_all('tr')
    headers = [th.getText() for th in table.find('thead').find_all('tr')[1].find_all('th')][1:][:4]

    data = []
    for row in rows:
        row_classes = row.get('class', [])
        if 'over_header thead' in row_classes or 'thead' in row_classes:
            continue

        cells = row.find_all('td')
        row_data = [cell.getText().strip() for cell in cells][:4]
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)
    return df.to_dict(orient='records')
