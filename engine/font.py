from engine.imports import *

class Font(object):
    def __init__(self):
        freetype.init()
        self.__path: str = 'resources/font'
        self.emoji = freetype.Font(f'{self.__path}/seguiemj.ttf')
        self.font: freetype.Font = freetype.Font(f'{self.__path}/JetBrainsMono-Medium.ttf')
