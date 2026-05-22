# Utilities functions

from config import PID_FILE, CMD_FILE, SONGS, SONGS_DIR
import os

def get_song_path(songname):
    '''Return the relative filepath for a song'''

    filename = SONGS.get(songname)
    if not filename:
        return None
    return os.path.join(SONGS_DIR, filename)

def is_process_running(pid: int) -> bool:
    '''Check if a windows process with PID exists'''

    if pid <= 0:
        return False
    
    try:
        import ctypes
        PROCESS_QUERY_INFORMATION = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)

        if handle == 0:
            return False
        
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    except Exception:
        return False

def read_pid() -> int | None:
    '''Read PID from PID_FILE, return None if invalid or doesn't exist'''

    if not os.path.exists(PID_FILE):
        return None
    try:
        with open(PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        return pid
    except Exception:
        try:
            os.remove(PID_FILE)
        except OSError:
            pass
        return None

def write_pid(pid: int) -> None:
    '''Write PID to PID file'''

    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(pid))

def clear_ipc_files() -> None:
    '''Remove existing IPC files'''
    for path in (PID_FILE, CMD_FILE):
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass

def read_cmd():
    '''Read and delete command file if it exists'''

    if not os.path.exists(CMD_FILE):
        return None
    
    with open(CMD_FILE, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    if line:
        try:
            os.remove(CMD_FILE)
        except OSError:
            pass
        return line

    return None

def write_cmd(cmd: str, arg: str | None = None) -> None:
    '''Write a single command to CMD_FILE'''
    
    line = cmd if arg is None else f"{cmd} {arg}"
    with open(CMD_FILE, "w", encoding="utf-8") as f:
        f.write(line)

def parse_cmd(line: str) -> tuple[str, str | None]:
    '''Split line into a command and an argument. For example "play kiki" -> ("play", "kiki")'''

    line = line.strip()
    if not line:
        return "", None
    
    if " " in line:
        cmd, arg = line.split(" ", 1)
        return cmd.lower(), arg.strip().lower()
    else:
        return line.lower(), None

# Music control functions
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

def stop_music():
    '''Stop played music'''
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except Exception:
        pass

def play_music(song: str) -> bool:
    '''Play one song in a loop'''
    songpath = get_song_path(song)
    if not songpath:
        return False
    
    pygame.mixer.music.load(songpath)
    pygame.mixer.music.play(loops=-1)
    return True

song_index = 0
def play_next_song() -> bool:
    '''Play the next song in the song list'''
    global song_index
    songnames = list(SONGS.keys())
    if not songnames:
        return False
    
    songname = songnames[song_index]
    songpath = get_song_path(songname)
    if not songpath:
        return False
    
    pygame.mixer.music.load(songpath)
    pygame.mixer.music.play()
    song_index = (song_index + 1) % len(songnames)
    return True

# Volume control functions
MUTED = 0.0
MAX_VOLUME = 1.0
VOL_STEP = 0.1

def increase_volume():
    '''Increment volume of current music'''
    current_volume = pygame.mixer.music.get_volume()
    new_volume = min(MAX_VOLUME, current_volume + VOL_STEP)
    
    pygame.mixer.music.set_volume(new_volume)

def decrease_volume():
    '''Decrement volume of current music'''
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(MUTED, current_volume - VOL_STEP)
    
    pygame.mixer.music.set_volume(new_volume)

def set_volume(vol):
    '''Set volume of current music using percentage (0-100)'''
    if vol < 0: vol = 0
    elif vol > 100: vol = 100

    pygame.mixer.music.set_volume(vol / 100)