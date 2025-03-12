import requests
import json
from typing import List

# Example Apple Music API endpoints
BASE_URL = "https://api.music.apple.com/v1/me"

# Assume we have a valid authorization token (you'll need to implement the OAuth flow or have a token stored)
APPLE_MUSIC_TOKEN = "your_apple_music_token_here"

def create_apple_music_playlist(name: str) -> str:
    """
    Creates a playlist in Apple Music with a name that includes '[Spotify > Apple]' prefix.
    """
    playlist_name = f"[Spotify > Apple] {name}"
    url = f"{BASE_URL}/library/playlists"
    headers = {
        "Authorization": f"Bearer {APPLE_MUSIC_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "attributes": {
            "name": playlist_name,
            "description": "Playlist synced from Spotify to Apple Music."
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        playlist_data = response.json()
        return playlist_data['data'][0]['id']  # Return playlist ID
    else:
        raise Exception(f"Error creating playlist: {response.status_code} - {response.text}")

def search_apple_music_track(track_name: str, artist_name: str) -> str:
    """
    Searches for a track in Apple Music by track name and artist.
    Returns the track ID if found.
    """
    search_url = f"{BASE_URL}/catalog/us/search"
    headers = {
        "Authorization": f"Bearer {APPLE_MUSIC_TOKEN}",
    }

    params = {
        "term": f"{track_name} {artist_name}",
        "types": "songs",
        "limit": 1
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        search_data = response.json()
        songs = search_data.get('results', {}).get('songs', {}).get('data', [])
        if songs:
            return songs[0]['id']  # Return track ID
        else:
            raise Exception(f"Track not found in Apple Music: {track_name}")
    else:
        raise Exception(f"Error searching for track: {response.status_code} - {response.text}")

def add_tracks_to_apple_playlist(playlist_id: str, track_ids: List[str]) -> None:
    """
    Adds tracks to an Apple Music playlist.
    """
    url = f"{BASE_URL}/library/playlists/{playlist_id}/relationships/tracks"
    headers = {
        "Authorization": f"Bearer {APPLE_MUSIC_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "data": [{"id": track_id, "type": "songs"} for track_id in track_ids]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Error adding tracks to playlist: {response.status_code} - {response.text}")

def sync_spotify_to_apple(spotify_playlist: dict) -> None:
    """
    Syncs a Spotify playlist to Apple Music.
    """
    # 1. Create Playlist in Apple Music
    apple_playlist_id = create_apple_music_playlist(spotify_playlist['name'])
    print(f"Created Apple Music Playlist: {apple_playlist_id}")

    # 2. Loop through Spotify tracks and add them to the Apple Music Playlist
    track_ids = []
    for track in spotify_playlist['tracks']:
        track_name = track['name']
        artist_name = track['artists'][0]['name']

        try:
            # 3. Search for the track in Apple Music
            apple_track_id = search_apple_music_track(track_name, artist_name)
            print(f"Found Track: {track_name} - {artist_name}")
            track_ids.append(apple_track_id)
        except Exception as e:
            print(f"Error syncing track '{track_name}': {e}")

    # 4. Add Tracks to Apple Music Playlist
    add_tracks_to_apple_playlist(apple_playlist_id, track_ids)
    print(f"Successfully added {len(track_ids)} tracks to Apple Music Playlist!")

