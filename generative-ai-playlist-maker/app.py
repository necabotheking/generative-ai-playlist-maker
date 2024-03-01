"""
This file contains the main code for the Streamlit app that will hold the front end code
"""

##TODO: create util functions for front end 
# import the necessary functions to run the app
import spotipy
import streamlit as st
from api.web_api import generate_auth_url, get_access_token, get_random_genre_seed, generate_recommendations

def parse_user_input(selected_option, spotipy_instance):
    """
    Inputs:
            selected_option (str): Option selected
            spotipy_instance (Spotify): Spotipy instance of the Spotify class

    Returns:
    """
    if "tracks" in selected_option.lower():
        return "tracks"
    elif "artists" in selected_option.lower():
        return "artists"
    else:
        genre = get_random_genre_seed(spotipy_instance)
        return genre
                

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
            "About": "Created by Aïcha"
        }
    )
    
    col1, col2 = st.columns([1, 3]) 

    with col1:
        st.image("img/casette.png", width=200)

    with col2:
        st.title("INFINI∞TRACKS", anchor=False)
    
    

def load_custom_styling():
    """
    Load custom CSS styles
    """
    st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>', unsafe_allow_html=True)
    with open("styles.css", "r") as f:
        css = f.read()
    
    # Apply custom styles using Markdown
    st.markdown(
        f"""
        <style>
        {css}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''
    
    st.markdown(
        """
        <footer style="text-align:center; margin-top: 50px;">
            <p>Made with ♡ by <a href="https://github.com/necabotheking">Aïcha</a></p>
        </footer>
        """,
        unsafe_allow_html=True
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
        unsafe_allow_html=True
    )


def main():
    """
    Runs the main app to create the streamlit app with interactivity and generative content based on the user's spotify account
    """
    #TODO: finish configuration for the menu items and the page
    set_page_configuration()
    
    load_custom_styling()
    
    auth_url, auth_manager = generate_auth_url()
    
    
    st.write("Welcome to **INFINI∞TRACKS** - your ultimate destination for limitless music exploration!")
    st.write("Explore curated music recommendations tailored to your mood, genre preferences, and personal taste, let our AI-powered recommendations guide you to your next favorite track. With INFINI∞TRACKS, the journey never ends - dive in and discover your perfect soundtrack today!")

    # adds spaces to the app between elements
    st.markdown('##')
    
    display_login_button(auth_url)
    
    st.markdown('##')
    
    # Get redirected URL from user input
    redirect_url = st.text_input("Enter the redirected URL here:")
    
    st.markdown('##')
    
    # Check if redirected URL is provided
    if redirect_url:
        
        access_token = get_access_token(auth_manager, redirect_url)
        sp = spotipy.Spotify(auth=access_token)

        
        st.write("Let's see your recommendations ")
        st.markdown('##')
        
        user_option = st.selectbox(
            "What kind of recommendations would you like?",
            ("Based on my top tracks", "Based on my top artists", "Surprise Me!"),
            index=None,
            placeholder="Please select a choice below...",
      ) 
        if user_option:
            parsed_user_selection = parse_user_input(user_option, sp)
            num_songs = st.number_input(
                "How many songs would you like?", 1, 20, value=None
            )
            if num_songs:
                st.text(f"Creating a playlist recommendation with {num_songs} songs! \n")

                uris, names = generate_recommendations(parsed_user_selection, num_songs, sp)
 
                for idx, name in enumerate(names):
                    st.text(f"{idx + 1}. {name}")

                
                st.markdown("##")
                
                st.text("Want to save your playlist?")



if __name__ == "__main__":
    main()