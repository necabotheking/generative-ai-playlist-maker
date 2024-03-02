"""
This file contains the styling elements for the Streamlit app
"""

import spotipy
import streamlit as st

from api.web_api import (
    generate_auth_url,
    generate_recommendations,
    get_access_token,
    get_random_genre_seed,
)


def set_page_configuration():
    """
    Sets the page configuration for the Streamlit App

    Inputs: None

    Returns: None, modifies the Streamlit App in-place

    """
    st.set_page_config(
        page_title="INFINI∞TRACKS",
        page_icon="🎙️",
        menu_items={
            "Get Help": "https://www.google.com",
            "Report a bug": "https://www.github.com/necabotheking",
            "About": "Created by Aïcha",
        },
    )

    col1, col2 = st.columns([1, 3])
    
    htp="https://raw.githubusercontent.com/necabotheking/generative-ai-playlist-maker/663abc707b16089e12a72f6b6c664524e4aab8a4/generative-ai-playlist-maker/img/casette.png"
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
    with open("generative-ai-playlist-maker/frontend/styles.css", "r") as f:
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


def parse_user_input(selected_option, spotipy_instance):
    """
    Inputs:
            selected_option (str): recommendation ption selected by the user
            spotipy_instance (Spotify): Spotipy instance of the Spotify class

    Returns:
            string representing the option that the user selected "tracks",
            "artist" or a random genre
    """
    if "tracks" in selected_option.lower():
        return "tracks"
    elif "artists" in selected_option.lower():
        return "artists"
    else:
        genre = get_random_genre_seed(spotipy_instance)
        return genre


# NOTE: This function did not work as intended
@st.cache_data(experimental_allow_widgets=True)
def get_user_selections(_sp):
    """
    Function meant to be used to cache the user's selections and feedback

    Input:
        _sp (Spotify): Spotipy instances of the Spotify Class

    Returns:
        parsed_user_selection (str)
        num_songs (int)

    """
    user_option = st.selectbox(
        "What kind of recommendations would you like?",
        ("Based on my top tracks", "Based on my top artists", "Surprise Me!"),
        index=None,
        placeholder="Please select a choice below...",
    )
    if user_option:
        parsed_user_selection = parse_user_input(user_option, _sp)
        num_songs = st.number_input("How many songs would you like?", 1, 20, value=None)
        return parsed_user_selection, num_songs


def display_app():
    """
    Main function to display and run the Streamlit app

    Inputs: None

    Returns: None, modifies the app in-place
    """
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
    
    if "authenticated" not in st.session_state:
        display_login_button(auth_url)

        # Handle redirect URL after authentication
        redirect_url = st.text_input("Enter the redirected URL here:")

        if redirect_url:
            access_token = get_access_token(auth_manager, redirect_url)
            sp = spotipy.Spotify(auth=access_token)

            # Set authenticated state
            st.session_state.authenticated = True
            st.session_state.sp = sp
    
    if "authenticated" in st.session_state:
        st.write("Let's develop your music recommendations!")
        st.markdown("##")

        user_option = st.selectbox(
            "What kind of recommendations would you like?",
            ("Based on my top tracks", "Based on my top artists", "Surprise Me!"),
            index=None,
            placeholder="Please select a choice below...",
        )
        if user_option:
            parsed_user_selection = parse_user_input(user_option, st.session_state.sp)
            num_songs = st.number_input(
                "How many songs would you like?", 1, 20, value=None
            )

            if num_songs:
                st.text(f"Creating a playlist with {num_songs} songs!")

                st.markdown("##")

                uris, names = generate_recommendations(
                    parsed_user_selection, num_songs, st.session_state.sp
                )

                for idx, name in enumerate(names):
                    st.text(f"{idx + 1}. {name}")

                st.markdown("##")

                st.text("Want to save your playlist?")


    # st.markdown("##")

    # redirect_url = st.text_input("Enter the redirected URL here:")

    # st.markdown("##")

    # if redirect_url:
    #     access_token = get_access_token(auth_manager, redirect_url)
    #     sp = spotipy.Spotify(auth=access_token)

    #     st.write("Let's develop your music recommendations!")
    #     st.markdown("##")

    #     user_option = st.selectbox(
    #         "What kind of recommendations would you like?",
    #         ("Based on my top tracks", "Based on my top artists", "Surprise Me!"),
    #         index=None,
    #         placeholder="Please select a choice below...",
    #     )
    #     if user_option:
    #         parsed_user_selection = parse_user_input(user_option, sp)
    #         num_songs = st.number_input(
    #             "How many songs would you like?", 1, 20, value=None
    #         )

    #         if num_songs:
    #             st.text(f"Creating a playlist with {num_songs} songs!")

    #             st.markdown("##")

    #             uris, names = generate_recommendations(
    #                 parsed_user_selection, num_songs, sp
    #             )

    #             for idx, name in enumerate(names):
    #                 st.text(f"{idx + 1}. {name}")

    #             # NOTE: The code below was meant to get user feedback to
    #             # fine-tune the playlist recommendations

    #             # thumbs_up = []
    #             # thumbs_down = []

    #             # for idx, name in enumerate(names):
    #             #     feedback = st.radio(f"{idx + 1}. {name}", ('👍', '👎'))
    #             #     # Feedback to adjust recommendations
    #             #     if feedback == '👍':
    #             #         thumbs_up.append(uris[idx])
    #             #     elif feedback == '👎':
    #             #         thumbs_down.append(uris[idx])

    #             st.markdown("##")

    #             st.text("Want to save your playlist?")