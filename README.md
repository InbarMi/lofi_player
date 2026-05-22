# Lofi

A lightweight CLI-based lofi background music player that runs as a detached background service.

This project was built as a learning exercise to better understand background processes, inter-process communication (via shared files), and separation between a CLI and a long-running service.

## Features
* Play a single song on repeat
* Play all songs in a continuous playlist
* Switch between single-song and playlist modes at runtime
* Stop the background service
* Volume control (increase, decrease, or set 0-100%)
* Detached background process (independent of terminal session)
* Minimal CLI

## Architecture
* A CLI process sends commands to a long-running background service via shared command and PID files
* The service manages audio playback independently of the terminal
* Commands can be sent without restarting the service

## Setup
1. Clone the repo
2. Add audio files to `songs/`
3. Update `config.py` to use correct audio filenames
4. Make sure `lofi` script executable and added to PATH

> Note: Currently tested on Windows (uses `pythonw` and Windows process APIs).

## Usage
Once installed, the following commands can be used:

```bash
lofi play           # Start playlist mode (loops through all songs)
lofi play [song]    # Play one song on repeat
lofi stop           # Stop the lofi service
lofi vol up         # Increase volume
lofi vol down       # Decrease volume
lofi vol [0-100]    # Set volume percentage
```

## Additional Notes
> Audio files are not included in this repository