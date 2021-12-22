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
    result_ids = []
    for index in neighbors_indexes[0]:
        result_ids.append("https://open.spotify.com/track/" + Y.iloc[index].id)

    artist_track = sp.track(input_url)["artists"][0]["name"]
    title_track = sp.track(input_url)["name"]
    preview_track = sp.track(input_url)["preview_url"]
    picture_track = sp.track(input_url)["album"]["images"][0]["url"]

    artist_track_1 = sp.track(result_ids[0])["artists"][0]["name"]
    title_track_1 = sp.track(result_ids[0])["name"]
    preview_track_1 = sp.track(result_ids[0])["preview_url"]
    picture_track_1 = sp.track(result_ids[0])["album"]["images"][0]["url"]

    artist_track_2 = sp.track(result_ids[1])["artists"][0]["name"]
    title_track_2 = sp.track(result_ids[1])["name"]
    preview_track_2 = sp.track(result_ids[1])["preview_url"]
    picture_track_2 = sp.track(result_ids[1])["album"]["images"][0]["url"]

    artist_track_3 = sp.track(result_ids[2])["artists"][0]["name"]
    title_track_3 = sp.track(result_ids[2])["name"]
    preview_track_3 = sp.track(result_ids[2])["preview_url"]
    picture_track_3 = sp.track(result_ids[2])["album"]["images"][0]["url"]

    artist_track_4 = sp.track(result_ids[3])["artists"][0]["name"]
    title_track_4 = sp.track(result_ids[3])["name"]
    preview_track_4 = sp.track(result_ids[3])["preview_url"]
    picture_track_4 = sp.track(result_ids[3])["album"]["images"][0]["url"]

    radars = []
    for song in result_ids:
        radars.append(radar_charts(input_url, song, sp))

    return render_template(
        "analyze.html",
        preview_track=preview_track,
        picture_track=picture_track,
        title_track=title_track,
        artist_track=artist_track,
        preview_track_1=preview_track_1,
        picture_track_1=picture_track_1,
        title_track_1=title_track_1,
        artist_track_1=artist_track_1,
        preview_track_2=preview_track_2,
        picture_track_2=picture_track_2,
        title_track_2=title_track_2,
        artist_track_2=artist_track_2,
        preview_track_3=preview_track_3,
        picture_track_3=picture_track_3,
        title_track_3=title_track_3,
        artist_track_3=artist_track_3,
        preview_track_4=preview_track_4,
        picture_track_4=picture_track_4,
        title_track_4=title_track_4,
        artist_track_4=artist_track_4,
        radars=radars,
    )


def radar_charts(input_url, output_url, sp):
    analyze_track_1 = list((sp.audio_features(input_url)[0]).items())[:11]
    analyze_track_2 = list((sp.audio_features(output_url)[0]).items())[:11]
    song_and_artist_1 = (
        str(sp.track(input_url)["name"])
        + " by "
        + str(sp.track(input_url)["artists"][0]["name"])
    )
    song_and_artist_2 = (
        str(sp.track(output_url)["name"])
        + " by "
        + str(sp.track(output_url)["artists"][0]["name"])
    )

    categories = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]
    categories1 = [*categories, categories[0]]

    Song1 = [x[1] for x in analyze_track_1]
    Song1[2] = (Song1[2] - (-1)) / (11 + 1)
    Song1[3] = (Song1[3] - (-60)) / (7.234 + 60)
    Song1[10] = (Song1[10] - (0)) / (249)
    Song1.pop(4)

    Song2 = [x[1] for x in analyze_track_2]
    Song2[2] = (Song2[2] - (-1)) / (11 + 1)
    Song2[3] = (Song2[3] - (-60)) / (7.234 + 60)
    Song2[10] = (Song2[10] - (0)) / (249)
    Song2.pop(4)

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=Song1, theta=categories1, fill="toself", name=song_and_artist_1
            ),
            go.Scatterpolar(
                r=Song2, theta=categories1, fill="toself", name=song_and_artist_2
            ),
        ],
        layout=go.Layout(
            showlegend=False,
        ),
    )

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        autosize=True,
        width=400,
        height=200,
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == "__main__":
    app.run()
