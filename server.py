import os
import requests
from flask import Flask, request, redirect, jsonify
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Flask app
app = Flask(__name__)
TOKEN_INFO = {}

# Helper function to refresh token
def refresh_access_token():
    global TOKEN_INFO
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": TOKEN_INFO.get("refresh_token"),
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    TOKEN_INFO.update(response.json())

# Step 1: Redirect user to Spotify login
@app.route("/login")
def login():
    scope = "user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-public"
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}"
    return redirect(auth_url)

# Step 2: Handle Spotify callback
@app.route("/callback")
def callback():
    global TOKEN_INFO
    code = request.args.get("code")
    if not code:
        return "Error: No authorization code received.", 400

    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    TOKEN_INFO = response.json()

    return "Authorization successful! You can now control Spotify."

# Step 3: Fetch current playing song
@app.route("/current-song")
def current_song():
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    if response.status_code == 200:
        song_data = response.json()
        song_name = song_data["item"]["name"]
        artist_name = song_data["item"]["artists"][0]["name"]
        return f"Currently Playing: {song_name} by {artist_name}"
    return "No song is currently playing."

# Step 4: Play/Pause controls
@app.route("/play")
def play():
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers)
    return "Playback started!"

@app.route("/pause")
def pause():
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.put("https://api.spotify.com/v1/me/player/pause", headers=headers)
    return "Playback paused!"

@app.route("/next")
def next_track():
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.post("https://api.spotify.com/v1/me/player/next", headers=headers)
    return "Skipped to next track!"

@app.route("/previous")
def previous_track():
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.post("https://api.spotify.com/v1/me/player/previous", headers=headers)
    return "Went back to previous track!"

# Step 5: Adjust Volume
@app.route("/volume")
def set_volume():
    volume = request.args.get("volume")
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.put(f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume}", headers=headers)
    return f"Volume set to {volume}%"

# Step 6: Fetch User’s Playlists
@app.route("/playlists")
def get_playlists():
    headers = {"Authorization": f"Bearer {TOKEN_INFO['access_token']}"}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    if response.status_code == 200:
        playlists = response.json()["items"]
        playlist_names = [playlist["name"] for playlist in playlists]
        return "Your Playlists: " + ", ".join(playlist_names)
    return "Could not retrieve playlists."

# Step 9: MCP Integration (Placeholder)
@app.route("/mcp-command")
def mcp_command():
    command = request.args.get("command")
    if "play" in command:
        return play()
    elif "pause" in command:
        return pause()
    elif "next" in command:
        return next_track()
    elif "previous" in command:
        return previous_track()
    elif "volume" in command:
        volume_level = command.split()[-1]  # Extract volume from command
        return set_volume()
    return "Unknown command. Please try again."

# Run the server
if __name__ == "__main__":
    app.run(port=5500)
