"""
This file contains the code related to the Spotify Web API & Open AI API calls 
"""

import random
from openai import OpenAI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import streamlit as st

from utils.functions import get_web_api_variables
from utils.constants import REDIRECT_URL, SCOPE



def generate_auth_url():
    """
    Generate authorization URL
    
    Inputs: None
    
    Returns:
            auth_url (str): authorization URL for users
            auth_manager (SpotifyOAuth Instance): SpotifyOAuth Instance
    """
    CLIENT_ID, CLIENT_SECRET = get_web_api_variables()
    

    auth_manager = SpotifyOAuth(client_id=CLIENT_ID,
                                client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URL,
                                scope=SCOPE)
    
    # Generate authorization URL from SpotifyOAuth instance
    auth_url = auth_manager.get_authorize_url()
    
    return auth_url, auth_manager


def get_access_token(auth_manager, redirect_url):
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
    access_token = access_token_info['access_token']
    
    return access_token


def get_random_genre_seed(spotipy_instance):
    """
    Fetch all available Spotify Genres and grab a random genre seed for the 
    "Surprise Me!" option for users
    
    Inputs:
        spotipy_instance: Spotipy
    
    Returns:
        random_genre (str): Randomly selected genre
    """
    genres = spotipy_instance.recommendation_genre_seeds()
 
    random_genre = random.choice(genres['genres'])
    
    return random_genre

    
def get_user_top_artists(spotipy_instance):
    """
    
    Inputs:
        spotipy_instance:  
    
    Returns:
        top_artists (list): List of the user's top artists' SpotifyIDs
    """ 
    top_artists = spotipy_instance.current_user_top_artists(limit=5)
    
    seed_artists = [artist["id"] for artist in top_artists["items"]]
    
    return seed_artists

#NOTE: MAX 5 TRACKS PER RECOMMENDATION, MUST BE SPLIT FOR LARGER EXAMPLES
def get_user_top_tracks(spotipy_instance):
    """
    Display user's top tracks using the spotipy instance
    
    Inputs:
        spotipy_instance: 
    
    Returns: None, modifies the streamlit app in-place
    """
    
    # Retrieves the user's top tracks using spotipy
    top_tracks = spotipy_instance.current_user_top_tracks(limit=5)

    seed_tracks = [track["uri"] for track in top_tracks["items"]]
    
    return seed_tracks
       

# TODO: additional functionality that interacts with spotify web api and OpenAI to create playlist recommendations

def extract_track_info(raw_track_info):
    """
    
    Inputs:
        raw_track_info:
    
    Returns: 
        track_uris
        track_names:
    """
    track_uris = []
    track_names = []
    for track in raw_track_info["tracks"]:
        track_name = track["name"]
        
        artists = ', '.join(artist['name'] for artist in track['artists'])
        

        track_names.append(f"{track_name} - {artists}")
        

        track_uris.append(track["uri"])
        
        
    return (track_uris, track_names)

#TODO: LIMIT INTAKE FOR RECOMMENDATIONS TO 5 SONGS/ARTISTS then set the recommendations to LIMIT to return 1- 20 songs
def generate_song_recommendations(spotipy_instance, num_tracks, seed_tracks=None, seed_artists=None, seed_genres=None):
    """
    Generates song recommendations for the user based on the provided seed.
    
    Inputs:
        spotipy_instance: An instance of the Spotipy library authenticated with Spotify.
        seed_tracks (list): List (or list of lists) of track URIs for seed tracks.
        seed_artists (list): List (or list of lists) of artist IDs for seed artists.
        seed_genres (list): List with a single genre seed 
        
    Returns:
    """
    recommendations = spotipy_instance.recommendations(seed_tracks=seed_tracks, seed_artists=seed_artists, seed_genres=seed_genres, limit=num_tracks)
    
    processed_uris, processed_names = extract_track_info(recommendations)
    
    return (processed_uris, processed_names)

def generate_recommendations(user_selection, num_tracks, spotipy_instance):
    """
    Generates song recommendations based on the user_input 
    
    Inputs:
        user_selection (str): User's selection of the type of recommendations
        num_tracks (int): The number of tracks for the user's recommendation
        spotipy_instance: 
    
    Returns:
            recommendations (): Song recommendations for the user based on
                their input
    
    """
    
    if user_selection == "tracks":
        seed_tracks = get_user_top_tracks(spotipy_instance)
        processed_uris, processed_names = generate_song_recommendations(spotipy_instance, seed_tracks=seed_tracks, num_tracks=num_tracks)
    elif user_selection == "artists":
        seed_artists = get_user_top_artists(spotipy_instance)
        processed_uris, processed_names = generate_song_recommendations(spotipy_instance, seed_artists=seed_artists, num_tracks=num_tracks)
    else:
        seed_genres=[user_selection]
        st.text(f"✨ Your random genre is {seed_genres[0]}✨ Enjoy!!")
        processed_uris, processed_names = generate_song_recommendations(spotipy_instance, seed_genres=seed_genres, num_tracks=num_tracks)
    
    return (processed_uris, processed_names)