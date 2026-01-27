import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import time
import sys
import subprocess
import utils
from config import HELP_MESSAGE


#========================
# Service mode
#========================
def run_lofi_service(start_mode: str, init_song: str | None) -> None:
    '''
    Entry point for the lofi background service. Responsible for:
    - managing audio playback via pygame
    - maintaining playback state (single song vs playlist)
    - receiving commands from the CLI via a shared command file
    - running independently of the terminal that launched it
    '''

    # write PID so future CLI calls can detect and communicate with this
    # service instead of spawning a new one
    utils.write_pid(os.getpid())

    pygame.init()
    pygame.mixer.init()

    # track current playback mode ("single" or "playlist")
    mode = start_mode

    def start_single(song: str) -> None:
        '''
        Switch service into single-song mode and stops any current playback
        '''
        nonlocal mode
        mode = "single"
        utils.stop_music()
        if not utils.play_music(song):
            print(f"Unknown song chosen: {song}")
            print(HELP_MESSAGE)

    def start_playlist() -> None:
        '''
        Switch service into playlist mode and stops any current playback
        '''
        nonlocal mode
        mode = "playlist"
        utils.stop_music()
        if not utils.play_next_song():
            print("No songs found")
            print(HELP_MESSAGE)
    
    # initial start based on how service was launched
    if mode == "single" and init_song:
        start_single(init_song)
    elif mode == "playlist":
        start_playlist()


    try:
        while True:
            # check for command written by CLI
            line = utils.read_cmd()
            if line:
                cmd, arg = utils.parse_cmd(line)

                if cmd == "play" and arg:
                    start_single(arg)
                elif cmd == "playlist":
                    start_playlist()
                elif cmd == "stop":
                    break
                else:
                    print(f"Invalid command: {line}")
                    print(HELP_MESSAGE)
            
            # in playlist mode, automatically advance when playback ends
            if mode == "playlist" and not pygame.mixer.music.get_busy():
                utils.play_next_song()

            time.sleep(0.1)
    finally:
        utils.stop_music()
        pygame.quit()
        utils.clear_ipc_files()


#========================
# CLI mode
#========================
def ensure_play_service_running(song: str) -> None:
    '''
    If service is already running, send 'play song' command,
    else start detached service (normal mode)
    '''

    pid = utils.read_pid()

    # service is running, send new play command
    if pid is not None and utils.is_process_running(pid):
        utils.write_cmd("play", song)
        return
    
    # stale pid file so need to remove shared memory files
    if pid is not None and not utils.is_process_running(pid):
        utils.clear_ipc_files()
    
    # start detached service
    subprocess.Popen(
        ["pythonw", sys.argv[0], "service", song],
        creationflags=subprocess.DETACHED_PROCESS
    )

def ensure_playlist_service_running() -> None:
    '''
    If service is already running, send playlist command,
    else start detached service is playlist mode
    '''
    pid = utils.read_pid()

    # service is running, send new command
    if pid is not None and utils.is_process_running(pid):
        utils.write_cmd("playlist")
        return
    
    # stale pid file so need to remove shared memory files
    if pid is not None and not utils.is_process_running(pid):
        utils.clear_ipc_files()
    
    # start detached service
    subprocess.Popen(
        ["pythonw", sys.argv[0], "service", "playlist"],
        creationflags=subprocess.DETACHED_PROCESS
    )

def run_cli(args: list[str]) -> int:
    '''
    Entry point for CLI. Responsible for:
    - starting the background service if needed
    - sending commands to an already running service
    - printing help/usage information for invalid input
    '''

    if not args:
        print(HELP_MESSAGE)
        return 0
    
    cmd = args[0].lower()

    if cmd == "play":
        # `lofi play` with no song defaults to playlist mode
        if len(args) < 2:
            ensure_playlist_service_running()
            return 0
        
        # `lofi play [song]` starts or updates single-song mode`
        song = " ".join(args[1:]).strip().lower()
        ensure_play_service_running(song)
        return 0
    
    if cmd == "stop":
        # stop the running service if one exists
        pid = utils.read_pid()
        if pid is None or not utils.is_process_running(pid):
            print("Lofi service is not running.")
            utils.clear_ipc_files()
            return 0
        
        utils.write_cmd("stop")
        return 0

    if cmd == "help":
        print(HELP_MESSAGE)
        return 0
    
    print(f"Unknown command: {cmd}")
    print(HELP_MESSAGE)
    return 0

#==============
# Entrypoint
#==============
def main() -> int:
    # service command: py lofi.py service <song>
    if len(sys.argv) > 1 and sys.argv[1].lower() == "service":
        if len(sys.argv) < 3:
            print(HELP_MESSAGE)
            return 0
        
        arg = sys.argv[2].lower()

        if arg == "playlist":
            run_lofi_service(start_mode="playlist", init_song=None)
            return 0

        song = " ".join(sys.argv[2:]).strip().lower()
        run_lofi_service(start_mode="single", init_song=song)
        return 0
    
    # cli command: py lofi.py play <song> | py lofi.py stop | py lofi.py playlist
    return run_cli(sys.argv[1:])

if __name__ == "__main__":
    raise SystemExit(main())