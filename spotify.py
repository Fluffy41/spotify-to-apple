import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os

load_dotenv()

# Setup your Spotify credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                               redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                               scope="playlist-read-private"))

def get_spotify_playlists():
    """Fetch all playlists from the authenticated Spotify account."""
    playlists = sp.current_user_playlists()
    return [{'name': playlist['name'], 'id': playlist['id']} for playlist in playlists['items']]

def get_spotify_tracks(playlist_id):
    """Fetch tracks from a specific playlist."""
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        tracks.append({'name': track['name'], 'artist': track['artists'][0]['name']})
    return tracks
