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
def run_lofi_service(init_song: str) -> None:
    utils.write_pid(os.getpid())
    print(f"Service started with song: {init_song}")

    pygame.init()
    pygame.mixer.init()

    if not utils.play_music(init_song):
        print(f"Unknown song chosen: {init_song}")
        print(HELP_MESSAGE)
        utils.stop_music()

    try:
        while True:
            line = utils.read_cmd()
            if line:
                cmd, arg = utils.parse_cmd(line)

                if cmd == "play":
                    utils.stop_music()
                elif cmd == "stop":
                    break

            time.sleep(0.5)
    finally:
        utils.stop_music()
        pygame.quit()
        utils.clear_ipc_files()

#========================
# CLI mode
#========================
def ensure_service_running(song: str) -> None:
    '''
    If service is already running, send 'play song' command,
    else start detached service
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

def run_cli(args: list[str]) -> int:
    if not args:
        print(HELP_MESSAGE)
        return 0
    
    cmd = args[0].lower()
    if cmd == "play":
        if len(args) < 2:
            print("Please specify a song to play.")
            print(HELP_MESSAGE)
            return 0
        song = " ".join(args[1:]).strip().lower()
        ensure_service_running(song)
        return 0
    
    if cmd == "stop":
        pid = utils.read_pid()
        if pid is None or not utils.is_process_running(pid):
            print("Lofi service is not running.")
            utils.clear_ipc_files()
            return 0
        utils.write_cmd("stop")
        return 0
    
    print(f"Unknown command: {cmd}")
    print("Usage: lofi play <song> | stop")
    print(HELP_MESSAGE)
    return 0

#==============
# Entrypoint
#==============
def main() -> int:
    # service command: py lofi.py service <song>
    if len(sys.argv) > 1 and sys.argv[1].lower() == "service":
        if len(sys.argv) < 3:
            print("Please specify a song to play.")
            print(HELP_MESSAGE)
            return 0
        song = " ".join(sys.argv[2:]).strip().lower()
        run_lofi_service(song)
        return 0
    
    # cli command: py lofi.py play <song> | py lofi.py stop
    return run_cli(sys.argv[1:])

if __name__ == "__main__":
    raise SystemExit(main())