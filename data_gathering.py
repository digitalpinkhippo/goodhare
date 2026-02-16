"""
Data gathering module for retrieving playlists and track information from Spotify API.
"""

from spotipy import Spotify
from spotipy.exceptions import SpotifyException


def get_spotify_client(token_info):
    """
    Create and return a Spotify client with the given token.
    
    Args:
        token_info (dict): Token information containing access_token
        
    Returns:
        Spotify: Authenticated Spotify client
    """
    return Spotify(auth=token_info['access_token'])


def get_user_playlists(token_info):
    """
    Fetch all user playlists.
    
    Args:
        token_info (dict): Token information
        
    Returns:
        list: List of playlist dictionaries with id, name, description, track_count, owner
    """
    try:
        sp = get_spotify_client(token_info)
        playlists = []
        results = sp.current_user_playlists(limit=50)
        
        while results:
            for playlist in results.get('items', []):
                # Safely get track count from items object
                # The API returns track count in 'items' field, not 'tracks'
                items_info = playlist.get('items', {})
                if isinstance(items_info, dict):
                    # Check if 'total' exists in items
                    track_count = items_info.get('total', 0)
                else:
                    # Fallback to 'tracks' field if 'items' doesn't exist
                    tracks_info = playlist.get('tracks', {})
                    if isinstance(tracks_info, dict):
                        track_count = tracks_info.get('total', 0)
                    else:
                        track_count = 0
                
                # Safely get owner information
                owner_info = playlist.get('owner', {})
                if isinstance(owner_info, dict):
                    owner = owner_info.get('display_name') or owner_info.get('id', 'Unknown')
                else:
                    owner = 'Unknown'
                
                playlists.append({
                    'id': playlist.get('id', ''),
                    'name': playlist.get('name', 'Unnamed Playlist'),
                    'description': playlist.get('description', ''),
                    'track_count': track_count,
                    'owner': owner
                })
            
            if results.get('next'):
                results = sp.next(results)
            else:
                break
        
        return playlists
    except (SpotifyException, KeyError) as e:
        raise Exception(f"Error fetching playlists: {str(e)}")


def get_liked_songs(token_info):
    """
    Fetch user's liked songs (saved tracks).
    
    Args:
        token_info (dict): Token information
        
    Returns:
        dict: Playlist-like object representing "Liked Songs"
    """
    try:
        sp = get_spotify_client(token_info)
        liked_songs = {
            'id': 'liked_songs',
            'name': 'Liked Songs',
            'description': 'Your saved tracks',
            'track_count': 0,
            'owner': 'You'
        }
        
        # Count total liked songs
        results = sp.current_user_saved_tracks(limit=1)
        if results:
            liked_songs['track_count'] = results['total']
        
        return liked_songs
    except SpotifyException as e:
        raise Exception(f"Error fetching liked songs: {str(e)}")


def get_playlist_tracks(token_info, playlist_id):
    """
    Get all tracks in a specific playlist.
    
    Args:
        token_info (dict): Token information
        playlist_id (str): Spotify playlist ID or 'liked_songs' for saved tracks
        
    Returns:
        list: List of track dictionaries with id, name, artist, album, year, duration_ms
    """
    try:
        sp = get_spotify_client(token_info)
        tracks = []
        
        if playlist_id == 'liked_songs':
            # Fetch liked songs
            results = sp.current_user_saved_tracks(limit=50)
            while results:
                for item in results.get('items', []):
                    track = item.get('track')
                    if track and track.get('id'):  # Some tracks might be None or unavailable
                        tracks.append(extract_track_info(track))
                
                if results.get('next'):
                    results = sp.next(results)
                else:
                    break
        else:
            # Fetch playlist tracks
            try:
                results = sp.playlist_tracks(playlist_id, limit=50, additional_types=('track',))
            except SpotifyException as e:
                print(e)
                if e.http_status == 403:
                    raise Exception(f"Access denied to playlist. You may need to re-authenticate with updated permissions, or this playlist may not be accessible with your current permissions.")
                elif e.http_status == 404:
                    raise Exception(f"Playlist not found. It may have been deleted or you may not have access.")
                else:
                    raise Exception(f"Error accessing playlist: {str(e)}")
            
            while results:
                for item in results.get('items', []):
                    # According to Spotify API docs (https://developer.spotify.com/documentation/web-api/reference/get-playlists-items):
                    # Each item in the response has:
                    # - 'item': the track/episode object (new field)
                    # - 'track': deprecated but still present for backward compatibility
                    # - 'added_at', 'added_by', 'is_local', etc.
                    track = item.get('item') or item.get('track')
                    
                    # Handle both direct track objects and nested track objects
                    # Some tracks might be None, unavailable, or local files
                    if track and isinstance(track, dict):
                        # Only process tracks (not episodes) and ensure it has an ID
                        track_type = track.get('type', '')
                        track_id = track.get('id')
                        
                        # Process track if it's a track type and has an ID
                        if track_type == 'track' and track_id:
                            tracks.append(extract_track_info(track))
                
                if results.get('next'):
                    results = sp.next(results)
                else:
                    break
        
        return tracks
    except SpotifyException as e:
        if e.http_status == 403:
            raise Exception(f"Access denied. You may need to re-authenticate with updated permissions.")
        elif e.http_status == 404:
            raise Exception(f"Resource not found. It may have been deleted or you may not have access.")
        else:
            raise Exception(f"Error fetching playlist tracks: {str(e)}")


def extract_track_info(track):
    """
    Extract relevant information from a track object.
    
    Args:
        track (dict): Spotify track object
    
    Returns:
        dict: Track information with id, name, artist, album, year, duration_ms
    """
    # Safely extract artist names
    artists_list = track.get('artists', [])
    if artists_list and isinstance(artists_list, list):
        artist_names = [artist.get('name', 'Unknown Artist') for artist in artists_list if isinstance(artist, dict)]
        artists = ', '.join(artist_names) if artist_names else 'Unknown Artist'
    else:
        artists = 'Unknown Artist'
    
    # Safely extract album information
    album = track.get('album', {})
    if isinstance(album, dict):
        album_name = album.get('name', 'Unknown Album')
        release_date = album.get('release_date', '')
    else:
        album_name = 'Unknown Album'
        release_date = ''
    
    # Extract year from release_date (format: YYYY-MM-DD or YYYY)
    year = ''
    if release_date:
        try:
            year = str(release_date).split('-')[0]
        except (AttributeError, IndexError):
            year = ''
    
    return {
        'id': track.get('id', ''),
        'name': track.get('name', 'Unknown Track'),
        'artist': artists,
        'album': album_name,
        'year': year,
        'duration_ms': track.get('duration_ms', 0)
    }


def get_track_details(token_info, track_id):
    """
    Get detailed track information.
    
    Args:
        token_info (dict): Token information
        track_id (str): Spotify track ID
        
    Returns:
        dict: Detailed track information
    """
    try:
        sp = get_spotify_client(token_info)
        track = sp.track(track_id)
        return extract_track_info(track)
    except SpotifyException as e:
        raise Exception(f"Error fetching track details: {str(e)}")

