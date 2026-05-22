import os
import json
import re
import subprocess


class GFNLogMonitor:
    def __init__(self, config_path="games_config_merged.json"):
        self.log_path = os.path.expanduser('~/Library/Application Support/NVIDIA/GeForceNOW/console.log')
        self.file_handle = None
        self.current_game = "GeForce NOW Dashboard"
        self.is_playing = False
        
        # Load KarmaDevz's configuration mapping
        self.game_mappings = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.game_mappings = json.load(f)
                print(f"Successfully loaded {len(self.game_mappings)} game configurations from JSON!")
            except Exception as e:
                print(f"Error loading JSON configuration file: {e}")
 
    def sanitize_string(self, text):
        """Strips out special characters like ®, ™, and strange trailing spaces.
        
        Ensures a log string like 'Cyberpunk 2077®' cleanly matches a JSON key like 'Cyberpunk 2077'.
        """
        if not text:
            return ""
        
        clean = text.replace("®", "").replace("™", "")
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def init_stream(self):
        """Locks onto the bottom of the log file on startup."""
        if os.path.exists(self.log_path):
            self.file_handle = open(self.log_path, 'r', encoding='utf-8', errors='ignore')
            self.file_handle.seek(0, os.SEEK_END)
            return True
        return False

    def scan_new_lines(self):
        """Scans newly appended lines in real-time, sanitizing names on the fly."""
        if not self.file_handle:
            self.init_stream()
            return self.current_game, self.is_playing

        lines = self.file_handle.readlines()
        if lines:
            for line in lines:
                if "ApplicationClass" in line and "Launch game" in line:
                    match = re.search(r'Launch game\s+(.*?)\s+\[', line)
                    if match:
                        raw_name = match.group(1).strip()
                        self.current_game = self.sanitize_string(raw_name)
                        self.is_playing = True
                        print(f"[Event Trigger]: Launched {self.current_game}")
                
                elif "source onFocus for key Library" in line or "onFocus for key SessionChange" in line:
                    if self.is_playing:
                        print(f"[Event Trigger]: Game closed. Returning to Dashboard.")
                        self.current_game = "GeForce NOW Dashboard"
                        self.is_playing = False

        return self.current_game, self.is_playing

