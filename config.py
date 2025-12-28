# Configuration file for lofi:
# SONGS mapping should match filenames in songs directory

import os

# configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONGS_DIR = os.path.join(BASE_DIR, "songs")
PID_FILE = os.path.join(BASE_DIR, "lofi.pid")
CMD_FILE = os.path.join(BASE_DIR, "lofi.cmd")

# map songnames to filenames
SONGS = {
    'inuyasha' : "inuyasha.mp3",
    'kiki' : "kiki.mp3",
    'tarzan' : "tarzan.mp3",
    'mary poppins' : "poppins.mp3",
    'kate bush' : "KateBush.mp3",
    'still with you' : "StillWithYou.mp3"
}

HELP_MESSAGE = '''
===============================================================
|    Tracklist:                                               |
===============================================================
|   inuyasha: Affections Touching Across Time                 |
|   kiki: Kiki's Delivery Service: A Town with an Ocean View  |
|   tarzan: You'll Be in My Heart                             |
|   "mary poppins": Chim Chim Cheree                          |
|   "kate bush": Running Up That Hill                         |
|   "still with you"                                          |
===============================================================
'''