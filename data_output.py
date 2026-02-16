"""
Data output module for formatting and exporting track data to CSV.
"""

import csv
import io
from datetime import datetime


def format_track_data(tracks, playlist_name=''):
    """
    Structure track data for export.
    
    Args:
        tracks (list): List of track dictionaries
        playlist_name (str): Name of the playlist
        
    Returns:
        list: Formatted track data ready for CSV export
    """
    formatted = []
    for track in tracks:
        formatted.append({
            'Name': track.get('name', 'Unknown Track'),
            'Artist': track.get('artist', 'Unknown Artist'),
            'Album': track.get('album', 'Unknown Album'),
            'Year': track.get('year', ''),
            'Duration (ms)': track.get('duration_ms', 0),
            'Playlist': playlist_name
        })
    return formatted


def generate_csv_content(tracks_data):
    """
    Create CSV string in memory.
    
    Args:
        tracks_data (list): List of formatted track dictionaries
        
    Returns:
        str: CSV content as string
    """
    if not tracks_data:
        return ''
    
    output = io.StringIO()
    fieldnames = ['Name', 'Artist', 'Album', 'Year', 'Duration (ms)', 'Playlist']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for track in tracks_data:
        writer.writerow(track)
    
    return output.getvalue()


def export_to_csv(tracks_data, filename=None):
    """
    Write tracks to CSV file.
    
    Args:
        tracks_data (list): List of formatted track dictionaries
        filename (str): Optional filename. If None, generates timestamp-based name
        
    Returns:
        str: Filename of the created CSV file
    """
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'spotify_export_{timestamp}.csv'
    
    fieldnames = ['Name', 'Artist', 'Album', 'Year', 'Duration (ms)', 'Playlist']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for track in tracks_data:
            writer.writerow(track)
    
    return filename


def combine_tracks_from_playlists(playlist_tracks_dict):
    """
    Combine tracks from multiple playlists into a single list.
    
    Args:
        playlist_tracks_dict (dict): Dictionary mapping playlist names to track lists
        
    Returns:
        list: Combined and formatted track data
    """
    all_tracks = []
    for playlist_name, tracks in playlist_tracks_dict.items():
        formatted = format_track_data(tracks, playlist_name)
        all_tracks.extend(formatted)
    
    return all_tracks

