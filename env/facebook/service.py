import requests
import urllib.parse

APP_ID = ".."
APP_SECRET = ".."
REDIRECT_URI = "http://localhost:8000/facebook/callback"

def get_facebook_login_url():
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "email",
        "response_type": "code"
    }
    return f"https://www.facebook.com/v17.0/dialog/oauth?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code: str):
    token_url = "https://graph.facebook.com/v17.0/oauth/access_token"
    params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "client_secret": APP_SECRET,
        "code": code
    }
    response = requests.get(token_url, params=params)
    return response.json()["access_token"]

def get_facebook_user_info(access_token: str):
    user_info_url = "https://graph.facebook.com/me"
    params = {
        "fields": "id,name,email",
        "access_token": access_token
    }
    response = requests.get(user_info_url, params=params)
    return response.json()
