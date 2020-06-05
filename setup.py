
from setuptools import setup

setup(
    name="Slimy",
    version='1.0',
    options = {
        'build_apps': {
            'include_modules': [
                'pypresence'
            ],
            'platforms': ['win_amd64'
            ],
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.ptf',
                '**/*.mp3'
            ],
            'gui_apps': {
                'Slimy': 'main.py',
            },
            'log_filename': '$USER_APPDATA/.Slimy/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
                'p3ffmpeg',
                'p3ptloader',
            ],
        }
    }
)