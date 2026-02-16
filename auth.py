"""
Authentication module for Spotify OAuth2 flow.
Handles user authentication and token management.
"""

import os
import time
from spotipy import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def get_spotify_oauth():
    """
    Initialize and return Spotify OAuth manager.
    
    Returns:
        SpotifyOAuth: Configured OAuth manager instance
    """
    return SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private',
        cache_path=None  # We'll handle token storage in session
    )


def get_auth_url():
    """
    Generate Spotify authorization URL.
    
    Returns:
        str: Authorization URL for user to visit
    """
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


def get_token_from_code(code):
    """
    Exchange authorization code for access token.
    
    Args:
        code (str): Authorization code from Spotify callback
        
    Returns:
        dict: Token information including access_token and refresh_token
    """
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_access_token(code)
    return token_info


def refresh_token(token_info):
    """
    Refresh an expired access token.
    
    Args:
        token_info (dict): Current token information
        
    Returns:
        dict: Updated token information
    """
    if not token_info or 'refresh_token' not in token_info:
        raise Exception("No refresh token available")
    
    sp_oauth = get_spotify_oauth()
    new_token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return new_token_info


def is_token_expired(token_info):
    """
    Check if token is expired.
    
    Args:
        token_info (dict): Token information
        
    Returns:
        bool: True if token is expired, False otherwise
    """
    if not token_info:
        return True
    
    now = int(time.time())
    return token_info['expires_at'] - now < 60  # Refresh if expires in less than 60 seconds

