from engine.imports import *

class State(object):
    def __init__(self, is_pausable: bool = False):
        self.is_pausable: bool = is_pausable
        self.__is_running: bool = True
        self.__key_time_max: float = 1.5
        self.__key_time: float = self.__key_time_max

    def end_state(self):
        print('Exiting State')
        self.__is_running = False

    def reset(self):
        self.__key_time = self.__key_time_max

    def is_running(self):
        return self.__is_running

    def is_key_time(self):
        if self.__key_time >= self.__key_time_max:
            return True
        return False

    def handle_events(self, events):
        pass

    def update(self, dt: float):
        pass

    def update_key_time(self, dt: float):
        if self.__key_time < self.__key_time_max:
            self.__key_time += dt

    def render(self, screen: pygame.Surface):
        pass
