import rumps
from src.gfn_presence_engine import GFNPresenceEngine
import os
import sys
import rumps
from src.gfn_presence_engine import GFNPresenceEngine



class GFNMenuBarUI(rumps.App):
    def __init__(self, default_id):
        super(GFNMenuBarUI, self).__init__("GFN", quit_button="Quit App")
        
        self.engine = GFNPresenceEngine(default_id=default_id)
        
        self.status_label = rumps.MenuItem("Status: Syncing...")
        self.menu.add(self.status_label)
        #self.icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "nvidia_icon.png")


        icon_name = "nvidia_icon.png"

        # not sure why icon is not showing up (pls help someone)
        if "RESOURCEPATH" in os.environ:
            self.icon_path = os.path.join(os.environ["RESOURCEPATH"], icon_name) 
        else:
            self.icon_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "assets", icon_name)
            )
            
        print(f"[Debug Asset Mapping Path]: {self.icon_path}")

        if os.path.exists(self.icon_path):
            self.icon = self.icon_path
            self.template = True 
        else:
            self.title = "GFN"
        
        self.menu.add(rumps.separator)
        
        self.toggle_setting = rumps.MenuItem("Enable Presence", callback=self.toggle_presence)
        self.toggle_setting.state = 1 
        self.menu.add(self.toggle_setting)

    def toggle_presence(self, sender):
        """Callback function that fires whenever 'Enable Presence' is clicked."""
        sender.state = 0 if sender.state == 1 else 1
        
        if sender.state == 0:
            print("[Settings Alert]: Presence Disabled by User.")
            self.engine.disconnect()
            self.status_label.title = "Status: Disabled"
        else:
            print("[Settings Alert]: Presence Enabled by User.")
            self.engine.re_enable()
            self.status_label.title = "Status: Syncing..."

    @rumps.timer(1)
    def refresh_tick(self, timer):
        """Asynchronously updates UI tracking tags based on engine outputs."""
        if self.toggle_setting.state == 0:
            return
            
        active_game, display_text = self.engine.compute_state()
        self.status_label.title = display_text
        

    def terminate_cleanly(self):
        self.engine.disconnect()