from game_states.state import *
from game_states.game_select_state import *
from game_states.saper_state import *

class MainMenuState(State):
    def __init__(self, state_stack: Deque[State]):
        super().__init__(is_pausable=False)
        self.palette: Palette = Palette()
        self.buttons: Dict[str, Button] = dict()
        self.state_stack: Deque[State] = state_stack

        self.init_buttons()

    def init_buttons(self):
        self.buttons['GAME_LIST'] = Button("Game Select", pygame.Rect(600, 100, 200, 50), 20, roundness=0.2)
        self.buttons['NEXT'] = Button("Debug", pygame.Rect(600, 160, 200, 50), 20, roundness=0.2)
        self.buttons['EXIT'] = Button("Exit", pygame.Rect(600, 220, 200, 50), 20, roundness=0.2)

    def handle_events(self, events):
        for button in self.buttons.values():
            button.handle_events(events)
        self.__handle_buttons()

    def __handle_buttons(self):
        if self.buttons['EXIT'].is_clicked and self.is_key_time():
            self.end_state()
        if self.buttons['NEXT'].is_clicked and self.is_key_time():
            self.state_stack.append(SaperState(self.state_stack))
        if self.buttons['GAME_LIST'].is_clicked and self.is_key_time():
            self.state_stack.append(GameSelectState(self.state_stack))

    def update(self, dt: float):
        self.update_key_time(dt)

        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.SurfaceType):
        screen.fill(self.palette.background)

        for button in self.buttons.values():
            button.render(screen)

    def reset(self):
        print('Resetting mainmenu')
        for button in self.buttons.values():
            button.reset()
