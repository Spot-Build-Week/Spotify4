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
from plotly import io
import sys

import time

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
    # Query users to display on the home page
    return render_template("main.html", title="Spotify4")


@app.route("/analyze", methods=["POST"])
def analyze():
    # Query users to display on the home page
    input_url = request.values["song_link"]

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

    _, neighbors_indexes = model.kneighbors(analyze_track)
    Y = pd.read_csv("indexes")
    start_time = time.time()
    result_ids = []
    for index in neighbors_indexes[0]:
        result_ids.append("https://open.spotify.com/track/" + Y.iloc[index].id)
    print(time.time() - start_time, file=sys.stderr)
    
    track_temp = sp.track(input_url)
    artist_track = track_temp["artists"][0]["name"]
    title_track = track_temp["name"]
    preview_track = track_temp["preview_url"]
    picture_track = track_temp["album"]["images"][0]["url"]

    track_temp = sp.track(result_ids[0])
    artist_track_1 = track_temp["artists"][0]["name"]
    title_track_1 = track_temp["name"]
    preview_track_1 = track_temp["preview_url"]
    picture_track_1 = track_temp["album"]["images"][0]["url"]

    track_temp = sp.track(result_ids[1])
    artist_track_2 = track_temp["artists"][0]["name"]
    title_track_2 = track_temp["name"]
    preview_track_2 = track_temp["preview_url"]
    picture_track_2 = track_temp["album"]["images"][0]["url"]

    track_temp = sp.track(result_ids[2])
    artist_track_3 = track_temp["artists"][0]["name"]
    title_track_3 = track_temp["name"]
    preview_track_3 = track_temp["preview_url"]
    picture_track_3 = track_temp["album"]["images"][0]["url"]

    track_temp = sp.track(result_ids[3])
    artist_track_4 = track_temp["artists"][0]["name"]
    title_track_4 = track_temp["name"]
    preview_track_4 = track_temp["preview_url"]
    picture_track_4 = track_temp["album"]["images"][0]["url"]
    
    track_temp = sp.track(result_ids[4])
    artist_track_5 = track_temp["artists"][0]["name"]
    title_track_5 = track_temp["name"]
    preview_track_5 = track_temp["preview_url"]
    picture_track_5 = track_temp["album"]["images"][0]["url"]
    
    track_temp = sp.track(result_ids[5])
    artist_track_6 = track_temp["artists"][0]["name"]
    title_track_6 = track_temp["name"]
    preview_track_6 = track_temp["preview_url"]
    picture_track_6 = track_temp["album"]["images"][0]["url"]
    
    track_temp = sp.track(result_ids[6])
    artist_track_7 = track_temp["artists"][0]["name"]
    title_track_7 = track_temp["name"]
    preview_track_7 = track_temp["preview_url"]
    picture_track_7 = track_temp["album"]["images"][0]["url"]
    
    track_temp = sp.track(result_ids[7])
    artist_track_8 = track_temp["artists"][0]["name"]
    title_track_8 = track_temp["name"]
    preview_track_8 = track_temp["preview_url"]
    picture_track_8 = track_temp["album"]["images"][0]["url"]
    
    track_temp = sp.track(result_ids[8])
    artist_track_9 = track_temp["artists"][0]["name"]
    title_track_9 = track_temp["name"]
    preview_track_9 = track_temp["preview_url"]
    picture_track_9 = track_temp["album"]["images"][0]["url"]
    
    track_temp = sp.track(result_ids[9])
    artist_track_10 = track_temp["artists"][0]["name"]
    title_track_10 = track_temp["name"]
    preview_track_10 = track_temp["preview_url"]
    picture_track_10 = track_temp["album"]["images"][0]["url"]    
    
    radars = []
    for song in result_ids:
        radars.append(radar_charts(song, sp))    
    
    return render_template(
        "analyze.html",
        preview_track=preview_track, picture_track=picture_track, title_track=title_track, artist_track=artist_track,
        preview_track_1=preview_track_1, picture_track_1=picture_track_1, title_track_1=title_track_1, artist_track_1=artist_track_1,
        preview_track_2=preview_track_2, picture_track_2=picture_track_2, title_track_2=title_track_2, artist_track_2=artist_track_2,
        preview_track_3=preview_track_3, picture_track_3=picture_track_3, title_track_3=title_track_3, artist_track_3=artist_track_3,
        preview_track_4=preview_track_4, picture_track_4=picture_track_4, title_track_4=title_track_4, artist_track_4=artist_track_4,
        preview_track_5=preview_track_5, picture_track_5=picture_track_5, title_track_5=title_track_5, artist_track_5=artist_track_5,
        preview_track_6=preview_track_6, picture_track_6=picture_track_6, title_track_6=title_track_6, artist_track_6=artist_track_6,
        preview_track_7=preview_track_7, picture_track_7=picture_track_7, title_track_7=title_track_7, artist_track_7=artist_track_7,
        preview_track_8=preview_track_8, picture_track_8=picture_track_8, title_track_8=title_track_8, artist_track_8=artist_track_8,
        preview_track_9=preview_track_9, picture_track_9=picture_track_9, title_track_9=title_track_9, artist_track_9=artist_track_9,
        preview_track_10=preview_track_10, picture_track_10=picture_track_10, title_track_10=title_track_10, artist_track_10=artist_track_10,
        radars=radars)


def radar_charts(output_url, sp):
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

    fig = go.Figure(data=[go.Scatterpolar(r=Song2, theta=categories, fill="toself")])

    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), width=520, height=400, paper_bgcolor='rgb(14, 13, 13)', font_color=('#acacac'))
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


if __name__ == "__main__":
    app.run()
