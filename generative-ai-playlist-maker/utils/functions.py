"""
This file contains utility functions used throughout the project
"""

from dotenv import load_dotenv
import os


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