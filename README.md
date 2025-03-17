# Spotify MCP Server

This is a Flask-based MCP server that integrates with the **Spotify Web API** to control playback, manage volume, retrieve playlists, and more.

## 🚀 Features
- ✅ Authenticate with Spotify
- ✅ Control playback (Play/Pause/Next/Previous)
- ✅ Adjust volume
- ✅ Fetch currently playing song
- ✅ Retrieve user playlists
- ✅ MCP Command Execution (for custom commands)



## 🔗 API Endpoints
| Endpoint | Description |
|----------|-------------|
| `/login` | Redirects to Spotify for authentication |
| `/callback` | Handles Spotify OAuth callback |
| `/current-song` | Fetches currently playing song |
| `/play` | Starts playback |
| `/pause` | Pauses playback |
| `/next` | Skips to the next track |
| `/previous` | Returns to the previous track |
| `/volume?volume=50` | Sets volume to 50% (replace 50 with desired level) |
| `/playlists` | Fetches user playlists |
| `/mcp-command?command=play` | Executes MCP command |

