# Basketball Reference Web Scraper API

## Overview
This project provides a simple API for retrieving basketball statistics from [Basketball Reference](https://www.basketball-reference.com). The API uses web scraping techniques to extract game logs, season stats, and other relevant data for specific players and returns it in JSON format. This allows users to easily retrieve and manipulate the data for further analysis or display.

## Features
- Retrieves team rosters, draft data and player stats
- API returns data in JSON format for easy integration into other applications
- Provides informative error responses (e.g., 404 for not found, 500 for server issues, and 429 for rate limiting)
- Limits the number of requests per user in a specified time period to prevent abuse and ensure fair access
- Uses BeautifulSoup for scraping and parsing HTML data from Basketball Reference’s web pages

## Libraries/Frameworks Used 
- Flask
- pandas
- beautifulsoup4

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
