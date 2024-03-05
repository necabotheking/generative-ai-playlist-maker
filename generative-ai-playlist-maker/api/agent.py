"""
This file contains the LangChain ReAct AI agent and custom Spotify tools to interact with the Spotify Web API for the Streamlit app
"""
import os
import random

import spotipy
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.base import BaseTool
from langchain_community.chat_models import ChatOpenAI


class SpotifyTopTracksTool(BaseTool):
    """
    Tool that interacts with the SpotifyWeb API to fetch the user's top tracks then generates recommendations based on the top tracks.
    """

    name = "SpotifyTopTracksTool"
    description = "Tool that fetches the user's top tracks from Spotify and generates recommendations based on the top tracks."

    def _run(self, *args, **kwargs):
        token = os.getenv("SPOTIFY_TOKEN")
        if not token:
            raise ValueError("SPOTIFY_TOKEN environment variable is not set.")

        sp = spotipy.Spotify(auth=token)
        top_tracks = sp.current_user_top_tracks(limit=5)

        seed_tracks = [track["uri"] for track in top_tracks["items"]]

        recommendations = sp.recommendations(
            seed_tracks=seed_tracks,
            seed_artists=None,
            seed_genres=None,
            limit=20,
        )
        track_names = []

        for track in recommendations["tracks"]:
            track_name = track["name"]

            artists = ", ".join(artist["name"] for artist in track["artists"])

            track_names.append(f"{track_name} - {artists}")

        return track_names

    async def _arun(self, *args, **kwargs):
        """Use the SpotifyTopTracksTool asynchronously."""
        return self._run()


class SpotifyTopArtistsTool(BaseTool):
    """
    Tool that interacts with the SpotifyWeb API to fetch the user's top artists then generates recommendations based on the artists.
    """

    name = "SpotifyTopArtistsTool"
    description = "Tool that fetches the user's top artists from Spotify nd generates recommendations based on the top artists."

    def _run(self, *args, **kwargs):
        token = os.getenv("SPOTIFY_TOKEN")
        if not token:
            raise ValueError("SPOTIFY_TOKEN environment variable is not set.")

        sp = spotipy.Spotify(auth=token)

        top_artists = sp.current_user_top_artists(limit=5)

        seed_artists = [artist["id"] for artist in top_artists["items"]]

        recommendations = sp.recommendations(
            seed_tracks=None,
            seed_artists=seed_artists,
            seed_genres=None,
            limit=20,
        )
        track_names = []

        for track in recommendations["tracks"]:
            track_name = track["name"]

            artists = ", ".join(artist["name"] for artist in track["artists"])

            track_names.append(f"{track_name} - {artists}")

        return track_names

    async def _arun(self, *args, **kwargs):
        """Use the TopArtistsTool asynchronously."""
        return self._run()


class SpotifyGenreTool(BaseTool):
    """
    Tool that interacts with the SpotifyWeb API to fetch a random genre then generates recommendations based on that genre.
    """

    name = "SpotifyGenreTool"
    description = "Tool that fetches a random genre from Spotify and generates recommendations based on the genre."

    def _run(self, *args, **kwargs):
        token = os.getenv("SPOTIFY_TOKEN")
        if not token:
            raise ValueError("SPOTIFY_TOKEN environment variable is not set.")

        sp = spotipy.Spotify(auth=token)

        genres = sp.recommendation_genre_seeds()

        random_genre = random.choice(genres["genres"])
        seed_genres = [random_genre]

        recommendations = sp.recommendations(
            seed_tracks=None,
            seed_artists=None,
            seed_genres=seed_genres,
            limit=20,
        )
        track_names = []

        for track in recommendations["tracks"]:
            track_name = track["name"]

            artists = ", ".join(artist["name"] for artist in track["artists"])

            track_names.append(f"{track_name} - {artists}")

        return track_names

    async def _arun(self, *args, **kwargs):
        """Use the GenreTool asynchronously."""
        return self._run()


def create_agent():
    """
    Creates the LangChain ReAct agent

    Inputs: None

    Returns:
        agent_executor (AgentExecutor): Lanchain ReAct Agent Executor

    """
    prompt = hub.pull("hwchase17/react")

    tools = [SpotifyTopTracksTool(), SpotifyTopArtistsTool(), SpotifyGenreTool()]

    llm = ChatOpenAI(
        temperature=0, model="gpt-4-0613"
    )  # set the temperature to 0 to make the LLM deterministic

    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


def generate_response(user_input, num_songs, cfg):
    """
     Runs the LangChain ReAct Agent to generate a response to the user

    Inputs:
        user_input (str): The type of playlist the user wants to create (e.g., based on top tracks, top artists, or a random genre)
        num_songs (int): The number of songs the user selected
        cfg (RunnableConfig): The type of playlist the user wants to create (e.g., based on top tracks, top artists, or a random genre)

    Returns:
        response (str): The response generated by the LangChain ReAct Agent
    """
    agent = create_agent()

    s = str(num_songs)

    input_value = f"Create a playlist {user_input} that has {s} songs. Please number and separate the songs in your response. If the user selects a random genre, please tell them the genre in your response i.e. Your random genre is (genre)~"

    response = agent.invoke({f"input": input_value}, cfg)

    return response
