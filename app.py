from flask import Flask, render_template, request
from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.neighbors import NearestNeighbors
import pickle
import numpy as np
import json
import pandas as pd
import plotly
import plotly.graph_objects as go

with open("base_model", "rb") as f:
    model = pickle.load(f)

# initializes our app
app = Flask(__name__)

# Get API keys from .env
cid = getenv("CLIENT_ID")
secret = getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route("/")
def root():
    '''Root bage'''
    return render_template("main.html", title="Spotify4")

@app.route("/about-the-team")
def abouttheteam():
    '''About The Team - page'''
    return render_template("about-the-team.html", title="Spotify4")

@app.route("/how-it-works")
def howitworks():
    '''How It Works - page'''
    return render_template("how-it-works.html", title="Spotify4")


@app.route("/analyze", methods=["POST"])
def analyze():
    '''Where the magic happens'''
    input_url = request.values["song_link"]

    # Get audio features for supplied URL
    analyze_track = sp.audio_features(input_url)[0]
    analyze_track = pd.DataFrame(
        {
            "id": [analyze_track["id"]],
            "acousticness": [analyze_track["acousticness"]],
            "danceability": [analyze_track["danceability"]],
            "duration_ms": [analyze_track["duration_ms"]],
            "energy": [analyze_track["energy"]],
            "instrumentalness": [analyze_track["instrumentalness"]],
            "key": [analyze_track["key"]],
            "liveness": [analyze_track["liveness"]],
            "loudness": [analyze_track["loudness"]],
            "mode": [analyze_track["mode"]],
            "speechiness": [analyze_track["speechiness"]],
            "tempo": [analyze_track["tempo"]],
            "time_signature": [analyze_track["time_signature"]],
        }
    )
    analyze_track.set_index("id", inplace=True)

    # Model variable assignment
    _, neighbors_indexes = model.kneighbors(analyze_track)
    Y = pd.read_csv("indexes")
    
    # Generating the links
    result_ids = []
    for index in neighbors_indexes[0]:
        result_ids.append("https://open.spotify.com/track/" + Y.iloc[index].id)
    
    # Generating the radar charts
    radars = []
    radars.append(radar_charts(input_url, input_url, sp))
    for song in result_ids:
        radars.append(radar_charts(input_url, song, sp))
    
    # Messy variable assignments
    track_temp = sp.track(input_url)
    artist_track = track_temp["artists"][0]["name"]
    title_track = track_temp["name"]
    preview_track = track_temp["preview_url"]
    picture_track = track_temp["album"]["images"][0]["url"]

    # Loop1
    track_temp = sp.track(result_ids[0])
    artist_track_1 = track_temp["artists"][0]["name"]
    title_track_1 = track_temp["name"]
    preview_track_1 = track_temp["preview_url"]
    picture_track_1 = track_temp["album"]["images"][0]["url"]

    # Loop 2
    track_temp = sp.track(result_ids[1])
    artist_track_2 = track_temp["artists"][0]["name"]
    title_track_2 = track_temp["name"]
    preview_track_2 = track_temp["preview_url"]
    picture_track_2 = track_temp["album"]["images"][0]["url"]

    # Loop "Three-Is-Company"
    track_temp = sp.track(result_ids[2])
    artist_track_3 = track_temp["artists"][0]["name"]
    title_track_3 = track_temp["name"]
    preview_track_3 = track_temp["preview_url"]
    picture_track_3 = track_temp["album"]["images"][0]["url"]

    # Loop "Four score and seven years ago"
    track_temp = sp.track(result_ids[3])
    artist_track_4 = track_temp["artists"][0]["name"]
    title_track_4 = track_temp["name"]
    preview_track_4 = track_temp["preview_url"]
    picture_track_4 = track_temp["album"]["images"][0]["url"]
    
    # Loop 5... Something
    track_temp = sp.track(result_ids[4])
    artist_track_5 = track_temp["artists"][0]["name"]
    title_track_5 = track_temp["name"]
    preview_track_5 = track_temp["preview_url"]
    picture_track_5 = track_temp["album"]["images"][0]["url"]
    
    # Loops half-a-dozen
    track_temp = sp.track(result_ids[5])
    artist_track_6 = track_temp["artists"][0]["name"]
    title_track_6 = track_temp["name"]
    preview_track_6 = track_temp["preview_url"]
    picture_track_6 = track_temp["album"]["images"][0]["url"]
    
    # Loop 7 deadly sins
    track_temp = sp.track(result_ids[6])
    artist_track_7 = track_temp["artists"][0]["name"]
    title_track_7 = track_temp["name"]
    preview_track_7 = track_temp["preview_url"]
    picture_track_7 = track_temp["album"]["images"][0]["url"]
    
    # Loop "I h8 this project"
    track_temp = sp.track(result_ids[7])
    artist_track_8 = track_temp["artists"][0]["name"]
    title_track_8 = track_temp["name"]
    preview_track_8 = track_temp["preview_url"]
    picture_track_8 = track_temp["album"]["images"][0]["url"]
    
    # Loop Nine-Inch-Nails
    track_temp = sp.track(result_ids[8])
    artist_track_9 = track_temp["artists"][0]["name"]
    title_track_9 = track_temp["name"]
    preview_track_9 = track_temp["preview_url"]
    picture_track_9 = track_temp["album"]["images"][0]["url"]
    
    # Loop Countdown from 10
    track_temp = sp.track(result_ids[9])
    artist_track_10 = track_temp["artists"][0]["name"]
    title_track_10 = track_temp["name"]
    preview_track_10 = track_temp["preview_url"]
    picture_track_10 = track_temp["album"]["images"][0]["url"]            
    
    return render_template(
        "analyze.html",
        preview_track=preview_track, picture_track=picture_track, title_track=title_track, artist_track=artist_track, link_url=input_url,
        preview_track_1=preview_track_1, picture_track_1=picture_track_1, title_track_1=title_track_1, artist_track_1=artist_track_1, link_url_1=result_ids[0],
        preview_track_2=preview_track_2, picture_track_2=picture_track_2, title_track_2=title_track_2, artist_track_2=artist_track_2, link_url_2=result_ids[1],
        preview_track_3=preview_track_3, picture_track_3=picture_track_3, title_track_3=title_track_3, artist_track_3=artist_track_3, link_url_3=result_ids[2],
        preview_track_4=preview_track_4, picture_track_4=picture_track_4, title_track_4=title_track_4, artist_track_4=artist_track_4, link_url_4=result_ids[3],
        preview_track_5=preview_track_5, picture_track_5=picture_track_5, title_track_5=title_track_5, artist_track_5=artist_track_5, link_url_5=result_ids[4],
        preview_track_6=preview_track_6, picture_track_6=picture_track_6, title_track_6=title_track_6, artist_track_6=artist_track_6, link_url_6=result_ids[5],
        preview_track_7=preview_track_7, picture_track_7=picture_track_7, title_track_7=title_track_7, artist_track_7=artist_track_7, link_url_7=result_ids[6],
        preview_track_8=preview_track_8, picture_track_8=picture_track_8, title_track_8=title_track_8, artist_track_8=artist_track_8, link_url_8=result_ids[7],
        preview_track_9=preview_track_9, picture_track_9=picture_track_9, title_track_9=title_track_9, artist_track_9=artist_track_9, link_url_9=result_ids[8],
        preview_track_10=preview_track_10, picture_track_10=picture_track_10, title_track_10=title_track_10, artist_track_10=artist_track_10, link_url_10=result_ids[9],
        radars=radars)


def radar_charts(input_url, output_url, sp):
    # Generates a radar chart for variables given a supplied Spotify url
    analyze_track = list((sp.audio_features(output_url)[0]).items())[:11]
    categories = ["danceability", "energy",
                  "key", "loudness", "speechiness",
                  "acousticness", "instrumentalness",
                  "liveness", "valence", "tempo"]

    Song2 = [x[1] for x in analyze_track]
    Song2[2] = (Song2[2] - (-1)) / (11 + 1)
    Song2[3] = (Song2[3] - (-60)) / (7.234 + 60)
    Song2[10] = (Song2[10] - (0)) / (249)
    Song2.pop(4)

    if output_url == input_url:
        fig = go.Figure(data=[go.Scatterpolar(r=Song2, theta=categories, fill="toself", fillcolor='rgba(0,128,255,0.7)', line=dict(color="rgba(0,0,0,0.5)"))])
    else:    
        fig = go.Figure(data=[go.Scatterpolar(r=Song2, theta=categories, fill="toself", fillcolor='rgba(29,185,84,0.7)', line=dict(color="rgba(0,0,0,0.5)"))])
    fig.update_layout(template='plotly_dark', margin=dict(t=20, b=20, l=20, r=20), width=420, height=300, paper_bgcolor='rgba(14,13,13,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=('#acacac'))
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == "__main__":
    app.run()
