"""
This file contains the code related to the Spotify Web API & Open AI API calls 
"""

from spotipy.oauth2 import SpotifyOAuth
from utils.constants import REDIRECT_URL, SCOPE
from utils.functions import get_web_api_variables


def generate_auth_url():
    """
    Generate authorization URL

    Inputs: None

    Returns:
            auth_url (str): authorization URL for users
            auth_manager (SpotifyOAuth Instance): SpotifyOAuth Instance
    """
    CLIENT_ID, CLIENT_SECRET = get_web_api_variables()

    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope=SCOPE,
        show_dialog=True,
    )

    auth_url = auth_manager.get_authorize_url()

    return auth_url, auth_manager


def retrieve_access_token(auth_manager, redirect_url):
    """
    Retrieves the Spotify Web API access token from redirect URL

    Inputs:
        auth_manager (SpotifyOAuth): SpotifyOAuth instance
        redirect_url (str): URL that user's are redirected to containing
            the access token

    Returns:
        access_token (str): Spotify Web API access token
    """
    parsed_code = auth_manager.parse_response_code(redirect_url)

    access_token_info = auth_manager.get_access_token(parsed_code)
    access_token = access_token_info["access_token"]

    return access_token
