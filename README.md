# Lofi

A lightweight CLI lofi background music player that runs as a detached background process.

## Features
* Play lofi tracks in a loop
* Switch songs
* Background service (process is not dependent on terminal)
* Simple CLI

## Setup
1. Clone the repo
2. Add audio files to `songs/`
3. Update `config.py` to use correct audio filenames
4. Make sure `lofi` script executable and added to PATH

## Usage
```bash
lofi play <song name>
lofi play <different song name>
lofi stop
```

## Notes
Audi files are not included in this repository