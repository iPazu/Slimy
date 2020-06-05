from setuptools import setup

setup(
    name = "Slimy",
    options = {
        'build_apps': {
            'include_modules': [
                'pconsole',
                'mysql-connector'
            ],
            'include_patterns':[
                '**/*.bmp',
                '**/*.png',
                '**/*.ttf',
                '**/*.egg',
                '**/*.frag',
                '**/*.vert',
                '**/*.mp3'
            ],
            'platforms':[
                'win_amd64'
                #,'macosx_10_6_x86_64'
            ],
            'gui_apps':{
                'Slimy':'main.py',
            },
            'plugins':[
                'pandagl',
                'p3openal_audio',
                'p3fmod_audio', # idk which one is necessary so I just use both
                'p3ffmpeg',
                'p3ptloader'
            ]
        }
    }
)