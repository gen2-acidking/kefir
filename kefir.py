##################################################################
# umlaut fixer script
# author: gen2acidking
##################################################################

import json
import subprocess
import time
import argparse
import os
import signal
import sys
from pynput import keyboard

##################################################################
# main class for converting ascii finnish text into proper umlauts
# loads a word mapping from a json file
# manages umlaut mode and input buffering for real-time correction
##################################################################
class UmlautFixer:
    
    ##################################################################
    # initializes the fixer and loads word map
    # expects:
    #   mapping_path: string - path to the json mapping file
    # returns: none
    # used by: main when starting the fixer
    ##################################################################
    def __init__(self, mapping_path="finnish_ascii_map.json"):
        with open(mapping_path, encoding="utf-8") as f:
            self.word_map = json.load(f)
        self.buffer = ""
        self.in_umlaut_mode = False
        self.block_until = 0
        self.listener = keyboard.Listener(on_press=self.on_key)
        self.listener.start()

    ##################################################################
    # handles key events and processes buffered characters
    # expects:
    #   key: keyboard.Key - the key event received
    # returns: none
    # used by: listener when a key is pressed
    ##################################################################
    def on_key(self, key):
        # timing workaround to prevent input race conditions
        if time.time() < self.block_until:
            return
        try:
            if key == keyboard.Key.space:
                if self.buffer:
                    self.commit_word()
                else:
                    subprocess.run(["xdotool", "key", "space"])
                self.buffer = ""
            elif key == keyboard.Key.backspace:
                if self.buffer:
                    self.buffer = self.buffer[:-1]
            elif hasattr(key, 'char') and key.char is not None:
                char = key.char
                if self.in_umlaut_mode:
                    if char == 'a':
                        self.block_until = time.time() + 0.1
                        subprocess.run(["xdotool", "key", "BackSpace"])
                        subprocess.run(["xdotool", "type", "ä"])
                        char = 'ä'
                    elif char == 'o':
                        self.block_until = time.time() + 0.1
                        subprocess.run(["xdotool", "key", "BackSpace"])
                        subprocess.run(["xdotool", "type", "ö"])
                        char = 'ö'
                self.buffer += char
        except Exception as e:
            print(f"[!] error: {e}")

    ##################################################################
    # commits the buffered word by checking for corrections
    # replaces incorrect ascii letters with proper umlauts
    # expects: none
    # returns: none
    # used by: on_key when space is pressed
    ##################################################################
    def commit_word(self):
        if not self.buffer:
            return
        ascii_word = self.buffer.replace("ä", "a").replace("ö", "o").lower()
        corrected = self.word_map.get(ascii_word)
        if corrected and corrected != self.buffer:
            print(f"[✓] fixing '{self.buffer}' → '{corrected}'")
            self.block_until = time.time() + 0.5
            subprocess.run(["xdotool", "key", "--repeat", str(len(self.buffer) + 1), "--delay", "2", "BackSpace"])
            time.sleep(0.2)
            subprocess.run(["xdotool", "type", "--clearmodifiers", "--delay", "2", corrected])
            self.in_umlaut_mode = True
        else:
            subprocess.run(["xdotool", "key", "space"])
            self.in_umlaut_mode = False

    ##################################################################
    # runs the main loop and starts keyboard capture
    # creates a pid file to track the process
    # expects: none
    # returns: none
    # used by: main when starting the fixer
    ##################################################################
    def run(self):
        print("[⇄] umlaut fixer active. type in ascii, press space for corrections.")
        with open(os.path.expanduser("~/.umlaut_fixer.pid"), "w") as f:
            f.write(str(os.getpid()))
        self.listener.join()


##################################################################
# stops any running instance using the pid file
# expects: none
# returns: bool - true if stopped, false otherwise
# used by: cli interface to shut down the fixer
##################################################################
def stop_running_instance():
    pid_file = os.path.expanduser("~/.umlaut_fixer.pid")
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            os.remove(pid_file)
            print(f"[✓] stopped umlaut fixer process (pid: {pid})")
            return True
        except (ProcessLookupError, ValueError, FileNotFoundError):
            os.remove(pid_file)
            print("[!] no valid umlaut fixer process found to stop")
    else:
        print("[!] no umlaut fixer process is currently running")
    return False


##################################################################
# checks if umlaut fixer is currently running
# expects: none
# returns: bool - true if running, false otherwise
# used by: cli interface before starting or stopping
##################################################################
def check_status():
    pid_file = os.path.expanduser("~/.umlaut_fixer.pid")
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"[✓] umlaut fixer is running (pid: {pid})")
            return True
        except (ProcessLookupError, ValueError, FileNotFoundError):
            os.remove(pid_file)
            print("[!] umlaut fixer is not running (stale pid file removed)")
    else:
        print("[!] umlaut fixer is not running")
    return False


##################################################################
# entry point for command-line usage
# parses arguments and controls startup behavior
# expects: none
# returns: none
# used by: python interpreter
##################################################################
def main():
    parser = argparse.ArgumentParser(description="umlaut fixer - convert ascii-typed finnish words to proper umlauts")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start", action="store_true", help="start the umlaut fixer")
    group.add_argument("--stop", action="store_true", help="stop the umlaut fixer")
    group.add_argument("--status", action="store_true", help="check if umlaut fixer is running")
    parser.add_argument("--mapping", default="finnish_ascii_map.json", help="path to the mapping json file")

    args = parser.parse_args()

    if args.stop:
        stop_running_instance()
    elif args.status:
        check_status()
    elif args.start:
        if check_status():
            print("[!] umlaut fixer is already running. stop it first to restart.")
            return
        fixer = UmlautFixer(mapping_path=args.mapping)
        fixer.run()


if __name__ == "__main__":
    main()
