import time
import sys
import subprocess
import re
import json
from pypresence import Presence
import os
import logging
from logging.handlers import RotatingFileHandler

from src.gfn_menu import GFNMenuBarUI

CLIENT_ID = '1507462111997984928'  

def redirect_logs():
    """Sets up a self-cleaning log rotator that will never overflow your disk."""
    log_dir = os.path.expanduser("~/Library/Logs/GFN_Presence")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, "gfn_presence_debug.log")
    
    # maxBytes=5*1024*1024 caps the file at exactly 5 Megabytes
    rotator = RotatingFileHandler(
        log_file_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=1, 
        encoding="utf-8"
    )
    
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    rotator.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(rotator)
    
    class StreamToLogger:
        def __init__(self, log_level):
            self.log_level = log_level
        def write(self, buf):
            for line in buf.rstrip().splitlines():
                root_logger.log(self.log_level, line.rstrip())
        def flush(self):
            pass

    sys.stdout = StreamToLogger(logging.INFO)
    sys.stderr = StreamToLogger(logging.ERROR)
    
def main():
    redirect_logs()

    print("Launching GFN Discord Rich Presence for Mac")
    
    app = GFNMenuBarUI(default_id=CLIENT_ID)
    
    try:
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        app.terminate_cleanly()

if __name__ == "__main__":
    main()