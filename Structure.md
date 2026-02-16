# Software Architecture Document: goodhare

## Overview

**goodhare** is a Python web application that facilitates migration from Spotify by extracting user's liked songs and playlists. The application provides a Flask-based web interface where users can authenticate with Spotify, view their playlists (including liked songs), select which playlists to export, and download the song information as a CSV file.

## Architecture Components

The application follows a modular architecture with clear separation of concerns:

1. **Authentication Module** - Handles Spotify OAuth2 authentication
2. **Data Gathering Module** - Retrieves playlists and track information from Spotify API
3. **Data Output Module** - Formats and exports data to CSV
4. **Flask Web Interface** - Provides user interaction layer
5. **Configuration Management** - Manages credentials and environment variables

## File Structure

```
goodhare/
├── app.py                 # Main Flask application entry point
├── auth.py                # Spotify authentication module
├── data_gathering.py      # Playlist and track data retrieval
├── data_output.py         # CSV export functionality
├── .env                   # Environment variables (credentials, secrets)
├── .env.example           # Template for .env file
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main web interface template
├── static/
│   └── style.css          # CSS styling (optional)
└── README.md              # Project documentation
```

## Dependencies

### Required Python Packages

- `flask` - Web framework for the user interface
- `spotipy` - Spotify Web API Python library
- `python-dotenv` - Environment variable management
- `pandas` or `csv` - CSV file generation
- `requests` - HTTP requests (if not using spotipy)

### Spotify API Requirements

- Spotify Developer Account
- Spotify App registered in Spotify Developer Dashboard
- Client ID and Client Secret
- Redirect URI configured in Spotify app settings

## Implementation Instructions

### Step 1: Project Setup

1. Create a new Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install flask spotipy python-dotenv pandas
   ```

3. Create `requirements.txt`:
   ```
   flask==2.3.0
   spotipy==2.23.0
   python-dotenv==1.0.0
   pandas==2.0.0
   ```

### Step 2: Environment Configuration

1. Create `.env` file in the project root:
   ```
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
   FLASK_SECRET_KEY=your_secret_key_here
   ```

2. Create `.env.example` as a template (without actual credentials)

3. Add `.env` to `.gitignore` to prevent committing secrets

### Step 3: Authentication Module (`auth.py`)

**Purpose**: Handle Spotify OAuth2 authentication flow

**Key Functions**:
- `get_spotify_oauth()` - Initialize Spotify OAuth manager
- `get_auth_url()` - Generate authorization URL
- `get_token_from_code(code)` - Exchange authorization code for access token
- `refresh_token(token)` - Refresh expired tokens

**Implementation Notes**:
- Use Spotipy's `SpotifyOAuth` class
- Store tokens in session or temporary storage
- Handle token refresh automatically
- Implement error handling for authentication failures

### Step 4: Data Gathering Module (`data_gathering.py`)

**Purpose**: Retrieve playlists and track information from Spotify API

**Key Functions**:
- `get_user_playlists(token)` - Fetch all user playlists
- `get_liked_songs(token)` - Fetch user's liked songs (saved tracks)
- `get_playlist_tracks(token, playlist_id)` - Get all tracks in a specific playlist
- `get_track_details(token, track_id)` - Get detailed track information

**Data Structure**:
- Playlist object: `{id, name, description, track_count, owner}`
- Track object: `{id, name, artist, album, year, duration_ms}`

**Implementation Notes**:
- Handle pagination for playlists and tracks (Spotify API limits results)
- Cache results to avoid redundant API calls
- Include error handling for API rate limits
- Support both playlists and "Liked Songs" as a special playlist

### Step 5: Data Output Module (`data_output.py`)

**Purpose**: Format and export track data to CSV

**Key Functions**:
- `format_track_data(tracks)` - Structure track data for export
- `export_to_csv(tracks, filename)` - Write tracks to CSV file
- `generate_csv_content(tracks)` - Create CSV string in memory

**CSV Format**:
- Columns: `Name`, `Artist`, `Album`, `Year`, `Duration (ms)`, `Playlist`
- UTF-8 encoding
- Handle special characters in track/artist names

**Implementation Notes**:
- Use pandas DataFrame or csv module
- Support both file download and in-memory generation
- Include playlist name in each row for multi-playlist exports
- Handle missing data gracefully (e.g., missing year)

### Step 6: Flask Web Interface (`app.py`)

**Purpose**: Main application entry point and web interface

**Key Routes**:
- `GET /` - Home page with login button
- `GET /login` - Initiate Spotify authentication
- `GET /callback` - Handle OAuth callback, store token
- `GET /playlists` - Display user playlists for selection
- `POST /export` - Process selected playlists and generate CSV
- `GET /download/<filename>` - Download generated CSV file

**Session Management**:
- Store access token in Flask session
- Implement session timeout
- Clear session on logout

**Implementation Notes**:
- Use Flask sessions for token storage
- Implement CSRF protection
- Add error pages (404, 500)
- Include loading states for API calls

### Step 7: Frontend Template (`templates/index.html`)

**Purpose**: User interface for playlist selection and export

**Key Features**:
- Playlist list with checkboxes
- "Select All" / "Deselect All" functionality
- Export button
- Loading indicators
- Error messages
- Responsive design

**UI Flow**:
1. Login page → Click "Login with Spotify"
2. Redirect to Spotify → User authorizes
3. Callback → Redirect to playlists page
4. Playlists page → Select playlists → Click "Export"
5. Processing → Download CSV file

## Data Flow

```
User → Flask App → Spotify OAuth → User Authorizes
  ↓
Callback → Store Token → Fetch Playlists
  ↓
Display Playlists → User Selects → Fetch Track Details
  ↓
Format Data → Generate CSV → Download
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **Token Storage**: Store tokens securely in server-side sessions
3. **HTTPS**: Use HTTPS in production (Spotify requires secure redirect URIs)
4. **Token Expiration**: Implement automatic token refresh
5. **Rate Limiting**: Handle Spotify API rate limits gracefully
6. **Input Validation**: Validate user inputs and playlist selections

## Error Handling

Implement error handling for:
- Authentication failures
- Token expiration
- API rate limits (429 errors)
- Network timeouts
- Invalid playlist IDs
- Missing track metadata
- File I/O errors

## Testing Checklist

- [ ] Authentication flow works correctly
- [ ] Playlists are fetched and displayed
- [ ] Liked songs are included in the list
- [ ] Multiple playlists can be selected
- [ ] CSV export contains correct data (name, artist, album, year)
- [ ] CSV file downloads successfully
- [ ] Token refresh works automatically
- [ ] Error messages display appropriately
- [ ] Session management works correctly

## Future Expansion Points

As mentioned in requirements, the modular structure allows for:
- Adding support for other music platforms (Apple Music, YouTube Music, etc.)
- Exporting to other formats (JSON, XML, Excel)
- Batch processing for large playlists
- Scheduled exports
- Playlist comparison features
- Track metadata enrichment

## Build Instructions Summary

1. **Setup Environment**: Create virtual environment and install dependencies
2. **Configure Spotify App**: Register app in Spotify Developer Dashboard
3. **Set Environment Variables**: Create `.env` file with credentials
4. **Implement Modules**: Build `auth.py`, `data_gathering.py`, `data_output.py`
5. **Create Flask App**: Implement routes in `app.py`
6. **Build Frontend**: Create HTML template for user interface
7. **Test**: Run application locally and test full flow
8. **Deploy**: Configure for production (HTTPS, proper redirect URIs)

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Set environment variables (or use .env file)
export FLASK_APP=app.py
export FLASK_ENV=development

# Run Flask application
flask run
# Or: python app.py
```

Access the application at `http://localhost:5000`

---

**Note**: This architecture document provides a comprehensive guide for building the goodhare application. Follow the steps sequentially and ensure all security best practices are implemented before deploying to production.

