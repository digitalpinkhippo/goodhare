"""
Main Flask application for goodhare.
Handles web interface and coordinates authentication, data gathering, and export.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from dotenv import load_dotenv
import io

from auth import get_auth_url, get_token_from_code, refresh_token, is_token_expired
from data_gathering import get_user_playlists, get_liked_songs, get_playlist_tracks
from data_output import format_track_data, generate_csv_content, combine_tracks_from_playlists

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')


def ensure_valid_token():
    """
    Ensure the token in session is valid, refresh if needed.
    
    Returns:
        dict: Valid token information or None if not authenticated
    """
    token_info = session.get('token_info')
    if not token_info:
        return None
    
    if is_token_expired(token_info):
        try:
            token_info = refresh_token(token_info)
            session['token_info'] = token_info
        except Exception as e:
            flash(f'Error refreshing token: {str(e)}', 'error')
            session.pop('token_info', None)
            return None
    
    return token_info


@app.route('/')
def index():
    """Home page - shows login or playlist selection."""
    token_info = ensure_valid_token()
    
    if not token_info:
        return render_template('index.html')
    
    # Fetch playlists and liked songs
    try:
        playlists = get_user_playlists(token_info)
        liked_songs = get_liked_songs(token_info)
        
        # Add liked songs as the first item
        playlists.insert(0, liked_songs)
        
        return render_template('index.html', playlists=playlists, token_info=token_info)
    except Exception as e:
        flash(f'Error loading playlists: {str(e)}', 'error')
        return render_template('index.html', token_info=token_info)


@app.route('/login')
def login():
    """Initiate Spotify authentication."""
    auth_url = get_auth_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Handle OAuth callback from Spotify."""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash(f'Authentication error: {error}', 'error')
        return redirect(url_for('index'))
    
    if not code:
        flash('No authorization code received', 'error')
        return redirect(url_for('index'))
    
    try:
        token_info = get_token_from_code(code)
        session['token_info'] = token_info
        flash('Successfully authenticated with Spotify!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error during authentication: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Clear session and log out user."""
    session.pop('token_info', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))


@app.route('/export', methods=['POST'])
def export():
    """Process selected playlists and generate CSV."""
    token_info = ensure_valid_token()
    
    if not token_info:
        flash('Please login first', 'error')
        return redirect(url_for('index'))
    
    playlist_ids = request.form.getlist('playlist_ids')
    
    if not playlist_ids:
        flash('Please select at least one playlist to export', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get playlist names for reference
        all_playlists = get_user_playlists(token_info)
        liked_songs = get_liked_songs(token_info)
        all_playlists.insert(0, liked_songs)
        
        playlist_dict = {p['id']: p['name'] for p in all_playlists}
        
        # Fetch tracks from selected playlists
        all_tracks_data = {}
        for playlist_id in playlist_ids:
            playlist_name = playlist_dict.get(playlist_id, f'Playlist {playlist_id}')
            
            try:
                tracks = get_playlist_tracks(token_info, playlist_id)
                all_tracks_data[playlist_name] = tracks
            except Exception as e:
                flash(f'Error fetching tracks from {playlist_name}: {str(e)}', 'error')
                continue
        
        if not all_tracks_data:
            flash('No tracks were retrieved from selected playlists', 'error')
            return redirect(url_for('index'))
        
        # Combine and format tracks
        combined_tracks = combine_tracks_from_playlists(all_tracks_data)
        
        # Generate CSV content
        csv_content = generate_csv_content(combined_tracks)
        
        # Create file-like object for download
        output = io.BytesIO()
        output.write(csv_content.encode('utf-8'))
        output.seek(0)
        
        # Generate filename
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'spotify_export_{timestamp}.csv'
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        flash(f'Error during export: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('index.html', error='Internal server error'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

