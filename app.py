from flask import Flask, render_template, request
from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.neighbors import NearestNeighbors
import pickle
import numpy as np
import pandas as pd

with open('base_model' , 'rb') as f:
    model = pickle.load(f)

# initializes our app
app = Flask(__name__)

# Get API keys from .env
cid = getenv('CLIENT_ID')
secret = getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

@app.route('/')
def root():
    # Query users to display on the home page
    return render_template('main.html', title="Spotify4")

@app.route('/analyze', methods=['POST'])
def analyze():
    # Query users to display on the home page
    input_url = request.values['song_link']
    
    analyze_track = sp.audio_features(input_url)[0]
    analyze_track = pd.DataFrame({'id':[analyze_track['id']],
                                  'acousticness':[analyze_track['acousticness']],
                                  'danceability':[analyze_track['danceability']],
                                  'duration_ms':[analyze_track['duration_ms']],
                                  'energy':[analyze_track['energy']],
                                  'instrumentalness':[analyze_track['instrumentalness']],
                                  'key':[analyze_track['key']],
                                  'liveness':[analyze_track['liveness']],
                                  'loudness':[analyze_track['loudness']],
                                  'mode':[analyze_track['mode']],
                                  'speechiness':[analyze_track['speechiness']],
                                  'tempo':[analyze_track['tempo']],
                                  'time_signature':[analyze_track['time_signature']]})
    analyze_track.set_index('id', inplace=True)
    
    _, neighbors_indexes = model.kneighbors(analyze_track)
    Y=pd.read_csv('indexes')
    result_ids = []
    for index in neighbors_indexes[0]:
        result_ids.append("https://open.spotify.com/track/" + Y.iloc[index].id)
        
                    
    artist_track = sp.track(input_url)['artists'][0]['name']
    title_track = sp.track(input_url)['name']
    preview_track = sp.track(input_url)['preview_url']
    picture_track = sp.track(input_url)['album']['images'][0]['url']
    
    artist_track_1 = sp.track(result_ids[0])['artists'][0]['name']
    title_track_1 = sp.track(result_ids[0])['name']
    preview_track_1 = sp.track(result_ids[0])['preview_url']
    picture_track_1 = sp.track(result_ids[0])['album']['images'][0]['url']
    
    artist_track_2 = sp.track(result_ids[1])['artists'][0]['name']
    title_track_2 = sp.track(result_ids[1])['name']
    preview_track_2 = sp.track(result_ids[1])['preview_url']
    picture_track_2 = sp.track(result_ids[1])['album']['images'][0]['url']
    
    artist_track_3 = sp.track(result_ids[2])['artists'][0]['name']
    title_track_3 = sp.track(result_ids[2])['name']
    preview_track_3 = sp.track(result_ids[2])['preview_url']
    picture_track_3 = sp.track(result_ids[2])['album']['images'][0]['url']
    
    artist_track_4 = sp.track(result_ids[3])['artists'][0]['name']
    title_track_4 = sp.track(result_ids[3])['name']
    preview_track_4 = sp.track(result_ids[3])['preview_url']
    picture_track_4 = sp.track(result_ids[3])['album']['images'][0]['url']
    
    return render_template('analyze.html',
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
                            )


if __name__=="__main__":
    app.run()

