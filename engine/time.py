from engine.imports import *

class Time(object):
    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.dt: float = 0
        self.fps: int = 0

    def update_dt(self, refresh_rate):
        self.dt = self.__clock.tick(refresh_rate)/1000

    def update_fps(self):
        self.fps = self.__clock.get_fps()
