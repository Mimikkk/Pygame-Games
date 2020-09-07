from game_states.snake_state import *
from game_states.saper_state import *

class GameSelectState(State):
    def __init__(self, state_stack: Deque[State]):
        super().__init__(is_pausable=False)
        self.palette: Palette = Palette()
        self.buttons: Dict[str, Button] = dict()
        self.state_stack: Deque[State] = state_stack

        self.init_buttons()

    def init_buttons(self):
        self.buttons['CLASSIC_SNAKE'] = Button("Snake", pygame.Rect(80, 60, 200, 50), 20, roundness=0.2)
        self.buttons['SPACE_INVADERS'] = Button("Space Invaders", pygame.Rect(300, 60, 200, 50), 20, roundness=0.2)
        self.buttons['FANCY_SNAKE'] = Button("Fancy Snake", pygame.Rect(520, 60, 200, 50), 20, roundness=0.2)

        self.buttons['ARKANOID'] = Button("Arkanoid", pygame.Rect(80, 120, 200, 50), 20, roundness=0.2)
        self.buttons['TETRIS'] = Button("Tetris", pygame.Rect(300, 120, 200, 50), 20, roundness=0.2)
        self.buttons['SAPER'] = Button("Saper", pygame.Rect(520, 120, 200, 50), 20, roundness=0.2)

        self.buttons['BOMBERMAN'] = Button("Bomberman", pygame.Rect(80, 180, 200, 50), 20, roundness=0.2)
        self.buttons['PACMAN'] = Button("Pacman", pygame.Rect(300, 180, 200, 50), 20, roundness=0.2)
        self.buttons['ASTEROIDS'] = Button("Asteroids", pygame.Rect(520, 180, 200, 50), 20, roundness=0.2)

        self.buttons['EXIT'] = Button("Return", pygame.Rect(600, 500, 200, 50), 20, roundness=0.2)

    def handle_events(self, events):
        for button in self.buttons.values():
            button.handle_events(events)
        self.__handle_buttons()

    def __handle_buttons(self):
        if self.buttons['EXIT'].is_clicked and self.is_key_time():
            self.end_state()
        elif self.buttons['CLASSIC_SNAKE'].is_clicked and self.is_key_time():
            self.state_stack.append(SnakeGameState(self.state_stack))
        elif self.buttons['SAPER'].is_clicked and self.is_key_time():
            self.state_stack.append(SaperState(self.state_stack))

    def update(self, dt: float):
        self.update_key_time(dt)

        for button in self.buttons.values():
            button.update(dt)

    def render(self, screen: pygame.SurfaceType):
        screen.fill(self.palette.background)

        for button in self.buttons.values():
            button.render(screen)

    def reset(self):
        print('Resetting Game Select')
        for button in self.buttons.values():
            button.reset()
