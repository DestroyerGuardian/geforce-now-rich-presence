from setuptools import setup

APP = ['main.py']
DATA_FILES = ['games_config_merged.json']
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        # This tells macOS it's a top-bar-only utility (hides the dock icon)
        'LSUIElement': True,
    },
    'packages': ['src', 'pypresence', 'rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)