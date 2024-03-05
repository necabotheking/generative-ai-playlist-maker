"""
This file contains the styling elements for the Streamlit app
"""

import streamlit as st
from api.agent import generate_response
from api.web_api import generate_auth_url, retrieve_access_token
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.runnables import RunnableConfig
from utils.functions import cleanup, save_spotify_access_token_to_env


def set_page_configuration():
    """
    Sets the page configuration for the Streamlit App

    Inputs: None

    Returns: None, modifies the Streamlit App in place

    """
    st.set_page_config(
        page_title="INFINI∞TRACKS",
        page_icon="🎙️",
        menu_items={
            "Report a bug": "https://github.com/necabotheking/generative-ai-playlist-maker",
            "About": "INFINI∞TRACKS: Created by Aïcha",
        },
    )

    col1, col2 = st.columns([1, 3])

    htp = "https://raw.githubusercontent.com/necabotheking/generative-ai-playlist-maker/663abc707b16089e12a72f6b6c664524e4aab8a4/generative-ai-playlist-maker/img/casette.png"
    with col1:
        st.image(htp, width=200)

    with col2:
        st.title("INFINI∞TRACKS", anchor=False)


def load_custom_styling():
    """
    Load custom CSS styles

    Inputs: None

    Returns: None, modifies the Streamlit App in-place
    """
    st.write(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>',
        unsafe_allow_html=True,
    )
    with open("./frontend/styles.css", "r") as f:
        css = f.read()

    st.markdown(
        f"""
        <style>
        {css}
        </style>
        """,
        unsafe_allow_html=True,
    )

    hide_img_fs = """
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    """

    st.markdown(
        """
        <footer style="text-align:center; margin-top: 50px;">
            <p>Made with ♡ by <a href="https://github.com/necabotheking">Aïcha</a></p>
        </footer>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(hide_img_fs, unsafe_allow_html=True)


def display_login_button(auth_url):
    """
    Display the "Sign in with Spotify" button with authorization URL

    Inputs:
        auth_url: URL to authorize the user's content for the Spotify Web API

    Returns: None, modifies the app in-place to display the login button
    """
    st.markdown(
        f"""
        <div id="button_wrapper">
            <a href="{auth_url}" class="auth-url">
                <button class="spotify-btn">
                    <i class="fab fa-spotify"></i> Sign in with Spotify
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_app():
    """
    Main function to display and run the Streamlit app

    Inputs: None

    Returns: None, modifies the app in-place
    """
    # Load Streamlit App Configuration functions and remove cached token
    cleanup()
    set_page_configuration()
    load_custom_styling()

    auth_url, auth_manager = generate_auth_url()

    st.write(
        "Welcome to **INFINI∞TRACKS** - your ultimate destination for limitless music exploration!"
    )
    st.write(
        "Explore curated music recommendations tailored to your mood, genre preferences, and personal taste, let our AI-powered recommendations guide you to your next favorite track. With INFINI∞TRACKS, the journey never ends - dive in and discover your perfect soundtrack today!"
    )

    st.markdown("##")

    display_login_button(auth_url)
    redirect_url = st.text_input("Enter the redirected URL here:")

    if redirect_url:
        access_token = retrieve_access_token(auth_manager, redirect_url)
        save_spotify_access_token_to_env(access_token)

        st.write(f"Access Token Acquired and Saved!")
        st.markdown("##")
        st.write("Please enter your playlist preferences for the INFINI∞TRACKS AI!")
        st.markdown("##")

        user_option = st.selectbox(
            "What kind of recommendations would you like?",
            ("Based on my top tracks", "Based on my top artists", "Surprise Me!"),
            index=None,
            placeholder="Please select a choice below...",
        )
        if user_option:
            num_songs = st.number_input(
                "How many songs would you like?", 1, 20, value=None
            )

            if num_songs:
                st.markdown("##")
                st.text(
                    f"INFINI∞TRACKS AI is creating your new playlist with {num_songs} songs!"
                )
                st.text("Please wait while your agent generates some tunes 🎵")

                st.markdown("##")

                output_container = st.empty()

                answer_container = output_container.container().chat_message(
                    "assistant", avatar="🦜"
                )
                st_callback = StreamlitCallbackHandler(answer_container)
                cfg = RunnableConfig()
                cfg["callbacks"] = [st_callback]

                answer = generate_response(user_option, num_songs, cfg)
                answer_container.write("Here is your INFINI∞TRACKS generated playlist!")
                answer_container.write(answer["output"])
