import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load in environment variables
load_dotenv()
username = os.getenv("username")
password = os.getenv("password")

# The required URLs to scrapey scrape
login_url = "https://myaccount.nytimes.com/auth/login?redirect_uri=https%3A%2F%2Fwww.nytimes.com%2Fpuzzles" \
            "%2Fleaderboards%3Fauth%3Dlogin-email%26login%3Demail&response_type=cookie&client_id=games&application" \
            "=crosswords&asset=navigation-bar "
board_url = "https://www.nytimes.com/puzzles/leaderboards"

# Run the session
with requests.Session() as session:

    # Do a GET request to pull initial form tokens
    scrape_login = session.get(login_url)

    # The token is located inside a div component with an attribute data-auth-options
    soup = BeautifulSoup(scrape_login.text, 'html.parser')
    auth_opts = soup.div['data-auth-options']

    # The attribute is huge and we only need a very specific token.  Brute forcing it into various lines
    broken_string = auth_opts.split(",")
    search_param = "authToken"
    auth_token = ""

    # Grab the single line that we need
    for item in broken_string:
        if search_param in item:
            auth_token = item
            auth_token = auth_token.split(":")[1]

    # Now you can login
    login = session.post(
        login_url,
        data={
            "username": username,
            "password": password,
            "remember_me": "Y",
            "auth_token": auth_token,
            "form_view": "login"
        },
        headers=dict(referer=login_url, )
    )

    # Successful?
    print(login.ok)
    print(login.status_code)

    # Hopefully you are logged in and can grab the leaderboard info
    leaderboard = session.get(board_url, headers=dict(referer=board_url))

    # Successful?
    print(leaderboard.ok)
    print(leaderboard.status_code)

    # This is the final data to parse
    soup = BeautifulSoup(leaderboard.text, 'html.parser')

