# goodhare 🐰

A Python web application that helps you migrate out of Spotify by exporting your liked songs and playlists to CSV format.

## Features

- 🔐 Secure Spotify OAuth2 authentication
- 📋 View all your playlists and liked songs
- ✅ Select multiple playlists to export
- 📊 Export track data (name, artist, album, year) to CSV
- 🎨 Modern, responsive web interface

## Prerequisites

- Python 3.8 or higher
- Spotify Developer Account
- Spotify App credentials (Client ID and Client Secret)

## Setup Instructions

### 1. Clone or Download the Repository

```bash
cd goodhare
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Spotify Developer Account

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in app details:
   - App name: `goodhare` (or any name)
   - App description: `Export playlists and liked songs`
   - Redirect URI: `http://localhost:5000/callback`
5. Save your **Client ID** and **Client Secret**

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
FLASK_SECRET_KEY=your_secret_key_here
```

**Important:** 
- Replace `your_client_id_here` and `your_client_secret_here` with your actual Spotify credentials
- Generate a random string for `FLASK_SECRET_KEY` (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)

### 6. Run the Application

```bash
python app.py
```

Or using Flask:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### 7. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Login**: Click "Login with Spotify" and authorize the application
2. **Select Playlists**: Check the playlists you want to export (including "Liked Songs")
3. **Export**: Click "Export Selected Playlists"
4. **Download**: The CSV file will download automatically

## CSV Format

The exported CSV file contains the following columns:
- **Name**: Track name
- **Artist**: Artist name(s)
- **Album**: Album name
- **Year**: Release year
- **Duration (ms)**: Track duration in milliseconds
- **Playlist**: Name of the playlist containing the track

## Project Structure

```
goodhare/
├── app.py                 # Main Flask application
├── auth.py                # Spotify authentication module
├── data_gathering.py      # Playlist and track data retrieval
├── data_output.py         # CSV export functionality
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore file
├── templates/
│   └── index.html        # Web interface template
└── README.md             # This file
```

## Troubleshooting

### Authentication Issues
- Ensure your redirect URI in `.env` matches exactly with the one in Spotify Developer Dashboard
- Check that your Client ID and Client Secret are correct
- Make sure you're using `http://localhost:5000/callback` (not `https`)

### API Rate Limits
- Spotify API has rate limits. If you encounter errors, wait a few minutes and try again
- The app handles rate limits automatically where possible

### Missing Tracks
- Some tracks may be unavailable in certain regions
- Private playlists may not be accessible if you don't have permission

## Security Notes

- Never commit your `.env` file to version control
- Use a strong `FLASK_SECRET_KEY` in production
- For production deployment, use HTTPS
- Update redirect URI in Spotify Dashboard for production URL

## License

This project is provided as-is for personal use.

## Contributing

Feel free to submit issues or pull requests if you'd like to improve the application!

