from fastapi import FastAPI
from pydantic import BaseModel
from spotify import get_spotify_playlists, get_spotify_tracks
from apple import add_tracks_to_apple_music

app = FastAPI()

# Pydantic model for adding tracks to Apple Music
class Playlist(BaseModel):
    spotify_playlist_id: str

# Endpoint to get Spotify playlists
@app.get("/playlists")
def get_playlists():
    """Fetch playlists from Spotify."""
    playlists = get_spotify_playlists()
    return {"playlists": playlists}

# Endpoint to get tracks from a Spotify playlist
@app.get("/playlist/{playlist_id}")
def get_playlist_tracks(playlist_id: str):
    """Fetch tracks from a specific Spotify playlist."""
    tracks = get_spotify_tracks(playlist_id)
    return {"tracks": tracks}

# Endpoint to add tracks to Apple Music
@app.post("/add_to_apple_music")
def add_to_apple_music(playlist: Playlist):
    """Add tracks from a Spotify playlist to Apple Music."""
    spotify_tracks = get_spotify_tracks(playlist.spotify_playlist_id)
    result = add_tracks_to_apple_music(spotify_tracks)
    return result

