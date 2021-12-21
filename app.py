from flask import Flask, render_template, request
from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

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
    analyze_track = list((sp.audio_features(input_url)[0]).items())[:11]
    artist_track = sp.track(input_url)['artists'][0]['name']
    title_track = sp.track(input_url)['name']
    preview_track = sp.track(input_url)['preview_url']
    picture_track = sp.track(input_url)['album']['images'][0]['url']
    #return str([artist_track, title_track, analyze_track, preview_track])
    return render_template('analyze.html',
                           preview_track=preview_track,
                           picture_track=picture_track,
                           title_track=title_track,
                           artist_track=artist_track)

if __name__=="__main__":
    app.run()

