from engine.transparent_screen import *
from engine.view import *
from engine.time import *

from game_states.main_menu_state import *
from game_states.state import *
from game_objects.text import *
from resources.color_paletes.snake_colors import *


class Game(object):
    def __init__(self):
        # Init
        pygame.init()
        self.__state_stack: Deque[State] = deque()
        self.__view: View = View()
        self.__time: Time = Time()
        self.__colors: Palette = Palette()

        # Const Private Variables
        self.__is_running: bool = True
        self.__is_paused: bool = False

        self.__pause_screen: TransparentScreen = TransparentScreen(self.__view.width, self.__view.height, roundness=0.2)
        self.__fps_counter: TextObject = TextObject((0, 0), "", 24, 0,
                                                    color=pygame.Color(255, 255, 255, 255),
                                                    is_centered=False)
        print("Starting Game")
        self.__game_loop()

    def __game_loop(self):
        self.__state_stack.append(MainMenuState(self.__state_stack))
        while self.__is_running:
            self.__handle_events()
            self.__update()

            self.__render()

    def __handle_events(self):
        events = pygame.event.get()

        if not self.__state_stack:
            self.__is_running = False

        elif not self.__is_paused:
            self.__state_stack[-1].handle_events(events)
        else:
            self.__pause_screen.handle_events(events)

        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__is_running = False
            if (self.__state_stack[-1].is_pausable
                    and (self.__pause_screen.is_closed or (event.type == pygame.KEYDOWN and event.key == pygame.K_p))):
                self.__is_paused = False if self.__is_paused else True
                self.__pause_screen.reset()

    def __update(self):  # __TIME.DT
        self.__time.update_dt(self.__view.refresh_rate)
        self.__time.update_fps()
        self.__update_fps_counter()

        if self.__state_stack and not self.__is_paused: self.__state_stack[-1].update(self.__time.dt)

        if self.__state_stack and not self.__state_stack[-1].is_running():
            self.__state_stack.pop()
            if self.__state_stack:
                self.__state_stack[-1].reset()

    def __update_fps_counter(self):
        self.__fps_counter.set_str(str(round(self.__time.fps)))

    def __render(self):  # __VIEW.SCREEN
        if self.__state_stack and not self.__pause_screen.is_blurred: self.__state_stack[-1].render(self.__view.screen)
        if self.__is_paused:
            self.__pause_screen.update(self.__time.dt)
            self.__pause_screen.render(self.__view.screen)
        self.__fps_counter.render(self.__view.screen)

        pygame.display.flip()
