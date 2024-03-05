"""
This file contains utility functions used throughout the project
"""

import os

from dotenv import load_dotenv


def get_web_api_variables():
    """
    Retrieves the Spotify Web API's credentials from the environment variables

    Inputs: None

    Returns:
            CLIENT_ID (str): Spotify Web API CLIENT_ID
            CLIENT_SECRET (str): Spotify Web API CLIENT_SECRET
    """

    load_dotenv()

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    return CLIENT_ID, CLIENT_SECRET


def get_openai_api_key():
    """
    Retrieves the OpenAI API credentials from the environment variables

    Inputs: None

    Returns:
        OPENAI_API_KEY (str): OPENAI API key
    """
    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    return OPENAI_API_KEY


def save_spotify_access_token_to_env(access_token):
    """
    Saves the Spotify access token to the .env file

    Inputs:
        access_token (str): Spotify access_token

    Returns: None, modifies the .env file to add the Spotify token
    """
    token_present = False
    file_path = "utils/.env"

    with open(file_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("SPOTIFY_TOKEN"):
            lines[i] = f"\SPOTIFY_TOKEN={access_token}"
            token_present = True
            break

    if not token_present:
        lines.append(f"\nSPOTIFY_TOKEN={access_token}")

    with open(file_path, "w") as f:
        f.writelines(lines)
        

def cleanup():
    """
    Removes the local .cache file containing the user's Spotify access token

    Inputs: None

    Returns: None, removes the developer's .cache file
    """
    cache_file = '.cache'
    if os.path.exists(cache_file):
        os.remove(cache_file)
