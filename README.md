# INFINI∞TRACKS

## Table of Contents: 
- Summary
- Technologies/Project Prerequisites
- Demo
- Status
- Reflection
- References & Inspiration

## Summary
This project, "INFINI∞TRACKS," is the final project for the University of Chicago's MPCS 57200: Generative AI Course for the Winter 2024 Quarter. The project leverages a LangChain ReAct agent to facilitate communication between the myself and the Spotify Web API to create personalized playlists based on my top songs, top artists, or a surprise random genre.


## Technologies/Project Prerequisites 

- [LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Python](https://www.python.org/)
- [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/?highlight=top#)
- [Spotify Web Api](https://developer.spotify.com/documentation/web-api)
- [Streamlit](https://streamlit.io/)
- [Spotify Web Api](https://developer.spotify.com/documentation/web-api)

To run the application locally, ensure you have the following:

OPENAI_API_KEY: API key for ChatGPT integration.
SPOTIFY_CLIENT: Spotify client ID for authentication.
SPOTIFY_SECRET: Spotify secret key for authentication.

1. Sign up for the Spotify Web API and OpenAI to receive api keys
2. Create a `.env` file and insert the api keys above
3. Install the requirements with `pip install -r requirements.txt`
4. Run the project within the directory that `app.py` is in using `streamlit run app.py`

## Demo

![](https://github.com/necabotheking/generative-ai-playlist-maker/blob/main/readme_content/infinitracks_demo.gif)

## Status
The project is finished.

## Reflection
During development, several challenges were encountered, particularly due to the complexities and limitation associated with the development mode of apps in the Spotify Web API. Additionally, Spotify API restrictions prevented my original plan of integrating ChatGPT for personalized recommendations. 

During the development of INFINI∞TRACKS, I gained valuable insights into integrating AI tools into Streamlit applications and learned extensively about working with the Spotify Web API. The project provided me with hands-on experience in creating personalized Spotify experience by allowing me to "speak" directly to my Spotify data with the ReAct agent. I was able to explore the intersection of LangChain, Streamlit, and the Spotify Web API's recommendation AI to create custom tools for my ReAct agent to interact with my spotify data. Despite the twists and turns, this project was a fascinating experience and exploration of the uses of AI tools within LangChain and Spotify.

## References & Inspiration
1. [Build your own playlist generator with Spotify’s API 🎧 (in Python!)](https://medium.com/analytics-vidhya/build-your-own-playlist-generator-with-spotifys-api-in-python-ceb883938ce4) by [rob_med](https://github.com/rob-med)
2. [Spotify’s Authorization Code Flow For Dummies](https://cjohanaja.com/posts/spotify-auth-primer/) by [ChrisOh431](https://github.com/ChrisOh431)
3. [Make your Streamlit App Look Better](https://medium.com/international-school-of-ai-data-science/make-your-streamlit-web-app-look-better-14355c2db871) by Yash Chuanhan
4. [LangChain: Creating an AI Agent utilizing the Spotify API Part I & II](https://medium.com/@astropomeai/langchain-creating-an-ai-agent-utilizing-the-spotify-api-f0975470fd26) by Astropromeai
5. [Spotify GPT AGent](https://github.com/trancethehuman/spotify-chat) by [trancethehuman](https://github.com/trancethehuman)
